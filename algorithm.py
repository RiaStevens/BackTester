#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:43:37 2020

@author: riastevens
"""

import numpy as np 
import math

cashLSTM = 0
portfolioLSTM = {}
equitiesLSTM = {}
movesLSTM = ""

cashMA = 0
portfolioMA = {}
equitiesMA = {}
movesMA = ""

def run_algo(stock_dict, start_date, end_date, initial_investment):
    global cashLSTM
    global cashMA
    global equitiesLSTM
    global equitiesMA
    global movesLSTM
    global movesMA
    
    
    cashLSTM = initial_investment
    cashMA = initial_investment
    
    while start_date <= end_date and start_date <= np.datetime64("2020-08-10"):
        for ticker in stock_dict:
            tup = stock_dict[ticker]
            df = tup[0]
            stock_start = tup[1]
            stock_end = tup[2]
            
            if stock_start > end_date or stock_end < start_date:
                continue
            
            if not (start_date in df.index.values):
                continue
            
           
            decideLSTM(df, start_date, ticker)
            decideMA(df, start_date, ticker)
            
        
        evaluate_portfolio(start_date, stock_dict)
        start_date = start_date + np.timedelta64(1, 'D')
        
    return movesLSTM, equitiesLSTM, movesMA, equitiesMA

def decideLSTM(df, date, ticker):
    global portfolioLSTM
    global cashLSTM
    
    # CANT LOOK FURTHER THAN TODAY IN PREDICTIONS!
    predicted_open = df.loc[date]['<PREDICTIONS>']
    mv_close = df.loc[date]['<CLOSE>']
    pct_change = ((predicted_open - mv_close) / mv_close) * 100
    
    if pct_change < 0 and cashLSTM > 0:
        if pct_change > 10 and cashLSTM >= 2 * mv_close:
            buyLSTM(ticker=ticker, date=date, shares=2, price=mv_close)
        elif cashLSTM >= mv_close:
            buyLSTM(ticker=ticker, date=date, shares=1, price=mv_close)
        else:
            shares = cashLSTM / mv_close
            buyLSTM(ticker=ticker, date=date, shares=shares, price=mv_close)
            
    owned = 0
    try:
        owned = portfolioLSTM[ticker][0]
    except KeyError:
        pass
    
    if pct_change > 0 and owned > 0:
        if pct_change < -20 and owned > 2:
            sellLSTM(ticker=ticker, date=date, shares=2, price=mv_close)
        elif owned > 1:
            sellLSTM(ticker=ticker, date=date, shares=1, price=mv_close)
        else:
            sellLSTM(ticker=ticker, date=date, shares=owned, price=mv_close)
        
            
def decideMA(df, date, ticker):
    global portfolioMA
    global cashMA
    
    mv_close = df.loc[date]['<CLOSE>'] 
    
    if not ('<10-DAY MOVING AVERAGE>' in df.columns):
        df['<10-DAY MOVING AVERAGE>'] = np.nan
              
    if not ('<50-DAY MOVING AVERAGE>' in df.columns):
        df['<50-DAY MOVING AVERAGE>'] = np.nan
        
    mov_avg_10 = np.NaN               
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
        if cashMA >= mv_close:
            buyMA(ticker=ticker, date=date, shares=1, price=mv_close)
        elif not cashMA == 0:
            shares = cashMA / mv_close
            buyMA(ticker=ticker, date=date, shares=shares, price=mv_close)
            
    elif mov_avg_10 < mov_avg_50:
        if ticker in portfolioMA:
            if portfolioMA[ticker][0] >= 1:
                sellMA(ticker=ticker, date=date, shares=1, price=mv_close)
            elif portfolioMA[ticker][0] > 0:
                sellMA(ticker=ticker, date=date, shares=portfolioMA[ticker][0], price=mv_close)
            
def buyLSTM(ticker, date, shares, price):
    global cashLSTM
    global portfolioLSTM
    global movesLSTM
    
    cashLSTM -= shares * price
    
    if ticker in portfolioLSTM:
        portfolioLSTM[ticker] = (portfolioLSTM[ticker][0] + shares, price)
    else:
        portfolioLSTM[ticker] = (shares, price)
    movesLSTM += ("\n" + str(date) + ": Bought " + str(shares) + " of " + ticker + " for " + str(price) + 
           " each. Cash in bank: " + str(cashLSTM) + ". Shares of this stock: " 
           + str(portfolioLSTM[ticker][0]) + ".")
    return
    
def sellLSTM(ticker, date, shares, price):
    global cashLSTM
    global portfolioLSTM
    global movesLSTM
    
    cashLSTM += shares * price
    portfolioLSTM[ticker] = (portfolioLSTM[ticker][0] - shares, price)
    movesLSTM += ("\n" + str(date) + ": Sold " + str(shares) + " of " + ticker + " for " + str(price) + 
           " each. Cash in bank: " + str(cashLSTM) + ". Shares of this stock: " 
           + str(portfolioLSTM[ticker][0]) + ".")
    return

def buyMA(ticker, date, shares, price):
    global cashMA
    global portfolioMA
    global movesMA
    
    cashMA -= shares * price
    
    if ticker in portfolioMA:
        portfolioMA[ticker] = (portfolioMA[ticker][0] + shares, price)
    else:
        portfolioMA[ticker] = (shares, price)
    movesMA += ("\n" + str(date) + ": Bought " + str(round(shares, 2)) + " of " + ticker + " for " + str(price) + 
           " each. Cash in bank: " + str(round(cashMA, 2)) + ". Shares of this stock: " 
           + str(portfolioMA[ticker][0]) + ".")
    return
    
def sellMA(ticker, date, shares, price):
    global cashMA
    global portfolioMA
    global movesMA
    
    cashMA += shares * price
    portfolioMA[ticker] = (portfolioMA[ticker][0] - shares, price)
    movesMA += ("\n" + str(date) + ": Sold " + str(round(shares, 2)) + " of " + ticker + " for " + str(price) + 
           " each. Cash in bank: " + str(round(cashMA, 2)) + ". Shares of this stock: " 
           + str(portfolioMA[ticker][0]) + ".")
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
    
def evaluate_portfolio(date, stock_dict):
    global cashLSTM
    global cashMA
    global portfolioLSTM
    global portfolioMA
    global equitiesLSTM
    global equitiesMA
    
    total_equityLSTM = cashLSTM
    date_var = date
    
    for ticker in portfolioLSTM:
        date_var = date
        sharesLSTM = portfolioLSTM[ticker][0]
        
        if sharesLSTM == 0:
            continue
        
        df = stock_dict[ticker][0]
       
        done = False
        stock_mvLSTM = portfolioLSTM[ticker][1]
        while not done:
            try:    
                stock_mvLSTM = df.loc[date_var]['<CLOSE>']
                done = True
            except:
                date_var = date_var - np.timedelta64(1, 'D')

        total_equityLSTM += stock_mvLSTM * sharesLSTM
        portfolioLSTM[ticker] = (sharesLSTM, stock_mvLSTM)
        
    equitiesLSTM[date] = total_equityLSTM
    
    total_equityMA = cashMA
    
    
    for ticker in portfolioMA:
        date_var = date
        sharesMA = portfolioMA[ticker][0]
        
        if sharesMA == 0:
            continue
        
        df = stock_dict[ticker][0]
       
        done = False
        stock_mvMA = portfolioMA[ticker][1]
        while not done:
            try:    
                stock_mvMA = df.loc[date_var]['<CLOSE>']
                done = True
            except:
                date_var = date_var - np.timedelta64(1, 'D')

        total_equityMA += stock_mvMA * sharesMA
        portfolioMA[ticker] = (sharesMA, stock_mvMA)
        
    equitiesMA[date] = total_equityMA
    
    
   # print(str(date) + ': ')
    #for ticker in portfolioLSTM:
       # print(ticker + ' shares: ' + str(portfolioLSTM[ticker][0]) + ' mv: ' + str(portfolioLSTM[ticker][1]))
    return 
            
            
            
    