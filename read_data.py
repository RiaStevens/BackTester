#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 20:03:57 2020

@author: riastevens
"""

import pandas as pd
import os
from datetime import datetime
import numpy as np
from lstm import train
import platform

def read_data(start, end):
    pd.set_option('display.max_columns', 500)
    
    directory = './testers/'
    if platform.system() == "Windows": #windows workaround for path issues
        directory = "D:\Programming\Python\BackTester\\"
    stock_dict = {}
    stock_start = 0
    stock_end = 0
    
    for input_file in os.listdir(directory):
        if not input_file.endswith(".txt"):
            continue
        filepath = directory + input_file
        try:
            with open(filepath, 'r') as f:
                f.readline()
                line = f.readline()
                stock_start = line.split(',')[2]
                for line in f:
                    pass
                stock_end = line.split(',')[2]
            
            stock_start = datetime.strptime(stock_start, '%Y%m%d')
            stock_start = np.datetime64(stock_start)
            stock_end = datetime.strptime(stock_end, '%Y%m%d')
            stock_end = np.datetime64(stock_end)
            
            if stock_start > end or stock_end < start:
                continue
            
            stock_df = pd.read_csv(filepath, 
                             index_col = '<DATE>', 
                             usecols = ['<DATE>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>'],
                             parse_dates = ['<DATE>'],
                             header = 0)
        except:
            continue
        
        ticker = input_file.split('.')[0]

        predict_start = start
        if stock_start > start:
            predict_start = stock_start
        
        predictions = train(stock_df, predict_start)
        
        stock_df['<PREDICTIONS>'] = predictions
        
        stock_dict[ticker] = (stock_df, stock_start, stock_end) 
        
     
    return stock_dict
