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
    dataframe = pd.read_csv(path,usecols=["TRIP_ID","TIMESTAMP","POLYLINE"],dtype={'TIMESTAMP':'int'},nrows=200000)
    return dataframe

dataframe= get_data('C:/Users/Vivek_Chole/Downloads/21098_27195_compressed_train/train.csv')
processed_data = []
for i in dataframe.TRIP_ID:
    object_data = dataframe[dataframe.TRIP_ID == i]
    gps_data = object_data.POLYLINE.tolist()
    x = len(gps_data[0])
    l_data = gps_data[0][1:x-1]
    l_data = list(l_data.split(']'))

    if len(l_data)>35:
        check_fv = 0
        timestamp = int(object_data.TIMESTAMP) + 15
        for j in l_data:
            if check_fv ==0:
                check_fv +=1
                continue
            if not j :
                continue
            temp_data = j[2:]
            temp_data = temp_data.split(',')
            temp_dict={'RF':i,'Time':timestamp,'Latitude':temp_data[1],'Longitude':temp_data[0],'Altitude':0}
            timestamp+=15
            processed_data.append(temp_dict)
            temp_dict = {}

        
import csv
csv_columns = ['RF','Time','Latitude','Longitude','Altitude']

csv_file = "taxidata2.csv"
try:
    with open(csv_file, 'w',encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in processed_data:
            writer.writerow(data)
except IOError:
    print("I/O error")

    
    
    
    
