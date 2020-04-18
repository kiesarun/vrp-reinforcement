import mlrose
from math import cos, asin, sqrt
import numpy as np


def computeDistance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
        cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin... as km.


def path_distance(routes, cities):
    distances = 0

    for r in range(len(routes)):
        currentNode = cities[routes[r - 1]]
        nextNode = cities[routes[r]]

        c_dist = computeDistance(currentNode[0], currentNode[1], nextNode[0], nextNode[1])

        distances += c_dist

    return distances


# Reverse the order of all elements from element i to element k in array r.
two_opt_swap = lambda r, i, k: np.concatenate((r[0:i], r[k:-len(r) + i - 1:-1], r[k + 1:len(r)]))


def two_opt(orders, improvement_threshold, solution='qlearning'):  # 2-opt Algorithm adapted from https://en.wikipedia.org/wiki/2-opt
    if len(orders) <= 1:
        return 0, []
    cities = []
    for order in orders:
        cities.append((order.coordinate['lat'], order.coordinate['lon']))
    number_of_orders = len(cities)
    cities = np.array(cities)
    route = np.arange(cities.shape[0])
    improvement_factor = 1
    best_distance = path_distance(route, cities)
    # print(f'best distance: {best_distance}')
    while improvement_factor > improvement_threshold:
        distance_to_beat = best_distance
        for swap_first in range(1, len(route) - 2):
            for swap_last in range(swap_first + 1, len(route)):
                new_route = two_opt_swap(route, swap_first, swap_last)
                new_distance = path_distance(new_route, cities)
                # print(f'new distance: {new_distance}')
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
        if distance_to_beat != 0:
            improvement_factor = 1 - best_distance / distance_to_beat

    return best_distance, route
