import pandas as pd

performance = pd.read_csv("performance.csv")

print("Mutual Fund Recommender")

risk = input("Enter Risk Appetite (Low/Moderate/High): ")

if risk.lower() == "low":
    result = performance.sort_values(
        "return_1yr_pct",
        ascending=False
    ).head(3)

elif risk.lower() == "moderate":
    result = performance.sort_values(
        "return_2yr_pct",
        ascending=False
    ).head(3)

elif risk.lower() == "high":
    result = performance.sort_values(
        "return_2yr_pct",
        ascending=False
    ).head(3)

else:
    print("Invalid Risk Appetite")
    exit()

print("\nTop 3 Recommended Funds:\n")

print(
    result[
        [
            "scheme_name",
            "fund_house",
            "category",
            "return_1yr_pct",
            "return_2yr_pct"
        ]
    ]
)