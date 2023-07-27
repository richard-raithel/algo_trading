from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

# no keys required for crypto data
client = CryptoHistoricalDataClient(os.getenv("API_KEY_PAPER"), os.getenv("SECRET_KEY_PAPER"))
request_params = CryptoBarsRequest(
                            symbol_or_symbols=["DOGE/USD"],
                            timeframe=TimeFrame.Minute,
                            start="2023-01-23 00:00:00",
                            end="2023-01-28 00:00:00"
                        )

bars = client.get_crypto_bars(request_params)
bars_df = bars.df

# save to csv, remove symbol comlumn, rename timestamp column, add adj close column
bars_df.to_csv('crypto_onemin.csv')
data = pd.read_csv('crypto_onemin.csv')
data = data.drop('symbol', axis=1)
data = data.rename(columns={"timestamp": "date"})
data = data.reset_index(drop=True)
data.insert(5, 'Adj Close', data['close'])

# save to csv
data.to_csv('crypto_onemin.csv', index=False)
print(data.head())

#
# # ----------- FOR PLOTTING --------------
# MA5_cross_up = dict()
# MA20_cross_up = dict()
#
# for index, row in df.iterrows():
#     i = int(str(index))
#     if i >= 1:
#         MA5_b = df['MA5'].iloc[i-1]
#         MA5_a = df['MA5'].iloc[i]
#         MA20_b = df['MA20'].iloc[i-1]
#         MA20_a = df['MA20'].iloc[i]
#
#         # define MA5 cross up over MA20
#         if MA5_b < MA20_b and MA5_a > MA20_a:
#             # print('MA5 before: ', MA5_b)
#             # print('MA20 before: ', MA20_b)
#             # print('MA5 after: ', MA5_a)
#             # print('MA20 after: ', MA20_a)
#             # print('MA5 is now greater than MA20')
#             MA5_cross_up[i] = df['timestamp'][i]
#
#
#         # define MA20 cross up over MA5
#         elif MA20_b < MA5_b and MA20_a > MA5_a:
#             # print('MA5 before: ', MA5_b)
#             # print('MA20 before: ', MA20_b)
#             # print('MA5 after: ', MA5_a)
#             # print('MA20 after: ', MA20_a)
#             # print('MA20 is now greater than MA5')
#             MA20_cross_up[i] = df['timestamp'][i]
#
#         else:
#             pass
#
# fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
#                                      open=df['open'],
#                                      high=df['high'],
#                                      low=df['low'],
#                                      close=df['close'],
#                                      name='Daily'),
#                       go.Scatter(
#                           x=df.timestamp,
#                           y=df.MA5,
#                           name='Moving Average (5 day)',
#                           line=dict(color='blue', width=2)),
#                       go.Scatter(
#                           x=df.timestamp,
#                           y=df.MA20,
#                           name='Moving Average (20 day)',
#                           line=dict(color='purple', width=2))
#                       ])
#
# for k in MA5_cross_up.keys():
#     fig.add_shape(
#         type='line',
#         yref='paper', y0=0, y1=1,
#         xref='x', x0=MA5_cross_up[k], x1=MA5_cross_up[k],
#         line=dict(color='green', width=3)
#     )
#
# for k in MA20_cross_up.keys():
#     fig.add_shape(
#         type='line',
#         yref='paper', y0=0, y1=1,
#         xref='x', x0=MA20_cross_up[k], x1=MA20_cross_up[k],
#         line=dict(color='red', width=3)
#     )
#
# fig.show()
