import numpy as np
from math import cos, asin, sqrt

CAR_CAPACITY = 10
ROOT_NODE = [13.72919, 100.77564]
# CAR_WIDTH = 150
# CAR_LENGTH = 180
# CAR_HEIGHT = 150

class State:
    def __init__(self, orders):
        self.cars = []
        self.cars.append(orders)
        self.finish = False

    # def __init__(self):
    #     self.cars = []
    #     self.cars.append(np.zeros(CAR_CAPACITY, dtype=int))
    #     self.finish = False

    def carDeliverable(self):
        if self.cars[0].count() <= CAR_CAPACITY:
            self.finish = True 
        else:
            self.finish = False

    def distanceBetweenCoordinate(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295     #Pi/180
        a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a)) #2*R*asin... as km.

    def selectOrder(self):
        max = 0
        selected_order = ''
        for order in self.cars[0]:
            dist = self.distanceBetweenCoordinate(ROOT_NODE[0], ROOT_NODE[1], order['coordinates'][0], order['coordinates'][1])
            order['distanceFromRoot'] = dist
            if dist > max:
                max = dist
                selected_order = order
        return selected_order
            
    def takeAction(self):
        while (True):
            self.carDeliverable()
            if (self.finish == False):
                select_order = self.selectOrder()
                print(type(self.cars[0]))
            else:
                break

            
# if __name__ == "__main__":
#     s1 = State() 
#     distance = s1.distanceFromRoot(13.72919, 100.77564, 13.7251, 100.77039)