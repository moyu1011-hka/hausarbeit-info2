# 3rd question functions
import streamlit as st
import requests
import matplotlib.pyplot as plt

#function to get 5 most popular coins
def get_top_5_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # list of dicts
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return []

def get_volume_data(coins):
    labels = []
    volumes = []
    for coin in coins:
        if isinstance(coin, dict):
            name = coin.get('name', 'Unknown')
            volume = coin.get('total_volume', 0)
            labels.append(name)
            volumes.append(volume)
        else:
            st.warning(f"Unexpected data format: {coin}")
    return labels, volumes

#pie chart erstellen
def plot_pie_chart(labels, volumes):
    fig, ax = plt.subplots(figsize=(8,6))
    ax.pie(volumes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Top 5 Cryptocurrencies by 24h Trading Volume')
    ax.axis('equal')
    return fig