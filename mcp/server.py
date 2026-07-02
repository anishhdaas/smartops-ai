#!/usr/bin/env python3
"""Read-only incident intelligence MCP-style tool server.

The module exposes callable tools and a simple JSON-over-stdin/stdout loop for
OpenRouter-enabled MCP integration wrappers.
"""

from __future__ import annotations

import json
import logging
import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from pathlib import Path
from typing import Any, Callable

import requests
import snowflake.connector
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 30
RUNBOOK_DIR = Path("docs/runbooks")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "qwen/qwen3-32b:free"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_incidents")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "validation_group")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "INCIDENT_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

shutdown_requested = False


def _shutdown(_signum: int, _frame: Any) -> None:
    global shutdown_requested
    shutdown_requested = True


def _run_with_timeout(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(fn, *args, **kwargs)
        try:
            return future.result(timeout=TIMEOUT_SECONDS)
        except FutureTimeout as exc:
            raise TimeoutError(f"Tool timed out after {TIMEOUT_SECONDS}s") from exc


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


def _fetch_all(sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    logger.info("Snowflake query: %s params=%s", sql, params)
    with _snowflake_connection() as conn:
        with conn.cursor(snowflake.connector.DictCursor) as cur:
            cur.execute(sql, params or {})
            rows = list(cur.fetchall())
    logger.info("Snowflake rows returned: %s", len(rows))
    return rows


def _openrouter_generate(prompt: str) -> str:
    response = requests.post(
        OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": OPENROUTER_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def query_incidents(region: str, event_type: str, date_range: str) -> list[dict[str, Any]]:
    """Return incidents by region, event type, and date range such as '7 days'."""
    sql = """
        SELECT f.*
        FROM fct_incidents f
        JOIN dim_regions r ON f.region_key = r.region_id
        WHERE r.region_name = %(region)s
          AND f.event_type = %(event_type)s
          AND f.event_date >= DATEADD(day, -TRY_TO_NUMBER(SPLIT_PART(%(date_range)s, ' ', 1)), CURRENT_DATE)
        ORDER BY f.event_date DESC
        LIMIT 500
    """
    return _run_with_timeout(_fetch_all, sql, {"region": region, "event_type": event_type, "date_range": date_range})


def query_snowflake(sql: str) -> list[dict[str, Any]]:
    """Execute read-only custom SQL against Snowflake."""
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        raise ValueError("Only read-only SELECT statements are allowed")
    return _run_with_timeout(_fetch_all, sql)


def get_incident_history(server_id: str, days: int) -> list[dict[str, Any]]:
    """Return a time series of incident counts for a server over the requested number of days."""
    sql = """
        SELECT
            event_date,
            severity,
            event_type,
            COUNT(*) AS incident_count
        FROM fct_incidents
        WHERE server_id = %(server_id)s
          AND event_date >= DATEADD(day, -%(days)s, CURRENT_DATE)
        GROUP BY event_date, severity, event_type
        ORDER BY event_date ASC, severity, event_type
    """
    return _run_with_timeout(_fetch_all, sql, {"server_id": server_id, "days": days})


def suggest_runbook(issue_type: str) -> dict[str, str]:
    """Retrieve a matching runbook from docs/runbooks/ and optionally summarize it with OpenRouter."""
    safe_issue_type = "".join(ch for ch in issue_type.lower() if ch.isalnum() or ch in {"_", "-"})
    candidates = [RUNBOOK_DIR / f"{safe_issue_type}.md", RUNBOOK_DIR / f"{safe_issue_type}.txt"]
    for path in candidates:
        if path.exists() and path.is_file():
            content = path.read_text(encoding="utf-8")
            summary = None
            try:
                summary = _run_with_timeout(
                    _openrouter_generate,
                    f"Summarize this incident runbook into concise recommended actions:\n\n{content[:8000]}",
                )
            except Exception as exc:
                logger.warning("OpenRouter runbook summary unavailable: %s", exc)
            logger.info("Runbook returned for issue_type=%s path=%s", issue_type, path)
            return {"issue_type": issue_type, "path": str(path), "content": content, "ai_summary": summary or ""}
    raise FileNotFoundError(f"No runbook found for issue_type={issue_type}")


def kafka_health_check() -> dict[str, Any]:
    """Return Kafka broker status and approximate topic lag."""
    def _check() -> dict[str, Any]:
        consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
            group_id=KAFKA_CONSUMER_GROUP,
            enable_auto_commit=False,
            consumer_timeout_ms=1000,
        )
        try:
            partitions = consumer.partitions_for_topic(KAFKA_TOPIC) or set()
            topic_partitions = [TopicPartition(KAFKA_TOPIC, partition) for partition in partitions]
            end_offsets = consumer.end_offsets(topic_partitions) if topic_partitions else {}
            committed_offsets = {tp: consumer.committed(tp) or 0 for tp in topic_partitions}
            lag = sum(end_offsets.get(tp, 0) - committed_offsets.get(tp, 0) for tp in topic_partitions)
            result = {
                "broker_status": "available",
                "topic": KAFKA_TOPIC,
                "partitions": len(partitions),
                "consumer_group": KAFKA_CONSUMER_GROUP,
                "consumer_lag": lag,
            }
            logger.info("Kafka health result: %s", result)
            return result
        finally:
            consumer.close()

    try:
        return _run_with_timeout(_check)
    except KafkaError as exc:
        logger.exception("Kafka health check failed")
        return {"broker_status": "unavailable", "error": str(exc), "consumer_lag": None}


TOOLS: dict[str, Callable[..., Any]] = {
    "query_incidents": query_incidents,
    "query_snowflake": query_snowflake,
    "get_incident_history": get_incident_history,
    "suggest_runbook": suggest_runbook,
    "kafka_health_check": kafka_health_check,
}


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    tool_name = request.get("tool")
    args = request.get("args", {})
    if tool_name not in TOOLS:
        return {"ok": False, "error": f"Unknown tool: {tool_name}"}
    try:
        result = TOOLS[tool_name](**args)
        logger.info("Tool call success tool=%s result_count=%s", tool_name, len(result) if isinstance(result, list) else 1)
        return {"ok": True, "result": result}
    except Exception as exc:
        logger.exception("Tool call failed tool=%s", tool_name)
        return {"ok": False, "error": str(exc)}


def main() -> int:
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)
    for line in sys.stdin:
        if shutdown_requested:
            break
        if not line.strip():
            continue
        response = handle_request(json.loads(line))
        print(json.dumps(response, default=str), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
