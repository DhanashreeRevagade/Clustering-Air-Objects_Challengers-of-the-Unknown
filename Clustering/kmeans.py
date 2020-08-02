# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 00:41:17 2020

@author: Dhanashree
"""

import pandas as pd 
import numpy as np
import sys
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from sklearn.cluster import KMeans
from collections import Counter, defaultdict



def elbow_method(data):
    Error =[]
    for i in range(1, 11):
        kmeans = KMeans(n_clusters = i)
        kmeans.fit(data)
        Error.append(kmeans.inertia_)
    plt.plot(range(1, 11), Error)
    plt.title('Elbow method')
    plt.xlabel('No of clusters')
    plt.ylabel('Error')
    plt.show()

def class_centroids(data):
    p, r = data.shape
    grouped = {} 
    centroid = [] 
    for i in range(0, p):
        temp = data[i]
        if(temp[5] in grouped.keys()):
            grouped[temp[5]].append(temp)
        else:
            grouped[temp[5]] = []
            grouped[temp[5]].append(temp)
    for i in grouped.keys():
        centroid.append(np.average(grouped[i], axis = 0))
    class_centroid = np.array(centroid)
    return class_centroid

def alt_time(centres):
    centres = centres.reshape(-1, 1000, 3)
    print("centres shape ", centres.shape)
    c, t, f = centres.shape
    time = [i for i in range(0,t*10,10)]
    #in cluster centres class 
    alt1 = centres[ 0,:, 0]
    alt2 = centres[ 1,:, 0]
    plt.plot( alt1)
    plt.title('Drone centroid')
    plt.xlabel('Time')
    plt.ylabel('Altitude')
    plt.show()
    plt.plot(time, alt2)
    plt.title('Plane centroid')
    plt.xlabel('Time')
    plt.ylabel('Altitude')
    plt.show()
        
def calc_kmeans(data, clusters):
    kmeans = KMeans(n_clusters=clusters, random_state=0)
    y_kmeans = kmeans.fit_predict(data)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    print("Cluster centers are: ", centers)
    print("Length of predictions= ", len(y_kmeans)," Respective predictions= ", y_kmeans)
    data_distri = Counter(labels)
    print(data_distri)
    print(np.array(np.unique(y_kmeans[:151], return_counts=True)).T)
    
    return  centers, labels, y_kmeans
    
path = 'C:\\Users\\Dhanashree\\Desktop\\SIH2020\\Trajectory\\DATA Samples\\Our data\\cluster_data.npy'
data =  np.load(path)
data = data.reshape((-1, 1000, 6))
data_clus, label = data[:,:,:5], data[ :,:, 5]
label = label[:]
data_clus = data_clus[:,:,2:5]
data_clus = data_clus.reshape((288,3000))
centres, pred_labels, pred_y = calc_kmeans(data=data_clus, clusters = 2)
alt_time(centres)
elbow_method(data = data_clus)