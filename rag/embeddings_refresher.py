#!/usr/bin/env python3
"""Daily Pinecone integrated-embedding refresh job for incident intelligence."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd
import snowflake.connector
from pinecone import Pinecone

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_HOST = os.getenv("PINECONE_HOST", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "incidents")
PINECONE_NAMESPACE = "incidents"
PINECONE_EMBED_MODEL = "llama-text-embed-v2"
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
        f"in region {row.get('REGION') or row.get('REGION_KEY')} with event_type {row.get('EVENT_TYPE')} "
        f"and severity {row.get('SEVERITY')}. Metrics: cpu={row.get('CPU_PERCENT')}, "
        f"memory={row.get('MEMORY_PERCENT')}, api_latency_ms={row.get('API_LATENCY_MS')}."
    )


def pinecone_index() -> Any:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(host=PINECONE_HOST or PINECONE_INDEX)


def upsert_to_pinecone(records: pd.DataFrame) -> None:
    if records.empty:
        return
    index = pinecone_index()
    rows = []
    for _, row in records.iterrows():
        metadata = {key.lower(): str(value) for key, value in row.items() if pd.notna(value)}
        metadata["summary"] = row["summary"]
        rows.append(
            {
                "id": str(row.get("INCIDENT_ID")),
                "text": row["summary"],
                **metadata,
            }
        )
    index.upsert_records(namespace=PINECONE_NAMESPACE, records=rows)


def update_local_cache(records: pd.DataFrame) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    records.to_parquet(CACHE_PATH, index=False)


def main() -> int:
    incidents = fetch_recent_incidents()
    logger.info("Fetched %s incidents from Snowflake", len(incidents))
    if not incidents.empty:
        incidents["summary"] = incidents.apply(incident_summary, axis=1)
        upsert_to_pinecone(incidents)
    update_local_cache(incidents)
    print(f"Number of incidents processed: {len(incidents)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
