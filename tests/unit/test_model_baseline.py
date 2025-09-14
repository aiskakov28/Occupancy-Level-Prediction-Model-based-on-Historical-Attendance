from datetime import datetime, timezone
from services.forecast.app.model import BaselineForecaster

def test_forecast_nonnegative():
    m = BaselineForecaster()
    y = m.forecast_at(datetime.now(timezone.utc))
    assert y >= 0

def test_forecast_n_count():
    m = BaselineForecaster()
    res = m.forecast_n(datetime(2025,1,1,tzinfo=timezone.utc), 5)
    assert len(res) == 5
    assert {"ts","predicted"} <= set(res[0].keys())
