from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from pathlib import Path

from src.loader import load_operations
from src.features import create_features
from src.models import train_and_forecast
from src.anomaly import detect_anomalies

app = FastAPI(title="Forecast & Anomaly API")

OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

class ForecastResponse(BaseModel):
    site_id: str
    date: str
    forecast_units: Optional[float] = None
    forecast_power: Optional[float] = None

class AnomalyResponse(BaseModel):
    site_id: str
    date: str
    metric: str
    value: float


@app.get("/")
def root():
    return {"message": "Welcome to Forecast & Anomaly API"}


@app.get("/forecast", response_model=List[ForecastResponse])
def get_forecast(
    site_id: str,
    horizon: int = 14,
):
    
    ops_df = load_operations("365d")
    df = create_features(ops_df)

    _, forecast_units = train_and_forecast(df, target="units_produced", horizon=horizon)
    _, forecast_power = train_and_forecast(df, target="power_kwh", horizon=horizon)

    units_site = forecast_units[forecast_units["site_id"] == site_id]
    power_site = forecast_power[forecast_power["site_id"] == site_id]

    merged = units_site[["date", "site_id", "units_produced_xgb"]].merge(
        power_site[["date", "site_id", "power_kwh_xgb"]],
        on=["date", "site_id"],
        how="inner"
    )

    OUTPUTS_DIR.mkdir(exist_ok=True)
    merged.to_csv(OUTPUTS_DIR / f"forecast_{site_id}.csv", index=False)

    return [
        ForecastResponse(
            site_id=row["site_id"],
            date=str(row["date"]),
            forecast_units=row["units_produced_xgb"],
            forecast_power=row["power_kwh_xgb"],
        )
        for _, row in merged.iterrows()
    ]


@app.get("/anomalies", response_model=List[AnomalyResponse])
def get_anomalies(
    site_id: str,
    metric: str = Query("units_produced", enum=["units_produced", "power_kwh"]),
    window: int = 7,
    threshold: float = 3.5,
):
    
    ops_df = load_operations("365d")
    alerts = detect_anomalies(ops_df, col=metric, window=window, threshold=threshold)

    alerts_site = alerts[alerts["site_id"] == site_id]


    OUTPUTS_DIR.mkdir(exist_ok=True)
    alerts_site.to_csv(OUTPUTS_DIR / f"alerts_{site_id}.csv", index=False)

    return [
        AnomalyResponse(
            site_id=row["site_id"],
            date=str(row["date"]),
            metric=row["metric"],
            value=row[metric],
        )
        for _, row in alerts_site.iterrows()
    ]
