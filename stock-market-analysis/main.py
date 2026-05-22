import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download stock data
stock = yf.download("TCS.NS", start="2024-01-01", end="2025-01-01")

# Check if data is empty
if stock.empty:
    print("No data fetched. Check ticker or internet connection.")
    exit()

# Handle MultiIndex columns (if present)
if isinstance(stock.columns, pd.MultiIndex):
    stock.columns = stock.columns.get_level_values(0)

# Display first rows
print(stock.head())

# Save CSV
stock.to_csv("tcs_stock_data.csv")

# Ensure 'Close' column exists
if "Close" not in stock.columns:
    print("Close column not found in data")
    exit()

# Calculate 50-day Moving Average
stock["MA50"] = stock["Close"].rolling(window=50).mean()

# 👉 ADD THIS HERE
stock["Daily Return"] = stock["Close"].pct_change()

# Print last few rows
print(stock[["Close", "MA50", "Daily Return"]].tail())

# Plot
plt.figure(figsize=(12, 6))

plt.plot(stock.index, stock["Close"], label="Close Price")
plt.plot(stock.index, stock["MA50"], label="50-Day Moving Average")

plt.title("TCS Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()

plt.grid(True)  # Better visualization

plt.show()