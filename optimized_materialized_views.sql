-- Materialized views for top dashboard queries
-- To be created in the ANALYTICS schema

USE DATABASE INCIDENT_WAREHOUSE;
USE SCHEMA ANALYTICS;

-- View 1: Last 24h event count by severity (refresh every 1h)
CREATE OR REPLACE MATERIALIZED VIEW MV_EVENT_COUNT_BY_SEVERITY_24H AS
SELECT
    SEVERITY,
    COUNT(*) AS EVENT_COUNT
FROM FCT_INCIDENTS_V1
WHERE TIMESTAMP >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP())
GROUP BY SEVERITY;

-- View 2: Last 7d CPU% by server (refresh every 1h)
CREATE OR REPLACE MATERIALIZED VIEW MV_AVG_CPU_BY_SERVER_7D AS
SELECT
    SERVER_ID,
    AVG(CPU_PERCENT) AS AVG_CPU_PERCENT
FROM FCT_INCIDENTS_V1
WHERE TIMESTAMP >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
GROUP BY SERVER_ID;

-- View 3: Last 24h incident summary (count, avg latency, by server)
CREATE OR REPLACE MATERIALIZED VIEW MV_INCIDENT_SUMMARY_24H AS
SELECT
    SERVER_ID,
    COUNT(*) AS INCIDENT_COUNT,
    AVG(API_LATENCY_MS) AS AVG_API_LATENCY_MS
FROM FCT_INCIDENTS_V1
WHERE TIMESTAMP >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP())
GROUP BY SERVER_ID;

-- View 4: Last 30d top 10 servers by incident count
CREATE OR REPLACE MATERIALIZED VIEW MV_TOP_10_SERVERS_30D AS
SELECT
    SERVER_ID,
    COUNT(*) AS INCIDENT_COUNT
FROM FCT_INCIDENTS_V1
WHERE TIMESTAMP >= DATEADD(DAY, -30, CURRENT_TIMESTAMP())
GROUP BY SERVER_ID
ORDER BY INCIDENT_COUNT DESC
LIMIT 10;

-- View 5: Pipeline health (consumer lag, validation status, dbt health)
-- Note: This view requires data from external sources (Kafka, validation tables, dbt run history).
-- Since we don't have those tables in the ANALYTICS schema, we will create a placeholder.
-- In a real scenario, you would join with the appropriate tables.
CREATE OR REPLACE MATERIALIZED VIEW MV_PIPELINE_HEALTH AS
SELECT
    CURRENT_TIMESTAMP() AS HEALTH_CHECK_TIME,
    'PLACEHOLDER' AS STATUS,
    'KAFKA_LAG' AS METRIC_NAME,
    0 AS METRIC_VALUE
WHERE 1=0; -- Empty view, to be replaced with actual health data
