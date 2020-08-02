# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 11:22:04 2020

@author: Dhanashree
"""

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
    
def get_avg(data):
    w, p, r = data.shape
    avgdata = []
    for i in range(0, w):
        temp = data[i]    
        avgdata.append (np.average(temp, axis = 0))
    
    clus_d = np.array(avgdata)
    return clus_d

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
    

def calc_kmeans(data, clusters):
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(data)
    y_kmeans = kmeans.fit_predict(data)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    print("Cluster centers are: ", centers)
    print("Length of predictions= ", len(y_kmeans)," Respective predictions= ", y_kmeans)
    data_distri = Counter(labels)
    print(data_distri)
    print(np.array(np.unique(y_kmeans[:151], return_counts=True)).T)
    return  centers, labels, y_kmeans

def calc_acc(class_centres, centers, pred_labels, predictions, orig_labels):
    class_centres = class_centres[2:5]
    

path = 'C:\\Users\\Dhanashree\\Desktop\\SIH2020\\Trajectory\\DATA Samples\\Our data\\cluster_data.npy'
data_orig =  np.load(path)
data_orig = data_orig.reshape((-1, 1000, 6))
data_clus = get_avg(data_orig)
print("class centroid", class_centroids(data_clus))
class_centres = class_centroids(data_clus)   
print(data_clus.shape)
orig_labels = data_clus[:, -1]
data_clus = data_clus[:,2:5]
print(data_clus.shape)
centers, pred_labels, predictions = calc_kmeans(data=data_clus, clusters = 2)
calc_acc(class_centres, centers, pred_labels, predictions, orig_labels)
elbow_method(data = data_clus)

