import React from "react";

type Props = { children: React.ReactNode };

export default function Layout({ children }: Props) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800">
        <div className="mx-auto max-w-6xl px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl md:text-2xl font-semibold">Occupancy Dashboard</h1>
          <a href="/" className="text-sm text-slate-300 hover:text-white transition">
            Live
          </a>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6">{children}</main>
    </div>
  );
}
