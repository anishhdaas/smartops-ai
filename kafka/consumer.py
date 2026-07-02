#!/usr/bin/env python3
"""Kafka consumer that validates infrastructure incidents and stores them in Snowflake."""

from __future__ import annotations

import json
import logging
import os
import signal
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import snowflake.connector
from kafka import KafkaConsumer
from kafka.errors import KafkaError

try:
    from kafka.errors import NoBrokersAvailable
except ImportError:
    NoBrokersAvailable = KafkaError

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("smartops.kafka.consumer")

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_incidents")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "validation_group")
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
POLL_TIMEOUT_MS = 1_000
MAX_POLL_RECORDS = 500
METRICS_EVERY_EVENTS = 100

shutdown_requested = False


def request_shutdown(signum: int, _frame: Any) -> None:
    """Request a graceful shutdown for SIGTERM/SIGINT."""
    global shutdown_requested
    shutdown_requested = True
    logger.info("Shutdown requested by signal %s; stopping gracefully...", signum)


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
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
                group_id=KAFKA_CONSUMER_GROUP,
                enable_auto_commit=False,
                auto_offset_reset="earliest",
                value_deserializer=json_deserializer,
                max_poll_records=MAX_POLL_RECORDS,
                session_timeout_ms=30_000,
                heartbeat_interval_ms=10_000,
                request_timeout_ms=40_000,
            )
            logger.info(
                "Kafka connected: brokers=%s topic=%s group=%s",
                KAFKA_BOOTSTRAP_SERVERS,
                KAFKA_TOPIC,
                KAFKA_CONSUMER_GROUP,
            )
            return consumer
        except (NoBrokersAvailable, KafkaError) as exc:
            last_error = exc
            logger.warning(
                "Kafka unavailable on attempt %s/%s: %s",
                attempt,
                RETRY_ATTEMPTS,
                exc,
            )
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)

    raise RuntimeError(f"Unable to connect to Kafka after {RETRY_ATTEMPTS} attempts") from last_error


def create_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    """Create a Snowflake connection from environment variables."""
    connection = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    logger.info(
        "Snowflake connected: account=%s database=%s schema=%s",
        SNOWFLAKE_ACCOUNT,
        SNOWFLAKE_DATABASE,
        SNOWFLAKE_SCHEMA,
    )
    return connection


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


def snowflake_timestamp_or_none(value: Any) -> str | None:
    """Return a Snowflake-friendly timestamp string only when it is parseable."""
    if value is None:
        return None
    try:
        datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return str(value)


def insert_valid_incident(cursor: Any, event: dict[str, Any]) -> None:
    """Insert a validated incident into Snowflake."""
    cursor.execute(
        f"""
        INSERT INTO {VALID_INCIDENT_TABLE}
            (
                incident_id,
                timestamp,
                server_id,
                region,
                event_type,
                severity,
                cpu_percent,
                memory_percent,
                api_latency_ms,
                metadata,
                ingested_at
            )
        SELECT
            %(incident_id)s,
            %(timestamp)s,
            %(server_id)s,
            %(region)s,
            %(event_type)s,
            %(severity)s,
            %(cpu_percent)s,
            %(memory_percent)s,
            %(api_latency_ms)s,
            PARSE_JSON(%(metadata)s),
            %(ingested_at)s
        """,
        {
            "incident_id": str(uuid.uuid4()),
            "timestamp": event.get("timestamp"),
            "server_id": event.get("server_id"),
            "region": event.get("region"),
            "event_type": event.get("event_type"),
            "severity": event.get("severity"),
            "cpu_percent": event.get("cpu_percent"),
            "memory_percent": event.get("memory_percent"),
            "api_latency_ms": event.get("api_latency_ms"),
            "metadata": json.dumps(event.get("metadata") or {}),
            "ingested_at": utc_now_iso(),
        },
    )


def insert_invalid_incident(cursor: Any, event: dict[str, Any], errors: list[str]) -> None:
    """Insert an invalid incident into the Snowflake dead-letter table."""
    cursor.execute(
        f"""
        INSERT INTO {INVALID_INCIDENT_TABLE}
            (
                incident_id,
                timestamp,
                server_id,
                region,
                event_type,
                severity,
                cpu_percent,
                memory_percent,
                api_latency_ms,
                metadata,
                ingested_at
            )
        SELECT
            %(incident_id)s,
            %(timestamp)s,
            %(server_id)s,
            %(region)s,
            %(event_type)s,
            %(severity)s,
            %(cpu_percent)s,
            %(memory_percent)s,
            %(api_latency_ms)s,
            PARSE_JSON(%(metadata)s),
            %(ingested_at)s
        """,
        {
            "incident_id": str(uuid.uuid4()),
            "timestamp": snowflake_timestamp_or_none(event.get("timestamp")),
            "server_id": event.get("server_id"),
            "region": event.get("region"),
            "event_type": event.get("event_type"),
            "severity": event.get("severity"),
            "cpu_percent": event.get("cpu_percent"),
            "memory_percent": event.get("memory_percent"),
            "api_latency_ms": event.get("api_latency_ms"),
            "metadata": json.dumps(
                {
                    "validation_errors": errors,
                    "payload": event,
                    "metadata": event.get("metadata") if isinstance(event, dict) else None,
                }
            ),
            "ingested_at": utc_now_iso(),
        },
    )


def log_metrics(processed: int, valid: int, invalid: int) -> None:
    logger.info("Processed: %s, Valid: %s, Invalid: %s", processed, valid, invalid)


def commit_offsets(consumer: KafkaConsumer, snowflake_connection: Any) -> None:
    """Commit Snowflake transaction and Kafka offsets together."""
    snowflake_connection.commit()
    consumer.commit()


def process_messages() -> int:
    """Consume Kafka messages, validate them, and write incidents to Snowflake."""
    consumer = create_consumer()
    snowflake_connection = create_snowflake_connection()
    processed = 0
    valid = 0
    invalid = 0
    seen_since_commit = 0

    logger.info(
        "Consumer started: topic=%s group=%s bootstrap_servers=%s",
        KAFKA_TOPIC,
        KAFKA_CONSUMER_GROUP,
        KAFKA_BOOTSTRAP_SERVERS,
    )

    try:
        with snowflake_connection.cursor() as cursor:
            while not shutdown_requested:
                batches = consumer.poll(timeout_ms=POLL_TIMEOUT_MS, max_records=MAX_POLL_RECORDS)
                if not batches:
                    continue

                for _tp, records in batches.items():
                    for message in records:
                        if shutdown_requested:
                            break
                        event = message.value
                        processed += 1
                        seen_since_commit += 1

                        logger.info(
                            "Received event: partition=%s offset=%s key=%s",
                            message.partition,
                            message.offset,
                            message.key,
                        )

                        is_valid, validation_errors = validate_incident(event)
                        try:
                            if is_valid and should_store_valid_event(event):
                                insert_valid_incident(cursor, event)
                                valid += 1
                                logger.info(
                                    "Valid event stored: server_id=%s event_type=%s severity=%s",
                                    event.get("server_id"),
                                    event.get("event_type"),
                                    event.get("severity"),
                                )
                            elif is_valid:
                                # Valid INFO events are intentionally filtered out and not stored.
                                valid += 1
                                logger.info(
                                    "Valid event filtered (below WARNING): server_id=%s severity=%s",
                                    event.get("server_id"),
                                    event.get("severity"),
                                )
                            else:
                                insert_invalid_incident(cursor, event, validation_errors)
                                invalid += 1
                                logger.warning(
                                    "Invalid event: errors=%s payload=%s",
                                    validation_errors,
                                    event,
                                )
                            logger.info("Snowflake insert succeeded: offset=%s", message.offset)
                        except Exception as exc:
                            snowflake_connection.rollback()
                            logger.exception(
                                "Snowflake insert failed: offset=%s error=%s payload=%s",
                                message.offset,
                                exc,
                                event,
                            )
                            raise

                        if seen_since_commit >= METRICS_EVERY_EVENTS:
                            commit_offsets(consumer, snowflake_connection)
                            seen_since_commit = 0
                            log_metrics(processed, valid, invalid)

                    if shutdown_requested:
                        break

            commit_offsets(consumer, snowflake_connection)
            log_metrics(processed, valid, invalid)
    finally:
        try:
            consumer.close()
        finally:
            snowflake_connection.close()

    return 0


def main() -> int:
    logger.info(
        "Starting SmartOps Kafka consumer: topic=%s group=%s bootstrap_servers=%s",
        KAFKA_TOPIC,
        KAFKA_CONSUMER_GROUP,
        KAFKA_BOOTSTRAP_SERVERS,
    )
    signal.signal(signal.SIGINT, request_shutdown)
    signal.signal(signal.SIGTERM, request_shutdown)

    try:
        return process_messages()
    except Exception as exc:
        logger.exception("Consumer failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
