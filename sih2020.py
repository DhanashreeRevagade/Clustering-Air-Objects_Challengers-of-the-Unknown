import pandas as pd
import numpy as np
import sys

def get_data(path):
    dataframe = pd.read_csv(path)
    dataframe.drop(['#index','UTC_Stop','YYYYMMDD','P (hPa)', 'T(K)', 'CumDist (km)'], axis = 1, inplace= True)
    return dataframe

def preprocess(dataframe, limit):
    lst = []
    sum = 0
    for i in range(1, 53):
        object_data = dataframe[dataframe['RF'] == i]
        a = object_data.UTC_Start.iloc[0]
        object_data['UTC_Start'] = object_data.UTC_Start - a
        
        
        object_data['templat'] = object_data['Latitude'].shift(-1) - object_data['Latitude']
        object_data['templong'] = object_data['Longitude'].shift(-1) - object_data['Longitude']
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data['Speed'] = np.sqrt(object_data['templat']**2 + object_data['templong']**2)/10
        object_data['Acceleration'] = (object_data['Speed'].shift(-1) - object_data['Speed'])/10
        object_data.drop(object_data.tail(1).index,inplace=True)
        object_data.drop(['templat', 'templong'], axis = 1, inplace= True)
        
        # tp, num_feat = object_data.shape
        # columns = object_data.columns
        # if tp < limit:
        #     object_data = object_data.append(pd.DataFrame(np.zeros((limit-tp, num_feat)), columns= columns))
        # elif tp > limit:
        #     object_data = object_data.iloc[:limit,:]
        lst.append(object_data)
        
        
    dataframe = pd.concat(lst)
    return dataframe

if __name__ == '__main__':    
    path = "E:/Codes/newalldata.csv"
    dataframe = get_data(path)
    dataframe = preprocess(dataframe, 3200)
    index = dataframe.reset_index().loc[:,['RF','index']]
    index = pd.MultiIndex.from_frame(index)
    data = pd.DataFrame(dataframe.iloc[:,1:].to_numpy(), index = index)
    data = data.to_numpy().reshape((52, 3200, 5))