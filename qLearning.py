import numpy as np
import random
import string
from IPython.display import clear_output
from math import cos, asin, sqrt
from travellingSales import travelSalesMan
import copy

CAR_CAPACITY = 30
ROOT_NODE = {
    'lat': 13.72919,
    'lon': 100.77564
}
ALL_ORDERS = 300


CAR_WIDTH = 150
CAR_LENGTH = 180
CAR_HEIGHT = 150


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
        # print('max distance is ', max_distance, 'order index is ', max_distance_order_index)
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
        # print('moved', order_index, 'from car ', origin_car_index, 'to car ', destination_car_index)

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
    #         if total_distance > 20:
    #             print('tatal distance : ', total_distance, 'can not delivery')
    #             return False
    #         else:
    #             print('tatal distance : ', total_distance, 'can delivery')
    #             return True

    def isDelivery(self):
        capacity = 0
        car_capacity = CAR_WIDTH * CAR_HEIGHT * CAR_LENGTH
        for car in self.cars:
            for order in car.orders:
                volume = order.width * order.height * order.length
                capacity = capacity + volume
            if capacity > car_capacity:
                # print('total capacity : ', capacity, 'can not delivery')
                return False
            else:
                # print('total capacity : ', capacity, 'can delivery')
                return True

    def getState(self):
        if self.isFull() == True:
            if self.isDelivery() == True:
                state = 1
            else:
                state = 0
        else:
            if self.isDelivery() == True:
                state = 3
            else:
                state = 2
        return state

    def takeAction(self, action):
        if action == 0:
            reward = self.addCar()
            new_state = self.getState()
            # print('action : add car')
            # print('reward : ', reward)
            # print('current state : ', new_state)
            # print('#################################################################')
        if action == 1:
            reward = self.moveMostOrdersToLeastOrders()
            new_state = self.getState()
            # print('action : most orders ==> least orders')
            # print('reward : ', reward)
            # print('current state : ', new_state)
            # print('#################################################################')
        if action == 2:
            reward = self.moveMostTotalDistanceToLeastTotalDistance()
            new_state = self.getState()
            # print('action : most total distance ==> least total distance')
            # print('reward : ', reward)
            # print('current state : ', new_state)
            # print('#################################################################')
        if action == 3:
            reward = self.moveFarthestToNearestCar()
            new_state = self.getState()
            # print('action : farthest ==> nearest')
            # print('reward : ', reward)
            # print('current state : ', new_state)
            # print('#################################################################')

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
            reward = 2
        else:
            reward = -100
        return reward

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
            reward = 2
        else:
            reward = -100
        return reward

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
            reward = 3
        else:
            reward = -100
        return reward
    # def swapTwoNearestOrder(self):
    #     for i in self.cars:
    #         for j in self.cars:
    #             for order in i.orders:
    #                 distance = self.computeDistance(order.coordinate['lat'], farthest_order.coordinate['lon'], order.coordinate['lat'], order.coordinate['lon'])
    #     return 3


class QLearning:
    def __init__(self, learning_rate=0.1):
        self.alpha = learning_rate
        self.gamma = 0.89
        self.epsilon = 0.2
        self.state_value = []

        self.all_epochs = []
        self.all_penalties = []
        self.q_table = np.zeros((4, 4))
        car = Car(0)
        for i in range(ALL_ORDERS):
            car.addOrder(Order(i))
        self.env = Simulator(init_car=[car])

    def update_value(self):
        pass

    def training(self):
        for i in range(1, 10):
            print('train : ', i)
            self.env.reset()
            state = self.env.getState()

            epochs, penalties, reward, = 0, 0, 0
            done = False

            while not done:
                if random.uniform(0, 1) < self.epsilon:
                    action = random.randint(0, 3)
                else:
                    action = np.argmax(self.q_table[state])  # Exploit learned values

                print(f'Current Action : {action} state : {state}')
                print(f'Q table {self.q_table}')

                reward, next_state = self.env.takeAction(action)

                print(f'Next State {next_state}')

                old_value = self.q_table[state, action]
                next_max = np.max(self.q_table[next_state])

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state, action] = new_value

                if reward == -10:
                    penalties += 1

                state = next_state
                epochs += 1

                if state == 1 or state == 3:
                    done = True

            if i % 100 == 0:
                clear_output(wait=True)
                print(f"Episode: {i}")

        print("Training finished.\n")


if __name__ == "__main__":
    agent = QLearning()
    agent.training()

