{#
  Fact table for server metrics aggregated by hour.
  Incremental on (server_id, hour_bucket) to avoid reprocessing.
  Clustered by server_id and hour_bucket for efficient access.
#}
{{ config(
    materialized='incremental',
    unique_key=['server_id', 'hour_bucket'],
    cluster_by=['server_id', 'hour_bucket'],
    enabled=true
) }}

select
    server_id,
    date_trunc('hour', timestamp) as hour_bucket,
    count(*) as event_count,
    avg(cpu_percent) as avg_cpu_percent,
    avg(memory_percent) as avg_memory_percent,
    avg(api_latency_ms) as avg_api_latency_ms,
    -- We can also compute percentiles if needed, but average is simpler for now.
    -- Count by severity
    sum(case when severity = 'INFO' then 1 else 0 end) as info_count,
    sum(case when severity = 'WARNING' then 1 else 0 end) as warning_count,
    sum(case when severity = 'CRITICAL' then 1 else 0 end) as critical_count
from {{ ref('stg_events') }}

{% if is_incremental() %}
  where (server_id, date_trunc('hour', timestamp)) not in (
    select server_id, hour_bucket from {{ this }}
  )
{% endif %}

group by
    server_id,
    date_trunc('hour', timestamp)
