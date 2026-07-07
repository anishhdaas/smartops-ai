-- ============================================================================
-- SmartOps AI - Microsoft Fabric Reporting Layer SQL
-- ============================================================================
-- This file contains the exact Snowflake SQL for the Microsoft Fabric
-- semantic model reporting layer. Uses ONLY the final marts from dbt.
-- ============================================================================
-- Database: INCIDENT_WAREHOUSE
-- Schema: ANALYTICS (primary), RAW (sources)
-- ============================================================================

-- ============================================================================
-- 1. DIMENSION TABLES
-- ============================================================================

-- Dim Regions
-- Grain: One row per region
-- Source: dbt model 'dim_regions' (table materialization)
SELECT
    region_id,
    region_name,
    timezone,
    is_active,
    dbt_valid_from,
    dbt_valid_to
FROM incident_warehouse.analytics.dim_regions_v1
WHERE is_active = true;

-- Dim Servers
-- Grain: One row per server
-- Source: dbt model 'dim_servers' (incremental)
SELECT
    server_id,
    server_name,
    first_seen_at,
    last_seen_at
FROM incident_warehouse.analytics.dim_servers;

-- ============================================================================
-- 2. FACT TABLES
-- ============================================================================

-- Fact Incidents (Primary Fact Table)
-- Grain: One row per incident (server_id, timestamp)
-- Source: dbt model 'fct_incidents' (incremental)
SELECT
    fi.incident_id,
    fi.timestamp as incident_timestamp,
    fi.server_id,
    fi.region_key,
    fi.event_date,
    fi.region,
    fi.event_type,
    fi.severity,
    fi.cpu_percent,
    fi.memory_percent,
    fi.api_latency_ms,
    fi.cpu_spike_count,
    fi.memory_spike_count,
    fi.api_latency_count,
    fi.auth_failure_count,
    fi.metadata,
    fi.ingested_at
FROM incident_warehouse.analytics.fct_incidents_v1 fi;

-- Fact Metrics (Hourly Server Metrics)
-- Grain: One row per server per hour
-- Source: dbt model 'fct_metrics' (incremental)
SELECT
    fm.server_id,
    fm.hour_bucket,
    fm.event_count,
    fm.avg_cpu_percent,
    fm.avg_memory_percent,
    fm.avg_api_latency_ms,
    fm.info_count,
    fm.warning_count,
    fm.critical_count
FROM incident_warehouse.analytics.fct_metrics fm;

-- Fact Metrics Hourly (Mart Dashboard)
-- Grain: One row per server per hour (enriched with server name)
-- Source: dbt model 'mart_dashboard' (incremental)
SELECT
    md.server_id,
    md.hour_bucket,
    md.event_count,
    md.avg_cpu_percent,
    md.avg_memory_percent,
    md.avg_api_latency_ms,
    md.info_count,
    md.warning_count,
    md.critical_count,
    md.server_name
FROM incident_warehouse.analytics.mart_dashboard md;

-- ============================================================================
-- 3. STAGING VIEWS (for reference/debugging)
-- ============================================================================

-- Staged Incidents View (Cleaned & Deduplicated)
-- Source: dbt model 'stg_incidents' (view)
SELECT
    si.incident_id,
    si.incident_timestamp,
    si.incident_date,
    si.incident_hour,
    si.server_id,
    si.region,
    si.region_clean,
    si.event_type,
    si.severity,
    si.cpu_percent,
    si.memory_percent,
    si.api_latency_ms,
    si.metadata,
    si.ingested_at
FROM incident_warehouse.analytics.stg_incidents_v1 si;

-- Staged Events (Raw Events Incremental)
-- Source: dbt model 'stg_events' (incremental)
SELECT
    se.incident_id,
    se.timestamp,
    se.server_id,
    se.region,
    se.event_type,
    se.severity,
    se.cpu_percent,
    se.memory_percent,
    se.api_latency_ms,
    se.metadata,
    se.ingested_at
FROM incident_warehouse.analytics.stg_events se;

-- Staged Incident Metrics (Hourly Aggregations)
-- Source: dbt model 'stg_incident_metrics' (incremental)
SELECT
    sim.server_id,
    sim.incident_hour,
    sim.cpu_spike_count,
    sim.memory_spike_count,
    sim.api_latency_count,
    sim.auth_failure_count,
    sim.last_ingested_at
FROM incident_warehouse.analytics.stg_incident_metrics_v1 sim;

-- ============================================================================
-- 4. REPORTING VIEWS (Pre-built for Fabric)
-- ============================================================================

-- vw_incidents_full: Complete incident details with region & server lookup
CREATE OR REPLACE VIEW incident_warehouse.analytics.vw_incidents_full AS
SELECT
    fi.incident_id,
    fi.incident_timestamp,
    fi.event_date,
    EXTRACT(HOUR FROM fi.incident_timestamp) as incident_hour,
    fi.server_id,
    ds.server_name,
    fi.region_key,
    dr.region_name,
    dr.timezone,
    fi.event_type,
    fi.severity,
    fi.cpu_percent,
    fi.memory_percent,
    fi.api_latency_ms,
    fi.cpu_spike_count,
    fi.memory_spike_count,
    fi.api_latency_count,
    fi.auth_failure_count,
    fi.metadata,
    fi.ingested_at
FROM incident_warehouse.analytics.fct_incidents_v1 fi
LEFT JOIN incident_warehouse.analytics.dim_servers ds ON fi.server_id = ds.server_id
LEFT JOIN incident_warehouse.analytics.dim_regions_v1 dr ON fi.region_key = dr.region_id
WHERE dr.is_active = true;

-- vw_hourly_metrics: Hourly server metrics with region & server lookup
CREATE OR REPLACE VIEW incident_warehouse.analytics.vw_hourly_metrics AS
SELECT
    md.hour_bucket,
    md.server_id,
    ds.server_name,
    md.region_key,
    dr.region_name,
    dr.timezone,
    md.event_count,
    md.avg_cpu_percent,
    md.avg_memory_percent,
    md.avg_api_latency_ms,
    md.info_count,
    md.warning_count,
    md.critical_count,
    md.server_name
FROM incident_warehouse.analytics.mart_dashboard md
LEFT JOIN incident_warehouse.analytics.dim_servers ds ON md.server_id = ds.server_id
LEFT JOIN incident_warehouse.analytics.dim_regions_v1 dr ON md.region_key = dr.region_id
WHERE dr.is_active = true;

-- vw_daily_incidents: Daily incident counts by region, event_type, severity
CREATE OR REPLACE VIEW incident_warehouse.analytics.vw_daily_incidents AS
SELECT
    fi.event_date,
    fi.region,
    dr.region_name,
    fi.event_type,
    fi.severity,
    COUNT(*) as incident_count,
    AVG(fi.cpu_percent) as avg_cpu_percent,
    AVG(fi.memory_percent) as avg_memory_percent,
    AVG(fi.api_latency_ms) as avg_api_latency_ms,
    SUM(fi.cpu_spike_count) as total_cpu_spikes,
    SUM(fi.memory_spike_count) as total_memory_spikes,
    SUM(fi.api_latency_count) as total_api_latency_events,
    SUM(fi.auth_failure_count) as total_auth_failures
FROM incident_warehouse.analytics.fct_incidents_v1 fi
LEFT JOIN incident_warehouse.analytics.dim_regions_v1 dr ON fi.region_key = dr.region_id
WHERE dr.is_active = true
GROUP BY fi.event_date, fi.region, dr.region_name, fi.event_type, fi.severity;

-- vw_hourly_incidents: Hourly incident counts by region, server, event_type
CREATE OR REPLACE VIEW incident_warehouse.analytics.vw_hourly_incidents AS
SELECT
    DATE_TRUNC('HOUR', fi.incident_timestamp) as hour_bucket,
    fi.region,
    dr.region_name,
    fi.server_id,
    ds.server_name,
    fi.event_type,
    fi.severity,
    COUNT(*) as incident_count,
    AVG(fi.cpu_percent) as avg_cpu_percent,
    AVG(fi.memory_percent) as avg_memory_percent,
    AVG(fi.api_latency_ms) as avg_api_latency_ms
FROM incident_warehouse.analytics.fct_incidents_v1 fi
LEFT JOIN incident_warehouse.analytics.dim_regions_v1 dr ON fi.region_key = dr.region_id
LEFT JOIN incident_warehouse.analytics.dim_servers ds ON fi.server_id = ds.server_id
WHERE dr.is_active = true
GROUP BY DATE_TRUNC('HOUR', fi.incident_timestamp), fi.region, dr.region_name, fi.server_id, ds.server_name, fi.event_type, fi.severity;

-- vw_server_health: Server health scorecard
CREATE OR REPLACE VIEW incident_warehouse.analytics.vw_server_health AS
SELECT
    ds.server_id,
    ds.server_name,
    ds.first_seen_at,
    ds.last_seen_at,
    COUNT(fi.incident_id) as total_incidents,
    SUM(CASE WHEN fi.severity = 'CRITICAL' THEN 1 ELSE 0 END) as critical_incidents,
    SUM(CASE WHEN fi.severity = 'WARNING' THEN 1 ELSE 0 END) as warning_incidents,
    SUM(CASE WHEN fi.severity = 'INFO' THEN 1 ELSE 0 END) as info_incidents,
    AVG(fi.cpu_percent) as avg_cpu_percent,
    AVG(fi.memory_percent) as avg_memory_percent,
    AVG(fi.api_latency_ms) as avg_api_latency_ms,
    MAX(fi.incident_timestamp) as last_incident_at,
    DATEDIFF('HOUR', ds.last_seen_at, CURRENT_TIMESTAMP()) as hours_since_last_seen
FROM incident_warehouse.analytics.dim_servers ds
LEFT JOIN incident_warehouse.analytics.fct_incidents_v1 fi ON ds.server_id = fi.server_id
GROUP BY ds.server_id, ds.server_name, ds.first_seen_at, ds.last_seen_at;

-- vw_regional_summary: Regional health summary
CREATE OR REPLACE VIEW incident_warehouse.analytics.vw_regional_summary AS
SELECT
    dr.region_id,
    dr.region_name,
    dr.timezone,
    COUNT(DISTINCT fi.server_id) as active_servers,
    COUNT(fi.incident_id) as total_incidents,
    SUM(CASE WHEN fi.severity = 'CRITICAL' THEN 1 ELSE 0 END) as critical_incidents,
    SUM(CASE WHEN fi.severity = 'WARNING' THEN 1 ELSE 0 END) as warning_incidents,
    SUM(CASE WHEN fi.severity = 'INFO' THEN 1 ELSE 0 END) as info_incidents,
    AVG(fi.cpu_percent) as avg_cpu_percent,
    AVG(fi.memory_percent) as avg_memory_percent,
    AVG(fi.api_latency_ms) as avg_api_latency_ms,
    MAX(fi.incident_timestamp) as last_incident_at
FROM incident_warehouse.analytics.dim_regions_v1 dr
LEFT JOIN incident_warehouse.analytics.fct_incidents_v1 fi ON dr.region_id = fi.region_key
WHERE dr.is_active = true
GROUP BY dr.region_id, dr.region_name, dr.timezone;

-- ============================================================================
-- 5. SOURCE TABLES (for data lineage verification)
-- ============================================================================

-- Raw Incidents
SELECT
    incident_id,
    timestamp,
    server_id,
    region,
    event_type,
    severity,
    cpu_percent,
    memory_percent,
    api_latency_ms,
    metadata,
    ingested_at
FROM incident_warehouse.raw.incidents;

-- Raw Invalid Incidents (Dead Letter)
SELECT
    incident_id,
    timestamp,
    server_id,
    region,
    event_type,
    severity,
    cpu_percent,
    memory_percent,
    api_latency_ms,
    metadata,
    ingested_at
FROM incident_warehouse.raw.invalid_incidents;

-- ============================================================================
-- END OF FILE
-- ============================================================================