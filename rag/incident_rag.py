#!/usr/bin/env python3
"""RAG assistant for incident intelligence over Snowflake, Pinecone, and OpenRouter."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import snowflake.connector
from pinecone import Pinecone

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "qwen/qwen3-32b:free"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_HOST = os.getenv("PINECONE_HOST", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "incidents")
PINECONE_EMBED_MODEL = "llama-text-embed-v2"

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "INCIDENT_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

CACHE_PATH = Path("/vector_db/incidents.parquet")


def _snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    args: dict[str, Any] = {
        "user": SNOWFLAKE_USER,
        "password": SNOWFLAKE_PASSWORD,
        "account": SNOWFLAKE_ACCOUNT,
        "database": SNOWFLAKE_DATABASE,
        "schema": SNOWFLAKE_SCHEMA,
        "warehouse": SNOWFLAKE_WAREHOUSE,
    }
    if SNOWFLAKE_ROLE:
        args["role"] = SNOWFLAKE_ROLE
    return snowflake.connector.connect(**args)


def _query_current_incidents() -> list[dict[str, Any]]:
    sql = """
        SELECT TOP 100 *
        FROM fct_incidents
        WHERE region = 'Bangalore'
          AND event_type = 'auth_failure'
        ORDER BY timestamp DESC
    """
    with _snowflake_connection() as conn:
        with conn.cursor(snowflake.connector.DictCursor) as cur:
            cur.execute(sql)
            return list(cur.fetchall())


def _pinecone_index() -> Any:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(host=PINECONE_HOST or PINECONE_INDEX)


def _pinecone_history(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    index = _pinecone_index()
    result = index.search(
        namespace="incidents",
        query={
            "inputs": {"text": query},
            "top_k": top_k,
        },
        fields=["summary", "incident_id", "server_id", "region", "event_type", "severity", "timestamp"],
    )
    hits = result.get("result", {}).get("hits", []) if isinstance(result, dict) else []
    return [hit.get("fields", {}) for hit in hits]


def _cache_history(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    if not CACHE_PATH.exists():
        return []
    cache = pd.read_parquet(CACHE_PATH)
    if cache.empty:
        return []
    query_terms = {term.lower() for term in query.split() if len(term) > 3}
    if not query_terms or "summary" not in cache.columns:
        return cache.head(top_k).to_dict("records")
    cache["_score"] = cache["summary"].fillna("").str.lower().apply(
        lambda value: sum(term in value for term in query_terms)
    )
    return cache.sort_values("_score", ascending=False).head(top_k).drop(columns=["_score"]).to_dict("records")


def _historical_context(query: str) -> tuple[list[dict[str, Any]], str | None]:
    try:
        return _pinecone_history(query), None
    except Exception as exc:
        return _cache_history(query), f"Pinecone unavailable; skipped vector search and used local cache when available: {exc}"


def _snowflake_only_analysis(query: str, current_incidents: list[dict[str, Any]], warning: str | None) -> str:
    affected_systems = sorted({str(row.get("SERVER_ID") or row.get("server_id")) for row in current_incidents if row.get("SERVER_ID") or row.get("server_id")})[:10]
    severities = [str(row.get("SEVERITY") or row.get("severity")) for row in current_incidents]
    critical_count = severities.count("CRITICAL")
    warning_count = severities.count("WARNING")
    result = {
        "root_cause": (
            f"OpenRouter was unavailable, so this is a Snowflake-only analysis for: {query}. "
            f"The latest sample contains {len(current_incidents)} Bangalore auth_failure incidents, "
            f"including {critical_count} CRITICAL and {warning_count} WARNING events. "
            "Likely causes include authentication service instability, credential attack bursts, or upstream identity-provider latency."
        ),
        "affected_systems": affected_systems,
        "timeline": "Based on the latest 100 Snowflake records ordered by timestamp descending.",
        "recommended_actions": [
            "Inspect authentication service logs for the affected servers.",
            "Check identity-provider latency and error rates.",
            "Review failed-login source IP patterns for brute-force activity.",
            "Correlate auth failures with deployment and infrastructure changes.",
        ],
    }
    if warning:
        result["recommended_actions"].append(warning)
    return json.dumps(result, ensure_ascii=False)


def _call_openrouter(query: str, current_incidents: list[dict[str, Any]], historical_incidents: list[dict[str, Any]], warning: str | None) -> str:
    context = {
        "current_incidents": current_incidents,
        "historical_similar_incidents": historical_incidents,
        "retrieval_warning": warning,
    }
    prompt = f"""
Analyze this incident intelligence question using the supplied Snowflake incidents and historical Pinecone context.
Return only valid JSON with this exact shape:
{{
  "root_cause": "string",
  "affected_systems": ["string"],
  "timeline": "string",
  "recommended_actions": ["string"]
}}

Question: {query}
Context JSON: {json.dumps(context, default=str)}
"""
    response = requests.post(
        OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"]


def ask_incident_question(query: str) -> str:
    """Answer an incident intelligence question as a JSON string."""
    current_incidents = _query_current_incidents()
    historical_incidents, warning = _historical_context(query, top_k=5)

    try:
        answer = _call_openrouter(query, current_incidents, historical_incidents, warning)
    except Exception:
        return _snowflake_only_analysis(query, current_incidents, warning)

    try:
        parsed = json.loads(answer)
    except json.JSONDecodeError:
        parsed = {
            "root_cause": answer,
            "affected_systems": [],
            "timeline": "Unable to parse structured timeline from model response.",
            "recommended_actions": [],
        }
    return json.dumps(parsed, ensure_ascii=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ask the incident RAG assistant a question.")
    parser.add_argument("query")
    args = parser.parse_args()
    print(ask_incident_question(args.query))
