#!/usr/bin/env python3
"""Run incident warehouse validations against Snowflake and emit JSON/HTML/text reports."""

from __future__ import annotations

import html
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import great_expectations as gx  # Imported to make the validation runtime explicit.
import snowflake.connector

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS_FILE = PROJECT_ROOT / "tests" / "expectations.json"
HTML_REPORT_FILE = PROJECT_ROOT / "tests" / "validation_report.html"
LOG_FILE = PROJECT_ROOT / "tests" / "validation_log.txt"

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "INCIDENT_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_suite() -> dict[str, Any]:
    with EXPECTATIONS_FILE.open("r", encoding="utf-8") as suite_file:
        return json.load(suite_file)


def snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    connection_args: dict[str, Any] = {
        "user": SNOWFLAKE_USER,
        "password": SNOWFLAKE_PASSWORD,
        "account": SNOWFLAKE_ACCOUNT,
        "database": SNOWFLAKE_DATABASE,
        "schema": SNOWFLAKE_SCHEMA,
        "warehouse": SNOWFLAKE_WAREHOUSE,
    }
    if SNOWFLAKE_ROLE:
        connection_args["role"] = SNOWFLAKE_ROLE
    return snowflake.connector.connect(**connection_args)


def run_expectation(cursor: Any, expectation: dict[str, Any]) -> dict[str, Any]:
    cursor.execute(expectation["sql"])
    row = cursor.fetchone()
    failed_count = int(row[0]) if row and row[0] is not None else 0
    return {
        "name": expectation["name"],
        "description": expectation.get("description", ""),
        "success": failed_count == 0,
        "failed_count": failed_count,
        "evaluated_at": utc_now(),
    }


def generate_html_report(suite: dict[str, Any], results: list[dict[str, Any]]) -> None:
    passed = sum(1 for result in results if result["success"])
    total = len(results)
    rows = "\n".join(
        f"""
        <tr class=\"{'passed' if result['success'] else 'failed'}\">
          <td>{html.escape(result['name'])}</td>
          <td>{'PASS' if result['success'] else 'FAIL'}</td>
          <td>{result['failed_count']}</td>
          <td>{html.escape(result['description'])}</td>
        </tr>
        """
        for result in results
    )
    report = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>Incident Validation Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; color: #172b4d; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #dfe1e6; padding: 0.65rem; text-align: left; }}
    th {{ background: #f4f5f7; }}
    .passed td:nth-child(2) {{ color: #00875a; font-weight: 700; }}
    .failed td:nth-child(2) {{ color: #de350b; font-weight: 700; }}
  </style>
</head>
<body>
  <h1>Incident Validation Report</h1>
  <p><strong>Suite:</strong> {html.escape(suite['expectation_suite_name'])}</p>
  <p><strong>Asset:</strong> {html.escape(suite['database'])}.{html.escape(suite['schema'])}.{html.escape(suite['table'])}</p>
  <p><strong>Generated:</strong> {utc_now()}</p>
  <p><strong>Summary:</strong> Passed {passed}/{total} expectations</p>
  <table>
    <thead>
      <tr><th>Expectation</th><th>Status</th><th>Failed rows/checks</th><th>Description</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>
"""
    HTML_REPORT_FILE.write_text(report, encoding="utf-8")


def write_log(suite: dict[str, Any], results: list[dict[str, Any]]) -> None:
    payload = {
        "suite": suite["expectation_suite_name"],
        "asset": f"{suite['database']}.{suite['schema']}.{suite['table']}",
        "generated_at": utc_now(),
        "results": results,
    }
    LOG_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    suite = load_suite()
    results: list[dict[str, Any]] = []

    with snowflake_connection() as connection:
        with connection.cursor() as cursor:
            for expectation in suite["expectations"]:
                results.append(run_expectation(cursor, expectation))

    generate_html_report(suite, results)
    write_log(suite, results)

    passed = sum(1 for result in results if result["success"])
    total = len(results)
    status_mark = "✓" if passed == total else "✗"
    print(f"Passed {passed}/{total} expectations {status_mark}")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
