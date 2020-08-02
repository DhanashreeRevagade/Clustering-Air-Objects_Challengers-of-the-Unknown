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

path = 'C:\\Users\\Dhanashree\\Desktop\\SIH2020\\Trajectory\\DATA Samples\\Our data\\cluster_data.npy'
data =  np.load(path)
data = data.reshape((-1, 1000, 6))
data_clus, label = data[:,:,:5], data[ :,:, 5]
label = label[:]
#data_clus = data_clus[:,:,2:]
data_clus = data_clus.reshape((288,5000))

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

def calc_kmeans(data, clusters):
    kmeans = KMeans(n_clusters=clusters, random_state=0)
    y_kmeans = kmeans.fit_predict(data)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    print("Cluster centers are: ", centers)
    print("Length of predictions= ", len(y_kmeans)," Respective predictions= ", y_kmeans)
    data_distri = Counter(labels)
    print(data_distri)
    print(np.array(np.unique(y_kmeans[:144], return_counts=True)).T)
    
calc_kmeans(data=data_clus, clusters = 2)
elbow_method(data = data_clus)