from question3_functions import get_top_5_coins, get_volume_data
import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Function to plot pie chart
def plot_pie_chart(labels, volumes):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(volumes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Top 5 Cryptocurrencies by 24h Trading Volume')
    ax.axis('equal')
    return fig

# Streamlit UI
st.title("Analysis of the Most Popular Cryptocurrencies")

# Show pie chart for top 5 coins
coins = get_top_5_coins()
labels, volumes = get_volume_data(coins)

if volumes and sum(volumes) > 0:
    fig = plot_pie_chart(labels, volumes)
    st.pyplot(fig)
else:
    st.warning("No volume data available to plot.")

# Line chart section
coin = st.selectbox("Choose the currency", ["bitcoin", "ethereum", "solana", "ripple", "cardano"])
url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params = {"vs_currency": "usd", "days": "30"}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if "prices" in data and data["prices"]:
        prices = data["prices"]
        dates = pd.to_datetime([x[0] for x in prices], unit='ms')
        values = [x[1] for x in prices]

        fig2, ax2 = plt.subplots()
        ax2.plot(dates, values, color='blue')
        ax2.set_title(f"{coin.capitalize()} Price Over the Last 30 Days")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Price (USD)")
        ax2.grid(True)
        st.pyplot(fig2)
    else:
        st.warning(f"No price data available for {coin}.")

except requests.exceptions.RequestException as e:
    st.error(f"Request failed: {e}")
except ValueError:
    st.error("Invalid data format received.")


# from question3_functions import get_top_5_coins, get_volume_data
# import streamlit as st
# import requests
# import matplotlib.pyplot as plt


# def plot_pie_chart(labels, volumes):
#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.pie(volumes, labels=labels, autopct='%1.1f%%', startangle=140)
#     ax.set_title('Top 5 Cryptocurrencies by 24h Trading Volume')
#     ax.axis('equal')
#     return fig

# # Programming the Frontend
# st.title("Analysis of the most popular cryptocurrencies")

# #show the pie chart
# coins = get_top_5_coins()
# labels, volumes = get_volume_data(coins)

# if volumes and sum(volumes) > 0:
#     fig = plot_pie_chart(labels, volumes)
#     st.pyplot(fig)
# else:
#     st.warning("No volume data available to plot.")


# coin = st.selectbox("Choose the currency", ["bitcoin", "ethereum", "solana", "ripple", "cardano"])
# # get data from CoinGecko
# url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
# params = {"vs_currency": "usd", "days": "30"}
# response = requests.get(url, params=params).json()
# # parse data
# prices = response["prices"]
# dates = [x[0] for x in prices]
# values = [x[1] for x in prices]
# #show the line graph
# fig, ax = plt.subplots()
# ax.plot(values)
# ax.set_title(f"Cost of {coin} for the last 30 days")
# st.pyplot(fig)


# # Загрузка и фильтрация данных
# prices = load_token_prices(days=days, token=token)
# today_prices, analysis_date = filter_today_data(prices)

# # Расчёт волатильности и доходности
# prices_with_returns, volatility = calculate_hourly_volatility(today_prices)
# hours = max(prices_with_returns.index.hour)

# # Отображение волатильности
# st.subheader(f"Волатильность за {hours} часов: {volatility:.4f}")

# # График цены
# sns.set_theme(style="whitegrid", palette="muted", font_scale=1)
# fig_price, ax_price = plt.subplots(figsize=(10, 5))
# sns.lineplot(data=prices_with_returns, x=prices_with_returns.index, y='price', ax=ax_price,
#              linewidth=2.5, marker='o', markersize=7, color='darkgreen')
# ax_price.set_title(f'{token.capitalize()} — Цена по часам ({analysis_date})')
# ax_price.set_xlabel('Время')
# ax_price.set_ylabel('Цена')
# ax_price.grid(True, linestyle='--', alpha=0.5)
# st.pyplot(fig_price)

# # График доходности
# fig_return, ax_return = plt.subplots(figsize=(12, 6))
# sns.lineplot(data=prices_with_returns, x=prices_with_returns.index, y='return', ax=ax_return,
#              linewidth=2.5, marker='o', markersize=7, color='olivedrab')
# ax_return.set_title(f'{token.capitalize()} — Почасовая доходность ({analysis_date})')
# ax_return.set_xlabel('Время')
# ax_return.set_ylabel('Доходность')
# ax_return.grid(True, linestyle='--', alpha=0.5)
# st.pyplot(fig_return)