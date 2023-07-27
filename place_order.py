import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# load env file
load_dotenv()

trading_client = TradingClient(os.getenv('API_KEY'), os.getenv('SECRET_KEY'))

# preparing order data
market_order_data = MarketOrderRequest(
                      symbol="BTC/USD",
                      qty=0.0001,
                      side=OrderSide.BUY,
                      time_in_force=TimeInForce.DAY
                  )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
                )

