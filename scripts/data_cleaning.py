import pandas as pd

nav = pd.read_csv("data/raw/02_nav_history.csv")

nav.columns = nav.columns.str.lower().str.strip()

nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(["amfi_code", "date"])

nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

nav = nav.drop_duplicates()

nav = nav[nav["nav"] > 0]

nav.to_csv("data/processed/nav_history_clean.csv", index=False)