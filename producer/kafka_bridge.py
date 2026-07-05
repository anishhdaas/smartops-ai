#!/usr/bin/env python3
"""Kafka bridge that reads JSON Lines from stdin and sends to Kafka topic.

Implements retry logic for connection and efficient batching.
"""
import json
import logging
import os
import sys
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError, BrokerNotAvailableError

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("smartops.producer.kafka_bridge")

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092").split(",")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_incidents")

# Producer configuration as per requirements
PRODUCER_CONFIG = {
    "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
    "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
    "acks": "all",
    "linger_ms": 100,
    "batch_size": 65536,
    "compression_type": "gzip",
    "retries": 10,
    "retry_backoff_ms": 1000,
    "max_block_ms": 120000,
}

# Flush every FLUSH_EVERY events
FLUSH_EVERY = 1000

# Connection retry settings
CONNECT_RETRY_SECONDS = 60
CONNECT_RETRY_INTERVAL = 1  # second between attempts


def create_producer_with_retry() -> KafkaProducer:
    """Create a Kafka producer with retry logic for broker availability."""
    start_time = time.time()
    attempt = 0
    while time.time() - start_time < CONNECT_RETRY_SECONDS:
        try:
            producer = KafkaProducer(**PRODUCER_CONFIG)
            # Test connection by fetching metadata (this will raise if successful if it fails, we retry )
            producer.bootstrap_connected()
            logger.info("Connected to Kafka brokers: %s", KAFKA_BOOTSTRAP_SERVERS)
            return producer
        except BrokerNotAvailableError as e:
            attempt += 1
            elapsed = int(time.time() - start_time)
            logger.warning(
                "Kafka unavailable (attempt %d, elapsed %ds): %s. Retrying in %d seconds...",
                attempt,
                elapsed,
                e,
                CONNECT_RETRY_INTERVAL,
            )
            time.sleep(CONNECT_RETRY_INTERVAL)
        except Exception as e:
            # Other exceptions (e.g., timeout) we also retry
            attempt += 1
            elapsed = int(time.time() - start_time)
            logger.warning(
                "Unexpected error (attempt %d, elapsed %ds): %s. Retrying in %d seconds...",
                attempt,
                elapsed,
                e,
                CONNECT_RETRY_INTERVAL,
            )
            time.sleep(CONNECT_RETRY_INTERVAL)
    raise RuntimeError(f"Failed to connect to Kafka after {CONNECT_RETRY_SECONDS} seconds")


def main() -> int:
    """Main function to read from stdin and produce to Kafka."""
    producer = None
    try:
        producer = create_producer_with_retry()
        event_count = 0
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as e:
                logger.error("Failed to parse JSON line: %s", e)
                continue
            # Send event to Kafka
            producer.send(KAFKA_TOPIC, event)
            event_count += 1
            if event_count % FLUSH_EVERY == 0:
                producer.flush()
                logger.info("Flushed %d events to Kafka", event_count)
        # Final flush for remaining events
        if event_count % FLUSH_EVERY != 0:
            producer.flush()
            logger.info("Flushed final %d events to Kafka", event_count)
        logger.info("Finished processing. Total events sent: %d", event_count)
        return 0
    except Exception as exc:
        logger.exception("Bridge failed: %s", exc)
        return 1
    finally:
        if producer:
            producer.close()

if __name__ == "__main__":
    sys.exit(main())
