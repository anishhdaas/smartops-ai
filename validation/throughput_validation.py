#!/usr/bin/env python3
"""
Throughput validation script for SmartOps pipeline.
Measures:
- Snowflake ingestion rate (events in last 5 minutes)
- Kafka consumer lag
- End-to-end latency (produce to insert)
Logs results to Snowflake metrics table.
Alerts if Kafka lag > 100k events.
"""
import os
import sys
import time
import json
import logging
from datetime import datetime, timezone, timedelta

import snowflake.connector
from snowflake.connector.errors import ProgrammingError, OperationalError
from kafka import KafkaConsumer, KafkaAdminClient
from kafka.admin import ConfigResource, ConfigResourceType
from kafka.errors import KafkaError

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("smartops.validation.throughput")

# -----------------------------------------------------------------------------
# Configuration from environment
# -----------------------------------------------------------------------------
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "INCIDENT_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAW")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_incidents")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "validation_group")

# Validation parameters
LOOKBACK_MINUTES = 5
LAG_ALERT_THRESHOLD = 100_000  # events
METRICS_TABLE = "VALIDATION_METRICS"  # will be created if not exists

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def get_snowflake_connection():
    """Create and return a Snowflake connection."""
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            role=SNOWFLAKE_ROLE if SNOWFLAKE_ROLE else None,
        )
        logger.debug("Snowflake connection established.")
        return conn
    except Exception as e:
        logger.error("Failed to connect to Snowflake: %s", e)
        raise

def get_kafka_admin_client():
    """Create and return a Kafka admin client."""
    try:
        admin = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
            request_timeout_ms=3000,
        )
        logger.debug("Kafka admin client established.")
        return admin
    except Exception as e:
        logger.error("Failed to connect to Kafka: %s", e)
        raise

def get_snowflake_recent_count(conn):
    """
    Get count of events in the landing table ingested in the last LOOKBACK_MINUTES minutes.
    Returns integer count.
    """
    try:
        with conn.cursor() as cs:
            query = f"""
                SELECT COUNT(*) 
                FROM {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.INCIDENTS
                WHERE INGESTED_AT >= DATEADD(MINUTE, -{LOOKBACK_MINUTES}, CURRENT_TIMESTAMP())
            """
            cs.execute(query)
            result = cs.fetchone()
            count = result[0] if result else 0
            logger.info("Snowflake recent count (%s min): %s", LOOKBACK_MINUTES, count)
            return count
    except Exception as e:
        logger.error("Failed to query Snowflake recent count: %s", e)
        raise

def get_kafka_lag(admin_client):
    """
    Get consumer lag for the given consumer group and topic.
    Returns total lag across all partitions (int).
    """
    try:
        # Fetch consumer group offsets
        # Note: This method works with kafka-python 2.0.2+
        # We'll list consumer groups and then describe the group.
        # However, the admin client doesn't have a direct method for lag.
        # We can use KafkaConsumer to get the lag? But we don't want to join the group.
        # Alternative: Use the admin client to describe the group and then compute lag.
        # Let's use a temporary consumer to get the lag for the group.
        # We'll create a consumer with the same group id, but we won't actually consume.
        # We'll use the partitions_for_topic and then get the end offsets and committed offsets.
        # This is a bit heavy but acceptable for a validation script.
        consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
            group_id=KAFKA_CONSUMER_GROUP,
            enable_auto_commit=False,
            consumer_timeout_ms=1000,
        )
        # Get partitions for the topic
        partitions = consumer.partitions_for_topic(KAFKA_TOPIC)
        if partitions is None:
            logger.warning("Topic %s not found.", KAFKA_TOPIC)
            consumer.close()
            return 0
        topic_partitions = [kafka.TopicPartition(KAFKA_TOPIC, p) for p in partitions]
        # Get end offsets (latest available)
        end_offsets = consumer.end_offsets(topic_partitions)
        # Get committed offsets (if any)
        committed = consumer.committed(topic_partitions, timeout=5000)
        if committed is None:
            # No committed offsets, lag is the end offset (assuming we start from beginning)
            lag = sum(end_offsets.values())
        else:
            lag = sum(end_offsets[tp] - committed.get(tp, 0) for tp in topic_partitions)
        consumer.close()
        logger.info("Kafka consumer lag for group %s: %s", KAFKA_CONSUMER_GROUP, lag)
        return lag
    except Exception as e:
        logger.error("Failed to get Kafka lag: %s", e)
        # Return -1 to indicate error
        return -1

def get_average_latency(conn):
    """
    Compute average latency (seconds) between event timestamp and ingestion timestamp
    for events in the last LOOKBACK_MINUTES minutes.
    Returns float seconds, or None if no data.
    """
    try:
        with conn.cursor() as cs:
            query = f"""
                SELECT AVG(DATEDIFF('second', TIMESTAMP, INGESTED_AT)) 
                FROM {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.INCIDENTS
                WHERE INGESTED_AT >= DATEADD(MINUTE, -{LOOKBACK_MINUTES}, CURRENT_TIMESTAMP())
                  AND TIMESTAMP IS NOT NULL
                  AND INGESTED_AT IS NOT NULL
            """
            cs.execute(query)
            result = cs.fetchone()
            avg_latency = result[0] if result and result[0] is not None else None
            if avg_latency is not None:
                logger.info("Average latency (%s min): %s seconds", LOOKBACK_MINUTES, avg_latency)
            else:
                logger.info("No events with timestamps in the last %s min to compute latency.", LOOKBACK_MINUTES)
            return avg_latency
    except Exception as e:
        logger.error("Failed to compute average latency: %s", e)
        return None

def ensure_metrics_table_exists(conn):
    """Create the metrics table if it doesn't exist."""
    try:
        with conn.cursor() as cs:
            # Check if table exists
            check_sql = f"""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = '{SNOWFLAKE_SCHEMA}' 
                AND TABLE_NAME = '{METRICS_TABLE}'
            """
            cs.execute(check_sql)
            result = cs.fetchone()
            if result and result[0] == 0:
                # Table doesn't exist, create it
                create_sql = f"""
                    CREATE TABLE {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{METRICS_TABLE} (
                        VALIDATION_TIMESTAMP TIMESTAMP_NTZ,
                        SNOWFLAKE_COUNT_5M NUMBER,
                        KAFKA_LAG NUMBER,
                        AVERAGE_LATENCY_SECONDS FLOAT,
                        LAG_EXCEEDED BOOLEAN
                    )
                """
                cs.execute(create_sql)
                conn.commit()
                logger.info("Created metrics table: %s.%s.%s", SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, METRICS_TABLE)
    except Exception as e:
        logger.error("Failed to ensure metrics table exists: %s", e)
        # We'll continue; the insert might fail but we'll try
        pass

def insert_metrics(conn, snowflake_count, kafka_lag, avg_latency):
    """Insert a row into the metrics table."""
    try:
        with conn.cursor() as cs:
            lag_exceeded = kafka_lag > LAG_ALERT_THRESHOLD if kafka_lag >= 0 else False
            insert_sql = f"""
                INSERT INTO {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{METRICS_TABLE}
                (VALIDATION_TIMESTAMP, SNOWFLAKE_COUNT_5M, KAFKA_LAG, AVERAGE_LATENCY_SECONDS, LAG_EXCEEDED)
                VALUES (
                    CURRENT_TIMESTAMP(),
                    %s,
                    %s,
                    %s,
                    %s
                )
            """
            cs.execute(
                insert_sql,
                (
                    snowflake_count,
                    kafka_lag if kafka_lag >= 0 else None,
                    avg_latency,
                    lag_exceeded,
                ),
            )
            conn.commit()
            logger.info("Inserted metrics into %s.%s.%s", SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, METRICS_TABLE)
            if lag_exceeded:
                logger.warning("Kafka lag (%s) exceeds threshold (%s)", kafka_lag, LAG_ALERT_THRESHOLD)
    except Exception as e:
        logger.error("Failed to insert metrics: %s", e)
        conn.rollback()
        raise

def main():
    """Main validation routine."""
    # Validate required environment variables
    required_env = [
        ("SNOWFLAKE_USER", SNOWFLAKE_USER),
        ("SNOWFLAKE_PASSWORD", SNOWFLAKE_PASSWORD),
        ("SNOWFLAKE_ACCOUNT", SNOWFLAKE_ACCOUNT),
    ]
    for name, value in required_env:
        if not value:
            logger.error("Missing required environment variable: %s", name)
            sys.exit(1)

    # Initialize connections
    snowflake_conn = None
    kafka_admin = None
    try:
        snowflake_conn = get_snowflake_connection()
        kafka_admin = get_kafka_admin_client()
        
        # Ensure metrics table exists
        ensure_metrics_table_exists(snowflake_conn)
        
        # Collect metrics
        snowflake_count = get_snowflake_recent_count(snowflake_conn)
        kafka_lag = get_kafka_lag(kafka_admin)
        avg_latency = get_average_latency(snowflake_conn)
        
        # Insert into metrics table
        insert_metrics(snowflake_conn, snowflake_count, kafka_lag, avg_latency)
        
        # Log summary
        logger.info(
            "Validation complete: Snowflake 5m count=%s, Kafka lag=%s, Avg latency=%s seconds",
            snowflake_count,
            kafka_lag if kafka_lag >= 0 else "error",
            avg_latency if avg_latency is not None else "N/A",
        )
        
    except Exception as e:
        logger.exception("Validation failed: %s", e)
        sys.exit(1)
    finally:
        if snowflake_conn:
            snowflake_conn.close()
        if kafka_admin:
            kafka_admin.close()

if __name__ == "__main__":
    main()
