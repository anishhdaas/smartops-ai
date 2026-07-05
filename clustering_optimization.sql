-- Clustering optimization for key tables
-- Check current clustering keys and suggest optimizations

USE DATABASE INCIDENT_WAREHOUSE;
USE SCHEMA ANALYTICS;

-- 1. Check current clustering keys for FCT_INCIDENTS_V1
SHOW TABLES LIKE 'FCT_INCIDENTS_V1';
-- Note: The SHOW TABLES output includes a "clustering_key" column.

-- 2. Check current clustering keys for FCT_METRICS_V1
SHOW TABLES LIKE 'FCT_METRICS_V1';

-- 3. Check current clustering keys for DIM_SERVERS
SHOW TABLES LIKE 'DIM_SERVERS';

-- Based on typical query patterns, we recommend the following clustering keys:

-- For FCT_INCIDENTS_V1:
--   Queries often filter by time range (last 24h, last 7d) and group by server_id, severity, event_type.
--   Recommended clustering key: (DATE_TRUNC('HOUR', TIMESTAMP), SERVER_ID, SEVERITY, EVENT_TYPE)
ALTER TABLE FCT_INCIDENTS_V1 CLUSTER BY (DATE_TRUNC('HOUR', TIMESTAMP), SERVER_ID, SEVERITY, EVENT_TYPE);

-- For FCT_METRICS_V1:
--   Assuming this table has columns: SERVER_ID, TIMESTAMP (or HOUR_BUCKET), and metrics.
--   Queries often filter by server_id and time range.
--   Recommended clustering key: (SERVER_ID, DATE_TRUNC('HOUR', TIMESTAMP))
ALTER TABLE FCT_METRICS_V1 CLUSTER BY (SERVER_ID, DATE_TRUNC('HOUR', TIMESTAMP));

-- For DIM_SERVERS:
--   This is a small dimension table (likely few rows). Clustering may not be necessary,
--   but if we must, we can cluster by SERVER_ID (the primary key).
ALTER TABLE DIM_SERVERS CLUSTER BY (SERVER_ID);

-- Note: After altering the clustering key, Snowflake will automatically recluster the data in the background.
-- To monitor the clustering process, you can use:
--   SELECT SYSTEM$CLUSTERING_INFORMATION('FCT_INCIDENTS_V1', '(DATE_TRUNC(''HOUR'', TIMESTAMP), SERVER_ID, SEVERITY, EVENT_TYPE)');
