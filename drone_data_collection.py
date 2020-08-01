import os
import pandas as pd
import numpy as np

rootdir = "C:\\Users\\Dhanashree\\Desktop\\SIH2020\\Trajectory\\DATA Samples\\DRONE\\DroneFlightData\\WithoutTakeoff"

lst = []
lst2=[]
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        lst.append(os.path.join(subdir, file))
#print(lst)
        
for i in lst:
    if i.endswith('.csv'):
        lst2.append(i)

print(len(lst2))


cols = ['RF','Time', 'Latitude', 'Longitude', 'Altitude']
df = pd.DataFrame(columns= cols)
k=1
for i in range(0, len(lst2)):
    curr_df = pd.read_csv(lst2[i])
    tempdf = pd.DataFrame()
    tempdf['Time']= curr_df['time']
    tempdf['Latitude'] = curr_df['lat']
    tempdf['Longitude'] = curr_df['lon']
    tempdf['Altitude'] = curr_df['alt']
    tempdf['RF'] = str(i+1)
   # print(tempdf)
    df= df.append(tempdf, ignore_index=True)
    
print(df)    
df.to_csv(rootdir+"droneall.csv")