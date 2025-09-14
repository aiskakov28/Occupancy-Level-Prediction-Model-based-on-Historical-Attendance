export default function LiveIndicator({ ok = true }: { ok?: boolean }) {
  return (
    <div className="flex items-center gap-2">
      <span
        className={`relative inline-flex h-3 w-3 rounded-full ${
          ok ? "bg-emerald-400" : "bg-rose-500"
        }`}
      >
        <span
          className={`animate-ping absolute inline-flex h-full w-full rounded-full ${
            ok ? "bg-emerald-400" : "bg-rose-500"
          } opacity-60`}
        />
      </span>
      <span className="text-xs text-slate-300">{ok ? "Live" : "Offline"}</span>
    </div>
  );
}
