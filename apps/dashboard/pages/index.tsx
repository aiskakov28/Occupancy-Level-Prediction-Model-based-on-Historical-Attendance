import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import LiveIndicator from "../components/LiveIndicator";
import OccupancyCard from "../components/OccupancyCard";
import ForecastChart from "../components/ForecastChart";
import { getCurrentOccupancy, getHourlyForecast, subscribeLive, type CurrentOccupancy, type ForecastPoint } from "../lib/api";

export default function Home() {
  const [current, setCurrent] = useState<CurrentOccupancy | null>(null);
  const [forecast, setForecast] = useState<ForecastPoint[]>([]);
  const [liveOk, setLiveOk] = useState(true);

  useEffect(() => {
    let cancel = () => {};
    (async () => {
      try {
        const [c, f] = await Promise.all([getCurrentOccupancy(), getHourlyForecast(24)]);
        setCurrent(c);
        setForecast(f);
      } catch {
        setLiveOk(false);
      }
      cancel = subscribeLive(
        (d) => {
          setCurrent(d);
          setLiveOk(true);
        },
        () => setLiveOk(false)
      );
    })();
    return () => cancel();
  }, []);

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg md:text-xl font-semibold">Live Occupancy</h2>
        <LiveIndicator ok={liveOk} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <OccupancyCard value={current?.occupancy ?? null} updatedAt={current?.updatedAt ?? null} />
        <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-5">
          <div className="text-sm text-slate-400">Location</div>
          <div className="mt-2 text-2xl font-semibold">{current?.locationId ?? "—"}</div>
        </div>
        <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-5">
          <div className="text-sm text-slate-400">Data Source</div>
          <div className="mt-2 text-2xl font-semibold">Kafka → Gateway</div>
        </div>
      </div>

      <ForecastChart data={forecast} />
    </Layout>
  );
}
