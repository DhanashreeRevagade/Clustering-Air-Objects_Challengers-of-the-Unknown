import pandas as pd
import numpy as np
import sys

def get_data(path):
    dataframe = pd.read_csv(path)
    dataframe.drop(['#index','UTC_Stop','YYYYMMDD','P (hPa)', 'T(K)', 'CumDist (km)'], axis = 1, inplace= True)
    return dataframe

def preprocess(dataframe):
    lst = []
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
        
        tp, num_feat = object_data.shape
        columns = object_data.columns
        if tp < 1000:
            object_data = object_data.append(pd.DataFrame(np.zeros((1000-tp, num_feat)), columns= columns))
        elif tp > 1000 and tp< 2000:
            object_data = object_data.append(pd.DataFrame(np.zeros((2000-tp, num_feat)), columns= columns))
            object_data_org = object_data.iloc[:1000,:]
            object_data_gen = object_data.iloc[1000:2000, :]
            object_data_gen.RF = object_data_gen.RF.apply(lambda a: a + 52)
            object_data = object_data_org
            lst.append(object_data_gen)
            print(object_data_gen.shape)
        else:
            if tp > 3000:
                object_data = object_data.iloc[:3000,:]
            else:        
                object_data = object_data.append(pd.DataFrame(np.zeros((3000-tp, num_feat)), columns= columns))
            object_data_org = object_data.iloc[:1000,:]
            object_data_gen = object_data.iloc[1000:2000,:]
            object_data_gen.RF = object_data_gen.RF.apply(lambda a: a + 52)
            lst.append(object_data_gen)
            object_data_gen = object_data.iloc[2000:3000,:]
            object_data_gen.RF = object_data_gen.RF.apply(lambda a: a + 104)
            object_data = object_data_org
            lst.append(object_data_gen)
            print(object_data_gen.shape)

        lst.append(object_data)
        print(object_data.shape)
    dataframe = pd.concat(lst)
    return dataframe

def get_air_data(path):
    dataframe = get_data(path)
    dataframe = preprocess(dataframe)
    # index = dataframe.reset_index().loc[:,['RF']]
    # index = pd.MultiIndex.from_frame(index)
    # data = pd.DataFrame(dataframe.iloc[:,1:].to_numpy(), index = index)
    return dataframe

if __name__ == '__main__':    
    path = "data/newalldata.csv"
    limit = 3200
    data = get_air_data(path)
    print(data)
    data = data.to_numpy().reshape((-1, 1000, 7))