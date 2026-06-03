from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///bluestock_mf.db")

tables = [
    "fund_master",
    "nav_history",
    "transactions",
    "performance",
    "aum"
]

with engine.connect() as conn:
    for table in tables:
        count = conn.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar()

        print(f"{table}: {count}")