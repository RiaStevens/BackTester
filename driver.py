#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:07:55 2020

@author: riastevens
"""
import matplotlib.pyplot as plt
import datetime
import numpy as np
from read_data import read_data
from algorithm import run_algo
using_config = True #automate testing and use a config file
config_file_name = "settings.cfg" #name of  config file TODO let the user choose this

initial_investment = 0
start_date = None
end_date = None



def get_config_from_console():
    global start_date, end_date, initial_investment
    initial_investment = int(input('Enter an initial investment: '))
    done = False
    while not done:
        valid = False
        while not valid:
            try:
                start_date = input(
                    'When would you like to begin the stock simulation? Enter a date in DD-MM-YYYY format: ')
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

def get_config_from_file():
    config_file = open(config_file_name, "r")
    global start_date, end_date, initial_investment

    #reading the file line by line and converting to a useful format
    initial_investment = int(config_file.readline())

    start_date = config_file.readline()
    start_day, start_month, start_year = map(int, start_date.split('-'))
    start_date = datetime.datetime(start_year, start_month, start_day)
    start_date = np.datetime64(start_date)

    end_date = config_file.readline()
    end_day, end_month, end_year = map(int, end_date.split('-'))
    end_date = datetime.date(end_year, end_month, end_day)
    end_date = np.datetime64(end_date)

if not using_config:
    get_config_from_console()

else:
    get_config_from_file()


stock_dict = read_data()

moves, equities = run_algo(stock_dict, start_date, end_date, initial_investment)

for date in equities:
    print(str(date) + ': $' + str(equities[date]))

dates = list(equities.keys())
equity_list = list(equities.values())

plt.plot(dates, equity_list)
plt.show()

moves_file = open("moves.txt", "w")
moves_file.write(moves)
moves_file.close()
