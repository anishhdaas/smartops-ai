-- Query optimization patterns for Snowflake
-- Examples of how to apply best practices

-- 1. Avoid SELECT * (column pruning)
-- Instead of:
--   SELECT * FROM fact_incidents_v1 WHERE event_date >= '2026-06-01';
-- Do:
SELECT
    event_date,
    server_id,
    event_type,
    severity,
    cpu_percent,
    memory_percent,
    api_latency_ms
FROM fact_incidents_v1
WHERE event_date >= '2026-06-01';

-- 2. Use WHERE predicates before JOIN
-- Instead of:
--   SELECT *
--   FROM fact_incidents_v1 f
--   JOIN dim_servers d ON f.server_id = d.server_id
--   WHERE f.event_date >= '2026-06-01';
-- Do:
SELECT
    f.event_date,
    f.server_id,
    f.event_type,
    f.severity,
    f.cpu_percent,
    f.memory_percent,
    f.api_latency_ms,
    d.server_name
FROM fact_incidents_v1 f
JOIN dim_servers d ON f.server_id = d.server_id
WHERE f.event_date >= '2026-06-01';

-- 3. Aggregate first, join second
-- Instead of:
--   SELECT
--       d.region,
--       AVG(f.cpu_percent) AS avg_cpu
--   FROM fact_incidents_v1 f
--   JOIN dim_servers d ON f.server_id = d.server_id
--   WHERE f.event_date >= '2026-06-01'
--   GROUP BY d.region;
-- Do:
WITH agg AS (
    SELECT
        server_id,
        AVG(cpu_percent) AS avg_cpu
    FROM fact_incidents_v1
    WHERE event_date >= '2026-06-01'
    GROUP BY server_id
)
SELECT
    d.region,
    a.avg_cpu
FROM agg a
JOIN dim_servers d ON a.server_id = d.server_id
GROUP BY d.region, a.avg_cpu;

-- 4. Use APPROX_COUNT_DISTINCT for large datasets
-- Instead of:
--   SELECT COUNT(DISTINCT server_id) AS unique_servers
--   FROM fact_incidents_v1
--   WHERE event_date >= '2026-06-01';
-- Do:
SELECT
    APPROX_COUNT_DISTINCT(server_id) AS unique_servers
FROM fact_incidents_v1
WHERE event_date >= '2026-06-01';

-- 5. Use clustering keys effectively (example query that benefits from clustering on event_type, server_id, time_bucket)
-- This query will prune micro-partitions based on the WHERE clause and use clustering for efficient scanning
SELECT
    event_type,
    server_id,
    DATE_TRUNC('hour', timestamp) AS hour_bucket,
    COUNT(*) AS event_count,
    AVG(cpu_percent) AS avg_cpu
FROM fact_incidents_v1
WHERE timestamp >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP())
  AND event_type IN ('cpu_spike', 'memory_full')
  AND server_id IN ('APP-001', 'APP-002')
GROUP BY event_type, server_id, hour_bucket;
