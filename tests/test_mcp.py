from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path


def test_mcp_query_snowflake_returns_plain_json(monkeypatch, mcp_module):
    monkeypatch.setattr(
        mcp_module,
        "_fetch_all",
        lambda sql, params=None: [{"value": Decimal("1.5"), "seen_at": datetime(2026, 7, 2, 12, 0, 0)}],
    )

    response = mcp_module.handle_request({"tool": "query_snowflake", "args": {"sql": "select 1"}})

    assert response["ok"] is True
    json.dumps(response)
    assert response["result"] == [{"value": 1.5, "seen_at": "2026-07-02T12:00:00"}]


def test_mcp_blocks_mutating_sql(mcp_module):
    response = mcp_module.handle_request({"tool": "query_snowflake", "args": {"sql": "delete from fct_incidents"}})

    assert response["ok"] is False
    assert "read-only" in response["error"]


def test_mcp_tools_return_json_safe_payloads(monkeypatch, tmp_path, mcp_module):
    monkeypatch.setattr(mcp_module, "_fetch_all", lambda sql, params=None: [{"incident_id": "INC-1"}])
    monkeypatch.setattr(mcp_module, "_run_with_timeout", lambda fn, *args, **kwargs: fn(*args, **kwargs))
    monkeypatch.setattr(
        mcp_module,
        "kafka_health_check",
        lambda: {"broker_status": "available", "consumer_lag": 0},
    )
    mcp_module.TOOLS["kafka_health_check"] = mcp_module.kafka_health_check

    runbook_dir = tmp_path / "runbooks"
    runbook_dir.mkdir()
    (runbook_dir / "auth_failure.md").write_text("Restart auth workers.", encoding="utf-8")
    monkeypatch.setattr(mcp_module, "RUNBOOK_DIR", runbook_dir)
    monkeypatch.setattr(mcp_module, "_openrouter_generate", lambda prompt: "Restart auth workers.")

    requests = [
        {"tool": "query_incidents", "args": {"region": "Bangalore", "event_type": "auth_failure", "date_range": "7 days"}},
        {"tool": "get_incident_history", "args": {"server_id": "AUTH-001", "days": 7}},
        {"tool": "suggest_runbook", "args": {"issue_type": "auth_failure"}},
        {"tool": "kafka_health_check", "args": {}},
    ]

    for request in requests:
        response = mcp_module.handle_request(request)
        assert response["ok"] is True
        json.dumps(response)


def test_no_anthropic_references_remain():
    project_root = Path(__file__).resolve().parents[1]
    searched_suffixes = {".py", ".txt", ".yml", ".yaml", ".example", "Dockerfile"}
    matches = []

    for path in project_root.rglob("*"):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.name == "test_mcp.py":
            continue
        if path.suffix in searched_suffixes or path.name in searched_suffixes:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            if "anthropic" in text:
                matches.append(str(path.relative_to(project_root)))

    assert matches == []
