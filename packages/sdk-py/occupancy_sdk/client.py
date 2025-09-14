import os
import requests

class Client:
    def __init__(self, base_url: str | None = None):
        self.base = base_url or os.getenv("OCCUPANCY_GATEWAY", "http://localhost:8080")

    def current(self) -> dict:
        r = requests.get(f"{self.base}/api/occupancy/current", timeout=10)
        r.raise_for_status()
        return r.json()

    def forecast(self, hours: int = 24) -> list[dict]:
        r = requests.get(f"{self.base}/api/forecast/hourly", params={"hours": hours}, timeout=10)
        r.raise_for_status()
        return r.json()
