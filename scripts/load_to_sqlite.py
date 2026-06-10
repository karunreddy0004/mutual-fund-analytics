import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///mutual_fund.db")

base = "data/processed/"

# ONLY EXISTING FILES

transactions = pd.read_csv(base + "investor_transactions_clean.csv")
transactions.to_sql("transactions", engine, if_exists="replace", index=False)

nav = pd.read_csv(base + "nav_history_clean.csv")
nav.to_sql("nav_history", engine, if_exists="replace", index=False)

perf = pd.read_csv(base + "scheme_performance_clean.csv")
perf.to_sql("performance", engine, if_exists="replace", index=False)

print("✅ SQLite updated successfully with 3 tables")