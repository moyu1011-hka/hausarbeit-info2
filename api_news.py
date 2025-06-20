#connecting api
import requests
import numpy as np
import pandas as pd
from api_key import API_KEY
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import textwrap

token = 'solana'

role = """You are a crypto-market analyst.

Respond ONLY in **German**, regardless of the input language.
For choosed token price change, return a explanation of the cause with the following fields:
- Zeitraum (start bis end)
- Preisänderung
- Ursache (in detail but in one-two sentences)
- Ereignistyp (z.B. Politisch, Markt, Regulierung, Unbekannt)
- Vertrauensniveau (Hoch, Mittel, Gering)
- Quellen (URLs)

Antworte ausschließlich mit gültigem JSON im folgenden Format:
[
  {
    "zeitraum": "...",
    "preisänderung": "...",
    "ursache": "...",
    "ereignistyp": "...",
    "vertrauen": "...",
    "quellen": ["..."]
  }
]
No extra text, no commentary, no formatting."""

def load_token_prices(days, currency = 'usd', token = None):

    url = f"https://api.coingecko.com/api/v3/coins/{token}/market_chart"

    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": API_KEY
    }
    params = {
        'vs_currency': currency,
        'days': days
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')
    prices.set_index('timestamp', inplace=True)
    return prices

def biggest_moves(prices, window=5, n_results=None, direction="both", allow_overlap=False):
    if "price" not in prices:
        raise ValueError("prices DataFrame must contain column 'price'")

    # Calculate % change
    pct_change = prices["price"].pct_change(periods=window) * 100

    # Create the DataFrame
    df = pd.DataFrame({
        "end_price": prices["price"],
        "pct_change": pct_change
    }).dropna()

    df["start_price"] = df["end_price"].shift(window)
    df["start"] = df.index - pd.Timedelta(days=window)
    df["end"] = df.index
    df["direction"] = np.where(df["pct_change"] > 0, "up", "down")
    df["abs_move"] = df["pct_change"].abs()

    # Filter by direction
    if direction in {"up", "down"}:
        df = df[df["direction"] == direction]

    # Sort by absolute move
    ranked = df.sort_values("abs_move", ascending=False)

    # Remove overlapping periods
    if not allow_overlap:
        kept_idx, spans = [], []
        for idx, row in ranked.iterrows():
            s, e = row["start"], row["end"]
            if not any((s <= ee) and (e >= ss) for ss, ee in spans):
                kept_idx.append(idx)
                spans.append((s, e))
            if n_results is not None and len(kept_idx) == n_results:
                break
        ranked = ranked.loc[kept_idx]

    # Final output
    result = (
        ranked[["start", "end", "start_price", "end_price", "pct_change", "direction"]]
        .sort_values("pct_change", ascending=(direction == "down"))
        .head(n_results)
        .reset_index(drop=True)
        .round({"start_price": 2, "end_price": 2, "pct_change": 2})
    )
     # Strip time from datetime
    result["start"] = pd.to_datetime(result["start"]).dt.date
    result["end"] = pd.to_datetime(result["end"]).dt.date
    
    return result

def load_news(token, start, end, pct_change):
  load_dotenv()

  client = OpenAI(
      api_key = os.getenv('OPENAI_API_KEY')
      )

  message = f'{token}, period: from  {start} to {end}, returns: {pct_change}'

  response = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[
      {
        "role": "system",
        "content": [
          {
            "text": role,
            "type": "text"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": message
          }
        ]
      }
    ],
    response_format={
      "type": "text"
    },
    web_search_options={
      "user_location": {
        "type": "approximate",
        "approximate": {
          "country": "DE"
        }
      }
    }
  )
  return response.choices[0].message.content

prices = load_token_prices(days=365,token=token)
result = biggest_moves(prices, window=7, n_results=3)
print(result)
json_str = load_news(token=token, start=result['start'], end= result['end'], pct_change=result['pct_change'])
events = json.loads(json_str)

for event in events:
    print(f"\nZeitraum: {event['zeitraum']}")
    print(f"Preisänderung: {event['preisänderung']}")
    print(textwrap.fill(event['ursache'], width=80))
    print(f"Ereignistyp: {event['ereignistyp']}")
    print(f"Vertrauen: {event['vertrauen']}")
    print("Quellen:")
    if event['quellen']: 
        for url in event['quellen']:
            print(f"  - {url}")
    else: print('Keine Quellen')
    print()