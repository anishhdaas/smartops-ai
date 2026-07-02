from __future__ import annotations


def test_validate_incident_accepts_good_event(consumer_module):
    event = {
        "timestamp": "2026-07-02T12:00:00Z",
        "server_id": "APP-001",
        "event_type": "cpu_spike",
        "severity": "WARNING",
        "region": "Bangalore",
        "metadata": {"threshold": 80},
    }

    is_valid, errors = consumer_module.validate_incident(event)

    assert is_valid is True
    assert errors == []
    assert consumer_module.should_store_valid_event(event) is True


def test_validate_incident_rejects_bad_event(consumer_module):
    event = {
        "timestamp": "not-a-timestamp",
        "server_id": "APP-001",
        "event_type": "cpu_spike",
        "severity": "SEVERE",
        "region": "Mars",
        "metadata": "not-json",
    }

    is_valid, errors = consumer_module.validate_incident(event)

    assert is_valid is False
    assert any("invalid severity" in error for error in errors)
    assert any("invalid region" in error for error in errors)
    assert any("metadata must be an object" in error for error in errors)
    assert any("invalid timestamp" in error for error in errors)


def test_validate_incident_rejects_missing_required_fields(consumer_module):
    is_valid, errors = consumer_module.validate_incident({"severity": "INFO"})

    assert is_valid is False
    assert any("missing required fields" in error for error in errors)
