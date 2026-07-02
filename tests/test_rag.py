from __future__ import annotations

import json


class MockResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


def test_rag_calls_openrouter_with_expected_model(monkeypatch, rag_module):
    calls = {}

    def fake_post(url, headers, json, timeout):
        calls["url"] = url
        calls["headers"] = headers
        calls["json"] = json
        calls["timeout"] = timeout
        return MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": '{"root_cause":"auth burst","affected_systems":["AUTH-001"],"timeline":"now","recommended_actions":["inspect logs"]}'
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr(rag_module.requests, "post", fake_post)

    answer = rag_module._call_openrouter(
        "why are auth failures rising?",
        [{"SERVER_ID": "AUTH-001", "SEVERITY": "CRITICAL"}],
        [{"summary": "prior auth failure"}],
        None,
    )

    assert json.loads(answer)["root_cause"] == "auth burst"
    assert calls["url"] == "https://openrouter.ai/api/v1/chat/completions"
    assert calls["json"]["model"] == "qwen/qwen3-32b:free"


def test_rag_falls_back_when_openrouter_fails(monkeypatch, rag_module):
    monkeypatch.setattr(
        rag_module,
        "_query_current_incidents",
        lambda: [{"SERVER_ID": "AUTH-001", "SEVERITY": "CRITICAL"}],
    )
    monkeypatch.setattr(rag_module, "_historical_context", lambda query, top_k=5: ([], None))

    def fail_openrouter(*_args, **_kwargs):
        raise RuntimeError("OpenRouter unavailable")

    monkeypatch.setattr(rag_module, "_call_openrouter", fail_openrouter)

    payload = json.loads(rag_module.ask_incident_question("what happened?"))

    assert "OpenRouter was unavailable" in payload["root_cause"]
    assert payload["affected_systems"] == ["AUTH-001"]
    assert payload["recommended_actions"]


def test_pinecone_history_uses_integrated_embedding_search(monkeypatch, rag_module):
    class FakeIndex:
        def search(self, namespace, query, fields):
            assert namespace == "incidents"
            assert query == {"inputs": {"text": "auth failures"}, "top_k": 3}
            assert "summary" in fields
            return {"result": {"hits": [{"fields": {"summary": "matched incident"}}]}}

    monkeypatch.setattr(rag_module, "_pinecone_index", lambda: FakeIndex())

    assert rag_module._pinecone_history("auth failures", top_k=3) == [{"summary": "matched incident"}]
