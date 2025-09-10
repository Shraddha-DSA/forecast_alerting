import pandas as pd
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import joblib

def train_and_forecast(df: pd.DataFrame, target: str, horizon: int = 14):
    
    features = [c for c in df.columns if c not in ["date", "site_id", "units_produced", "power_kwh"]]

    results = []
    forecasts = []

    for site in df["site_id"].unique():
        site_df = df[df["site_id"] == site].sort_values("date")
        train = site_df.iloc[:-horizon]
        test = site_df.iloc[-horizon:]

        X_train, y_train = train[features], train[target]
        X_test, y_test = test[features], test[target]

        # Baseline model
        baseline = LinearRegression()
        baseline.fit(X_train, y_train)
        y_pred_base = baseline.predict(X_test)

        # Improved model (XGBoost)
        xgb = XGBRegressor(random_state=42, n_estimators=200, learning_rate=0.1)
        xgb.fit(X_train, y_train)
        y_pred_xgb = xgb.predict(X_test)

        # Metrics
        mae_base = mean_absolute_error(y_test, y_pred_base)
        mape_base = mean_absolute_percentage_error(y_test, y_pred_base)
        mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
        mape_xgb = mean_absolute_percentage_error(y_test, y_pred_xgb)

        results.append({
            "site_id": site,
            "target": target,
            "mae_baseline": mae_base,
            "mape_baseline": mape_base,
            "mae_xgb": mae_xgb,
            "mape_xgb": mape_xgb,
        })

        forecast_df = test[["date", "site_id"]].copy()
        forecast_df[f"{target}_baseline"] = y_pred_base
        forecast_df[f"{target}_xgb"] = y_pred_xgb
        forecasts.append(forecast_df)

       
        joblib.dump(baseline, f"outputs/{site}_{target}_baseline.pkl")
        joblib.dump(xgb, f"outputs/{site}_{target}_xgb.pkl")

    return pd.DataFrame(results), pd.concat(forecasts)
