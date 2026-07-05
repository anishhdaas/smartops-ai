-- Analyze Snowflake query performance for the last 24 hours
-- Exports results in JSON format for easy consumption

SET start_time = DATEADD(HOUR, -24, CURRENT_TIMESTAMP());

SELECT
    query_text,
    total_elapsed_time / 1000 AS elapsed_time_seconds,
    rows_scanned,
    rows_produced,
    queued_provisioning_time / 1000 AS queued_provisioning_time_seconds,
    warehouse_name,
    database_name,
    schema_name,
    query_id
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= $start_time
  AND query_text NOT LIKE '%QUERY_HISTORY%'  -- Exclude monitoring queries
  AND query_text NOT LIKE '%ACCOUNT_USAGE%'  -- Exclude metadata queries
ORDER BY total_elapsed_time DESC
LIMIT 100;
