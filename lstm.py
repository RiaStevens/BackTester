#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:29:46 2020

@author: riastevens
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM

# input: dataframe of stock in the format:
    # '<DATE' '<OPEN>' '<HIGH>' '<LOW>' '<CLOSE>' '<VOL>',
    # date to start simulation

# output: supervised dataframe of stock in the format:
    # t open(t-1) high(t-1) low(t-1) close(t-1) vol(t-1) open(t) high(t) low(t) close(t) vol(t)
    
def train(df, sim_start):
    
    split_pos = 0
    find_date = pd.Timestamp(sim_start)
    done = False
    
    while not done:
        try:
            split_pos = df.index.get_loc(find_date)
        except:
            find_date = find_date + np.timedelta64(1, 'D')
            continue
        done = True

    values = df.to_numpy()
    first_y = values[0][1]
    data = []
    index = []
    num_rows = values.shape[0] - 1
    for i in range(0, num_rows + 1):
        if i == 0:
            continue
        index.append(i)
        new_row_i = [i]
        new_row_i.extend(values[i - 1])
        new_row_i.extend(values[i][0:3])
        new_row_i.append(values[i][4])
        new_row_i.append(values[i][3])
        data.append(new_row_i)
    
    for i in index:
        data[i-1][0] = i
        
    sup = pd.DataFrame(data, columns = ['t', 'open(t-1)', 'high(t-1)', 'low(t-1)', 'close(t-1)', 'vol(t-1)', 
                                  'open(t)', 'high(t)', 'low(t)', 'vol(t)', 'close(t)'])
    sup = sup.set_index('t')
    sup.dropna(inplace = True)
    
    dataset = sup.to_numpy()
    
    X = dataset[:,:-5]
    y = dataset[:, -5]
    
    X_train = X[:split_pos+1]
    X_test = X[split_pos + 1:]
    
    y_train = y[:split_pos+1]
    y_test = y[split_pos+1:]
    
    scaler = MinMaxScaler(feature_range = (0,1))
    
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    y_save = y_train
    y_train = scaler.fit_transform(y_train.reshape(-1,1))
    y_test = scaler.transform(y_test.reshape(-1,1))

    y_train = y_train.reshape(1,-1)[0]
    
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
    
    model = Sequential()
    model.add(LSTM(50, input_shape = (X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    
    model.fit(X_train, y_train, epochs = 50, batch_size = 50, verbose = 0)
    y_predictions = model.predict(X_test)
    y_predictions = scaler.inverse_transform(y_predictions)

    y_predictions = y_predictions.reshape(1, -1)[0]
    results = np.array([first_y])
    results = np.append(results, y_save)
    results = np.append(results, y_predictions)
    return results

def display(actual, predicted):
    
    plt.plot(actual, color = 'blue', label = 'Actual Stock Price')
    plt.plot(predicted, color = 'green', label = 'Predicted Stock Price')
    plt.title('Stock Price Predictions')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()
    
    
