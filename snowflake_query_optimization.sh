#!/bin/bash
# Snowflake Query Optimization Analysis Script
# This script analyzes query history, identifies slow queries, and outputs optimization recommendations.

# Exit on any error
set -e

# Configuration
SNOWSQL_ACCOUNT="${SNOWFLAKE_ACCOUNT}"
SNOWSQL_USER="${SNOWFLAKE_USER}"
SNOWSQL_PASSWORD="${SNOWFLAKE_PASSWORD}"
SNOWSQL_ROLE="${SNOWFLAKE_ROLE}"
SNOWSQL_WAREHOUSE="${SNOWFLAKE_WAREHOUSE:-COMPUTE_WH}"
SNOWSQL_DATABASE="${SNOWFLAKE_DATABASE:-INCIDENT_WAREHOUSE}"
SNOWSQL_SCHEMA="${SNOWFLAKE_SCHEMA:-ANALYTICS}"

# Output directory
OUTPUT_DIR="./query_analysis_output"
mkdir -p "${OUTPUT_DIR}"

# Timestamp for output files
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "Starting Snowflake query optimization analysis..."
echo "Output directory: ${OUTPUT_DIR}"
echo "Timestamp: ${TIMESTAMP}"

# Check if snowsql is available
if ! command -v snowsql &> /dev/null; then
    echo "Error: snowsql not found. Please install SnowSQL and ensure it's in your PATH."
    exit 1
fi

# 1. Query history: Get top slowest queries in the last 24 hours
echo "Fetching query history from the last 24 hours..."
snowsql -a "${SNOWSQL_ACCOUNT}" -u "${SNOWSQL_USER}" -p "${SNOWSQL_PASSWORD}" \
    -r "${SNOWSQL_ROLE}" -w "${SNOWSQL_WAREHOUSE}" -d "${SNOWSQL_DATABASE}" -s "${SNOWSQL_SCHEMA}" \
    -o heading=false -o output_format=csv \
    -q "
        SELECT 
            QUERY_ID,
            QUERY_TEXT,
            USER_NAME,
            ROLE_NAME,
            WAREHOUSE_NAME,
            DATABASE_NAME,
            SCHEMA_NAME,
            QUERY_TYPE,
            EXECUTION_STATUS,
            ERROR_CODE,
            ERROR_MESSAGE,
            START_TIME,
            END_TIME,
            TOTAL_ELAPSED_TIME / 1000 AS TOTAL_ELAPSED_SECONDS,
            COMPILATION_TIME / 1000 AS COMPILATION_SECONDS,
            EXECUTION_TIME / 1000 AS EXECUTION_SECONDS,
            QUEUED_PROVISIONING_TIME / 1000 AS QUEUED_PROVISIONING_SECONDS,
            QUEUED_REPAIR_TIME / 1000 AS QUEUED_REPAIR_SECONDS,
            QUEUED_OVERLOAD_TIME / 1000 AS QUEUED_OVERLOAD_SECONDS,
            TRANSACTION_BLOCKED_TIME / 1000 AS TRANSACTION_BLOCKED_SECONDS,
            OUTBOUND_DATA_TRANSFER_BYTES,
            INBOUND_DATA_TRANSFER_BYTES,
            LISTING_DISPLAY_NAME,
            CREDITS_USED_CLOUD_SERVICES
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
        WHERE START_TIME >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP())
          AND EXECUTION_STATUS = 'SUCCESS'
        ORDER BY TOTAL_ELAPSED_TIME DESC
        LIMIT 100
    " > "${OUTPUT_DIR}/query_history_${TIMESTAMP}.csv"

# 2. Get execution plans for the top 10 slowest queries
echo "Fetching execution plans for top 10 slowest queries..."
# We'll extract the top 10 query IDs from the query history (excluding the header)
# Since we set heading=false, the first line is data.
TOP_QUERY_IDS=$(tail -n +2 "${OUTPUT_DIR}/query_history_${TIMESTAMP}.csv" | cut -d',' -f1 | head -10)

# Create a file for execution plans
> "${OUTPUT_DIR}/execution_plans_${TIMESTAMP}.csv"
echo "QUERY_ID,EXPLAIN_JSON" > "${OUTPUT_DIR}/execution_plans_${TIMESTAMP}.csv"

for qid in $TOP_QUERY_IDS; do
    # Use the QUERY_TEXT from the history to get the explain plan
    # But note: we don't have the query text in the loop. We need to get it from the history file.
    # Instead, we can query the query text by ID.
    QUERY_TEXT=$(grep "^${qid}," "${OUTPUT_DIR}/query_history_${TIMESTAMP}.csv" | cut -d',' -f2 | sed 's/,/,/g' | head -1)
    if [ -n "$QUERY_TEXT" ]; then
        # Escape single quotes in the query text for SQL
        ESCAPED_QUERY=$(echo "$QUERY_TEXT" | sed "s/'/''/g")
        PLAN=$(snowsql -a "${SNOWSQL_ACCOUNT}" -u "${SNOWSQL_USER}" -p "${SNOWSQL_PASSWORD}" \
            -r "${SNOWSQL_ROLE}" -w "${SNOWSQL_WAREHOUSE}" -d "${SNOWSQL_DATABASE}" -s "${SNOWSQL_SCHEMA}" \
            -o heading=false -o output_format=csv \
            -q "SELECT EXPLAIN_JSON($$${ESCAPED_QUERY}$$);" 2>/dev/null || echo "Error explaining query")
        echo "${qid},\"$PLAN\"" >> "${OUTPUT_DIR}/execution_plans_${TIMESTAMP}.csv"
    fi
done

# 3. Analyze for temporary table usage in UDFs (simplistic pattern check)
echo "Checking for temporary table usage in user-defined functions..."
# This is a placeholder: we would need to look at the query text for patterns like CREATE TEMPORARY TABLE
# For simplicity, we'll just note that this requires manual review.
echo "Note: Automatic detection of temporary table usage in UDFs requires parsing query text. Please review the query_history CSV for patterns like 'CREATE TEMPORARY TABLE' or 'DECLARE LOCAL TEMPORARY TABLE'." > "${OUTPUT_DIR}/temp_table_check_${TIMESTAMP}.txt"

# 4. Generate the optimized materialized views SQL (we already have the file, but we can output it here)
echo "Saving recommended materialized views SQL..."
cp /Users/ishaan/Projects/smartops-ai/optimized_materialized_views.sql "${OUTPUT_DIR}/recommended_materialized_views_${TIMESTAMP}.sql"

# 5. Generate the clustering optimization SQL
echo "Saving recommended clustering changes SQL..."
cp /Users/ishaan/Projects/smartops-ai/clustering_optimization.sql "${OUTPUT_DIR}/recommended_clustering_${TIMESTAMP}.sql"

# 6. Generate the optimization report (we already have the JSON, but we can output it here)
echo "Saving optimization report..."
cp /Users/ishaan/Projects/smartos-ai/optimization_report.json "${OUTPUT_DIR}/optimization_report_${TIMESTAMP}.json"

# 7. Create a summary file
echo "Creating analysis summary..."
echo "Analysis complete. Files generated in ${OUTPUT_DIR}:"
ls -la "${OUTPUT_DIR}"
echo ""
echo "Next steps:"
echo "1. Review the query history CSV to identify slow queries."
echo "2. Review the execution plans CSV for optimization opportunities."
echo "3. Apply the recommended materialized views and clustering changes (after testing in a dev environment)."
echo "4. Consider setting up query monitoring and alerts for long-running queries."

exit 0
