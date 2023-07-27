from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import pandas as pd


# PARAMETERS -------------
FILENAME = 'stock_onemin.csv'
STARTING_CASH = 25000
STAKE_PERCENT = 0.5
BROKER_COMISH = 0
START_DATE = datetime.datetime(2000, 1, 1)
END_DATE = datetime.datetime(2023, 12, 31)


mydata = pd.read_csv(FILENAME)
start_price = mydata['close'].iloc[0]


# Create a Stratey
class TestStrategy(bt.Strategy):

    params = (
        ('ema8_period', 8),
        ('ema13_period', 13),
        ('ema21_period', 21),
        ('ema55_period', 55),
        ('entrytime', 15),  # 15 for 10:00am Eastern time
        ('exittime', 21)  # 21 for 4:00pm Eastern time
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0).strftime('%Y-%m-%d %H:%M:%S')
        print('%s, %s' % (dt, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # Add a MovingAverageSimple indicator
        self.EMA55 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema55_period, plotname='EMA55')
        self.EMA8 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema8_period, plotname='EMA8')
        self.EMA21 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema21_period, plotname='EMA21')
        self.EMA13 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema13_period, plotname='EMA13')


        # Indicators for the plotting show
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=8)
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=55)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # if self.datas[0].datetime.time() == datetime.time(self.params.entrytime, 0):
        #     # Check if we are in the market
        #
        #     if not self.position:
        #         # Not yet ... we MIGHT BUY if ...
        #         if self.EMA55[0] < self.EMA13[0]:
        #                 # current close less than previous close
        #
        #                 # if self.EMA8[0] > self.EMA13[0]:
        #                     # previous close less than the previous close
        #
        #                     # BUY, BUY, BUY!!! (with default parameters)
        #                     self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #
        #                     # Keep track of the created order to avoid a 2nd order
        #                     self.order = self.buy()

        if datetime.time(self.params.entrytime, 0) < self.datas[0].datetime.time() < datetime.time(self.params.exittime, 0):
            # Check if we are in the market

            if not self.position:
                # Not yet ... we MIGHT BUY if ...
                if self.EMA55[0] < self.EMA13[0] and self.EMA55[-1] > self.EMA13[-1]:
                        # current close less than previous close

                        # if self.EMA8[0] > self.EMA13[0]:
                            # previous close less than the previous close

                            # BUY, BUY, BUY!!! (with default parameters)
                            self.log('BUY CREATE, %.2f' % self.dataclose[0])

                            # Keep track of the created order to avoid a 2nd order
                            self.order = self.buy()

            elif self.position:
                # Already in the market ... we might sell
                if self.EMA55[0] > self.EMA13[0] and self.EMA55[-1] < self.EMA13[-1]:
                    # current close less than previous close

                    # if self.EMA8[0] < self.EMA13[0]:
                        # SELL, SELL, SELL!!! (with all possible default parameters)
                        self.log('SELL CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.sell()

        elif self.position and datetime.time(self.params.exittime, 0) > datetime.time(self.params.entrytime, 0):

            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('SELL CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()  # cheat_on_open=True

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname=FILENAME,
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
        fromdate=datetime.datetime(2023, 1, 30, 15, 00, 00),
        todate=datetime.datetime(2023, 2, 4, 21, 00, 00),
        # fromdate=START_DATE,
        # todate=END_DATE,
        sessionstart=datetime.time(15, 00, 00),
        sessionend=datetime.time(21, 00, 00),
        dtformat='%Y-%m-%d %H:%M:%S+00:00',
        timeformat="%H:%M:%S+00:00",
        # tz='US/Eastern',
        # tzinput='US/Eastern',
        useRTH=True,
        # outsideRth=False,
        reverse=False,
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=6,
        trade_count=7,
        vwap=8
        )

    # add above filters
    data.addfilter(bt.filters.SessionFilter(data))

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(STARTING_CASH)

    # Set the stake amount
    stake = (STARTING_CASH * STAKE_PERCENT) / start_price
    cerebro.addsizer(bt.sizers.FixedSize, stake=float(stake))

    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=BROKER_COMISH)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
