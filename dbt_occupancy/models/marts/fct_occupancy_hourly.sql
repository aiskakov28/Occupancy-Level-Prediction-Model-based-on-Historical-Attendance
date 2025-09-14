with hours as (select hour from {{ ref('dim_time') }}),
loc as (select 1 as location_id),
grid as (
  select l.location_id, h.hour
  from loc l cross join hours h
),
agg as (
  select
    location_id,
    date_trunc('hour', event_time) as hour,
    avg(people_count) as occupancy_avg,
    max(people_count) as occupancy_peak
  from {{ ref('stg_events') }}
  group by 1,2
)
select
  g.location_id,
  g.hour,
  coalesce(a.occupancy_avg, 0)::numeric(10,2) as occupancy_avg,
  coalesce(a.occupancy_peak, 0)::int as occupancy_peak
from grid g
left join agg a using (location_id, hour)
order by g.hour, g.location_id;
