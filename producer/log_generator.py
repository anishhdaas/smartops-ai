#!/usr/bin/env python3
"""Synthetic infrastructure incident log generator.

Emits JSON Lines to stdout for downstream ingestion, for example Kafka producers.
The generator is intentionally streaming-only and does not retain generated
records in memory.
"""

from __future__ import annotations

import json
import random
import signal
import sys
import time
import os
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Deque


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
REGION_LIST = ["Bangalore", "Singapore", "Tokyo"]
EVENT_DISTRIBUTION_PCT = {
    "cpu_spike": 25,
    "memory_full": 20,
    "api_latency": 25,
    "auth_failure": 15,
    "db_error": 15,
}
EVENTS_PER_HOUR = int(os.getenv("EVENTS_PER_HOUR", "125000")) * 2
RUN_HOURS = 8
PRINT_EVERY_EVENTS = 10_000
SERVER_COUNTS = {
    "APP": 120,
    "DB": 60,
    "AUTH": 40,
    "API": 100,
}

# -----------------------------------------------------------------------------
# Derived constants
# -----------------------------------------------------------------------------
TOTAL_EVENTS = EVENTS_PER_HOUR * RUN_HOURS
SECONDS_PER_EVENT = 3600 / EVENTS_PER_HOUR
REQUIRED_FIELDS = {
    "timestamp",
    "server_id",
    "region",
    "event_type",
    "severity",
    "metadata",
}

shutdown_requested = False
pending_correlations: Deque[dict[str, Any]] = deque()

def fake_user_name() -> str:
    """Generate a random username."""
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8))

def fake_ipv4_public() -> str:
    """Generate a random IPv4 address."""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))



def request_shutdown(signum: int, _frame: Any) -> None:
    """Handle SIGINT/SIGTERM without losing already emitted events."""
    global shutdown_requested
    shutdown_requested = True
    print(f"Shutdown requested by signal {signum}; stopping gracefully...", file=sys.stderr)


def utc_timestamp(value: datetime) -> str:
    """Return an ISO-8601 UTC timestamp with a Z suffix."""
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def weighted_event_type() -> str:
    """Select an event type from EVENT_DISTRIBUTION_PCT."""
    event_types = list(EVENT_DISTRIBUTION_PCT.keys())
    weights = list(EVENT_DISTRIBUTION_PCT.values())
    return random.choices(event_types, weights=weights, k=1)[0]


def server_id(prefix: str) -> str:
    """Generate stable-looking infrastructure server IDs like APP-001."""
    return f"{prefix}-{random.randint(1, SERVER_COUNTS[prefix]):03d}"


def severity_from_metric(value: float, warning: float, critical: float) -> str:
    """Map metric values to operational severity levels."""
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "INFO"


def base_event(now: datetime, event_type: str, server_prefix: str) -> dict[str, Any]:
    """Create required shared fields for every event."""
    return {
        "timestamp": utc_timestamp(now),
        "server_id": server_id(server_prefix),
        "region": random.choice(REGION_LIST),
        "event_type": event_type,
        "severity": "INFO",
        "metadata": {},
    }


def generate_cpu_spike(now: datetime) -> dict[str, Any]:
    cpu_percent = round(random.uniform(72.0, 99.9), 1)
    event = base_event(now, "cpu_spike", "APP")
    event.update(
        severity=severity_from_metric(cpu_percent, warning=80.0, critical=95.0),
        cpu_percent=cpu_percent,
        metadata={"threshold": 80, "load_avg": round(random.uniform(2.0, 16.0), 2)},
    )
    return event


def generate_memory_full(now: datetime) -> dict[str, Any]:
    memory_percent = round(random.uniform(70.0, 99.9), 1)
    event = base_event(now, "memory_full", random.choice(["APP", "DB"]))
    event.update(
        severity=severity_from_metric(memory_percent, warning=85.0, critical=95.0),
        memory_percent=memory_percent,
        metadata={"swap_used_percent": round(random.uniform(0.0, 75.0), 1)},
    )
    return event


def generate_api_latency(now: datetime, correlated_server: str | None = None) -> dict[str, Any]:
    api_latency_ms = round(random.uniform(250.0, 5_000.0), 1)
    event = base_event(now, "api_latency", "API")
    if correlated_server:
        event["server_id"] = correlated_server.replace("APP", "API", 1)
    event.update(
        severity=severity_from_metric(api_latency_ms, warning=800.0, critical=2_500.0),
        api_latency_ms=api_latency_ms,
        endpoint=random.choice(["/api/orders", "/api/inventory", "/api/users", "/api/health"]),
        metadata={"threshold_ms": 800, "p95_ms": round(api_latency_ms * random.uniform(0.85, 1.15), 1)},
    )
    if correlated_server:
        event["metadata"]["correlated_with"] = correlated_server
        event["metadata"]["correlation"] = "cpu_spike_to_api_latency"
    return event


def generate_auth_failure(now: datetime) -> dict[str, Any]:
    attempts = random.randint(1, 25)
    event = base_event(now, "auth_failure", "AUTH")
    event.update(
        severity="CRITICAL" if attempts >= 20 else "WARNING" if attempts >= 5 else "INFO",
        failed_attempts=attempts,
        user_id=fake_user_name(),
        source_ip=fake_ipv4_public(),
        metadata={"reason": random.choice(["bad_password", "expired_token", "mfa_failed", "locked_account"])},
    )
    return event


def generate_db_error(now: datetime) -> dict[str, Any]:
    error_code = random.choice(["CONNECTION_TIMEOUT", "DEADLOCK", "REPLICA_LAG", "QUERY_TIMEOUT"])
    event = base_event(now, "db_error", "DB")
    event.update(
        severity="CRITICAL" if error_code in {"CONNECTION_TIMEOUT", "DEADLOCK"} else "WARNING",
        error_code=error_code,
        query_time_ms=random.randint(500, 30_000),
        metadata={"database": random.choice(["orders", "inventory", "users", "billing"])},
    )
    return event


GENERATORS: dict[str, Callable[[datetime], dict[str, Any]]] = {
    "cpu_spike": generate_cpu_spike,
    "memory_full": generate_memory_full,
    "api_latency": generate_api_latency,
    "auth_failure": generate_auth_failure,
    "db_error": generate_db_error,
}


def is_recurring_failure_window(now: datetime) -> bool:
    """Return true during the synthetic recurring 2 AM UTC incident window."""
    utc_now = now.astimezone(timezone.utc)
    return utc_now.hour == 2 and utc_now.minute < 15


def validate_event(event: dict[str, Any]) -> None:
    """Ensure every emitted event includes the required schema fields."""
    missing = REQUIRED_FIELDS - event.keys()
    if missing:
        raise ValueError(f"Generated event missing required fields: {sorted(missing)}")


def queue_correlated_latency_event(cpu_event: dict[str, Any], now: datetime) -> None:
    """Queue a follow-on API latency event caused by a CPU spike."""
    correlated_at = now + timedelta(seconds=random.randint(5, 90))
    pending_correlations.append(generate_api_latency(correlated_at, correlated_server=cpu_event["server_id"]))


def generate_event(now: datetime) -> dict[str, Any]:
    """Generate one realistic synthetic event with operational patterns."""
    if pending_correlations and random.random() < 0.4:
        return pending_correlations.popleft()

    if is_recurring_failure_window(now) and random.random() < 0.65:
        event_type = random.choice(["auth_failure", "db_error"])
    else:
        event_type = weighted_event_type()

    event = GENERATORS[event_type](now)

    # Correlation pattern: CPU pressure often causes API latency soon after.
    if event_type == "cpu_spike" and random.random() < 0.35:
        queue_correlated_latency_event(event, now)

    return event


def run() -> int:
    signal.signal(signal.SIGINT, request_shutdown)
    signal.signal(signal.SIGTERM, request_shutdown)

    start_time = time.monotonic()
    logical_time = datetime.now(timezone.utc)
    events_sent = 0

    try:
        while events_sent < TOTAL_EVENTS and not shutdown_requested:
            event = generate_event(logical_time)
            validate_event(event)
            print(json.dumps(event, separators=(",", ":")), flush=False)

            events_sent += 1
            logical_time += timedelta(seconds=SECONDS_PER_EVENT)

            if events_sent % PRINT_EVERY_EVENTS == 0:
                elapsed_minutes = max((time.monotonic() - start_time) / 60, 1 / 60)
                rate_per_minute = round(events_sent / elapsed_minutes)
                print(f"Events sent: {events_sent}, Rate: {rate_per_minute}/min", file=sys.stderr, flush=True)

            target_elapsed = events_sent * SECONDS_PER_EVENT
            sleep_for = target_elapsed - (time.monotonic() - start_time)
            if sleep_for > 0:
                time.sleep(min(sleep_for, 1.0))
    except BrokenPipeError:
        return 0
    finally:
        print(f"Generator stopped. Total events sent: {events_sent}", file=sys.stderr, flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
