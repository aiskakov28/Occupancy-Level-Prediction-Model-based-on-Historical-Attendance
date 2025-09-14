from locust import HttpUser, task, between
import os

class GatewayUser(HttpUser):
    wait_time = between(0.2, 1.0)
    host = os.getenv("GATEWAY_URL", "http://localhost:8080")

    @task
    def forecast(self):
        with self.client.get("/api/forecast/hourly?hours=12", name="forecast:hourly", timeout=10, catch_response=True) as r:
            if r.status_code != 200:
                r.failure(str(r.status_code))
