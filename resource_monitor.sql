-- Resource monitor for cost control and query governance
-- Sets up a monitor to track credit usage, enforce timeouts, and log slow queries

USE ROLE ACCOUNTADMIN;  -- Required to create resource monitors and warehouses

-- 1. Create resource monitor for credit tracking
--    Daily quota: 100 credits (so 80% alert at 80 credits)
--    Note: This monitor will track the entire account by default. To monitor a specific warehouse,
--          you would need to create a resource monitor and then associate it with the warehouse.
--          However, Snowflake resource monitors are account-level by default and can be scoped to warehouses.
--    We'll create a monitor named DAILY_CREDIT_MONITOR that monitors the warehouse COMPUTE_WH.

-- First, check if the monitor cance
-- Drop if exists to recreate
DROP RESOURCE MONITOR IF EXISTS DAILY_CREDIT_MONITOR;

-- Create the resource monitor
CREATE RESOURCE MONITOR DAILY_CREDIT_MONITOR
  WITH CREDIT_QUOTA = 100
  FREQUENCY = DAILY
  START_TIMESTAMP = IMMEDIATELY
  END_TIMESTAMP = NEVER
  TRIGGERS ON 80 PERCENT DO NOTIFY;

-- Now associate the monitor with the warehouse
ALTER WAREHOUSE COMPUTE_WH SET RESOURCE_MONITOR = DAILY_CREDIT_MONITOR;

-- 2. Statement timeout is already set in warehouse_tuning.sql (300 seconds).
--    Note: Resource monitors cannot directly kill individual queries based on execution time.
--    The statement_timeout parameter (set at warehouse, session, or account level) handles this.
--    We have set STATEMENT_TIMEOUT_IN_SECONDS = 300 in the warehouse_tuning.sql.

-- 3. Create a table to log slow queries (for manual or periodic population)
--    This table can be populated by a scheduled task that queries the QUERY_HISTORY view
--    for queries exceeding a certain threshold (e.g., > 150 seconds) and inserts them here.
--    Since resource monitors cannot log queries directly, we provide the table structure.

USE SCHEMA ANALYTICS;  -- Assuming we want to store this in the analytics schema

CREATE TABLE IF NOT EXISTS SLOW_QUERIES (
    QUERY_ID VARCHAR,
    QUERY_TEXT VARCHAR,
    USER_NAME VARCHAR,
    ROLE_NAME VARCHAR,
    WAREHOUSE_NAME VARCHAR,
    DATABASE_NAME VARCHAR,
    SCHEMA_NAME VARCHAR,
    START_TIME TIMESTAMP_TZ,
    END_TIME TIMESTAMP_TZ,
    TOTAL_ELAPSED_TIME_MS NUMBER,
    ROWS_PRODUCED NUMBER,
    ROWS_SCANNED NUMBER,
    QUEUED_PROVISIONING_TIME_MS NUMBER,
    CLIENT_GENERATED_TIMESTAMP TIMESTAMP_TZ
);

-- Comment on the table
COMMENT ON TABLE SLOW_QUERIES IS 'Table to store slow queries for analysis. Populate via scheduled task querying SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY where TOTAL_ELAPSED_TIME > 150000 (150 seconds).';

-- 4. Optional: Create a task to periodically populate the SLOW_QUERIES table
--    This is commented out because it requires a warehouse to run and may need adjustment.
--    Uncomment and adjust as needed.

/*
CREATE OR REPLACE TASK POPULATE_SLOW_QUERIES
  WAREHOUSE = COMPUTE_WH
  SCHEDULE = 'USING CRON 0 */5 * * * UTC'  -- Every 5 minutes
AS
  INSERT INTO ANALYTICS.SLOW_QUERIES
  SELECT
    QUERY_ID,
    QUERY_TEXT,
    USER_NAME,
    ROLE_NAME,
    WAREHOUSE_NAME,
    DATABASE_NAME,
    SCHEMA_NAME,
    START_TIME,
    END_TIME,
    TOTAL_ELAPSED_TIME,
    ROWS_PRODUCED,
    ROWS_SCANNED,
    QUEUED_PROVISIONING_TIME,
    CLIENT_GENERATED_TIMESTAMP
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE START_TIME >= DATEADD(MINUTE, -5, CURRENT_TIMESTAMP())
    AND TOTAL_ELAPSED_TIME > 150000  -- More than 150 seconds
    AND QUERY_TEXT NOT LIKE '%QUERY_HISTORY%'  -- Exclude monitoring queries
    AND EXECUTION_STATUS = 'SUCCESS';

-- To start the task:
ALTER TASK POPULATE_SLOW_QUERIES RESUME;
*/

-- 5. Verify the resource monitor
SHOW RESOURCE MONITORS LIKE 'DAILY_CREDIT_MONITOR';
SHOW PARAMETERS LIKE 'RESOURCE_MONITOR' IN WAREHOUSE COMPUTE_WH;
