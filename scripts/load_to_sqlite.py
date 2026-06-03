import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///bluestock_mf.db")

files = {
    "fund_master": "data/raw/01_fund_master.csv",
    "nav_history": "data/processed/nav_history_clean.csv",
    "transactions": "data/processed/investor_transactions_clean.csv",
    "performance": "data/processed/scheme_performance_clean.csv",
    "aum": "data/raw/03_aum_by_fund_house.csv"
}

for table, file in files.items():
    df = pd.read_csv(file)
    df.to_sql(table, engine, if_exists="replace", index=False)
    print(f"{table}: {len(df)} rows loaded")