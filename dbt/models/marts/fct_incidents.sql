{{
  config(
    materialized='incremental',
    unique_key='incident_id',
    cluster_by=['event_date', 'region_key', 'severity'],
    meta={
      'owner': 'smartops-data',
      'sla_minutes': 120
    }
  )
}}

{# Fact model joining cleaned incidents with hourly incident metrics and the region dimension. Powers dashboards by date, region, severity, and event type. #}

with incidents as (

    select
        incident_id,
        incident_timestamp,
        incident_date,
        incident_hour,
        server_id,
        region_clean,
        event_type,
        severity,
        cpu_percent,
        memory_percent,
        api_latency_ms,
        metadata,
        ingested_at
    from {{ ref('stg_incidents') }}

    {% if is_incremental() %}
      where ingested_at > (
        select coalesce(max(ingested_at), '1900-01-01'::timestamp_ntz)
        from {{ this }}
      )
    {% endif %}

),

metrics as (

    select
        server_id,
        incident_hour,
        cpu_spike_count,
        memory_spike_count,
        api_latency_count,
        auth_failure_count
    from {{ ref('stg_incident_metrics') }}

),

regions as (

    select
        region_id,
        region_name
    from {{ ref('dim_regions') }}
    where is_active
      and dbt_valid_to is null

),

final as (

    select
        incidents.incident_id,
        incidents.server_id,
        regions.region_id as region_key,
        incidents.incident_date as event_date,
        incidents.severity,
        incidents.event_type,
        incidents.cpu_percent,
        incidents.memory_percent,
        incidents.api_latency_ms,
        coalesce(metrics.cpu_spike_count, 0) as cpu_spike_count,
        coalesce(metrics.memory_spike_count, 0) as memory_spike_count,
        coalesce(metrics.api_latency_count, 0) as api_latency_count,
        coalesce(metrics.auth_failure_count, 0) as auth_failure_count,
        incidents.metadata,
        incidents.ingested_at
    from incidents
    left join metrics
      on incidents.server_id = metrics.server_id
     and incidents.incident_hour = metrics.incident_hour
    left join regions
      on incidents.region_clean = regions.region_name

)

select *
from final
