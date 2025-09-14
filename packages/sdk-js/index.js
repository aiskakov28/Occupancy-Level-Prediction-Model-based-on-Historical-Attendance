const BASE = process.env.OCCUPANCY_GATEWAY || "http://localhost:8080";

export async function current() {
  const r = await fetch(`${BASE}/api/occupancy/current`);
  if (!r.ok) throw new Error("current failed");
  return r.json();
}

export async function forecast(hours = 24) {
  const r = await fetch(`${BASE}/api/forecast/hourly?hours=${hours}`);
  if (!r.ok) throw new Error("forecast failed");
  return r.json();
}
