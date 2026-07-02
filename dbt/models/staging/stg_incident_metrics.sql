{{
  config(
    materialized='incremental',
    unique_key=['server_id', 'incident_hour'],
    meta={
      'owner': 'smartops-data',
      'sla_minutes': 60
    }
  )
}}

{# Hourly incident metrics aggregated per server. Counts CPU, memory, API latency, and authentication failure events for downstream fact modeling. #}

with warning_incidents as (

    select
        server_id,
        incident_date,
        incident_hour,
        event_type,
        severity,
        ingested_at
    from {{ ref('stg_incidents') }}
    where severity in ('WARNING', 'CRITICAL')

    {% if is_incremental() %}
      and ingested_at > (
        select coalesce(max(last_ingested_at), '1900-01-01'::timestamp_ntz)
        from {{ this }}
      )
    {% endif %}

),

aggregated as (

    select
        server_id,
        incident_hour,
        count_if(event_type = 'cpu_spike') as cpu_spike_count,
        count_if(event_type = 'memory_full') as memory_spike_count,
        count_if(event_type = 'api_latency') as api_latency_count,
        count_if(event_type = 'auth_failure') as auth_failure_count,
        max(ingested_at) as last_ingested_at
    from warning_incidents
    group by
        server_id,
        incident_hour

)

select *
from aggregated
