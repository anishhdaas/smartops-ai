{{--
  Mart table for dashboard consumption.
  Combines metrics and server information for fast querying.
  Incremental on (server_id, hour_bucket) to match the grain of fct_metrics.
--}}
{{ config(
    materialized='incremental',
    unique_key=['server_id', 'hour_bucket'],
    cluster_by=['server_id', 'hour_bucket'],
    enabled=true
) }}

select
    m.server_id,
    m.hour_bucket,
    m.event_count,
    m.avg_cpu_percent,
    m.avg_memory_percent,
    m.avg_api_latency_ms,
    m.info_count,
    m.warning_count,
    m.critical_count,
    -- We don't have more server attributes, so we just pass through the server_id as the name.
    m.server_id as server_name
from {{ ref('fct_metrics') }} m

{% if is_incremental() %}
  where (m.server_id, m.hour_bucket) not in (
    select server_id, hour_bucket from {{ this }}
  )
{% endif %}
