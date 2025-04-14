import requests
from datetime import date, timedelta
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/bitcoin/history?date="

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-XNGBRE1zynSYLPRSQhjN7n2v"
}


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

start_date = date(2025, 4, 1)
end_date = date(2025, 4, 14)
res = []
for single_date in daterange(start_date, end_date):
    response = requests.get(url + single_date.strftime("%d-%m-%Y") + "&localization=false", headers=headers)
    data = response.json()
    res.append({
        "date" : single_date, 
        "price" : data["market_data"]["current_price"]["usd"], 
        "total volume" : data["market_data"]["total_volume"]["usd"],
        "market cap" : data["market_data"]["market_cap"]["usd"]})

df = pd.DataFrame(res)

print(df)