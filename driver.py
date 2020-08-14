#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:07:55 2020

@author: riastevens
"""
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import datetime
import numpy as np
from read_data import read_data
from algorithm import run_algo
from tabulate import tabulate

initial_investment = int(input('Enter an initial investment: '))
start_date = None
end_date = None

done = False
while not done:
    valid = False
    while not valid:
        try:
            start_date = input('When would you like to begin the stock simulation? Enter a date in DD-MM-YYYY format: ')
            start_day, start_month, start_year = map(int, start_date.split('-'))
            start_date = datetime.datetime(start_year, start_month, start_day)
            start_date = np.datetime64(start_date)
        except: 
            print('Please enter a valid date in the specified format!')
            continue
        valid = True

    valid = False
    while not valid:
        try:
            end_date = input('When would you like to end the simulation? Enter a date in DD-MM-YYYY format: ')
            end_day, end_month, end_year = map(int, end_date.split('-'))  
            end_date = datetime.date(end_year, end_month, end_day)
            end_date = np.datetime64(end_date)
        except:
            print('Please enter a valid date in the specified format!')
            continue
        valid = True
        
    if start_date < end_date:
        done = True
    
    else:
        print('Make sure your start date comes before your end date!')


stock_dict = read_data()

moves, equities = run_algo(stock_dict, start_date, end_date, initial_investment)


df = stock_dict['abt'][0]
print(tabulate(df, headers=['Date', 'Open', 'High', 'Low', 'Close', 'Vol', '10-Day Moving Average', '50-Day Moving Average']))
    
#for date in equities:
   # print(str(date) + ': $' + str(equities[date]))

dates = list(equities.keys())
equity_list = list(equities.values())

register_matplotlib_converters()

plt.plot(dates, equity_list)
plt.show()

moves_file = open("moves.txt", "w")
moves_file.write(moves)
moves_file.close()
