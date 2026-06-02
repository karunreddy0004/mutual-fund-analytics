import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")

csv_files = list(RAW_PATH.glob("*.csv"))

print(f"\nFound {len(csv_files)} CSV files\n")

for file in csv_files:

    print("="*60)
    print(file.name)

    df = pd.read_csv(file)

    print("Shape:")
    print(df.shape)

    print("\nDtypes:")
    print(df.dtypes)

    print("\nHead:")
    print(df.head())