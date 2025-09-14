with bounds as (
  select
    min(date_trunc('hour', event_time)) as min_ts,
    max(date_trunc('hour', event_time)) as max_ts
  from {{ ref('stg_events') }}
),
series as (
  select generate_series(min_ts, max_ts, interval '1 hour') as hour
  from bounds
)
select
  hour,
  date(hour) as d,
  extract(dow from hour)::int as dow,
  to_char(hour, 'Dy') as dow_short,
  extract(hour from hour)::int as hour_of_day
from series
order by hour;
