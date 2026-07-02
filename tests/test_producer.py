from __future__ import annotations

from datetime import datetime, timezone


def test_generate_event_creates_required_fields(producer_module):
    event = producer_module.generate_event(datetime(2026, 7, 2, tzinfo=timezone.utc))

    assert producer_module.REQUIRED_FIELDS <= event.keys()
    producer_module.validate_event(event)
    assert isinstance(event["metadata"], dict)


def test_generated_event_values_are_realistic(producer_module):
    now = datetime(2026, 7, 2, tzinfo=timezone.utc)

    for _ in range(100):
        event = producer_module.generate_event(now)
        assert event["region"] in producer_module.REGION_LIST
        assert event["event_type"] in producer_module.EVENT_DISTRIBUTION_PCT
        assert event["severity"] in {"INFO", "WARNING", "CRITICAL"}
        assert event["server_id"].split("-", 1)[0] in producer_module.SERVER_COUNTS

        if "cpu_percent" in event:
            assert 72.0 <= event["cpu_percent"] <= 99.9
        if "memory_percent" in event:
            assert 70.0 <= event["memory_percent"] <= 99.9
        if "api_latency_ms" in event:
            assert 250.0 <= event["api_latency_ms"] <= 5000.0
        if "failed_attempts" in event:
            assert 1 <= event["failed_attempts"] <= 25
        if "query_time_ms" in event:
            assert 500 <= event["query_time_ms"] <= 30000
