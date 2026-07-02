# Free Tier Setup

This guide helps beginners run SmartOps AI using free or low-cost tiers where possible.

## Accounts

Create accounts for:

- OpenRouter
- Snowflake
- Pinecone
- GitHub
- Microsoft Power BI Desktop

## OpenRouter

1. Create an OpenRouter account.
2. Create an API key.
3. Add it to `.env`:

```bash
OPENROUTER_API_KEY=your_key_here
```

SmartOps AI uses:

```text
qwen/qwen3-32b:free
```

Do not configure Anthropic. This project uses OpenRouter only.

## Snowflake

1. Create a Snowflake trial account.
2. Create or use a warehouse such as `COMPUTE_WH`.
3. Run the SQL setup in `snowflake/schema.sql`.
4. Add credentials to `.env`:

```bash
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_DATABASE=INCIDENT_WAREHOUSE
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

Beginner tip: keep the warehouse small while testing, and stop it when not in use.

## Pinecone

1. Create a Pinecone account.
2. Create an index named `incidents`.
3. Use integrated embeddings with:

```text
llama-text-embed-v2
```

4. Add values to `.env`:

```bash
PINECONE_API_KEY=...
PINECONE_HOST=...
PINECONE_INDEX=incidents
```

The embeddings refresh job writes incident summaries to Pinecone and stores a local cache in `vector_db/`.

## Docker

Install Docker Desktop and start it.

Run:

```bash
./shell/deploy.sh
```

This starts Kafka, Python services, dbt, Great Expectations, Pinecone refresh, and MCP.

## GitHub Actions

Add repository secrets:

- `OPENROUTER_API_KEY`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ACCOUNT`
- `PINECONE_API_KEY`
- `PINECONE_HOST`

The workflow runs on pushes to `main` and daily. It installs dependencies, checks syntax, runs pytest, builds Docker, and uploads logs on failure.

## Power BI

Power BI is the final step after data is loaded into Snowflake.

1. Open Power BI Desktop.
2. Connect to Snowflake.
3. Select analytics tables such as `fct_incidents` and `dim_regions`.
4. Build dashboard pages for incident volume, severity, region, event type, affected servers, latency, and authentication failures.

Power BI is intentionally kept out of Docker because it is a manual desktop dashboard step.

## Portfolio Notes

Use this project to demonstrate:

- Streaming ingestion of 1M+ synthetic infrastructure events.
- Python production services.
- Kafka event pipelines.
- Snowflake warehouse design.
- dbt analytics engineering.
- Great Expectations quality checks.
- Pinecone integrated embeddings with `llama-text-embed-v2`.
- OpenRouter LLM reasoning with `qwen/qwen3-32b:free`.
- MCP operational tools.
- Docker deployment.
- GitHub Actions CI.
- Power BI business reporting.
