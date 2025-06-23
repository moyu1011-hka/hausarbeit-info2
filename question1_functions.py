import requests
from datetime import date, timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import seaborn as sns

#connecting api
from api_key_coingecko import API_KEY

url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart" #api end point 

days_to_analyse = 2
currency = 'usd'

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": API_KEY
}

params = {
    'vs_currency' : currency,
    'days' : str(days_to_analyse)
}

response = requests.get(url, params=params, headers=headers)
data = response.json()

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#extract prices
def load_token_prices(days, currency = 'usd', token = None):
    
    url = f"https://api.coingecko.com/api/v3/coins/{token}/market_chart"
    
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
    
#extract volumes
def load_token_volumes(days, currency = 'usd', token = None):
    
    url = f"https://api.coingecko.com/api/v3/coins/{token}/market_chart" 
    
    params = {
        'vs_currency': currency,
        'days': days
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'total_volume'])
    volumes['timestamp'] = pd.to_datetime(volumes['timestamp'], unit='ms')
    volumes.set_index('timestamp', inplace=True)

    return volumes


#volatility calculation
def calculate_volatility(prices, days):
    results = []
    for i in range(1, days + 1):  # loop to analyse each day hourly from selected (today-n) days until today
        day = datetime.today() - timedelta(days=i) 
        next_day = day + timedelta(days=1)

        daily = prices[(prices.index >= day) & (prices.index < next_day)] #new list with prices by day
        daily= daily.copy()
        daily['return'] = daily['price'].pct_change() # calculating hourly returns for every day
        volatility = daily['return'].std() # calculating volatility for every day in week
        
        results.append({ # adding result to new the empty list
           'date': day.date(), 
         'weekday' : day.strftime('%A'),
         'volatility' : volatility
    })

    df = pd.DataFrame(results)
    df['weekday'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True)

    return df

#volume calculation
def calculate_volume(volumes, days):
    results = []
    for i in range(1,days + 1):
        day = datetime.today() - timedelta(days=i)
        next_day = day + timedelta(days=1)

        daily = volumes[(volumes.index >= day) & (volumes.index < next_day)] #new list with total_volumes by day
        daily= daily.copy()
        sum_volume = daily['total_volume'].sum() # sum hourly volumes
        results.append({ # adding result to new the empty list
         'date': day.date(),
         'weekday' : day.strftime('%A'),
         'volume' : sum_volume
    })

    df = pd.DataFrame(results) 
    df['weekday'] = pd.Categorical(df['weekday'],categories=weekday_order, ordered=True) #set right order of weekdays (default alphabetical order)

    return df

