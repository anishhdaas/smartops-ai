#!/usr/bin/env python3
"""Kafka consumer that validates infrastructure incidents and stores them in Snowflake."""

from __future__ import annotations

import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from typing import Any

import snowflake.connector
from kafka import KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
KAFKA_TOPIC = "raw_incidents"
KAFKA_CONSUMER_GROUP = "validation_group"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "INCIDENT_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAW")

VALID_INCIDENT_TABLE = "incident_warehouse.raw.incidents"
INVALID_INCIDENT_TABLE = "incident_warehouse.raw.invalid_incidents"

REQUIRED_FIELDS = {"timestamp", "server_id", "event_type", "severity", "region", "metadata"}
VALID_SEVERITIES = {"INFO", "WARNING", "CRITICAL"}
VALID_REGIONS = {"Bangalore", "Singapore", "Tokyo"}
MINIMUM_STORED_SEVERITIES = {"WARNING", "CRITICAL"}

RETRY_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 5
METRICS_EVERY_EVENTS = 5_000

shutdown_requested = False


def request_shutdown(signum: int, _frame: Any) -> None:
    """Request a graceful shutdown for SIGTERM/SIGINT."""
    global shutdown_requested
    shutdown_requested = True
    print(f"Shutdown requested by signal {signum}; stopping gracefully...", file=sys.stderr)


def json_deserializer(raw: bytes) -> dict[str, Any]:
    """Deserialize Kafka message values as JSON objects."""
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Kafka message value must be a JSON object")
    return value


def create_consumer() -> KafkaConsumer:
    """Create a Kafka consumer with retries for broker unavailability."""
    last_error: Exception | None = None

    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            return KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
                group_id=KAFKA_CONSUMER_GROUP,
                enable_auto_commit=False,
                auto_offset_reset="earliest",
                value_deserializer=json_deserializer,
                consumer_timeout_ms=1_000,
                max_poll_records=500,
            )
        except (NoBrokersAvailable, KafkaError) as exc:
            last_error = exc
            print(
                f"Kafka unavailable on attempt {attempt}/{RETRY_ATTEMPTS}: {exc}",
                file=sys.stderr,
            )
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)

    raise RuntimeError(f"Unable to connect to Kafka after {RETRY_ATTEMPTS} attempts") from last_error


def create_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    """Create a Snowflake connection from environment variables."""
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )


def validate_incident(event: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate an incident event against the required schema and allowed values."""
    errors: list[str] = []
    missing_fields = REQUIRED_FIELDS - event.keys()
    if missing_fields:
        errors.append(f"missing required fields: {sorted(missing_fields)}")

    severity = event.get("severity")
    if severity not in VALID_SEVERITIES:
        errors.append(f"invalid severity: {severity!r}")

    region = event.get("region")
    if region not in VALID_REGIONS:
        errors.append(f"invalid region: {region!r}")

    if "metadata" in event and not isinstance(event["metadata"], dict):
        errors.append("metadata must be an object")

    if "timestamp" in event:
        try:
            datetime.fromisoformat(str(event["timestamp"]).replace("Z", "+00:00"))
        except ValueError:
            errors.append(f"invalid timestamp: {event.get('timestamp')!r}")

    return not errors, errors


def should_store_valid_event(event: dict[str, Any]) -> bool:
    """Filter out valid events below WARNING severity."""
    return event.get("severity") in MINIMUM_STORED_SEVERITIES


def utc_now_iso() -> str:
    """Return the current UTC timestamp in Snowflake-friendly ISO format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def insert_valid_incident(cursor: Any, event: dict[str, Any]) -> None:
    """Insert a validated incident into Snowflake."""
    cursor.execute(
        f"""
        INSERT INTO {VALID_INCIDENT_TABLE}
            (timestamp, server_id, event_type, severity, region, metadata, raw_event, ingested_at)
        SELECT
            %(timestamp)s,
            %(server_id)s,
            %(event_type)s,
            %(severity)s,
            %(region)s,
            PARSE_JSON(%(metadata)s),
            PARSE_JSON(%(raw_event)s),
            %(ingested_at)s
        """,
        {
            "timestamp": event["timestamp"],
            "server_id": event["server_id"],
            "event_type": event["event_type"],
            "severity": event["severity"],
            "region": event["region"],
            "metadata": json.dumps(event.get("metadata", {})),
            "raw_event": json.dumps(event),
            "ingested_at": utc_now_iso(),
        },
    )


def insert_invalid_incident(cursor: Any, raw_event: Any, errors: list[str]) -> None:
    """Insert an invalid incident into the Snowflake dead-letter table."""
    cursor.execute(
        f"""
        INSERT INTO {INVALID_INCIDENT_TABLE}
            (raw_event, validation_errors, ingested_at)
        SELECT
            PARSE_JSON(%(raw_event)s),
            PARSE_JSON(%(validation_errors)s),
            %(ingested_at)s
        """,
        {
            "raw_event": json.dumps(raw_event),
            "validation_errors": json.dumps(errors),
            "ingested_at": utc_now_iso(),
        },
    )


def print_metrics(processed: int, valid: int, invalid: int) -> None:
    print(f"Processed: {processed}, Valid: {valid}, Invalid: {invalid}", flush=True)


def process_messages() -> int:
    """Consume Kafka messages, validate them, and write incidents to Snowflake."""
    consumer = create_consumer()
    snowflake_connection = create_snowflake_connection()
    processed = 0
    valid = 0
    invalid = 0

    try:
        with snowflake_connection.cursor() as cursor:
            while not shutdown_requested:
                for message in consumer:
                    raw_event = message.value
                    processed += 1

                    is_valid, validation_errors = validate_incident(raw_event)
                    if is_valid and should_store_valid_event(raw_event):
                        insert_valid_incident(cursor, raw_event)
                        valid += 1
                    elif is_valid:
                        # Valid INFO events are intentionally filtered out and not stored.
                        valid += 1
                    else:
                        insert_invalid_incident(cursor, raw_event, validation_errors)
                        invalid += 1

                    if processed % METRICS_EVERY_EVENTS == 0:
                        snowflake_connection.commit()
                        consumer.commit()
                        print_metrics(processed, valid, invalid)

                    if shutdown_requested:
                        break

                if shutdown_requested:
                    break

            snowflake_connection.commit()
            consumer.commit()
            print_metrics(processed, valid, invalid)
    finally:
        consumer.close()
        snowflake_connection.close()

    return 0


def main() -> int:
    signal.signal(signal.SIGINT, request_shutdown)
    signal.signal(signal.SIGTERM, request_shutdown)

    try:
        return process_messages()
    except Exception as exc:
        print(f"Consumer failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
