import os, pytest, requests

url = os.getenv("GATEWAY_URL")
pytestmark = pytest.mark.skipif(not url, reason="set GATEWAY_URL=http://localhost:8080")

def test_gateway_health():
    r = requests.get(f"{url}/healthz", timeout=5)
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_gateway_forecast_proxy():
    r = requests.get(f"{url}/api/forecast/hourly?hours=3", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 3
