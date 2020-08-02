# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 19:23:20 2020

@author: t7dev
"""

from airplane_pre import get_air_data
from drone_pre import get_drone_data
import numpy as np
import pandas as pd


if __name__ == '__main__':    
    path = "data/newalldata.csv"
    limit = 1000
    air_data = get_air_data(path)
    air_data = air_data.iloc[:,2:]
    sam_time, feat = air_data.shape
    air_data['label'] = 0
    
    path = "data/WithoutTakeoffdroneall.csv"
    drone_data = get_drone_data(path, limit)
    drone_data = drone_data.iloc[:,2:]
    sam_time, feat = drone_data.shape
    drone_data['label'] = 1
    
    data = np.append(air_data.to_numpy(), drone_data.to_numpy(),axis=0)
    # np.save('data/cluster_data', data)
    
    data = data.reshape((-1, 1000, 6))
    
    print(air_data.shape)
    print(drone_data.shape)
    print(data.shape)
