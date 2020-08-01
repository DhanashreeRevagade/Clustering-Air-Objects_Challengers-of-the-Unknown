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
    air_data = air_data.to_numpy().reshape((-1, 1000, 7))
    air_data = air_data[:,:,2:]
    
    path = "data/WithoutTakeoffdroneall.csv"
    drone_data = get_drone_data(path, limit)
    drone_data = drone_data.to_numpy().reshape((-1, limit, 6))
    drone_data = drone_data[:,:,1:]
    
    data = np.append(air_data, drone_data,axis=0)
    print(data.shape)
    
    np.save('data/cluster_data', data)

    print(air_data.shape)
    print(drone_data.shape)
