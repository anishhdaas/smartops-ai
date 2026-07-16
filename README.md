# SmartOps AI – End‑to‑End Data‑Engineering & AI‑Ops Portfolio

---

## Architecture Diagram

Architecture diagram will be added in a future update.
The complete architecture is already documented in docs/ARCHITECTURE.md.

**SmartOps AI** is a production‑grade data engineering and AI operations showcase that simulates, streams, validates, enriches and analyzes over 1 million synthetic infrastructure events. It demonstrates a modern analytics stack built using cloud‑native technologies and production engineering practices for real‑time streaming analytics, AI‑assisted incident intelligence and enterprise data warehousing.

---

## 📈 Business Problem & Value Proposition

Enterprises that run large‑scale cloud infrastructure need to **detect, diagnose, and act on incidents in real time**.  The challenges include:
- **High‑volume event ingestion** (millions of logs per day) without losing fidelity.
- **Reliable data quality** to avoid downstream analytic drift.
- **Fast, contextual incident lookup** for on‑call engineers.
- **Actionable business insights** presented in a self‑service BI dashboard.

**SmartOps AI** solves these problems by wiring together a best‑in‑class streaming pipeline, a cloud data‑warehouse, a robust ELT framework, automated data‑quality checks, and a Retrieval‑Augmented Generation (RAG) assistant that surfaces incident knowledge instantly.

---

## 🏗️ Architecture Overview

```
+----------------+      +-----------+      +----------------+      +----------+
| Synthetic      | -->  | Kafka     | -->  | Python Consumer| -->  | Snowflake |
| Event Generator|      | (zookeeper|      | (validation &  |      | (DW)      |
| (producer.py) |      |  broker)  |      |  loading)      |      +----------+
+----------------+      +-----------+      +----------------+            |
                                                                  |
                                      +---------------------------+-------------------+
                                      |                                            |
                                      v                                            v
                              +----------------+                         +-----------------+
                              | dbt (ELT)      |                         | Great          |
                              | (model layers) |                         | Expectations   |
                              +----------------+                         +-----------------+
                                      |                                            |
                                      v                                            v
                              +----------------+                         +-----------------+
                              | Snowflake      |                         | Pinecone       |
                              | (analytics)    | <-- RAG/LLM (MCP) --> | (vector store) |
                              +----------------+                         +-----------------+
                                      |                                            |
                                      v                                            v
                               +--------------+                         +-----------------+
                               | Power BI     |   ←  (manual) →        | LLM provider   |
                               | Dashboard    |                         +-----------------+
                               +--------------+
```

> **Diagram placeholders** – add rendered PNG/SVG files to `docs/` and reference them above.

### Core Data Flow
1. **Event Generation** – `producer.py` emits synthetic infrastructure logs to **Kafka** (`raw_incidents` topic).
2. **Streaming Validation** – `consumer.py` reads from Kafka, validates each record, and writes **valid** and **invalid** rows to **Snowflake** tables.
3. **ELT with dbt** – dbt models (`staging/`, `marts/`) transform raw tables into analytics‑ready views.
4. **Data Quality Assurance** – **Great Expectations** runs automated suites against the warehouse nightly.
5. **Semantic Search & RAG** – Incident embeddings are stored in **Pinecone**; the **MCP** server exposes a JSON‑API that performs context‑aware retrieval‑augmented generation using an LLM provider.
6. **BI Visualization** – Engineers connect **Power BI** to Snowflake to explore KPIs (throughput, error rates, incident resolution time, etc.).

---

## 📂 Repository Structure

```
smartops-ai/
├─ .github/                # GitHub Actions CI/CD workflows
│   └─ workflows/
│       └─ ci.yml
├─ .env.example            # Environment variable template
├─ Dockerfile              # Production container image
├─ docker-compose.yml      # Multi‑service stack (Kafka, Zookeeper, Snowflake‑mock, …)
├─ docs/                   # Architecture, deployment, API docs
│   ├─ ARCHITECTURE.md
│   ├─ DEPLOYMENT.md
│   ├─ API_DOCS.md
│   └─ POWERBI_DASHBOARD.md
├─ kafka/                  # Producer & consumer Python code
│   ├─ producer.py
│   └─ consumer.py
├─ dbt/                    # dbt project – models, seeds, tests
│   └─ models/
├─ mcp/                    # MCP server exposing RAG & analytics APIs
├─ rag/                    # Pinecone index refresh & query logic
├─ scripts/                # Helper scripts (validation, benchmarks)
├─ tests/                  # Pytest suite (unit + integration)
├─ vector_db/              # Pinecone client wrapper
├─ dashboard/              # Power BI assets & design system placeholders
└─ README.md               # ← This file
```

---

## 🛠️ Quick‑Start (Local Development)

### Prerequisites
- **Docker Desktop** (or Docker Engine) – runs Kafka, Zookeeper, and Snowflake mock.
- **Python 3.11+**
- **Snowflake account** (or use the Docker‑based mock).
- **Pinecone account & index** (configured for integrated embeddings).
- **LLM provider API key** (for inference).
- **Power BI Desktop** (for the final dashboard).

### 1. Clone & Initialise
```bash
git clone https://github.com/<your‑username>/smartops-ai.git
cd smartops-ai
cp .env.example .env   # edit the file with your credentials (see below)
```

### 2. Spin‑up the stack (Docker Compose)
```bash
./shell/deploy.sh          # builds & starts Kafka, Zookeeper, Snowflake mock, etc.
```
> The script creates a dedicated Docker network and streams logs to STDOUT.

### 3. Validate the environment
```bash
docker compose logs -f      # watch all services start up
curl http://localhost:5000/health   # MCP health check (should return 200)
```

### 4. Load synthetic data & run ELT
```bash
# Produce 1 M+ events (adjust COUNT in producer.py if you want more)
python -m producer.producer
# Consume, validate, and write to Snowflake
python -m consumer.consumer
# Run dbt transformations
cd dbt && dbt run && dbt test
```

### 5. Run data‑quality checks
```bash
python -m scripts.run_validations.py   # executes Great Expectations suites
```

### 6. Refresh Pinecone embeddings (RAG)
```bash
python -m rag.embeddings_refresher
```

### 7. Connect Power BI
Open **Power BI Desktop**, choose **Snowflake** as the data source, and point it at the `INCIDENT_WAREHOUSE` database (credentials from `.env`).  Import the `mart_dashboard` view and explore the pre‑built KPI tiles.

### 8. Run the test suite (CI)
```bash
pytest -q
```
> **GitHub Actions** automatically execute the above steps on every push (see `.github/workflows/ci.yml`).

---

## Technical Highlights

| Feature | Technology | Why it matters |
| ------- | ---------- | --------------- |
| **Scalable streaming** | **Kafka** (zookeeper coordination) | Handles high‑volume event ingestion with exactly‑once semantics |
| **Cloud‑native warehouse** | **Snowflake** (auto‑scaling compute) | Near‑instant ELT, separation of storage & compute |
| **ELT framework** | **dbt** (SQL‑first transformations) | Version‑controlled, testable data models (`dim_`, `fct_` mart layers) |
| **Data‑quality automation** | **Great Expectations** | Guarantees SLA‑grade data fidelity before analytics |
| **Semantic search** | **Pinecone** + **RAG** | Fast vector‑based incident retrieval for LLM assistant |
| **LLM orchestration** | **MCP server** + **LLM provider** | Provides a uniform tool‑interface for AI‑assisted troubleshooting |
| **Containerisation** | **Docker** + **Docker‑Compose** | One‑command reproducible environment for dev, CI, and demos |
| **CI/CD** | **GitHub Actions** (lint, test, dbt, Docker build) | Enforces code quality and zero‑downtime releases |
| **Visualization** | **Power BI** | Enterprise‑grade dashboards for executive reporting |
| **Language** | **Python** (3.11) | Rich ecosystem for data pipelines, async I/O, and testing |
| **RAG** | Retrieval‑Augmented Generation (MCP ↔ Pinecone) | Turns raw incident logs into actionable insights via LLM |

---

## Metrics & Impact

- 1M+ synthetic infrastructure events processed
- Kafka → Snowflake streaming pipeline
- 8+ dimensional dbt models
- 5 interactive Power BI dashboards
- 3 analytical warehouse tables
- MCP‑powered RAG assistant using Pinecone and LLM provider
- Automated data quality validation using Great Expectations
- GitHub Actions CI/CD pipeline
- Dockerized multi‑service deployment

---

## Achievements

- Built an end‑to‑end streaming analytics platform processing over 1M synthetic infrastructure events using Kafka, Snowflake, dbt and Python.
- Engineered dimensional warehouse models and five enterprise Power BI dashboards for executive, infrastructure, AI incident intelligence, warehouse and data quality reporting.
- Integrated MCP, Pinecone and an LLM provider to enable Retrieval‑Augmented Generation for natural‑language incident investigation.
- Automated validation, testing and deployment using Great Expectations, Docker and GitHub Actions.

---

## 🚀 Future Improvements
- **Real‑world data ingestion** – integrate actual CloudTrail / Azure Monitor streams.
- **Serverless deployment** – move Kafka to Confluent Cloud and Snowflake to Snowpipe for zero‑ops scaling.
- **Multi‑model LLM support** – add additional providers behind a unified MCP façade.
- **Automated dashboard generation** – use Power BI REST API to publish dashboards programmatically.
- **Observability** – add OpenTelemetry tracing across Kafka → Snowflake → RAG pipeline.

---

## 🤝 Contributing
Contributions are welcome!  Please fork the repo, create a feature branch, and submit a **pull request**.  Ensure that:
1. All tests pass (`pytest`).
2. `dbt run` and `dbt test` succeed.
3. Linting (`ruff`) and type‑checking (`mypy`) succeed.
4. The CI workflow completes without errors.

---

## 📄 License
This project is licensed under the **MIT License** – see `LICENSE` for details.

---

*Prepared for public portfolio showcase.*