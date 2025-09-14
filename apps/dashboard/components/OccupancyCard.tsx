type Props = {
  value: number | null;
  updatedAt?: string | null;
};

export default function OccupancyCard({ value, updatedAt }: Props) {
  const v = typeof value === "number" ? value : null;
  return (
    <div className="rounded-2xl bg-slate-900/60 border border-slate-800 p-5">
      <div className="text-sm text-slate-400">Current Occupancy</div>
      <div className="mt-2 text-4xl font-semibold tracking-tight">
        {v !== null ? v : "—"}
      </div>
      <div className="mt-1 text-xs text-slate-400">
        {updatedAt ? new Date(updatedAt).toLocaleString() : ""}
      </div>
    </div>
  );
}
