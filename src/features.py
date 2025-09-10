import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    df["units_lag1"] = df.groupby("site_id")["units_produced"].shift(1)
    df["power_lag1"] = df.groupby("site_id")["power_kwh"].shift(1)

    df["units_roll7"] = df.groupby("site_id")["units_produced"].shift(1).rolling(7).mean()
    df["power_roll7"] = df.groupby("site_id")["power_kwh"].shift(1).rolling(7).mean()

    return df.dropna().reset_index(drop=True)
