#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:43:37 2020

@author: riastevens
"""

import numpy as np 
import math

cash = 0
portfolio = {}
equities = {}
moves = ""

def run_algo(stock_dict, start_date, end_date, initial_investment):
    global cash
    cash = initial_investment
    
    while start_date <= end_date and start_date <= np.datetime64("2020-08-10"):
        for ticker in stock_dict:
            tup = stock_dict[ticker]
            df = tup[0]
            stock_start = tup[1]
            stock_end = tup[2]
            
            if stock_start > start_date or stock_end < start_date:
                continue
            
            if not (start_date in df.index.values):
                continue
            
            if not ('<10-DAY MOVING AVERAGE>' in df.columns):
                df['<10-DAY MOVING AVERAGE>'] = np.nan
              
            if not ('<50-DAY MOVING AVERAGE>' in df.columns):
               df['<50-DAY MOVING AVERAGE>'] = np.nan
            
            decide(df, start_date, ticker)
        
        evaluate_portfolio(start_date)
        start_date = start_date + np.timedelta64(1, 'D')
        
    return moves, equities

def decide(df, date, ticker):
    global portfolio
    global cash
    mv_close = df.loc[date]['<CLOSE>'] # date, open, high, low, close, vol, 10-day mv avg, 50-day mv avg
    mov_avg_10 = np.NaN                #   0     1     2    3     4     5          6           7
    mov_avg_50 = np.NaN
    date_loc = df.index.get_loc(date)
          
    if date_loc >= 50:
        past_date = date_loc - 1
        past_ma = df.iloc[past_date, 6]
        if not math.isnan(past_ma):
            delete_close = df.iloc[date_loc - 50, 3]
            sum_50 = past_ma * 50 - delete_close + mv_close
            mov_avg_50 = sum_50 / 50
        if math.isnan(mov_avg_50):
            mov_avg_50 = calculate_ma_50(df, date_loc)
        
        df.loc[date, '<50-DAY MOVING AVERAGE>'] = mov_avg_50
        
        past_date = date_loc - 1
        past_ma = df.iloc[past_date, 5]
        if not math.isnan(past_ma):
            delete_close = df.iloc[date_loc - 10, 3]
            sum_10 = past_ma * 10 - delete_close + mv_close
            mov_avg_10 = sum_10 / 10
        if math.isnan(mov_avg_10):
            mov_avg_10 = calculate_ma_10(df, date_loc)
        
        df.loc[date, '<10-DAY MOVING AVERAGE>'] = mov_avg_10
            
    if mov_avg_10 > mov_avg_50:
        if cash >= mv_close:
            buy(ticker=ticker, date=date, shares=1, price=mv_close)
        elif not cash == 0:
            shares = cash / mv_close
            buy(ticker=ticker, date=date, shares=shares, price=mv_close)
            
    elif mov_avg_10 < mov_avg_50:
        if ticker in portfolio:
            if portfolio[ticker][0] >= 1:
                sell(ticker=ticker, date=date, shares=1, price=mv_close)
            elif portfolio[ticker][0] > 0:
                sell(ticker=ticker, date=date, shares=portfolio[ticker][0], price=mv_close)
            
def buy(ticker, date, shares, price):
    global cash
    global portfolio
    global moves
    
    cash -= shares * price
    
    if ticker in portfolio:
        portfolio[ticker] = (portfolio[ticker][0] + shares, price)
    else:
        portfolio[ticker] = (shares, price)
    moves += ("\n" + str(date) + ": Bought " + str(shares) + " of " + ticker + " for " + str(price) + 
           " each. Cash in bank: " + str(cash) + ". Shares of this stock: " 
           + str(portfolio[ticker][0]) + ".")
    return
    
def sell(ticker, date, shares, price):
    global cash
    global portfolio
    global moves
    
    cash += shares * price
    portfolio[ticker] = (portfolio[ticker][0] - shares, price)
    moves += ("\n" + str(date) + ": Sold " + str(shares) + " of " + ticker + " for " + str(price) + 
           " each. Cash in bank: " + str(cash) + ". Shares of this stock: " 
           + str(portfolio[ticker][0]) + ".")
    return
    
def calculate_ma_10(df, date_loc):
    sum = 0
    for i in range(0, 10):
        add_close = df.iloc[date_loc - i, 3]
        sum += add_close
    return (sum / 10)
    
def calculate_ma_50(df, date_loc):
    sum = 0
    for i in range(0, 50):
        add_close = df.iloc[date_loc - i, 3]
        sum += add_close
    return (sum / 50)
    
def evaluate_portfolio(date):
    global cash
    global portfolio
    global equities
    
    total_equity = cash
    
    for ticker in portfolio:
        shares = portfolio[ticker][0]
        if shares == 0:
            continue
        stock_mv = portfolio[ticker][1]
        total_equity += stock_mv * shares
                
    equities[date] = total_equity
    return 
            
            
            
    