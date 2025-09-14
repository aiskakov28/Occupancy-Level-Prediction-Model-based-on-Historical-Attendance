import pytest
from fastapi.testclient import TestClient
from services.forecast.app.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True

@pytest.mark.parametrize("n", [1, 8, 24])
def test_hourly_shape(n):
    r = client.get(f"/forecast/hourly?hours={n}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == n
    assert {"ts","predicted"} <= set(data[0].keys())
