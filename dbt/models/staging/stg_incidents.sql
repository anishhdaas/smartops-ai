{{
  config(
    materialized='view',
    meta={
      'owner': 'smartops-data',
      'sla_minutes': 60
    }
  )
}}

{{ doc('stg_incidents') }}

with source_incidents as (

    select
        incident_id,
        timestamp as incident_timestamp,
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

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by incident_id
            order by ingested_at desc
        ) as dedup_rank
    from source_incidents

),

cleaned as (

    select
        incident_id,
        incident_timestamp,
        cast(incident_timestamp as date) as incident_date,
        extract(hour from incident_timestamp) as incident_hour,
        server_id,
        region,
        initcap(trim(region)) as region_clean,
        event_type,
        severity,
        cpu_percent,
        memory_percent,
        api_latency_ms,
        metadata,
        ingested_at
    from deduplicated
    where dedup_rank = 1

)

select *
from cleaned
