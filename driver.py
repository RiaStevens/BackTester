#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:07:55 2020

@author: riastevens
"""
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt

#from tabulate import tabulate


from read_data import read_data
from algorithm import run_algo
import  util

using_config = True #automate testing and use a config file
config_file_name = "settings.cfg" #name of  config file TODO let the user choose this



initial_investment = 0
start_date = None
end_date = None





if not using_config:
    art_date, end_date, initial_investment =   util.get_config_from_console()

else:
    start_date, end_date, initial_investment =  util.get_config_from_file(config_file_name)


stock_dict = read_data(start_date, end_date)

movesLSTM, equitiesLSTM, movesMA, equitiesMA = run_algo(stock_dict, start_date, end_date, initial_investment)



#df = stock_dict['abt'][0]
#print(tabulate(df, headers=['Date', 'Open', 'High', 'Low', 'Close', 'Vol', '10-Day Moving Average', '50-Day Moving Average']))
    
#for date in equitiesLSTM:
  #  print(str(date) + ': $' + str(equitiesLSTM[date]))

dates = list(equitiesLSTM.keys())
equityLSTM_list = list(equitiesLSTM.values())
equityMA_list = list(equitiesMA.values())

register_matplotlib_converters()

plt.plot(dates, equityLSTM_list, color = 'blue', label = 'LSTM results')
plt.plot(dates, equityMA_list, color = 'green', label = 'MA results')
plt.title('MA vs LSTM perfomance')
plt.xlabel('Date')
plt.ylabel('Equity')
plt.legend()
plt.show()



movesLSTM_file = open("movesLSTM.txt", "w")
movesLSTM_file.write(movesLSTM)
movesLSTM_file.close()

movesMA_file = open("movesMA.txt", "w")
movesMA_file.write(movesMA)
movesMA_file.close()
