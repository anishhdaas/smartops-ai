-- Snowflake DDL for the infrastructure incident data warehouse.
-- Database incident_warehouse is assumed to already exist.
-- All TIMESTAMP_NTZ columns are intended to store UTC timestamps.

USE DATABASE incident_warehouse;

CREATE SCHEMA IF NOT EXISTS raw
  COMMENT = 'Landing schema for raw incident events and dead-letter records from Kafka ingestion.';

CREATE SCHEMA IF NOT EXISTS staging
  COMMENT = 'Staging schema for validated, normalized, and deduplicated incident records.';

CREATE SCHEMA IF NOT EXISTS analytics
  COMMENT = 'Analytics schema for aggregate incident tables consumed by dashboards and reports.';

-- Raw transient landing table for valid WARNING and CRITICAL infrastructure incidents.
-- Stores original metrics, metadata JSON, and UTC ingestion timestamps from the Kafka consumer.
CREATE TRANSIENT TABLE IF NOT EXISTS incident_warehouse.raw.incidents (
  incident_id UUID PRIMARY KEY DEFAULT UUID_STRING(),
  timestamp TIMESTAMP_NTZ COMMENT 'UTC event timestamp emitted by the producer.',
  server_id VARCHAR COMMENT 'Infrastructure server identifier, for example APP-001.',
  region VARCHAR COMMENT 'Incident region: Bangalore, Singapore, or Tokyo.',
  event_type VARCHAR COMMENT 'Incident event type such as cpu_spike, memory_full, api_latency, auth_failure, or db_error.',
  severity VARCHAR COMMENT 'Incident severity: INFO, WARNING, or CRITICAL.',
  cpu_percent FLOAT COMMENT 'CPU utilization percentage when available.',
  memory_percent FLOAT COMMENT 'Memory utilization percentage when available.',
  api_latency_ms FLOAT COMMENT 'API latency in milliseconds when available.',
  metadata VARIANT COMMENT 'Additional event-specific metadata as JSON.',
  ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP COMMENT 'UTC timestamp when the record was loaded into Snowflake.'
)
COMMENT = 'Transient raw landing table for valid infrastructure incident events from Kafka.';

-- Dead-letter table for invalid incident payloads that fail validation.
-- Same analytical columns as raw incidents so malformed or partially valid records can be inspected consistently.
CREATE TRANSIENT TABLE IF NOT EXISTS incident_warehouse.raw.invalid_incidents (
  incident_id UUID PRIMARY KEY DEFAULT UUID_STRING(),
  timestamp TIMESTAMP_NTZ COMMENT 'UTC event timestamp when present and parseable.',
  server_id VARCHAR COMMENT 'Infrastructure server identifier when present.',
  region VARCHAR COMMENT 'Incident region when present.',
  event_type VARCHAR COMMENT 'Incident event type when present.',
  severity VARCHAR COMMENT 'Incident severity when present.',
  cpu_percent FLOAT COMMENT 'CPU utilization percentage when present.',
  memory_percent FLOAT COMMENT 'Memory utilization percentage when present.',
  api_latency_ms FLOAT COMMENT 'API latency in milliseconds when present.',
  metadata VARIANT COMMENT 'Original metadata or validation context as JSON.',
  ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP COMMENT 'UTC timestamp when the invalid record was loaded into Snowflake.'
)
COMMENT = 'Transient dead-letter table for invalid infrastructure incident events rejected by validation.';

-- Iceberg staging table for cleaned incidents, including a deduplication rank.
-- The table is clustered by timestamp and region for time-window and regional incident queries.
CREATE ICEBERG TABLE IF NOT EXISTS incident_warehouse.staging.incidents_cleaned (
  incident_id UUID PRIMARY KEY,
  timestamp TIMESTAMP_NTZ COMMENT 'UTC event timestamp.',
  server_id VARCHAR COMMENT 'Normalized infrastructure server identifier.',
  region VARCHAR COMMENT 'Normalized incident region.',
  event_type VARCHAR COMMENT 'Normalized incident event type.',
  severity VARCHAR COMMENT 'Normalized incident severity.',
  cpu_percent FLOAT COMMENT 'CPU utilization percentage when available.',
  memory_percent FLOAT COMMENT 'Memory utilization percentage when available.',
  api_latency_ms FLOAT COMMENT 'API latency in milliseconds when available.',
  metadata VARIANT COMMENT 'Normalized event metadata as JSON.',
  ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP COMMENT 'UTC timestamp when the record entered Snowflake.',
  dedup_rank INT COMMENT 'Deduplication rank; retain rank 1 as the canonical incident record.'
)
CLUSTER BY (timestamp, region)
COMMENT = 'Iceberg staging table for cleaned and deduplicated infrastructure incidents.';

-- Iceberg analytics aggregate table for daily incident rollups by date, region, and event type.
-- Severity score is expected to be computed upstream, for example INFO=1, WARNING=2, CRITICAL=3.
CREATE ICEBERG TABLE IF NOT EXISTS incident_warehouse.analytics.incidents_daily_agg (
  date DATE COMMENT 'UTC calendar date for the aggregate.' PRIMARY KEY,
  region VARCHAR COMMENT 'Incident region for the aggregate.' PRIMARY KEY,
  event_type VARCHAR COMMENT 'Incident event type for the aggregate.' PRIMARY KEY,
  incident_count INT COMMENT 'Total number of incidents for the date, region, and event type.',
  avg_severity_score DECIMAL(10, 2) COMMENT 'Average numeric severity score for the aggregate.',
  max_cpu_percent FLOAT COMMENT 'Maximum CPU utilization percentage for the aggregate.',
  created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP COMMENT 'UTC timestamp when the aggregate row was created.'
)
COMMENT = 'Iceberg analytics table containing daily incident aggregates by region and event type.';
