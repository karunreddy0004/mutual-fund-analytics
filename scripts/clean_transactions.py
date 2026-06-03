import pandas as pd

df = pd.read_csv("data/raw/08_investor_transactions.csv")

# Fix dates
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

# Keep positive transaction amounts
df = df[df["amount_inr"] > 0]

# Standardize transaction types
df["transaction_type"] = (
    df["transaction_type"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Validate KYC status
valid_kyc = ["Verified", "Pending", "Rejected"]
print("KYC Values:", df["kyc_status"].unique())

# Save cleaned file
df.to_csv(
    "data/processed/investor_transactions_clean.csv",
    index=False
)

print("Saved investor_transactions_clean.csv")