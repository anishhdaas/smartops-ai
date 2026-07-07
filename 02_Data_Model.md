# SmartOps AI - Data Model Documentation

## Overview

This document describes the complete data model for the SmartOps AI infrastructure monitoring platform, designed for Microsoft Fabric semantic modeling and Power BI reporting.

## Entity Relationship Diagram

```
┌─────────────────┐       ┌──────────────────┐       ┌─────────────────────┐
│  DIM_REGIONS    │       │   DIM_SERVERS    │       │   FACT_INCIDENTS    │
├─────────────────┤       ├──────────────────┤       ├─────────────────────┤
│ PK region_id    │       │ PK server_id     │       │ PK incident_id      │
│ region_name     │       │ server_name      │       │ PK timestamp        │
│ timezone        │       │ first_seen_at    │       │ FK server_id        │
│ is_active       │       │ last_seen_at     │       │ FK region_key       │
│ dbt_valid_from  │◄──────┘                  │       │ event_date          │
│ dbt_valid_to    │                          │       │ event_type          │
└─────────────────┘                          │       │ severity            │
                                             │       │ cpu_percent         │
                                             │       │ memory_percent      │
                                             │       │ api_latency_ms      │
                                             │       │ cpu_spike_count     │
                                             │       │ memory_spike_count  │
                                             │       │ api_latency_count   │
                                             │       │ auth_failure_count  │
                                             │       │ metadata            │
                                             │       │ ingested_at         │
                                             └─────────────────────┘
                                                      │
                                                      ▼
                                             ┌─────────────────────┐
                                             │   FACT_METRICS      │
                                             ├─────────────────────┤
                                             │ PK server_id        │
                                             │ PK hour_bucket      │
                                             │ event_count         │
                                             │ avg_cpu_percent     │
                                             │ avg_memory_percent  │
                                             │ avg_api_latency_ms  │
                                             │ info_count          │
                                             │ warning_count       │
                                             │ critical_count      │
                                             └─────────────────────┘
```

## Table Definitions

### 1. Dimension Tables

#### DIM_REGIONS_V1 (Type 1 SCD - Static)
| Column | Type | Description |
|--------|------|-------------|
| region_id | NUMBER(38,0) | Surrogate key (1=Bangalore, 2=Singapore, 3=Tokyo) |
| region_name | VARCHAR | Region name (Bangalore, Singapore, Tokyo) |
| timezone | VARCHAR | IANA timezone identifier |
| is_active | BOOLEAN | Active flag (always true) |
| dbt_valid_from | TIMESTAMP_NTZ | SCD valid from |
| dbt_valid_to | TIMESTAMP_NTZ | SCD valid to (NULL = current) |

**Grain**: One row per region (3 rows)
**Source**: dbt seed data
**Refresh**: Manual / dbt run

#### DIM_SERVERS (Type 1 SCD - Incremental)
| Column | Type | Description |
|--------|------|-------------|
| server_id | VARCHAR | Natural key (e.g., 'APP-001', 'DB-002') |
| server_name | VARCHAR | Display name (same as server_id) |
| first_seen_at | TIMESTAMP_NTZ | First event timestamp |
| last_seen_at | TIMESTAMP_NTZ | Most recent event timestamp |

**Grain**: One row per server (~340 servers)
**Source**: Aggregated from `stg_events`
**Refresh**: Incremental (new servers + updated last_seen_at)

### 2. Fact Tables

#### FACT_INCIDENTS_V1 (Primary Fact - Transactional)
| Column | Type | Description |
|--------|------|-------------|
| incident_id | VARCHAR | UUID from source |
| timestamp | TIMESTAMP_NTZ | Event timestamp (PK part 1) |
| server_id | VARCHAR | FK → DIM_SERVERS |
| region_key | NUMBER | FK → DIM_REGIONS |
| event_date | DATE | Date portion of timestamp |
| event_type | VARCHAR | cpu_spike, memory_full, api_latency, auth_failure, db_error |
| severity | VARCHAR | INFO, WARNING, CRITICAL |
| cpu_percent | FLOAT | CPU utilization % (nullable) |
| memory_percent | FLOAT | Memory utilization % (nullable) |
| api_latency_ms | FLOAT | API latency in ms (nullable) |
| cpu_spike_count | NUMBER | From stg_incident_metrics |
| memory_spike_count | NUMBER | From stg_incident_metrics |
| api_latency_count | NUMBER | From stg_incident_metrics |
| auth_failure_count | NUMBER | From stg_incident_metrics |
| metadata | VARIANT | Original JSON metadata |
| ingested_at | TIMESTAMP_NTZ | Snowflake ingestion time |

**Grain**: One row per incident (2.5M+ rows)
**Source**: `stg_events` + `stg_incident_metrics` + `dim_regions`
**Refresh**: Incremental (unique_key: incident_id, timestamp)

#### FACT_METRICS (Hourly Aggregations)
| Column | Type | Description |
|--------|------|-------------|
| server_id | VARCHAR | FK → DIM_SERVERS (PK part 1) |
| hour_bucket | TIMESTAMP_NTZ | Hour truncation of timestamp (PK part 2) |
| event_count | NUMBER | Total events in hour |
| avg_cpu_percent | FLOAT | Average CPU % |
| avg_memory_percent | FLOAT | Average Memory % |
| avg_api_latency_ms | FLOAT | Average API latency |
| info_count | NUMBER | INFO severity count |
| warning_count | NUMBER | WARNING severity count |
| critical_count | NUMBER | CRITICAL severity count |

**Grain**: One row per server per hour
**Source**: Aggregated from `stg_events`
**Refresh**: Incremental (unique_key: server_id, hour_bucket)

#### MART_DASHBOARD (Dashboard Optimized)
| Column | Type | Description |
|--------|------|-------------|
| server_id | VARCHAR | FK → DIM_SERVERS (PK part 1) |
| hour_bucket | TIMESTAMP_NTZ | Hour truncation (PK part 2) |
| event_count | NUMBER | Total events in hour |
| avg_cpu_percent_cpu_percent | FLOAT | Average CPU % |
| avg_memory_percent | FLOAT | Average Memory % |
| avg_api_latency_ms | FLOAT | Average API latency |
| info_count | NUMBER | INFO count |
| warning_count | NUMBER | WARNING count |
| critical_count | NUMBER | CRITICAL count |
| server_name | VARCHAR | Display name |

**Grain**: Same as FACT_METRICS with server_name denormalized
**Source**: FACT_METRICS + DIM_SERVERS
**Refresh**: Incremental (unique_key: server_id, hour_bucket)

### 3. Staging/Views

#### STG_INCIDENTS_V1 (View - Cleaned & Deduplicated)
- Deduplicates by incident_id (keeps latest by ingested_at)
- Normalizes region to initcap
- Extracts incident_date, incident_hour

#### STG_EVENTS (Incremental)
- Raw events from source
- Incremental on (incident_id, timestamp)

#### STG_INCIDENT_METRICS_V1 (Incremental)
- Hourly aggregations per server
- Pre-computes spike counts by event_type

### 4. Reporting Views (Pre-built for Fabric)

| View | Grain | Key Metrics |
|------|-------|-------------|
| vw_incidents_full | Incident | All incident details + lookups |
| vw_hourly_metrics | Server/Hour | Aggregated metrics + lookups |
| vw_daily_incidents | Date/Region/Event/Severity | Counts, averages |
| vw_hourly_incidents | Hour/Region/Server/Event/Severity | Counts, averages |
| vw_server_health | Server | Health scorecard |
| vw_regional_summary | Region | Regional health |

## Fabric Semantic Model Mapping

### Tables to Import (Minimum Set)
1. **DimRegions** → `incident_warehouse.analytics.dim_regions_v1`
2. **DimServers** → `incident_warehouse.analytics.dim_servers`
3. **FactIncidents** → `incident_warehouse.analytics.fct_incidents_v1`
4. **FactHourlyMetrics** → `incident_warehouse.analytics.mart_dashboard`
5. **vwDailyIncidents** → `incident_warehouse.analytics.vw_daily_incidents`
6. **vwServerHealth** → `incident_warehouse.analytics.vw_server_health`
7. **vwRegionalSummary** → `incident_warehouse.analytics.vw_regional_summary`

### Relationships

| From Table | From Column | To Table | To Column | Cardinality | Cross-Filter |
|------------|-------------|----------|-----------|-------------|--------------|
| FactIncidents | region_key | DimRegions | region_id | Many-to-One | Single |
| FactIncidents | server_id | DimServers | server_id | Many-to-One | Single |
| FactHourlyMetrics | server_id | DimServers | server_id | Many-to-One | Single |
| FactHourlyMetrics | region_key | DimRegions | region_id | Many-to-One | Single |

### Hidden Columns (Not for Reporting)
- dbt_valid_from, dbt_valid_to (DimRegions)
- first_seen_at, last_seen_at (DimServers - use in Server Health only)
- incident_id (FactIncidents - use for drill-through only)
- metadata (FactIncidents - JSON, not for slicing)
- ingested_at (audit only)

### Display Folders
- **Dimensions** → Region, Server, Time, Event
- **Incident KPIs** → Incident KPIs
- **Infrastructure** → CPU, Memory, Latency
- **Availability** → Health Score, Uptime
- **AI Insights** → Root Cause, Predictions

---

## Data Quality Notes

1. **STAGING.INCIDENTS_CLEANED** is an Iceberg table with no dbt model - currently empty (0 rows). All staging logic flows through ANALYTICS schema views.
2. **DIM_EVENT_TYPE** does not exist - event_type is a column in FactIncidents.
3. **Metadata** is stored as VARIANT/JSON - requires parsing for detailed analysis.
4. **Incremental refresh** works on unique keys - ensure no duplicate (incident_id, timestamp) pairs.
5. **Timezone handling** - All timestamps are UTC. Use DimRegions.timezone for local time conversion.

---

## Maintenance

- **Daily**: dbt build incremental (FactIncidents, FactMetrics, DimServers, MartDashboard)
- **Weekly**: Full dbt build (all models + tests)
- **Monitor**: Test row counts > 0 after each run
- **Alert**: If any model returns 0 rows after successful run