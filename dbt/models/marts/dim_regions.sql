{{
  config(
    materialized='table',
    meta={
      'owner': 'smartops-data',
      'sla_minutes': 1440
    }
  )
}}

{{ doc('dim_regions') }}

with region_seed as (

    select
        1 as region_id,
        'Bangalore' as region_name,
        'Asia/Kolkata' as timezone,
        true as is_active,
        '2026-01-01'::timestamp_ntz as dbt_valid_from,
        null::timestamp_ntz as dbt_valid_to

    union all

    select
        2 as region_id,
        'Singapore' as region_name,
        'Asia/Singapore' as timezone,
        true as is_active,
        '2026-01-01'::timestamp_ntz as dbt_valid_from,
        null::timestamp_ntz as dbt_valid_to

    union all

    select
        3 as region_id,
        'Tokyo' as region_name,
        'Asia/Tokyo' as timezone,
        true as is_active,
        '2026-01-01'::timestamp_ntz as dbt_valid_from,
        null::timestamp_ntz as dbt_valid_to

)

select *
from region_seed
