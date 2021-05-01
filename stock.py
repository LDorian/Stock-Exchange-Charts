from datetime import date
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import copy

# Define stock & date
stock = ['PG', 'UL', 'JNJ']
start_date = '2020-01-01'
end_date = '2021-01-01'

for v in stock:
    # Download .csv
    data = yf.download(v, start_date, end_date)
    data.to_csv('./Stocks/'+v+'.csv')

dates = pd.date_range(start_date, end_date)
dataFrame = pd.DataFrame(index=dates)

for v in stock:
    # Put in a frame
    data = pd.read_csv('./Stocks/'+v+'.csv', index_col="Date", parse_dates=True,
                       usecols=['Date', 'Close'], na_values=['nan'])
    data = data.rename(columns={'Close': v})

    dataFrame = dataFrame.join(data)
    dataFrame = dataFrame.dropna()

dfMerged = copy.deepcopy(dataFrame)

# Graph
mergedPlot = dataFrame.plot(title='Stock Prices')
mergedPlot.set_xlabel("Date")
mergedPlot.set_ylabel("Price")
plt.show()
