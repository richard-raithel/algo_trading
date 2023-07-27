# algo_trading
This repo contains scripts to backtest custom trading algorithms and indicators. It uses alpaca paper trading and backtrader.

To perform backtesting:

1. Put your data into this format in a csv file and save it to the 'data' folder:
date,open,high,low,close,Adj Close,volume,trade_count,vwap
2023-01-30 09:00:00+00:00,178.5,178.96,176.23,176.8,176.8,79410.0,1673.0,178.111354

2. Create a .env file and put it in the same directory as the backtest.py script.It must include your unique API keys obtained from aplaca.markets. The two necessary keys are: API_KEY_PAPER and SECRET_KEY_PAPER

3. Set your parameters within the backtest.py script. They are located just below the imports.

4. If desired, modify the 'TestStrategy' class to include other indicators and strategies.

5. Run the script

6. Results
   a. A line plot is produced with indicators in your strategy randomly colored.
   b. Volume is plotted below the line plot. macd is plotted in the first subplot. RSI is plotted in the second subplot.
   c. Entry and exit points are highlighted in green and red, respectively.
   d. Positive and negative results from the exits are highlighted as blue and red circles, respectively.
   e. The top right corner of the plot will display your final portfolio value.
