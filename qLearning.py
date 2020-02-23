import numpy as np
import random
import string
from math import cos, asin, sqrt
from travellingSales import travelSalesMan
import copy

CAR_CAPACITY = 30
ROOT_NODE = {
    'lat': 13.72919,
    'lon': 100.77564
}
ALL_ORDERS = 50


# CAR_WIDTH = 150
# CAR_LENGTH = 180
# CAR_HEIGHT = 150


class Order:
    def __init__(self, index):
        self.id = self.randomString()
        self.coordinate = {
            'lat': random.uniform(13.5, 14),
            'lon': random.uniform(100, 100.6)
        }
        self.width = random.uniform(1, 50)
        self.height = random.uniform(1, 50)
        self.length = random.uniform(1, 100)
        self.carNumber = 0
        self.deliveryOrder = 0
        # self.index = index

    def randomString(self, stringLength=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))


class Car:
    def __init__(self, carIndex):
        # self.carIndex = carIndex
        self.orders = []
        # self.deliveryStatus = False
        # self.isFull = False

    def addOrder(self, order):
        self.orders.append(order)

    def takeOutOrder(self, orderIndex):
        self.orders.pop(orderIndex)


class Simulator:
    def __init__(self, init_car=None):
        if init_car:
            self.init_car = copy.deepcopy(init_car)
            self.cars = copy.deepcopy(init_car)
        self.allCarsCanDeliveried = False

    def reset(self):
        self.cars = copy.deepcopy(self.init_car)
        self.allCarsCanDeliveried = False
        print('reset simulator')

    def findFarthestOrder(self, orders):
        max_distance = 0
        for i, order in enumerate(orders):
            distance = self.computeDistance(ROOT_NODE['lat'], ROOT_NODE['lon'], order.coordinate['lat'],
                                            order.coordinate['lon'])
            if distance > max_distance:
                max_distance = distance
                max_distance_order_index = i
        print('max distance is ', max_distance, 'order index is ', max_distance_order_index)
        return max_distance_order_index

    def computeDistance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295  # Pi/180
        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
            cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))  # 2*R*asin... as km.

    def moveOrder(self, origin_car_index, destination_car_index, order_index):
        origin_car_orders = self.cars[origin_car_index].orders
        destination_car_orders = self.cars[destination_car_index].orders
        selected_order = origin_car_orders.pop(order_index)
        destination_car_orders.append(selected_order)
        print('moved', order_index, 'from car ', origin_car_index, 'to car ', destination_car_index)

    def getMaxMinCarIndex(self):
        max_orders, car_index_max, car_index_min = 0, 0, 0
        min_orders = CAR_CAPACITY
        for i, car in enumerate(self.cars):
            number_of_order = len(car.orders)
            if number_of_order > max_orders:
                car_index_max = i
                max_orders = number_of_order

            if number_of_order <= min_orders:
                car_index_min = i
                min_orders = number_of_order
        return car_index_max, car_index_min

    def isFull(self):
        number_of_cars = len(self.cars)
        check_full = 0
        for car in self.cars:
            if len(car.orders) >= CAR_CAPACITY:
                check_full += 1
        if check_full == number_of_cars:
            return True
        else:
            return False

    # def isDelivery(self):
    #     for car in self.cars:
    #         print('orders ', car.orders)
    #         total_distance = travelSalesMan(car.orders)
    #         if total_distance > 500:
    #             print('tatal distance : ', total_distance, 'can not delivery')
    #             return False
    #         else:
    #             print('tatal distance : ', total_distance, 'can delivery')
    #             return True

    def isDelivery(self):
        capacity = 0
        for car in self.cars:
            for order in car.orders:
                volume = order.width * order.height * order.length
                capacity = capacity + volume
            if capacity > CAR_CAPACITY:
                print('total capacity : ', capacity, 'can not delivery')
                return False
            else:
                print('total capacity : ', capacity, 'can delivery')
                return True

    def getState(self):
        if self.isFull() == True:
            if self.isDelivery() == True:
                state = '01'
            else:
                state = '00'
        else:
            if self.isDelivery() == True:
                state = '11'
            else:
                state = '10'
        return state

    def takeAction(self, action):
        if action == 0:
            reward = self.addCar()
            new_state = self.getState()
            print('action : add car')
            print('reward : ', reward)
            print('current state : ', new_state)
            print('#################################################################')
        if action == 1:
            reward = self.moveMostOrdersToLeastOrders()
            new_state = self.getState()
            print('action : most orders ==> least orders')
            print('reward : ', reward)
            print('current state : ', new_state)
            print('#################################################################')
        if action == 2:
            reward = self.moveMostTotalDistanceToLeastTotalDistance()
            new_state = self.getState()
            print('action : most total distance ==> least total distance')
            print('reward : ', reward)
            print('current state : ', new_state)
            print('#################################################################')
        if action == 3:
            reward = self.moveFarthestToNearestCar()
            new_state = self.getState()
            print('action : farthest ==> nearest')
            print('reward : ', reward)
            print('current state : ', new_state)
            print('#################################################################')

        return reward, new_state

    # Action
    def addCar(self):
        self.cars.append(Car(len(self.cars)))
        self.moveMostOrdersToLeastOrders()
        return -1

    def moveMostOrdersToLeastOrders(self):
        if self.isFull() == False:
            car_index_max, car_index_min = self.getMaxMinCarIndex()

            farthest_order = self.findFarthestOrder(self.cars[car_index_max].orders)
            self.moveOrder(car_index_max, car_index_min, farthest_order)
        return 2

    def moveMostTotalDistanceToLeastTotalDistance(self):
        if self.isFull() == False:
            max_distance, car_index_max, car_index_min = 0, 0, 0
            min_diatance = 10000
            for i, car in enumerate(self.cars):
                best_distance = travelSalesMan(car.orders)
                if best_distance > max_distance:
                    car_index_max = i
                    max_distance = best_distance

                if best_distance < min_diatance:
                    car_index_min = i
                    min_diatance = best_distance

            farthest_order = self.findFarthestOrder(self.cars[car_index_max].orders)
            self.moveOrder(car_index_max, car_index_min, farthest_order)
        return 2

    def moveFarthestToNearestCar(self):
        if self.isFull() == False:
            car_index, x = self.getMaxMinCarIndex()
            farthest_order_index = self.findFarthestOrder(self.cars[car_index].orders)
            farthest_order = self.cars[car_index].orders[farthest_order_index]
            min_distance = 100000
            min_distance_order_index, min_distance_car_index = 0, 0
            for i, car in enumerate(self.cars):
                if i != car_index:
                    for j, order in enumerate(car.orders):
                        distance = self.computeDistance(farthest_order.coordinate['lat'],
                                                        farthest_order.coordinate['lon'], order.coordinate['lat'],
                                                        order.coordinate['lon'])
                        print('distance : ', distance, 'min distance : ', min_distance)
                        if distance < min_distance:
                            min_distance_car_index = i
                            min_distance = distance
            self.moveOrder(car_index, min_distance_car_index, farthest_order_index)
        return 3
    # def swapTwoNearestOrder(self):
    #     for i in self.cars:
    #         for j in self.cars:
    #             for order in i.orders:
    #                 distance = self.computeDistance(order.coordinate['lat'], farthest_order.coordinate['lon'], order.coordinate['lat'], order.coordinate['lon'])
    #     return 3


class QLearning:
    def __init__(self, learning_rate):
        self.learning_rate = 0.1
        self.gamma = 0.89
        self.epsilon = 0.2
        self.state_value = []

    def update_value(self):
        self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])


if __name__ == "__main__":
    car = Car(0)
    for i in range(ALL_ORDERS):
        car.addOrder(Order(i))
    s1 = Simulator(init_car=[car])
