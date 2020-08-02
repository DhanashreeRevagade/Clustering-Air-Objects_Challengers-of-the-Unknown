from minisom import MiniSom
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from pylab import plot,axis,show,pcolor,colorbar,bone

def centroid_comparision(actual, cluster_centroids):
    labels = {}
    for i, cc in cluster_centroids.iteritems():
        dif = [abs(cc - ac) for ac in actual]
        label = dif.index(min(dif))
        labels[i] = label
    return labels

path = 'data\\cluster_data.npy'
data =  np.load(path)
data = data.reshape((-1, 1000, 6))
data, label = data[:,:,:5], data[:,:,5]
label = label[:,0]

w,_,_ = data.shape
data = data[:,:,2:].reshape((w,3000))

scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

som = MiniSom(2,2, 3000, sigma=1, learning_rate=0.1) # initialization of 6x6 SOM
som.random_weights_init(data)

starting_weights = som.get_weights().copy()
som.train_random(data, 1000, verbose=True)
weights = som.get_weights().copy()

bone()
pcolor(som.distance_map().T) # distance map as background
colorbar()

# use different colors and markers for each label
markers = ['o','s']
colors = ['r','y']

air_clusters = [[0,0],[0,0]]
drone_clusters = [[0,0],[0,0]]
for cnt,xx in enumerate(data):
    w = som.winner(xx) # getting the winner
    # palce a marker on the winning position for the sample xx
    plot( w[0] + .5 , w[1] + .5 , markers [ list(map(int,label.tolist()))[cnt] ], markerfacecolor='None',
        markeredgecolor = colors[ list(map(int,label.tolist()))[cnt] ], markersize = 12, markeredgewidth = 2),axis([0,weights.shape[0],0, weights.shape[1]])
    x,y = w
    if cnt < 153:
        air_clusters[x][y]+= 1
    else:
        drone_clusters[x][y]+= 1

show()

win = som.win_map(data)
a= len(win[(0,0)])
b = len(win[(0,1)])
c = len(win[(1,0)])
d = len(win[(1,1)])

temp_weights = weights
scaler.inverse_transform(temp_weights.reshape(4,3000))
temp_weights = temp_weights.reshape(2,2,1000,3)
time = [i for i in range(0,10000,10)]

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(time, temp_weights[0,0,:,:1])
axs[0, 0].set_title(f'{a} cases: airplane:{air_clusters[0][0]}, drone:{drone_clusters[0][0]}')
axs[0, 1].plot(time, temp_weights[0,1,:,:1], 'tab:orange')
axs[0, 1].set_title(f'{b} cases: airplane:{air_clusters[0][1]}, drone:{drone_clusters[0][1]}')
axs[1, 0].plot(time, temp_weights[1,0,:,:1], 'tab:green')
axs[1, 0].set_title(f'{c} cases: airplane:{air_clusters[1][0]}, drone:{drone_clusters[1][0]}')
axs[1, 1].plot(time, temp_weights[1,1,:,:1], 'tab:red')
axs[1, 1].set_title(f'{d} cases: airplane:{air_clusters[1][1]}, drone:{drone_clusters[1][1]}')

plt.show()
# print(clusters)