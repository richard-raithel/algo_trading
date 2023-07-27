from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

client = StockHistoricalDataClient(os.getenv("API_KEY_PAPER"), os.getenv("SECRET_KEY_PAPER"))
request_params = StockBarsRequest(
                        symbol_or_symbols=["TSLA"],
                        timeframe=TimeFrame.Minute,
                        start="2023-01-30 00:00:00",
                        end="2023-02-04 00:00:00"
                 )

bars = client.get_stock_bars(request_params)
bars_df = bars.df

# save to csv, remove symbol comlumn, rename timestamp column, add adj close column
bars_df.to_csv('data/stock_onemin.csv')
data = pd.read_csv('data/stock_onemin.csv')
data = data.drop('symbol', axis=1)
data = data.rename(columns={"timestamp": "date"})
data = data.reset_index(drop=True)
data.insert(5, 'Adj Close', data['close'])

# save to csv
data.to_csv('data/stock_onemin.csv', index=False)
print(data.head())
