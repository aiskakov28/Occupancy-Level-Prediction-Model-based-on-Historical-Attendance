from datetime import datetime, timezone
from services.forecast.app.features import next_hours

def test_next_hours_len_and_start():
    start = datetime(2025,1,1,8,tzinfo=timezone.utc)
    out = list(next_hours(start, 3))
    assert len(out) == 3
    assert out[0] == start
    assert out[1].hour == 9
