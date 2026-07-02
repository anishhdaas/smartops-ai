#!/usr/bin/env python3
"""Daily embeddings refresh job for incident intelligence.

Schedule this script externally for 02:00 UTC, for example from CI/CD or a
cron-compatible scheduler.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import anthropic
import pandas as pd
import snowflake.connector
from pinecone import Pinecone

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_HOST = os.getenv("PINECONE_HOST", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "incidents")
EMBEDDING_MODEL = os.getenv("ANTHROPIC_EMBEDDING_MODEL", "embed-v3-small")
CACHE_PATH = Path("/vector_db/incidents.parquet")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "INCIDENT_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")


def snowflake_connection() -> snowflake.connector.SnowflakeConnection:
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


def fetch_recent_incidents() -> pd.DataFrame:
    sql = """
        SELECT *
        FROM fct_incidents
        WHERE created_at > DATEADD(day, -1, CURRENT_DATE)
    """
    with snowflake_connection() as conn:
        return pd.read_sql(sql, conn)


def incident_summary(row: pd.Series) -> str:
    return (
        f"Incident {row.get('INCIDENT_ID')} on server {row.get('SERVER_ID')} "
        f"in region_key {row.get('REGION_KEY')} with event_type {row.get('EVENT_TYPE')} "
        f"and severity {row.get('SEVERITY')}. Metrics: cpu={row.get('CPU_PERCENT')}, "
        f"memory={row.get('MEMORY_PERCENT')}, api_latency_ms={row.get('API_LATENCY_MS')}."
    )


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    embeddings: list[list[float]] = []
    for text in texts:
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
        embeddings.append(response.data[0].embedding)
    return embeddings


def upsert_to_pinecone(records: pd.DataFrame, embeddings: list[list[float]]) -> None:
    if records.empty:
        return
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(host=PINECONE_HOST or PINECONE_INDEX)
    vectors = []
    for (_, row), embedding in zip(records.iterrows(), embeddings, strict=True):
        incident_id = str(row.get("INCIDENT_ID"))
        metadata = {key.lower(): str(value) for key, value in row.items() if pd.notna(value)}
        metadata["summary"] = row["summary"]
        vectors.append({"id": incident_id, "values": embedding, "metadata": metadata})
    index.upsert(vectors=vectors)


def update_local_cache(records: pd.DataFrame, embeddings: list[list[float]]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    cached = records.copy()
    cached["embedding"] = [json.dumps(vector) for vector in embeddings]
    cached.to_parquet(CACHE_PATH, index=False)


def main() -> int:
    incidents = fetch_recent_incidents()
    logger.info("Fetched %s incidents from Snowflake", len(incidents))
    if incidents.empty:
        update_local_cache(incidents, [])
        logger.info("Number of incidents processed: 0")
        return 0

    incidents["summary"] = incidents.apply(incident_summary, axis=1)
    embeddings = embed_texts(incidents["summary"].tolist())
    upsert_to_pinecone(incidents, embeddings)
    update_local_cache(incidents, embeddings)
    logger.info("Number of incidents processed: %s", len(incidents))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
