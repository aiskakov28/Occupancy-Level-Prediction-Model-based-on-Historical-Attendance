from datetime import datetime, timezone, timedelta

def next_hours(start: datetime, n: int):
    cur = start.replace(minute=0, second=0, microsecond=0, tzinfo=start.tzinfo or timezone.utc)
    for i in range(n):
        yield cur + timedelta(hours=i)
