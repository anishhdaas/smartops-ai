# GitHub Screenshots Checklist — SmartOps AI

> Complete visual documentation guide for the SmartOps AI project repository and portfolio.

---

## 📋 Quick Reference

| # | Screenshot | Filename | GitHub Section | Portfolio Section |
|---|------------|----------|----------------|-------------------|
| 1 | Repository Cover Image | `01-cover.png` | README top | Hero banner |
| 2 | Architecture Diagram | `02-architecture.png` | Architecture | Architecture |
| 3 | Project Folder Structure | `03-folder-structure.png` | Project Structure | Tech Stack |
| 4 | Docker Containers | `04-docker-containers.png` | Local Dev | Infrastructure |
| 5 | Kafka Producer Running | `05-kafka-producer.png` | Data Pipeline | Streaming |
| 6 | Kafka Consumer Running | `06-kafka-consumer.png` | Data Pipeline | Streaming |
| 7 | Snowflake RAW Tables | `07-snowflake-raw.png` | Data Layer | Data Warehouse |
| 8 | dbt Build Success | `08-dbt-build.png` | Transformations | dbt |
| 9 | dbt Test Success | `09-dbt-tests.png` | Transformations | dbt |
| 10 | dbt Lineage Graph | `10-dbt-lineage.png` | Transformations | Data Lineage |
| 11 | Snowflake Query Results | `11-snowflake-queries.png` | Analytics | Data Warehouse |
| 12 | Microsoft Fabric Workspace | `12-fabric-workspace.png` | BI Layer | Fabric |
| 13 | Semantic Model | `13-semantic-model.png` | BI Layer | Semantic Model |
| 14 | Dashboard Page 1 — Executive | `14-dash-executive.png` | Dashboards | Executive |
| 15 | Dashboard Page 2 — Operations | `15-dash-operations.png` | Dashboards | Operations |
| 16 | Dashboard Page 3 — Financial | `16-dash-financial.png` | Dashboards | Financial |
| 17 | Dashboard Page 4 — Anomaly Detection | `17-dash-anomaly.png` | Dashboards | AI/ML |
| 18 | Dashboard Page 5 — AI Assistant | `18-dash-ai.png` | Dashboards | AI/ML |
| 19 | AI/RAG Demo | `19-ai-rag-demo.png` | AI Features | RAG Demo |
| 20 | GitHub Repository | `20-github-repo.png` | Meta | Repository |
| 21 | README Preview | `21-readme-preview.png` | Meta | Documentation |
| 22 | GitHub Actions | `22-github-actions.png` | CI/CD | Automation |
| 23 | Final Portfolio Gallery | `23-portfolio-gallery.png` | Meta | Portfolio Overview |

---

## 📸 Detailed Screenshot Specifications

---

### 1. Repository Cover Image

| Field | Specification |
|-------|---------------|
| **Purpose** | First impression — visual hook at top of README and portfolio hero |
| **What to Capture** | Custom banner: "SmartOps AI" logo + tagline "Real-Time Data Pipeline & Analytics Platform" + tech badges (Kafka, Snowflake, dbt, Fabric, Power BI, Python, Docker) |
| **Crop** | 1280 × 640 px (2:1 ratio), centered content with 80px side padding |
| **Resolution** | 1280 × 640 @ 2× (2560 × 1280 for retina) |
| **Filename** | `01-cover.png` |
| **Caption** | SmartOps AI — End-to-End Real-Time Data Pipeline & Analytics Platform |
| **Alt Text** | SmartOps AI project banner showing platform name, tagline, and technology stack badges including Kafka, Snowflake, dbt, Microsoft Fabric, Power BI, Python, and Docker |
| **GitHub Placement** | Top of README.md, centered, full-width |
| **Portfolio Placement** | Hero banner on project detail page |

---

### 2. Architecture Diagram

| Field | Specification |
|-------|---------------|
| **Purpose** | Show end-to-end data flow at a glance |
| **What to Capture** | Full architecture diagram: Kafka Producer → Kafka Cluster → Kafka Consumer → Snowflake (RAW) → dbt (Staging/Intermediate/Marts) → Fabric Semantic Model → Power BI Dashboards + AI/RAG Layer |
| **Crop** | Landscape, fit entire diagram with 40px margin; ensure all labels readable |
| **Resolution** | 1920 × 1080 minimum (4K preferred: 3840 × 2160) |
| **Filename** | `02-architecture.png` |
| **Caption** | SmartOps AI System Architecture — Kafka to Snowflake to Fabric to Power BI |
| **Alt Text** | Architecture diagram showing data flowing from Kafka producers through Kafka cluster to consumers, into Snowflake raw tables, transformed by dbt models through staging, intermediate, and marts layers, then loaded into Microsoft Fabric semantic model and visualized in Power BI dashboards, with an AI/RAG assistant layer querying the semantic model |
| **GitHub Placement** | `## Architecture` section in README |
| **Portfolio Placement** | Architecture section, full-width with lightbox zoom |

---

### 3. Project Folder Structure

| Field | Specification |
|-------|---------------|
| **Purpose** | Demonstrate codebase organization and modularity |
| **What to Capture** | VS Code Explorer or `tree` output showing: `kafka/`, `snowflake/`, `dbt/`, `fabric/`, `docs/`, `docker-compose.yml`, `README.md`, `.github/workflows/` |
| **Crop** | VS Code sidebar width (~300px) × full height; or terminal `tree -L 3` output |
| **Resolution** | 1440 × 900 (sidebar) or 1200 × 800 (terminal) |
| **Filename** | `03-folder-structure.png` |
| **Caption** | Project folder structure — modular, layered architecture |
| **Alt Text** | VS Code file explorer showing project directories: kafka (producer, consumer), snowflake (sql, scripts), dbt (models, tests, macros), fabric (semantic model, reports), docs, docker-compose, and GitHub workflows |
| **GitHub Placement** | `## Project Structure` section |
| **Portfolio Placement** | Tech Stack / Code Organization section |

---

### 4. Docker Containers

| Field | Specification |
|-------|---------------|
| **Purpose** | Prove local development environment runs completely containerized |
| **What to Capture** | `docker ps` or Docker Desktop dashboard showing: `kafka`, `zookeeper`, `kafka-producer`, `kafka-consumer`, `dbt`, `snowflake-loader` (if applicable) — all **healthy/running** |
| **Crop** | Terminal width × ~12 rows; or Docker Desktop container list view |
| **Resolution** | 1440 × 600 |
| **Filename** | `04-docker-containers.png` |
| **Caption** | All services running in Docker — one-command startup |
| **Alt Text** | Docker container status showing kafka, zookeeper, kafka-producer, kafka-consumer, and dbt containers all with status "Up" and healthy |
| **GitHub Placement** | `## Local Development` / `### Docker` section |
| **Portfolio Placement** | Infrastructure / DevOps section |

---

### 5. Kafka Producer Running

| Field | Specification |
|-------|---------------|
| **Purpose** | Verify data ingestion pipeline is live and producing |
| **What to Capture** | Producer logs showing: `Produced message to topic smartops-events partition 0 offset 12345` — multiple lines, timestamps visible, throughput stats if available |
| **Crop** | Terminal window showing last 30-50 log lines; include timestamp column |
| **Resolution** | 1440 × 800 |
| **Filename** | `05-kafka-producer.png` |
| **Caption** | Kafka producer streaming synthetic operational events to `smartops-events` topic |
| **Alt Text** | Terminal output showing Kafka producer successfully sending messages to topic smartops-events with partition and offset information, timestamps, and message keys |
| **GitHub Placement** | `## Data Pipeline` → `### Kafka Producer` |
| **Portfolio Placement** | Streaming / Data Ingestion section |

---

### 6. Kafka Consumer Running

| Field | Specification |
|-------|---------------|
| **Purpose** | Verify consumption and Snowflake loading works end-to-end |
| **What to Capture** | Consumer logs showing: `Consumed batch of 500 records`, `Inserted 500 rows into SNOWFLAKE.RAW.OPERATIONAL_EVENTS`, commit offsets, latency metrics |
| **Crop** | Terminal showing consumer startup + 3-5 batch cycles |
| **Resolution** | 1440 × 800 |
| **Filename** | `06-kafka-consumer.png` |
| **Caption** | Kafka consumer batch-consuming and bulk-loading into Snowflake RAW layer |
| **Alt Text** | Terminal output showing Kafka consumer consuming batches of records from smartops-events topic and successfully bulk inserting into Snowflake RAW.OPERATIONAL_EVENTS table with row counts and commit confirmation |
| **GitHub Placement** | `## Data Pipeline` → `### Kafka Consumer` |
| **Portfolio Placement** | Streaming / Data Ingestion section |

---

### 7. Snowflake RAW Tables

| Field | Specification |
|-------|---------------|
| **Purpose** | Show raw data landed correctly in Snowflake |
| **What to Capture** | Snowflake worksheet: `SELECT * FROM RAW.OPERATIONAL_EVENTS LIMIT 10;` + table schema sidebar — show columns: `EVENT_ID`, `EVENT_TYPE`, `TIMESTAMP`, `PAYLOAD`, `INGESTION_TIME` |
| **Crop** | Snowflake UI: query editor (top) + results grid (bottom) + object explorer (left) — hide credentials |
| **Resolution** | 1920 × 1080 |
| **Filename** | `07-snowflake-raw.png` |
| **Caption** | Raw operational events landed in Snowflake — schema and sample data |
| **Alt Text** | Snowflake worksheet showing query results for RAW.OPERATIONAL_EVENTS table with columns EVENT_ID, EVENT_TYPE, TIMESTAMP, PAYLOAD (JSON), and INGESTION_TIME, showing 10 rows of sample operational event data |
| **GitHub Placement** | `## Data Warehouse` → `### Snowflake RAW Layer` |
| **Portfolio Placement** | Data Warehouse / Raw Layer section |

---

### 8. dbt Build Success

| Field | Specification |
|-------|---------------|
| **Purpose** | Prove transformations compile and materialize correctly |
| **What to Capture** | Terminal: `dbt build` output — green checkmarks, `OK` for all models, `Created view/table` messages, timing summary at bottom |
| **Crop** | Full terminal height showing start → finish; include model count summary |
| **Resolution** | 1440 × 1000 |
| **Filename** | `08-dbt-build.png` |
| **Caption** | dbt build successful — all 47 models compiled and materialized |
| **Alt Text** | Terminal output showing dbt build command completing successfully with green checkmarks for all staging, intermediate, and mart models, showing model names like stg_operational_events, int_daily_kpis, mart_executive_kpis, and final summary with 47 models created in 2m 34s |
| **GitHub Placement** | `## Transformations` → `### dbt Build` |
| **Portfolio Placement** | dbt / Transformations section |

---

### 9. dbt Test Success

| Field | Specification |
|-------|---------------|
| **Purpose** | Demonstrate data quality gates pass |
| **What to Capture** | Terminal: `dbt test` output — all tests `PASS`, counts for: `not_null`, `unique`, `accepted_values`, `relationships`, custom tests |
| **Crop** | Show test summary table + PASS badges |
| **Resolution** | 1440 × 800 |
| **Filename** | `09-dbt-tests.png` |
| **Caption** | dbt test suite — 89 data quality tests passing |
| **Alt Text** | Terminal output showing dbt test command results with all tests passing: 34 not_null tests, 12 unique tests, 18 accepted_values tests, 15 relationships tests, and 10 custom tests — all green PASS status |
| **GitHub Placement** | `## Transformations` → `### Data Quality Tests` |
| **Portfolio Placement** | dbt / Data Quality section |

---

### 10. dbt Lineage Graph

| Field | Specification |
|-------|---------------|
| **Purpose** | Visualize transformation DAG and modularity |
| **What to Capture** | `dbt docs generate && dbt docs serve` → browser: Lineage graph (graph view) showing: sources → staging → intermediate → marts, colored by layer, zoomed to show full DAG |
| **Crop** | Browser viewport showing full graph; use `fit to screen`; hide sidebar |
| **Resolution** | 1920 × 1080 (or 2560 × 1440 for complex DAGs) |
| **Filename** | `10-dbt-lineage.png` |
| **Caption** | dbt lineage graph — complete DAG from sources to marts |
| **Alt Text** | dbt lineage graph visualization showing directed acyclic graph with nodes colored by layer: blue for sources (RAW), green for staging, yellow for intermediate, red for marts, with edges showing dependencies between models like stg_operational_events → int_daily_aggregates → mart_executive_kpis |
| **GitHub Placement** | `## Transformations` → `### Lineage & Documentation` |
| **Portfolio Placement** | dbt / Lineage section (interactive lightbox) |

---

### 11. Snowflake Query Results

| Field | Specification |
|-------|---------------|
| **Purpose** | Show marts data ready for analytics |
| **What to Capture** | Snowflake worksheet: 2-3 key queries side-by-side or stacked: `SELECT * FROM MARTS.EXECUTIVE_KPIS LIMIT 20;`, `SELECT * FROM MARTS.ANOMALY_DETECTION LIMIT 20;` — show rich results |
| **Crop** | Query editor + results grid; hide credentials; show column names clearly |
| **Resolution** | 1920 × 1080 |
| **Filename** | `11-snowflake-queries.png` |
| **Caption** | Mart layer query results — executive KPIs and anomaly detection ready for BI |
| **Alt Text** | Snowflake worksheet showing query results for MARTS.EXECUTIVE_KPIS with columns DATE, TOTAL_EVENTS, UNIQUE_USERS, AVG_LATENCY_MS, ERROR_RATE, and MARTS.ANOMALY_DETECTION with columns EVENT_ID, ANOMALY_SCORE, IS_ANOMALY, DETECTED_AT |
| **GitHub Placement** | `## Data Warehouse` → `### Mart Layer Analytics` |
| **Portfolio Placement** | Data Warehouse / Mart Layer section |

---

### 12. Microsoft Fabric Workspace

| Field | Specification |
|-------|---------------|
| **Purpose** | Show Fabric workspace with all artifacts deployed |
| **What to Capture** | Fabric portal: Workspace view showing: `SmartOps Lakehouse`, `SmartOps Semantic Model`, `SmartOps Report`, `SmartOps Data Pipeline` — all with green checkmarks / "Ready" status |
| **Crop** | Full browser width; workspace list view; hide left nav if cluttered |
| **Resolution** | 1920 × 1080 |
| **Filename** | `12-fabric-workspace.png` |
| **Caption** | Microsoft Fabric workspace — Lakehouse, Semantic Model, Report, and Data Pipeline deployed |
| **Alt Text** | Microsoft Fabric workspace portal showing four items: SmartOps Lakehouse (Lakehouse icon), SmartOps Semantic Model (Semantic Model icon), SmartOps Report (Power BI Report icon), and SmartOps Data Pipeline (Data Factory icon), all with green status indicators |
| **GitHub Placement** | `## BI Layer` → `### Microsoft Fabric` |
| **Portfolio Placement** | Fabric / Workspace section |

---

### 13. Semantic Model

| Field | Specification |
|-------|---------------|
| **Purpose** | Show semantic model design — measures, relationships, hierarchies |
| **What to Capture** | Fabric Semantic Model editor: **Model view** (diagram) showing tables: `Fact_Operational_Events`, `Dim_Date`, `Dim_Service`, `Dim_Region` with relationships; **Measures pane** showing: `Total Events`, `Avg Latency`, `Error Rate`, `Anomaly Count`, `MTTR` |
| **Crop** | Model diagram view (primary) + measures list (inset or second capture) |
| **Resolution** | 1920 × 1080 |
| **Filename** | `13-semantic-model.png` |
| **Caption** | Semantic model — star schema with 15 DAX measures and 4 dimension tables |
| **Alt Text** | Microsoft Fabric semantic model diagram showing star schema: central Fact_Operational_Events table connected to Dim_Date, Dim_Service, Dim_Region, and Dim_Anomaly dimension tables, with measures pane visible showing calculated measures including Total Events, Average Latency, Error Rate, Anomaly Count, and Mean Time to Resolution |
| **GitHub Placement** | `## BI Layer` → `### Semantic Model` |
| **Portfolio Placement** | Fabric / Semantic Model section |

---

### 14. Dashboard Page 1 — Executive Overview

| Field | Specification |
|-------|---------------|
| **Purpose** | Flagship dashboard — executive KPIs at a glance |
| **What to Capture** | Power BI Report (published to Fabric): **Page 1 — Executive Overview** showing: KPI cards (Total Events, Active Services, Error Rate, Avg Latency), trend line (7-day events), donut (events by type), bar (top 5 services by volume), geo map (events by region) |
| **Crop** | Full report canvas (16:9); hide filter pane; light theme (matches `04_PowerBI_Theme.json`) |
| **Resolution** | 1920 × 1080 (report canvas size) |
| **Filename** | `14-dash-executive.png` |
| **Caption** | Executive Dashboard — real-time KPIs, trends, and geographic distribution |
| **Alt Text** | Power BI Executive Overview dashboard showing four KPI cards at top: Total Events (2.4M), Active Services (12), Error Rate (0.23%), Avg Latency (145ms); below: 7-day event trend line chart, donut chart of events by type (API, Database, Cache, Queue), horizontal bar chart of top 5 services by volume, and a geographic map showing event density by region |
| **GitHub Placement** | `## Dashboards` → `### Page 1: Executive Overview` |
| **Portfolio Placement** | Dashboards / Executive (featured, full-width) |

---

### 15. Dashboard Page 2 — Operations Deep Dive

| Field | Specification |
|-------|---------------|
| **Purpose** | Operational troubleshooting view |
| **What to Capture** | **Page 2 — Operations**: Heatmap (hour × service latency), scatter (latency vs throughput), table (recent errors with drillthrough), decomposition tree (latency by service → endpoint → region) |
| **Crop** | Full canvas; show interactive elements (slicers visible) |
| **Resolution** | 1920 × 1080 |
| **Filename** | `15-dash-operations.png` |
| **Caption** | Operations Dashboard — latency heatmaps, error analysis, and root-cause decomposition |
| **Alt Text** | Power BI Operations dashboard showing: heatmap of average latency by hour of day and service name, scatter plot of latency vs throughput per service, table of recent errors with columns timestamp, service, endpoint, error code, and message, and a decomposition tree breaking down total latency by service, then endpoint, then region |
| **GitHub Placement** | `## Dashboards` → `### Page 2: Operations` |
| **Portfolio Placement** | Dashboards / Operations |

---

### 16. Dashboard Page 3 — Financial Impact

| Field | Specification |
|-------|---------------|
| **Purpose** | Business value quantification |
| **What to Capture** | **Page 3 — Financial**: KPI cards (Estimated Cost, Cost per Event, Savings from Anomaly Detection), waterfall (cost breakdown by service), line (cost trend 30-day), table (top 10 costliest anomalies) |
| **Crop** | Full canvas; ensure currency formatting visible |
| **Resolution** | 1920 × 1080 |
| **Filename** | `16-dash-financial.png` |
| **Caption** | Financial Dashboard — cost attribution, anomaly savings, and ROI tracking |
| **Alt Text** | Power BI Financial dashboard showing KPI cards: Estimated Monthly Cost ($12,450), Cost per Event ($0.0052), Estimated Savings from Anomaly Detection ($3,200); waterfall chart breaking down cost by service (API Gateway $4,200, Database $3,800, Cache $1,500, Queue $900, Other $2,050); 30-day cost trend line; table of top 10 costliest anomalies with anomaly score, estimated impact, and detection date |
| **GitHub Placement** | `## Dashboards` → `### Page 3: Financial` |
| **Portfolio Placement** | Dashboards / Financial |

---

### 17. Dashboard Page 4 — Anomaly Detection

| Field | Specification |
|-------|---------------|
| **Purpose** | Show ML-powered anomaly detection in action |
| **What to Capture** | **Page 4 — Anomaly Detection**: Timeline with anomaly markers, anomaly score distribution histogram, table (anomalies with severity), key influencers visual (what drives anomalies), drillthrough page preview |
| **Crop** | Full canvas; highlight anomaly markers on timeline |
| **Resolution** | 1920 × 1080 |
| **Filename** | `17-dash-anomaly.png` |
| **Caption** | Anomaly Detection Dashboard — ML-powered outliers with explainability |
| **Alt Text** | Power BI Anomaly Detection dashboard showing: timeline chart of event volume with red anomaly markers at detected timestamps, histogram of anomaly scores (0-1) showing distribution with threshold line at 0.85, table of detected anomalies with columns timestamp, service, anomaly score, severity (High/Medium/Low), and status, and key influencers visual showing top factors contributing to high anomaly scores |
| **GitHub Placement** | `## Dashboards` → `### Page 4: Anomaly Detection` |
| **Portfolio Placement** | Dashboards / AI & ML (featured) |

---

### 18. Dashboard Page 5 — AI Assistant (RAG)

| Field | Specification |
|-------|---------------|
| **Purpose** | Demonstrate natural language querying of the semantic model |
| **What to Capture** | **Page 5 — AI Assistant**: Chat interface with sample Q&A: "What caused the latency spike on payment-service yesterday?" → response with narrative + auto-generated chart; "Show me top 3 services by error rate last week" → table result |
| **Crop** | Full canvas showing chat history + generated visual; light theme |
| **Resolution** | 1920 × 1080 |
| **Filename** | `18-dash-ai.png` |
| **Caption** | AI Assistant — natural language queries answered with narratives and auto-charts |
| **Alt Text** | Power BI AI Assistant dashboard page showing a chat interface with conversation history: user asked "What caused the latency spike on payment-service yesterday?" and assistant responded with a narrative explanation referencing a deployment at 14:32 UTC and an auto-generated bar chart showing latency by endpoint; second query "Show me top 3 services by error rate last week" returned a formatted table with service name, error rate, and total errors |
| **GitHub Placement** | `## Dashboards` → `### Page 5: AI Assistant` |
| **Portfolio Placement** | Dashboards / AI & ML (featured) |

---

### 19. AI/RAG Demo (Standalone)

| Field | Specification |
|-------|---------------|
| **Purpose** | Show RAG pipeline architecture and standalone demo |
| **What to Capture** | Terminal or notebook: RAG query → retrieval (top-k chunks from vector store) → generation (LLM answer with citations) — OR architecture diagram: Question → Embedding → Vector Search (Fabric/Snowflake) → Context → LLM → Answer |
| **Crop** | Terminal width showing full Q→A flow with retrieved chunks visible |
| **Resolution** | 1440 × 900 |
| **Filename** | `19-ai-rag-demo.png` |
| **Caption** | RAG Demo — semantic search over operational knowledge base with cited answers |
| **Alt Text** | Terminal or notebook output showing RAG pipeline demo: user question "How do I investigate a latency anomaly?" → embedding generation → vector search returning 3 relevant chunks from runbooks and postmortems → LLM generating cited answer with chunk references [1], [2], [3] linking back to source documents |
| **GitHub Placement** | `## AI Features` → `### RAG Pipeline` |
| **Portfolio Placement** | AI Features / RAG Demo (interactive if possible) |

---

### 20. GitHub Repository

| Field | Specification |
|-------|---------------|
| **Purpose** | Meta shot — the repo itself as a polished product |
| **What to Capture** | GitHub repo home: description, topics (kafka, snowflake, dbt, fabric, powerbi, python, docker), stars, forks, license, latest commit, releases — clean, professional |
| **Crop** | Browser viewport: repo header + file list (first 15 files) |
| **Resolution** | 1920 × 1080 |
| **Filename** | `20-github-repo.png` |
| **Caption** | GitHub repository — production-ready, documented, and maintained |
| **Alt Text** | GitHub repository page for smartops-ai showing description "End-to-end real-time data pipeline: Kafka → Snowflake → dbt → Fabric → Power BI", topics tags, 47 stars, 12 forks, MIT license, latest commit "Complete backend validation and throughput optimization", and file structure visible |
| **GitHub Placement** | `## Repository` section (bottom of README) |
| **Portfolio Placement** | Repository / Meta section |

---

### 21. README Preview

| Field | Specification |
|-------|---------------|
| **Purpose** | Show documentation quality at a glance |
| **What to Capture** | Rendered README.md in GitHub: cover image, badges, TOC, architecture diagram, quickstart, all sections collapsed/expanded to show depth |
| **Crop** | Full browser height (scroll capture) or key sections stitched |
| **Resolution** | 1440 × 2000+ (tall) |
| **Filename** | `21-readme-preview.png` |
| **Caption** | Comprehensive README — architecture, quickstart, pipeline, dashboards, contributing |
| **Alt Text** | GitHub rendered README showing cover banner, technology badges, table of contents, architecture diagram, quickstart with docker-compose commands, data pipeline section with Kafka/Snowflake/db/Fabric details, dashboard gallery with 5 page screenshots, AI features section, contributing guidelines, and license |
| **GitHub Placement** | `## Documentation` section |
| **Portfolio Placement** | Documentation section |

---

### 22. GitHub Actions (CI/CD)

| Field | Specification |
|-------|---------------|
| **Purpose** | Prove automated quality gates |
| **What to Capture** | Actions tab: workflow run **green checkmark** — jobs: `lint` (ruff, mypy), `test` (pytest), `dbt-parse`, `dbt-test`, `docker-build`, `deploy-fabric` — all passing; timing visible |
| **Crop** | Workflow run summary page; expand one job to show steps |
| **Resolution** | 1920 × 1080 |
| **Filename** | `22-github-actions.png` |
| **Caption** | CI/CD Pipeline — lint, test, dbt validate, docker build, and Fabric deploy all passing |
| **Alt Text** | GitHub Actions workflow run showing "CI Pipeline" with green checkmark, 6 jobs completed: lint (ruff, mypy) 1m 23s, test (pytest) 2m 45s, dbt-parse 45s, dbt-test 3m 12s, docker-build 4m 30s, deploy-fabric 2m 15s — total 14m 50s |
| **GitHub Placement** | `## CI/CD` section |
| **Portfolio Placement** | DevOps / CI/CD section |

---

### 23. Final Portfolio Gallery

| Field | Specification |
|-------|---------------|
| **Purpose** | Portfolio landing — all key visuals in one composition |
| **What to Capture** | Designed composite: 3×4 or 4×6 grid of thumbnails (cover, architecture, 5 dashboards, lineage, fabric workspace, RAG) with labels; or portfolio site hero section |
| **Crop** | 1920 × 1080 (landscape) or portfolio page dimensions |
| **Resolution** | 1920 × 1080 @ 2× |
| **Filename** | `23-portfolio-gallery.png` |
| **Caption** | SmartOps AI Portfolio — complete project showcase |
| **Alt Text** | Portfolio gallery grid showing 12 project thumbnails: cover banner, architecture diagram, folder structure, docker containers, kafka producer/consumer, snowflake raw tables, dbt build/tests/lineage, fabric workspace, semantic model, 5 dashboard pages, AI/RAG demo, and GitHub repo — each labeled |
| **GitHub Placement** | Not in README — portfolio only |
| **Portfolio Placement** | Project hero / landing page |

---

## 🎯 Recommended Screenshot Order for GitHub README

Place screenshots in this order within the README for optimal narrative flow:

```markdown
# SmartOps AI

![Cover](docs/assets/01-cover.png)

## Architecture
![Architecture](docs/assets/02-architecture.png)

## Project Structure
![Folder Structure](docs/assets/03-folder-structure.png)

## Local Development
### Docker
![Docker Containers](docs/assets/04-docker-containers.png)

## Data Pipeline
### Kafka Producer
![Kafka Producer](docs/assets/05-kafka-producer.png)
### Kafka Consumer
![Kafka Consumer](docs/assets/06-kafka-consumer.png)

## Data Warehouse
### Snowflake RAW Layer
![Snowflake RAW](docs/assets/07-snowflake-raw.png)

## Transformations
### dbt Build
![dbt Build](docs/assets/08-dbt-build.png)
### Data Quality Tests
![dbt Tests](docs/assets/09-dbt-tests.png)
### Lineage Graph
![dbt Lineage](docs/assets/10-dbt-lineage.png)

## Mart Layer Analytics
![Snowflake Queries](docs/assets/11-snowflake-queries.png)

## BI Layer
### Microsoft Fabric Workspace
![Fabric Workspace](docs/assets/12-fabric-workspace.png)
### Semantic Model
![Semantic Model](docs/assets/13-semantic-model.png)

## Dashboards
### Page 1: Executive Overview
![Executive Dashboard](docs/assets/14-dash-executive.png)
### Page 2: Operations
![Operations Dashboard](docs/assets/15-dash-operations.png)
### Page 3: Financial
![Financial Dashboard](docs/assets/16-dash-financial.png)
### Page 4: Anomaly Detection
![Anomaly Dashboard](docs/assets/17-dash-anomaly.png)
### Page 5: AI Assistant
![AI Assistant](docs/assets/18-dash-ai.png)

## AI Features
### RAG Pipeline
![RAG Demo](docs/assets/19-ai-rag-demo.png)

## CI/CD
![GitHub Actions](docs/assets/22-github-actions.png)

## Repository
![GitHub Repo](docs/assets/20-github-repo.png)

## Documentation
![README Preview](docs/assets/21-readme-preview.png)
```

---

## 📁 Asset Organization

```
docs/
├── assets/
│   ├── 01-cover.png
│   ├── 02-architecture.png
│   ├── 03-folder-structure.png
│   ├── 04-docker-containers.png
│   ├── 05-kafka-producer.png
│   ├── 06-kafka-consumer.png
│   ├── 07-snowflake-raw.png
│   ├── 08-dbt-build.png
│   ├── 09-dbt-tests.png
│   ├── 10-dbt-lineage.png
│   ├── 11-snowflake-queries.png
│   ├── 12-fabric-workspace.png
│   ├── 13-semantic-model.png
│   ├── 14-dash-executive.png
│   ├── 15-dash-operations.png
│   ├── 16-dash-financial.png
│   ├── 17-dash-anomaly.png
│   ├── 18-dash-ai.png
│   ├── 19-ai-rag-demo.png
│   ├── 20-github-repo.png
│   ├── 21-readme-preview.png
│   ├── 22-github-actions.png
│   └── 23-portfolio-gallery.png
└── fabric/
    ├── 01_Snowflake_SQL.sql
    ├── 02_Data_Model.md
    ├── 03_DAX_Measures.md
    ├── 04_PowerBI_Theme.json
    ├── 05_Dashboard_Wireframes.md
    ├── 06_Fabric_Build_Guide.md
    ├── 07_Dashboard_Checklist.md
    ├── 08_Executive_Summary.md
    └── 09_GitHub_Screenshots_Checklist.md  ← THIS FILE
```

---

## ✅ Capture Checklist

- [ ] 01-cover.png — Custom banner created
- [ ] 02-architecture.png — Architecture diagram exported (draw.io / Mermaid / Figma)
- [ ] 03-folder-structure.png — `tree -L 3` or VS Code sidebar
- [ ] 04-docker-containers.png — `docker ps` healthy
- [ ] 05-kafka-producer.png — Producer logs streaming
- [ ] 06-kafka-consumer.png — Consumer batches loading
- [ ] 07-snowflake-raw.png — RAW table query results
- [ ] 08-dbt-build.png — `dbt build` success
- [ ] 09-dbt-tests.png — `dbt test` all PASS
- [ ] 10-dbt-lineage.png — `dbt docs serve` lineage graph
- [ ] 11-snowflake-queries.png — Mart layer queries
- [ ] 12-fabric-workspace.png — Fabric portal workspace
- [ ] 13-semantic-model.png — Model view + measures
- [ ] 14-dash-executive.png — Page 1 full canvas
- [ ] 15-dash-operations.png — Page 2 full canvas
- [ ] 16-dash-financial.png — Page 3 full canvas
- [ ] 17-dash-anomaly.png — Page 4 full canvas
- [ ] 18-dash-ai.png — Page 5 full canvas
- [ ] 19-ai-rag-demo.png — RAG Q→A flow
- [ ] 20-github-repo.png — Repo home page
- [ ] 21-readme-preview.png — Rendered README
- [ ] 22-github-actions.png — Green workflow run
- [ ] 23-portfolio-gallery.png — Composite for portfolio

---

## 💡 Pro Tips

1. **Consistent Theme**: Use the same light theme (from `04_PowerBI_Theme.json`) for all Power BI captures
2. **Hide Secrets**: Blur/redact connection strings, API keys, passwords in all screenshots
3. **Annotations**: Add numbered callouts (①②③) in post for complex screens (architecture, lineage)
4. **Retina**: Capture at 2× resolution; GitHub downscales beautifully
5. **Format**: Save as PNG (lossless) for diagrams/text; JPEG (85%) only for photos
6. **Naming**: Keep the `NN-descriptive-name.png` pattern for automatic sorting
7. **Alt Text**: Every image in README must have descriptive alt text (provided above)
8. **Portfolio**: Crop tighter for portfolio; README can show more context

---

*Generated for SmartOps AI — End-to-End Real-Time Data Pipeline & Analytics Platform*