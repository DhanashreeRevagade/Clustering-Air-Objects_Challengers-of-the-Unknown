import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
v = 700
g=9.8

def get_data(path):
    dataframe = pd.read_csv(path,usecols=['Longitude', 'Latitude','Altitude (m masl GPS)'],nrows=10)
    return dataframe
def check_std(df):
    '''
        df: Dataframe Object
        We will keep either Latitude/Longitude constant for initial position depending upon standard deviation
    '''
    std_lat = np.std(df.Latitude)
    std_long = np.std(df.Longitude)
    if std_lat>std_long:
        return({'cord_used':'Latitude','cord_notused':'Longitude'})
    else:
        return({'cord_notused':'Latitude','cord_used':'Longitude'})

def find_trajectory(df,initial_time,time_step):
    """
        df: Dataframe Object containing Predicted Longitude,Latitude , Altitude
        initial_time: Time to reach first predicted point
        time_step: Time Step for predicted data

        This function is to find elevation angle and coordinates for finding missile launch
    """
    lst=[]
    t = initial_time
    coordinate = check_std(df)
    for i in range(0,len(df.values)):

        inverse_value = ((df['Altitude (m masl GPS)'].values[i]) + ((0.5*g)*(t**2)))/(v*t) #Find angle at which we should hit

        if inverse_value<1 and inverse_value>-1:

            angle = math.asin(inverse_value)
            x_coordinate = ((v*t)*math.cos(angle))
            x_initial = df[coordinate['cord_used']].values[i] - ((x_coordinate)*math.pi)/180
            temp_dict = {coordinate['cord_used']:x_initial,coordinate['cord_notused']:df[coordinate['cord_notused']].values[i],'time_of_impact':t,'angle_of_elev':math.degrees(angle)}
            lst.append(temp_dict)

        t+=time_step
    return(lst)

df= get_data('C:/Users/Vivek_Chole/Desktop/SIH/data/newalldata.csv')
missile_data = find_trajectory(df,10,10)
print(missile_data)
