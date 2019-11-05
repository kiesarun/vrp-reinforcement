from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


coordinates = np.array([[10,10],[20,20],[13,13],[23,23],[30,30],[33,33]])

kmeans = KMeans(n_clusters=3, random_state=0).fit(coordinates)

print(kmeans.labels_)

y = [1, 2, 1, 2, 0, 0]

neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(coordinates, y)

print(neigh.predict([[15,15]]))

