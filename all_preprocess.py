# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 01:35:28 2020

@author: Dhanashree
"""
import pandas as pd
import numpy as np



def taxi_pre(dataframe, limit):
    lst = []
    sum = 0
    x = (dataframe.RF.unique())
    print("*******************************************",len(x))
    for i in range(0, 200):
        object_data = dataframe[dataframe['RF'] == x[i]]
        a = object_data.Time.iloc[0]
        object_data.loc[:,'Time'] = object_data.Time - a
         
        object_data['templat'] = object_data['Latitude'].shift(-1) - object_data['Latitude']
        object_data['templong'] = object_data['Longitude'].shift(-1) - object_data['Longitude']
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data['Speed'] = np.sqrt(object_data['templat']**2 + object_data['templong']**2)/3
        object_data['Acceleration'] = (object_data['Speed'].shift(-1) - object_data['Speed'])/3
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data.drop(['templat', 'templong'], axis = 1, inplace= True)
        #print(object_data.shape)
        tp, num_feat = object_data.shape
        columns = object_data.columns
        if tp < limit:
            object_data = object_data.append(pd.DataFrame(np.zeros((limit-tp, num_feat)), columns= columns))
        elif tp > limit:
            object_data = object_data.iloc[:limit,:]
        lst.append(object_data)
        
    dataframe = pd.concat(lst)
    return dataframe

def uav_pre(dataframe, limit):
    lst = []
    sum = 0
    x = (dataframe.SV.unique())
    print("***************************************", len(x))
    for i in range(0, len(x)):
        object_data = dataframe[dataframe['SV'] == x[i]]
        '''a = object_data.Time.iloc[0]
        object_data.loc[:,'Time'] = object_data.Time - a
         
        object_data['templat'] = object_data['Latitude'].shift(-1) - object_data['Latitude']
        object_data['templong'] = object_data['Longitude'].shift(-1) - object_data['Longitude']
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data['Speed'] = np.sqrt(object_data['templat']**2 + object_data['templong']**2)/3
        object_data['Acceleration'] = (object_data['Speed'].shift(-1) - object_data['Speed'])/3
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data.drop(['templat', 'templong'], axis = 1, inplace= True)
        #print(object_data.shape)'''
        object_data.drop(['Unnamed: 0'], axis = 1, inplace= True)
        tp, num_feat = object_data.shape
        columns = object_data.columns
        if tp < limit:
            object_data = object_data.append(pd.DataFrame(np.zeros((limit-tp, num_feat)), columns= columns))
        elif tp > limit:
            object_data = object_data.iloc[:limit,:]
        lst.append(object_data)
        
    dataframe = pd.concat(lst)
    return dataframe

def bird_pre(dataframe, limit):
    
    dataframe.dropna(axis = 0, how= 'any', inplace = True)
    dataframe.drop([ 'bird_name', 'direction'], axis=1, inplace = True)
    dataframe.rename(columns={'altitude': 'Altitude', 'device_info_serial' : 'RF', 'latitude': 'Latitude',
       'longitude': 'Longitude' , 'speed_2d': 'Speed'}, inplace=True)
    lst = []
    sum = 0
    x = (dataframe.RF.unique())
    print("********************",len(x))
    for i in range(0, len(x)):
        object_data = dataframe[dataframe['RF'] == x[i]]
        '''a = object_data.Time.iloc[0]
        object_data.loc[:,'Time'] = object_data.Time - a
         
        object_data['templat'] = object_data['Latitude'].shift(-1) - object_data['Latitude']
        object_data['templong'] = object_data['Longitude'].shift(-1) - object_data['Longitude']
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data['Speed'] = np.sqrt(object_data['templat']**2 + object_data['templong']**2)/3'''
        #object_data['Acceleration'] = (object_data['Speed'].shift(-1) - object_data['Speed'])/3
        #object_data.drop(object_data.tail(1).index,inplace=True)
        #object_data.drop(['templat', 'templong'], axis = 1, inplace= True)
        #print(object_data.shape)
        tp, num_feat = object_data.shape
        columns = object_data.columns
        if tp < limit:
            object_data = object_data.append(pd.DataFrame(np.zeros((limit-tp, num_feat)), columns= columns))
        elif tp > limit:
            object_data = object_data.iloc[:limit,:]
        lst.append(object_data)
        
    dataframe = pd.concat(lst)
    return dataframe

mis_path = 'C:\\Users\\Dhanashree\\Documents\\GitHub\\CK108_Challengers_of_the_Unknown\\data\\Trajectory_of_missile_data.npy'
uav_path = 'C:\\Users\\Dhanashree\\Documents\\GitHub\\CK108_Challengers_of_the_Unknown\\data\\usv_final.csv'
taxi_path = 'C:\\Users\\Dhanashree\\Documents\\GitHub\\CK108_Challengers_of_the_Unknown\\data\\taxidata.csv'
birds_path = 'C:\\Users\\Dhanashree\\Documents\\GitHub\\CK108_Challengers_of_the_Unknown\\data\\bird_tracking.txt'

taxi = pd.read_csv(taxi_path)
uav = pd.read_csv(uav_path)
mis = np.load(mis_path)
bird = pd.read_csv(birds_path)

taxi_pre = taxi_pre(taxi, 1000)
uav_pre = uav_pre(uav, 1000)
bird_pre = bird_pre(bird, 1000)