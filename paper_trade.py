from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import os
from dotenv import load_dotenv

load_dotenv()

subr_to_asset = {
    'ethereum': 'ETH/USD'
}

subreddit = 'ethereum'

# paper=True enables paper trading
trading_client = TradingClient(os.getenv("API_KEY_PAPER"), os.getenv("SECRET_KEY_PAPER"), paper=True)

# preparing orders
market_order_data = MarketOrderRequest(
                    symbol='TSLA',
                    qty=0.1,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )

