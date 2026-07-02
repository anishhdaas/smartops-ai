# SmartOps AI Deployment

This guide explains how to run SmartOps AI with Docker and how to validate the deployment.

## Prerequisites

- Docker Desktop running
- Git
- Snowflake account
- Pinecone index configured for integrated embeddings
- OpenRouter API key
- Power BI Desktop for the final dashboard step

## Environment Setup

Create `.env`:

```bash
cp .env.example .env
```

Fill in:

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

Optional:

```bash
SNOWFLAKE_SCHEMA=ANALYTICS
SNOWFLAKE_ROLE=ACCOUNTADMIN
EVENTS_PER_HOUR=125000
RUNTIME_HOURS=8
```

## Start With Docker

Use the deploy script:

```bash
./shell/deploy.sh
```

The script checks Docker, validates `.env`, builds containers, starts Docker Compose, prints status, and runs basic health checks.

Manual commands:

```bash
docker compose build
docker compose up -d
docker compose ps
```

## Services

- `zookeeper`
- `kafka`
- `log-generator`
- `kafka-consumer`
- `dbt-runner`
- `data-quality`
- `embeddings-refresh`
- `mcp-server`

Kafka exposes:

```text
localhost:9092
```

MCP exposes:

```text
http://localhost:5000
```

## Health Checks

MCP:

```bash
curl http://localhost:5000/health
```

Kafka and container status:

```bash
docker compose ps
```

Logs:

```bash
docker compose logs -f
```

## Local Non-Docker Run

Install dependencies first, then run:

```bash
./shell/start.sh
```

This validates required environment variables, waits for Kafka and Snowflake, creates the `raw_incidents` topic, and starts the producer, consumer, dbt, validation, embeddings refresh, and MCP services.

## CI/CD

GitHub Actions runs on pushes to `main` and on a daily schedule. The workflow:

- Uses Python 3.11
- Installs all requirements
- Validates required secrets
- Runs syntax checks
- Runs pytest
- Builds the Docker image
- Validates Docker Compose config
- Uploads logs on failure

## Final Dashboard Step

After Snowflake contains loaded and transformed data, open Power BI Desktop and connect it to Snowflake. Build visuals from `INCIDENT_WAREHOUSE.ANALYTICS`, especially `fct_incidents` and `dim_regions`.

Power BI is not containerized because it is a final manual desktop reporting step.
