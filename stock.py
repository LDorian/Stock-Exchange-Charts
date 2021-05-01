from datetime import date
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import copy

# Define stock & date
stock = ['TSLA']
start_date = '2020-01-01'
end_date = '2021-01-01'

# Download .csv
for v in stock:
    data = yf.download(v, start_date, end_date)
    data.to_csv('./Stocks/'+v+'.csv')

dates = pd.date_range(start_date, end_date)
dataFrame = pd.DataFrame(index=dates)

# Put in a frame
for v in stock:
    data = pd.read_csv('./Stocks/'+v+'.csv', index_col="Date", parse_dates=True,
                       usecols=['Date', 'Close'], na_values=['nan'])
    data = data.rename(columns={'Close': v})

    dataFrame = dataFrame.join(data)
    dataFrame = dataFrame.dropna()

# Graph
mergedPlot = dataFrame.plot(title='Stock Prices')
mergedPlot.set_xlabel("Date")
mergedPlot.set_ylabel("Price")
plt.show()

normalized = dataFrame/dataFrame.iloc[0,:]

mergedPlot = normalized.plot(title='Normalized')
mergedPlot.set_xlabel("Date")
mergedPlot.set_ylabel("Price")
plt.show()

# Moving Avg Graph
for v in stock:
    ax = dataFrame[v].plot(title=v+" moving average", label=v)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    avg = dataFrame[v].rolling(20).mean()
    avg.plot(label = "Moving Avg",ax=ax)
    plt.show()

    