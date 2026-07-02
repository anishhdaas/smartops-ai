# SmartOps AI

SmartOps AI is a production-style data engineering and AI operations project that simulates, processes, validates, enriches, and analyzes 1M+ synthetic infrastructure events. It shows an end-to-end modern analytics stack: Kafka, Python, Snowflake, dbt, Great Expectations, Pinecone, OpenRouter, MCP, Docker, GitHub Actions, and Power BI.

The AI layer uses OpenRouter, not Anthropic. The configured chat model is `qwen/qwen3-32b:free`. Historical incident retrieval uses Pinecone integrated embeddings with `llama-text-embed-v2`.

## Portfolio Summary

SmartOps AI is built as a resume-ready portfolio project for data engineering, analytics engineering, and AI platform roles. It demonstrates streaming ingestion, warehouse modeling, data quality validation, RAG, operational APIs, containerized deployment, and CI validation. The final Power BI dashboard is created after data is loaded into Snowflake.

Resume description:

> Built SmartOps AI, an end-to-end AI operations analytics platform processing 1M+ synthetic infrastructure events with Kafka, Python, Snowflake, dbt, Great Expectations, Pinecone integrated embeddings, OpenRouter LLM inference, MCP tools, Docker, GitHub Actions, and Power BI reporting.

## Architecture

1. Python generates synthetic infrastructure events.
2. Kafka streams events through the `raw_incidents` topic.
3. Python consumer validates events and writes valid and invalid records to Snowflake.
4. dbt transforms raw Snowflake tables into analytics models.
5. Great Expectations validates warehouse quality rules.
6. Pinecone stores incident history using integrated embeddings with `llama-text-embed-v2`.
7. RAG and MCP services answer incident questions through OpenRouter using `qwen/qwen3-32b:free`.
8. Power BI is the final manual dashboard step after Snowflake data is loaded.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Beginner Setup

Prerequisites:

- Docker Desktop
- Python 3.11
- Snowflake account
- Pinecone account and index using integrated embeddings
- OpenRouter API key
- Power BI Desktop for the final dashboard step

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Fill in `.env`:

```bash
OPENROUTER_API_KEY=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_DATABASE=INCIDENT_WAREHOUSE
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
PINECONE_API_KEY=...
PINECONE_HOST=...
PINECONE_INDEX=incidents
```

3. Start the production Docker stack:

```bash
./shell/deploy.sh
```

4. Watch logs:

```bash
docker compose logs -f
```

5. Check MCP health:

```bash
curl http://localhost:5000/health
```

6. After data is loaded and transformed in Snowflake, connect Power BI Desktop to Snowflake and build the dashboard.

## Local Development

Install test dependencies:

```bash
python3 -m pip install -r tests/requirements.txt
```

Run tests:

```bash
pytest -q
```

Run local processes without Docker:

```bash
./shell/start.sh
```

## Main Services

- `zookeeper`: Kafka coordination.
- `kafka`: Streaming broker on port `9092`.
- `log-generator`: Python synthetic infrastructure event producer.
- `kafka-consumer`: Python validation and Snowflake loader.
- `dbt-runner`: Snowflake transformation runner.
- `data-quality`: Great Expectations validation runner.
- `embeddings-refresh`: Pinecone incident history refresh job.
- `mcp-server`: JSON API and MCP-style tool server on port `5000`.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Deployment](docs/DEPLOYMENT.md)
- [API Docs](docs/API_DOCS.md)
- [Free Tier Setup](docs/FREE_TIER_SETUP.md)

## Notes

- OpenRouter is the only LLM provider used.
- Anthropic is intentionally not used.
- Pinecone embeddings are handled through integrated embeddings, not local embedding code.
- Power BI stays outside Docker because it is the final manual desktop reporting step.
