# BackTester

Backtests a trading strategy against historic market data

# Next Steps
Build more detailed graph
Improve the trading strategy
Create a webpage!

# Config files
settings.cfg is used to avoid re-inputting testing data every time you want to run it, e.g. not
having to type out dates. It looks like:
initial investment
start date
end date
e.g.
1000
01-01-2000
01-01-2020

# Driver.py
Gets start date, end date and initial investments from user or config file
Calls read_data, algorithm to simulate the market
Plots total equity in portfolio from start date to end date

# Algorithm.py
Tracks cash on hand, shares of each stock owned in the portfolio, moves (buys/sells made).
Executes trades if certain requirements are met (see current trading strategy)
Tracks and returns total equity in portfolio by day

Current trading strategy: Buy one share (or as much of a portion of one share is in cash) if 10-Day-Moving-Average surpasses 50-Day-Moving-Average, Sell one share (or as much of one share is in portfolio) if 50-Day-Moving-Average surpasses 10-Day-Moving-Average

# Read_data.py
Reads the historical data into a dictionary with tickers as keys and values of the format: (stock_df, stock_start, stock_end), where stock_df is a dataframe containing columns for date, open, close, high, low, volume
Reads the stock's data into the dataframe and dictionary only if it falls without the start and end date ranges
Returns this dictionary
