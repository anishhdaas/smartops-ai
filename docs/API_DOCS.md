# SmartOps AI API Docs

The MCP server exposes a plain JSON API for operational tools. It uses OpenRouter for LLM summaries and Snowflake, Kafka, and local runbook files for operational context.

Base URL:

```text
http://localhost:5000
```

## Health

```http
GET /health
```

Example:

```bash
curl http://localhost:5000/health
```

Response:

```json
{
  "ok": true,
  "service": "smartops-ai-mcp",
  "tools": [
    "get_incident_history",
    "kafka_health_check",
    "query_incidents",
    "query_snowflake",
    "suggest_runbook"
  ],
  "openrouter_configured": true,
  "openrouter_model": "qwen/qwen3-32b:free"
}
```

## Tool Calls

```http
POST /tools
Content-Type: application/json
```

Request shape:

```json
{
  "tool": "tool_name",
  "args": {}
}
```

Response shape:

```json
{
  "ok": true,
  "result": {}
}
```

Errors are returned as plain JSON:

```json
{
  "ok": false,
  "error": "message"
}
```

## query_incidents

Returns incidents filtered by region, event type, and date window.

```bash
curl -X POST http://localhost:5000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "query_incidents",
    "args": {
      "region": "Bangalore",
      "event_type": "auth_failure",
      "date_range": "7 days"
    }
  }'
```

## query_snowflake

Runs safe read-only SQL against Snowflake. Only single `SELECT` or `WITH` statements are allowed. Mutating SQL such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, and multi-statement SQL is blocked.

```bash
curl -X POST http://localhost:5000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "query_snowflake",
    "args": {
      "sql": "select event_type, count(*) as incidents from fct_incidents group by event_type"
    }
  }'
```

## get_incident_history

Returns incident counts for a server over a date window.

```bash
curl -X POST http://localhost:5000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_incident_history",
    "args": {
      "server_id": "AUTH-001",
      "days": 7
    }
  }'
```

## suggest_runbook

Returns a matching runbook and, when `OPENROUTER_API_KEY` is configured, an OpenRouter summary.

OpenRouter endpoint:

```text
https://openrouter.ai/api/v1/chat/completions
```

Model:

```text
qwen/qwen3-32b:free
```

```bash
curl -X POST http://localhost:5000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "suggest_runbook",
    "args": {
      "issue_type": "auth_failure"
    }
  }'
```

## kafka_health_check

Returns Kafka broker status, topic, partition count, consumer group, and approximate consumer lag.

```bash
curl -X POST http://localhost:5000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "kafka_health_check",
    "args": {}
  }'
```

## RAG Behavior

The RAG service combines current Snowflake incidents with Pinecone history. Pinecone uses integrated embeddings with `llama-text-embed-v2`; no local embedding model is required.

OpenRouter is the only LLM provider. Anthropic is not used.
