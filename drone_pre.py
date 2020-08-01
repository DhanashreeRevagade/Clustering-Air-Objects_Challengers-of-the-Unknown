import pandas as pd
import numpy as np
import sys

def convert_into_seconds(time):
    time_list = time.split(':')
    if not time_list:
        return
    hour_into_seconds = int(time_list[0])*60*60
    minutes_into_seconds = int(time_list[1])*60
    seconds = int(time_list[2])
    time_into_seconds = hour_into_seconds + minutes_into_seconds + seconds
    return time_into_seconds

def get_data(path):
    dataframe = pd.read_csv(path)
    dataframe.dropna(0, inplace = True)
    dataframe.Time = dataframe.Time.apply(convert_into_seconds)
    return dataframe

def preprocess(dataframe, limit):
    lst = []
    sum = 0
    for i in range(1, 53):
        object_data = dataframe[dataframe['RF'] == i]
        a = object_data.Time.iloc[0]
        object_data.loc[:,'Time'] = object_data.Time - a
         
        object_data['templat'] = object_data['Latitude'].shift(-1) - object_data['Latitude']
        object_data['templong'] = object_data['Longitude'].shift(-1) - object_data['Longitude']
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data['Speed'] = np.sqrt(object_data['templat']**2 + object_data['templong']**2)/3
        object_data['Acceleration'] = (object_data['Speed'].shift(-1) - object_data['Speed'])/3
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data.drop(['templat', 'templong'], axis = 1, inplace= True)
        
        tp, num_feat = object_data.shape
        columns = object_data.columns
        if tp < limit:
            object_data = object_data.append(pd.DataFrame(np.zeros((limit-tp, num_feat)), columns= columns))
        elif tp > limit:
            object_data = object_data.iloc[:limit,:]
        lst.append(object_data)
        print(object_data.shape[0])
        
    dataframe = pd.concat(lst)
    return dataframe

if __name__ == '__main__':    
    path = "WithoutTakeOffdroneall.csv"
    dataframe = get_data(path)
    dataframe = preprocess(dataframe, 3200)