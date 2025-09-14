const BASE = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8080";

export type CurrentOccupancy = {
  locationId: string | number;
  occupancy: number;
  updatedAt: string; // ISO
};

export type ForecastPoint = {
  timestamp: string; // ISO
  occupancy: number;
};

export async function getCurrentOccupancy(): Promise<CurrentOccupancy> {
  const r = await fetch(`${BASE}/api/occupancy/current`, { cache: "no-store" });
  if (!r.ok) throw new Error("failed to fetch current occupancy");
  return r.json();
}

export async function getHourlyForecast(hours = 24): Promise<ForecastPoint[]> {
  const r = await fetch(`${BASE}/api/forecast/hourly?hours=${hours}`, { cache: "no-store" });
  if (!r.ok) throw new Error("failed to fetch forecast");
  return r.json();
}

export function subscribeLive(
  onMessage: (d: CurrentOccupancy) => void,
  onError?: (e: any) => void
): () => void {
  if (typeof window === "undefined" || !("EventSource" in window)) {
    const id = setInterval(async () => {
      try { onMessage(await getCurrentOccupancy()); } catch (e) { onError?.(e); }
    }, 5000);
    return () => clearInterval(id);
  }
  const es = new EventSource(`${BASE}/stream/occupancy`);
  es.onmessage = (ev) => {
    try { onMessage(JSON.parse(ev.data)); } catch (e) { onError?.(e); }
  };
  es.onerror = (e) => onError?.(e);
  return () => es.close();
}
