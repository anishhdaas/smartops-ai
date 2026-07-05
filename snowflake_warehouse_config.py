#!/usr/bin/env python3
"""
Snowflake Warehouse Auto-Scaling Configuration Script
Configures a warehouse for high-throughput ingestion with cost controls.
"""

import os
import sys
import time
import snowflake.connector
from snowflake.connector.errors import ProgrammingError, OperationalError

def main():
    # Configuration from environment variables
    config = {
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
        'database': os.getenv('SNOWFLAKE_DATABASE', 'INCIDENT_WAREHOUSE'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA', 'RAW'),
        'role': os.getenv('SNOWFLAKE_ROLE'),  # Optional
    }
    
    # Validate required credentials
    required = ['user', 'password', 'account']
    for key in required:
        if not config[key]:
            print(f"Error: Missing required environment variable for SNOWFLAKE_{key.upper()}")
            sys.exit(1)
    
    # Warehouse configuration parameters
    warehouse_config = {
        'size': 'MEDIUM',          # 4 credits/hour
        'max_cluster_count': 3,    # Scale up to 3 clusters during peak
        'auto_suspend': 120,       # 2 minutes (120 seconds)
        'auto_resume': True,       # Resume automatically when queries submitted
        'min_cluster_count': 1,    # Minimum 1 cluster (always running when not suspended)
        'scaling_policy': 'STANDARD'  # Standard scaling policy
    }
    
    # Resource monitor configuration
    rm_config = {
        'name': 'DAILY_100_CREDIT_MONITOR',
        'credit_quota': 100,       # 100 credits per day
        'frequency': 'DAILY',
        'triggers': [{
            'type': 'PERCENTAGE',
            'value': 100,          # Notify at 100% of quota
            'action': 'NOTIFY'     # Soft limit: notify but don't suspend
        }]
    }
    
    # Statement timeout (900 seconds = 15 minutes)
    statement_timeout = 900
    
    try:
        # Establish connection
        ctx = snowflake.connector.connect(
            user=config['user'],
            password=config['password'],
            account=config['account'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema'],
            role=config['role'] if config['role'] else None
        )
        
        # Use a context manager for the cursor to ensure it's closed
        with ctx.cursor() as cs:
            # Use the specified database and schema
            cs.execute(f"USE DATABASE {config['database']}")
            cs.execute(f"USE SCHEMA {config['schema']}")
            
            # 1. Configure the warehouse
            print(f"Configuring warehouse: {config['warehouse']}")
            alter_wh_sql = f"""
                ALTER WAREHOUSE {config['warehouse']} SET
                    WAREHOUSE_SIZE = '{warehouse_config['size']}'
                    MAX_CLUSTER_COUNT = {warehouse_config['max_cluster_count']}
                    MIN_CLUSTER_COUNT = {warehouse_config['min_cluster_count']}
                    AUTO_SUSPEND = {warehouse_config['auto_suspend']}
                    AUTO_RESUME = {str(warehouse_config['auto_resume']).upper()}
                    SCALING_POLICY = '{warehouse_config['scaling_policy']}'
            """
            cs.execute(alter_wh_sql)
            print("Warehouse configuration applied.")
            
            # 2. Create or replace resource monitor
            print(f"Creating/updating resource monitor: {rm_config['name']}")
            # Drop if exists to recreate with new settings
            cs.execute(f"DROP RESOURCE MONITOR IF EXISTS {rm_config['name']}")
            
            # Create the resource monitor
            rm_create_sql = f"""
                CREATE RESOURCE MONITOR {rm_config['name']}
                WITH CREDIT_QUOTA = {rm_config['credit_quota']}
                FREQUENCY = '{rm_config['frequency']}'
                START_TIMESTAMP = IMMEDIATELY
                END_TIMESTAMP = NEVER
            """
            cs.execute(rm_create_sql)
            
            # Add triggers
            for trigger in rm_config['triggers']:
                if trigger['type'] == 'PERCENTAGE':
                    trigger_sql = f"""
                        ALTER RESOURCE MONITOR {rm_config['name']}
                        ADD TRIGGER AT {trigger['value']} PERCENT
                        DO {trigger['action']}
                    """
                    cs.execute(trigger_sql)
            
            # Assign resource monitor to warehouse
            print(f"Assigning resource monitor to warehouse...")
            cs.execute(f"ALTER WAREHOUSE {config['warehouse']} SET RESOURCE_MONITOR = {rm_config['name']}")
            
            # 3. Set statement timeout for the current user
            print(f"Setting statement timeout to {statement_timeout} seconds for current user...")
            cs.execute("SELECT CURRENT_USER()")
            current_user = cs.fetchone()[0]
            cs.execute(f"ALTER USER {current_user} SET STATEMENT_TIMEOUT_IN_SECONDS = {statement_timeout}")
            
            # 4. Validate configuration
            print("\n=== VALIDATION ===")
            
            # Check warehouse settings
            cs.execute(f"SHOW WAREHOUSES LIKE '{config['warehouse']}'")
            wh_result = cs.fetchone()
            if wh_result:
                # Columns: name, state, type, size, min_cluster_count, max_cluster_count, 
                #          started_clusters, running, queued, suspended, ... 
                # We'll check specific properties
                print(f"Warehouse '{config['warehouse']}' settings:")
                print(f"  Size: {wh_result[3]}")
                print(f"  Min Clusters: {wh_result[4]}")
                print(f"  Max Clusters: {wh_result[5]}")
                print(f"  Auto Suspend: {wh_result[9]} seconds")  # Approximate column index
                print(f"  Auto Resume: {wh_result[10]}")          # Approximate
            else:
                print(f"Warning: Could not retrieve warehouse {config['warehouse']} details")
            
            # Check resource monitor
            cs.execute(f"SHOW RESOURCE MONITORS LIKE '{rm_config['name']}'")
            rm_result = cs.fetchone()
            if rm_result:
                print(f"\nResource Monitor '{rm_config['name']}':")
                print(f"  Credit Quota: {rm_result[2]}")          # Credit quota
                print(f"  Frequency: {rm_result[3]}")           # Frequency
                print(f"  Start Timestamp: {rm_result[4]}")     # Start time
                print(f"  End Timestamp: {rm_result[5]}")       # End time
            else:
                print(f"Warning: Could not find resource monitor {rm_config['name']}")
            
            # Check statement timeout for current user
            cs.execute(f"SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN USER '{current_user}'")
            timeout_result = cs.fetchone()
            if timeout_result:
                print(f"\nStatement Timeout for user '{current_user}': {timeout_result[2]} seconds")
            else:
                print(f"Warning: Could not retrieve statement timeout for user {current_user}")
            
            print("\nConfiguration completed successfully.")
            
    except (ProgrammingError, OperationalError) as e:
        print(f"Snowflake error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        if 'ctx' in locals():
            ctx.close()

if __name__ == '__main__':
    main()
