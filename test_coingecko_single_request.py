import requests
import pandas as pd
from datetime import date

url = "https://api.coingecko.com/api/v3/coins/bitcoin/history?date=14-12-2024&localization=false"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-NnhqcL63hQzpfhzfkriyNxRr "
}

response = requests.get(url, headers=headers)

response = response.json()
df = pd.DataFrame(columns=['Date','Price','Market Cap'])
df.loc[0] = [date.today()] + [response["market_data"]["current_price"]["usd"]] + [response["market_data"]["market_cap"]["usd"]]

print(df)