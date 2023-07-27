import requests
import pandas as pd
import plotly.graph_objects as go
from webull import webull  # for paper trading, import 'paper_webull'

# Replace YOUR_API_KEY with your actual Alpha Vantage API key
api_key = 'Z0DHJZLEBFMLTH1A'

# Specify the stock symbol
symbol = 'HLBZ'

# Specify the interval (daily)
interval = 'weekly'

# Make the API request
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{interval.upper()}&symbol={symbol}&apikey={api_key}'
response = requests.get(url)
json_data = response.json()

# Convert to pandas
df = pd.DataFrame.from_dict(json_data['Weekly Time Series'])
df = df.T
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'Date'})
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns={'1. open': 'Open'})
df = df.rename(columns={'2. high': 'High'})
df = df.rename(columns={'3. low': 'Low'})
df = df.rename(columns={'4. close': 'Close'})
df = df.rename(columns={'5. volume': 'Volume'})
df = df.sort_values(by='Date')
df.reset_index(drop=True, inplace=True)

df['MA5'] = df.Close.rolling(5).mean()
df['MA20'] = df.Close.rolling(20).mean()

df.to_csv('asset_data', index=False)

yesterday = df['Open'].iloc[-2]
today = df['Open'].iloc[-1]

print(yesterday)
print(today)

email = 'rraithel@gmail.com'
password = 'GigiSofiaBeth27!@!@!'
wb = webull()

# if price goes down
if today > yesterday:
    print(wb.get_mfa(email))
    mfa_code = input("MFA code: ")
    print(wb.get_security(email))
    answer = input("Security Question Answer: ")
    question_id = input("Question: ")
    data = wb.login(email, password, 'PythonTest', mfa_code, question_id, answer)
    print(wb.get_trade_token('489132'))
    wb.place_order(stock='HLBZ', quant=1)  # price=90.0
    orders = wb.get_current_orders()
    print(orders)

# elif today < yesterday:
#     wb = webull()
#     wb.login('rraithel@gmail.com', 'GigiSofiaBeth27!@!@!')
#     wb.get_trade_token('489132')
#
#     # order stock
#     wb.place_order(stock='HLBZ', quant=1)  # price=90.0


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
#             MA5_cross_up[i] = df['Date'][i]
#
#
#         # define MA20 cross up over MA5
#         elif MA20_b < MA5_b and MA20_a > MA5_a:
#             # print('MA5 before: ', MA5_b)
#             # print('MA20 before: ', MA20_b)
#             # print('MA5 after: ', MA5_a)
#             # print('MA20 after: ', MA20_a)
#             # print('MA20 is now greater than MA5')
#             MA20_cross_up[i] = df['Date'][i]
#
#         else:
#             pass
#
# fig = go.Figure(data=[go.Candlestick(x=df['Date'],
#                                      open=df['Open'],
#                                      high=df['High'],
#                                      low=df['Low'],
#                                      close=df['Close'],
#                                      name='Daily'),
#                       go.Scatter(
#                           x=df.Date,
#                           y=df.MA5,
#                           name='Moving Average (5 day)',
#                           line=dict(color='blue', width=2)),
#                       go.Scatter(
#                           x=df.Date,
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
