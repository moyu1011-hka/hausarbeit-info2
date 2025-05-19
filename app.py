from question3_functions import get_top_5_coins, get_volume_data, plot_pie_chart
import streamlit as st
import requests
import matplotlib.pyplot as plt

# Programming the Frontend

st.title("Analysis of the most popular cryptocurrencies over the past 30 days")

#show the pie chart
coins = get_top_5_coins()
labels, volumes = get_volume_data(coins)

if volumes and sum(volumes) > 0:
    fig = plot_pie_chart(labels, volumes)
    st.pyplot(fig)
else:
    st.warning("No volume data available to plot.")


coin = st.selectbox("Choose the currency", ["bitcoin", "ethereum", "solana", "ripple", "cardano"])
# get data from CoinGecko
url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params = {"vs_currency": "usd", "days": "30"}
response = requests.get(url, params=params).json()
# parse data
prices = response["prices"]
dates = [x[0] for x in prices]
values = [x[1] for x in prices]
#show the line graph
fig, ax = plt.subplots()
ax.plot(values)
ax.set_title(f"Cost of {coin} for the last 30 days")
st.pyplot(fig)