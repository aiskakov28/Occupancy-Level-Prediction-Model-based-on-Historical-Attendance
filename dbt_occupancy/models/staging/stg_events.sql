with src as (
  select
    ("Date"::text || ' ' || "Time"::text)::timestamp as event_time,
    "People Detected"::int as people_count,
    1::int as location_id
  from {{ ref('gym_dataset') }}
)
select
  event_time,
  date_trunc('hour', event_time) as hour,
  date(event_time) as d,
  extract(hour from event_time)::int as hour_of_day,
  people_count,
  location_id
from src
order by event_time;
