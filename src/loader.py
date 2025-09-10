from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_operations(version="365d"):
   
    file_path = DATA_DIR / f"operations_daily_{version}.csv"
    return pd.read_csv(file_path, parse_dates=["date"])

def load_site_meta():
    return pd.read_csv(DATA_DIR / "site_meta.csv")
