"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import type { ForecastPoint } from "../lib/api";

export default function ForecastChart({ data }: { data: ForecastPoint[] }) {
  const rows = data.map(d => ({
    t: new Date(d.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    y: d.occupancy
  }));
  return (
    <div data-testid="forecast-chart" className="rounded-2xl bg-slate-900/60 border border-slate-800 p-5">
      <div className="text-sm text-slate-400 mb-3">Next 24h Forecast</div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={rows} margin={{ top: 10, right: 16, left: -16, bottom: 0 }}>
            <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />
            <XAxis dataKey="t" tick={{ fill: "#94a3b8", fontSize: 12 }} />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 12 }} />
            <Tooltip
              contentStyle={{ background: "#0f172a", border: "1px solid #1f2937", color: "#e2e8f0" }}
              labelStyle={{ color: "#94a3b8" }}
            />
            <Line type="monotone" dataKey="y" stroke="#60a5fa" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
