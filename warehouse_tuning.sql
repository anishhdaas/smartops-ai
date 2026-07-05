-- Warehouse tuning for sub-second query response
-- Set warehouse size to MEDIUM, auto-scaling min/max, auto-suspend, and enable result caching

USE ROLE ACCOUNTADMIN;  -- Required to alter warehouse and set account-level parameters

-- 1. Set the warehouse size and scaling properties
ALTER WAREHOUSE COMPUTE_WH SET
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 3
    AUTO_SUSPEND = 120          -- 2 minutes in seconds
    AUTO_RESUME = TRUE;

-- 2. Enable query result caching at the warehouse level
--    Note: The parameter is set at the account level by default, but we can override at warehouse level.
ALTER WAREHOUSE COMPUTE_WH SET
    QUERY_RESULT_CACHE = TRUE
    QUERY_RESULT_CACHE_TTL = 3600;  -- 1 hour in seconds

-- 3. Set statement timeout to 300 seconds (5 minutes) at the warehouse level
ALTER WAREHOUSE COMPUTE_WH SET
    STATEMENT_TIMEOUT_IN_SECONDS = 300;

-- 4. Verify the settings
SHOW WAREHOUSES LIKE 'COMPUTE_WH';
