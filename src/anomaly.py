import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame, col: str, window: int = 7, threshold: float = 3.5):
    df = df.copy()
    df[f"{col}_median"] = df.groupby("site_id")[col].transform(lambda x: x.rolling(window).median())
    df[f"{col}_mad"] = df.groupby("site_id")[col].transform(
        lambda x: (np.abs(x - x.median())).rolling(window).median()
    )

    df["anomaly"] = np.abs(df[col] - df[f"{col}_median"]) > threshold * df[f"{col}_mad"]
    alerts = df[df["anomaly"]][["date", "site_id", col]].copy()
    alerts["metric"] = col
    return alerts
