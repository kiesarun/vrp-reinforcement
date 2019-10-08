from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt
import numpy as np

def cluster(coor):

    # coordinates = np.array([[10, 5], [20, 15], [15, 10], [30, 20], [30, 10], [20, 20]])
    coordinates = np.array(coor)

    x = coordinates[:, 0]
    y = coordinates[:, 1]

    print(x)
    print(y)

    kmeans = KMeans(n_clusters=4, random_state=0).fit(coordinates)

    # print(kmeans.labels_)

    clustered = kmeans.predict(coordinates)

    # neigh = KNeighborsClassifier(n_neighbors=3)
    # neigh.fit(coordinates, clustered)

    print(clustered)

    colors = ("red", "green", "blue","coral")

    _color = [colors[cluster] for cluster in clustered]

    # print(_color)

    # print(neigh.predict([[15,15]]))

    area = np.pi * 3

    # Plot
    plt.scatter(x, y, s=area, c=_color, alpha=0.5)

    plt.title('Scatter plot pythonspot.com')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    return
