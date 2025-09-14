from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime, timezone
import os
from .model import BaselineForecaster

app = FastAPI(title="Occupancy Forecast")
_model = BaselineForecaster(os.getenv("DATA_CSV"))

class ForecastResponse(BaseModel):
    ts: str
    predicted: int

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/forecast/hourly", response_model=list[ForecastResponse])
def hourly(hours: int = Query(24, ge=1, le=168)):
    now = datetime.now(timezone.utc)
    return _model.forecast_n(now, hours)
