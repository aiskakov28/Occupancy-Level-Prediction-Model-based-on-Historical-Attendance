from pathlib import Path
from datetime import datetime
import pandas as pd

class BaselineForecaster:
    def __init__(self, csv_path: str | None = None):
        candidates = [
            csv_path,
            Path(__file__).resolve().parents[2] / "dbt_occupancy" / "seeds" / "gym_dataset.csv",
            Path(__file__).resolve().parents[2] / "data" / "raw" / "gym_occupancy" / "gym_dataset.csv",
        ]
        self.df = None
        for p in candidates:
            if p and Path(p).exists():
                self.df = pd.read_csv(p)
                break
        if self.df is None:
            self.avg = {(w, h): 0 for w in range(7) for h in range(24)}
            self.global_mean = 0
            return
        d = self.df.copy()
        d["DateTime"] = pd.to_datetime(d["Date"] + " " + d["Time"])
        d["dow"] = d["DateTime"].dt.dayofweek
        d["hour"] = d["DateTime"].dt.hour
        grp = d.groupby(["dow", "hour"])["People Detected"].mean()
        self.avg = {(int(k[0]), int(k[1])): float(v) for k, v in grp.items()}
        self.global_mean = float(d["People Detected"].mean())

    def forecast_at(self, ts: datetime) -> float:
        dow = int(ts.weekday())
        hour = int(ts.hour)
        return self.avg.get((dow, hour), self.global_mean)

    def forecast_n(self, start: datetime, n: int):
        from .features import next_hours
        out = []
        for t in next_hours(start, n):
            out.append({"ts": t.isoformat(), "predicted": round(self.forecast_at(t))})
        return out
