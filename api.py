import streamlit as st
import requests
import matplotlib.pyplot as plt

# UI
st.title("Анализ популярных криптовалют")
coin = st.selectbox("Выберите криптовалюту", ["bitcoin", "ethereum", "solana", "ripple", "cardano"])

# Получение данных с CoinGecko
url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params = {"vs_currency": "usd", "days": "30"}
response = requests.get(url, params=params).json()

# Парсим данные
prices = response["prices"]
dates = [x[0] for x in prices]
values = [x[1] for x in prices]

# График
fig, ax = plt.subplots()
ax.plot(values)
ax.set_title(f"Цена {coin} за 30 дней")
st.pyplot(fig)
