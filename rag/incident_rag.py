#!/usr/bin/env python3
"""RAG assistant for incident intelligence over Snowflake and Pinecone."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import anthropic
import pandas as pd
import snowflake.connector
from pinecone import Pinecone

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_HOST = os.getenv("PINECONE_HOST", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "incidents")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "INCIDENT_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

CACHE_PATH = Path("/vector_db/incidents.parquet")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
EMBEDDING_MODEL = os.getenv("ANTHROPIC_EMBEDDING_MODEL", "embed-v3-small")


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


def _query_current_incidents(region: str = "Bangalore", event_type: str = "auth_failure") -> list[dict[str, Any]]:
    sql = """
        SELECT TOP 100 *
        FROM fct_incidents
        WHERE region_key IN (
            SELECT region_id FROM dim_regions WHERE region_name = %(region)s
        )
          AND event_type = %(event_type)s
        ORDER BY ingested_at DESC
    """
    with _snowflake_connection() as conn:
        with conn.cursor(snowflake.connector.DictCursor) as cur:
            cur.execute(sql, {"region": region, "event_type": event_type})
            return list(cur.fetchall())


def _embed_text(text: str) -> list[float]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def _pinecone_history(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    embedding = _embed_text(query)
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(host=PINECONE_HOST or PINECONE_INDEX)
    result = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return [match.get("metadata", {}) for match in result.get("matches", [])]


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
    except Exception as exc:  # Pinecone outages must not block Snowflake-only analysis.
        return _cache_history(query), f"Pinecone unavailable; used local cache fallback: {exc}"


def _call_claude(query: str, current_incidents: list[dict[str, Any]], historical_incidents: list[dict[str, Any]], warning: str | None) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    context = {
        "current_incidents": current_incidents,
        "historical_incidents": historical_incidents,
        "retrieval_warning": warning,
    }
    prompt = f"""
You are an incident intelligence assistant. Analyze the user question using the supplied current Snowflake incidents and historical incident context.

Return only valid JSON with this exact shape:
{{
  "root_cause": "string",
  "affected_systems": ["string"],
  "timeline": "string",
  "recommended_actions": ["string"]
}}

User question: {query}
Context JSON: {json.dumps(context, default=str)}
"""
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1200,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def ask_incident_question(query: str) -> str:
    """Answer an incident intelligence question as a JSON string."""
    current_incidents = _query_current_incidents(region="Bangalore", event_type="auth_failure")
    historical_incidents, warning = _historical_context(query, top_k=5)
    answer = _call_claude(query, current_incidents, historical_incidents, warning)

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
