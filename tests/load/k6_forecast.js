import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: __ENV.VUS ? Number(__ENV.VUS) : 10,
  duration: __ENV.DURATION || "30s",
};

const BASE = __ENV.FORECAST_URL || "http://localhost:8000";

export default function () {
  const res = http.get(`${BASE}/forecast/hourly?hours=24`, { timeout: "10s" });
  check(res, { "200": (r) => r.status === 200, "len>0": (r) => r.json().length > 0 });
  sleep(0.5);
}
