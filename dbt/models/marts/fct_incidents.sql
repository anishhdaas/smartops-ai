{#
  Fact table for incidents.
  Contains one row per incident with all relevant details.
  Incremental on (incident_id, timestamp) to avoid duplicates.
#}
{{ config(
    materialized='incremental',
    unique_key=['incident_id', 'timestamp'],
    cluster_by=['event_type', 'server_id', "date_trunc('hour', timestamp)"],
    enabled=true
) }}

select
    e.incident_id,
    e.timestamp,
    e.server_id,
    r.region_id as region_key,
    cast(e.timestamp as date) as event_date,
    e.region,
    e.event_type,
    e.severity,
    e.cpu_percent,
    e.memory_percent,
    e.api_latency_ms,
    coalesce(m.cpu_spike_count, 0) as cpu_spike_count,
    coalesce(m.memory_spike_count, 0) as memory_spike_count,
    coalesce(m.api_latency_count, 0) as api_latency_count,
    coalesce(m.auth_failure_count, 0) as auth_failure_count,
    e.metadata,
    e.ingested_at
from {{ ref('stg_events') }} e
left join {{ ref('dim_regions') }} r on initcap(trim(e.region)) = r.region_name
left join {{ ref('stg_incident_metrics') }} m
  on e.server_id = m.server_id
  and extract(hour from e.timestamp) = m.incident_hour

{% if is_incremental() %}
  where (e.incident_id, e.timestamp) not in (select incident_id, timestamp from {{ this }})
{% endif %}
