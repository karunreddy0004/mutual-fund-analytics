import requests
import pandas as pd

schemes = {
    "HDFC_Top_100":125497,
    "SBI_Bluechip":119551,
    "ICICI_Bluechip":120503,
    "Nippon_Large_Cap":118632,
    "Axis_Bluechip":119092,
    "Kotak_Bluechip":120841
}

for fund_name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    print("Fetching:", fund_name)

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        nav_df.to_csv(
            f"data/raw/{fund_name}_nav.csv",
            index=False
        )

        print("Saved")