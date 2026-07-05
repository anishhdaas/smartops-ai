{#
  Dimension table for servers.
  Captures server metadata and tracks first/last seen times.
  Incremental on server_id to capture new servers and update last_seen.
#}
{{ config(
    materialized='incremental',
    unique_key='server_id',
    cluster_by=['server_id'],
    enabled=true
) }}

select
    server_id,
    min(timestamp) as first_seen_at,
    max(timestamp) as last_seen_at,
    -- We don't have more attributes in the source, so we just use the server_id as the name for now.
    server_id as server_name
from {{ ref('stg_events') }}

{% if is_incremental() %}
  -- For incremental runs, only process new or updated servers
  -- We need to update last_seen_at for existing servers and add new ones
  -- This is done by grouping all events and then merging
  -- Using a union approach: new servers + updated existing servers
  -- However, dbt incremental with unique_key does a merge, so we just need to return
  -- the full aggregate for all servers that have new data
  where timestamp >= (select max(last_seen_at) from {{ this }})
{% endif %}

group by server_id