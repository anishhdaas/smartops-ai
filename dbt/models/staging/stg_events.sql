{{--
  Staging model for raw events.
  Cleans and prepares the raw event data for downstream models.
  Incremental on (incident_id, timestamp) to avoid reprocessing the same event.
--}}
{{ config(
    materialized='incremental',
    unique_key=['incident_id', 'timestamp'],
    cluster_by=['event_type', 'server_id', "date_trunc('hour', timestamp)"],
    enabled=true
) }}

select
    incident_id,
    timestamp,
    server_id,
    region,
    event_type,
    severity,
    cpu_percent,
    memory_percent,
    api_latency_ms,
    metadata,
    ingested_at
from {{ source('raw', 'incidents') }}

{% if is_incremental() %}
  where (incident_id, timestamp) not in (select incident_id, timestamp from {{ this }})
{% endif %}
