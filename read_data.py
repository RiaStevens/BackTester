#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 20:03:57 2020

@author: riastevens
"""

import numpy as np
import pandas as pd
import os

def read_data():
    pd.set_option('display.max_columns', 500)
    
    #directory = '/Users/riastevens/Desktop/finances/hmd/daily/us/nyse_stocks/testers/'
    directory = 'D:\Programming\Python\BackTester\\'
    stock_dict = {}
    
    for file in os.listdir(directory):
        if not file.endswith(".txt"):
            continue
        filepath = directory + file
        try:
            stock_df = pd.read_csv(filepath, 
                             index_col = '<DATE>', 
                             usecols = ['<DATE>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>'],
                             parse_dates = ['<DATE>'],
                             header = 0)

        except:
            continue

        
        ticker = file.split('.')
        ticker = ticker[0]
        
        index_list = stock_df.index
        start_date = index_list[0]
        end_date = index_list[index_list.size - 1]
        stock_dict[ticker] = (stock_df, start_date, end_date) 
     
    return stock_dict
