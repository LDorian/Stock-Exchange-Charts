from datetime import date
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import copy

# Moving Avg
def getMovingAvg(values, gap):
    avg = values.rolling(gap).mean()
    return avg


def rsi(i):
    up = i[i > 0].mean()
    down = -1 * i[i < 0].mean()
    return 100 * up / (up + down)


# Define stock & date
stock = ["TSLA", "MSFT"]
start_date = "2020-01-01"
end_date = "2021-01-01"

# Download .csv
for v in stock:
    data = yf.download(v, start_date, end_date)
    data.to_csv("./Stocks/" + v + ".csv")

dates = pd.date_range(start_date, end_date)
dataFrame = pd.DataFrame(index=dates)

# Put in a frame
for v in stock:
    data = pd.read_csv(
        "./Stocks/" + v + ".csv",
        index_col="Date",
        parse_dates=True,
        usecols=["Date", "Close"],
        na_values=["nan"],
    )
    data = data.rename(columns={"Close": v})

    dataFrame = dataFrame.join(data)
    dataFrame = dataFrame.dropna()

# Graph
mergedPlot = dataFrame.plot(title="Stock Prices")
mergedPlot.set_xlabel("Date")
mergedPlot.set_ylabel("Price")
plt.show()

normalized = dataFrame / dataFrame.iloc[0, :]

mergedPlot = normalized.plot(title="Normalized")
mergedPlot.set_xlabel("Date")
mergedPlot.set_ylabel("Price")
plt.show()

# Moving Avg Graph
for v in stock:
    ax = dataFrame[v].plot(title=v + " moving average", label=v)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    avg = getMovingAvg(dataFrame[v], gap=20)
    avg.plot(label="Moving Avg", ax=ax)
    plt.show()

frame = copy.deepcopy(dataFrame)

for v in stock:
    # Avg
    avg = getMovingAvg(dataFrame[v], gap=20)

    # Standard Deviation
    std = dataFrame[v].rolling(20).std()
    largeAvg = getMovingAvg(dataFrame[v], gap=50)
    dataFrame["MovingAvg_" + v] = avg
    dataFrame["Avg" + v] = largeAvg
    dataFrame["RollStd_" + v] = std

    # Bollinger Bands Limits (2*standard deviation, 20 as period)
    up = avg + std * 2
    low = avg - std * 2
    dataFrame["Up_" + v] = up
    dataFrame["Low_" + v] = low

for v in stock:
    # Retrieve the Bollinger band data calculated earlier for this stock
    up = dataFrame["Up_" + v]
    low = dataFrame["Low_" + v]
    avg = dataFrame["MovingAvg_" + v]

    # Plot only the current stock and its Bollinger bands
    ax = dataFrame[v].plot(title="Bollinger Bands", label=v)
    up.plot(label="up -", ax=ax)
    low.plot(label="low -", ax=ax)
    avg.plot(label="RollingMean", ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

for v in stock:
    daily = (dataFrame[v] / dataFrame[v].shift(1)) - 1
    dataFrame["Daily_" + v] = daily
    ax = daily.plot(title="Daily " + v, label=v)
    plt.show()

for v in stock:
    dataFrame["Flux_" + v] = (dataFrame[v] - dataFrame[v].shift(1)).fillna(0)
    dataFrame["RSI_" + v] = (
        dataFrame["Flux_" + v].rolling(center=False, window=15).apply(rsi).fillna(0)
    )

for v in stock:
    ax = dataFrame["RSI_" + v].plot(title="RSI " + v, label=v)
    ax.set_xlabel("Date")
    ax.set_ylabel("RSI value")
    plt.show()
