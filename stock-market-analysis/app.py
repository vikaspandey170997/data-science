import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Stock Market Analysis Dashboard")

# Sidebar
stock_symbol = st.sidebar.selectbox(
    "Select Stock",
    ["TCS.NS", "INFY.NS", "RELIANCE.NS"]
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-01-01"))

# Fetch data
stock = yf.download(stock_symbol, start=start_date, end=end_date)

if stock.empty:
    st.error("No data found!")
else:
    # Fix multi-index if needed
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    # Calculations
    stock["MA50"] = stock["Close"].rolling(50).mean()
    stock["Daily Return"] = stock["Close"].pct_change()

    # Show raw data
    st.subheader("📊 Raw Data")
    st.dataframe(stock.tail())

    # Plot price + MA
    st.subheader("📉 Price & Moving Average")

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(stock["Close"], label="Close Price")
    ax.plot(stock["MA50"], label="MA50")
    ax.legend()
    ax.grid()

    st.pyplot(fig)

    # Daily return chart
    st.subheader("📈 Daily Returns")

    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(stock["Daily Return"], label="Daily Return")
    ax2.legend()
    ax2.grid()

    st.pyplot(fig2)

    # Stats
    st.subheader("📌 Key Insights")

    st.write(f"Average Daily Return: {stock['Daily Return'].mean():.5f}")
    st.write(f"Max Price: {stock['Close'].max():.2f}")
    st.write(f"Min Price: {stock['Close'].min():.2f}")