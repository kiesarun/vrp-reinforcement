import numpy as np
import random
import string
from IPython.display import clear_output
from math import cos, asin, sqrt
from travellingSales import two_opt
import copy

CAR_CAPACITY = 30
ROOT_NODE = {
    'lat': 13.72919,
    'lon': 100.77564
}
ALL_ORDERS = 300


CAR_WIDTH = 150
CAR_LENGTH = 200
CAR_HEIGHT = 180
CAR_VOLUME = CAR_LENGTH * CAR_HEIGHT * CAR_WIDTH


def compute_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
        cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin... as km.

class Order:
    def __init__(self):
        self.id = self.random_string()
        self.coordinate = {
            'lat': random.uniform(13.6, 13.9),
            'lon': random.uniform(100.1, 100.5)
        }
        self.width = random.uniform(10, 80)
        self.height = random.uniform(2, 100)
        self.length = random.uniform(15, 100)
        self.carNumber = 0
        self.deliveryOrder = 0
        # self.index = index

    def random_string(self, string_length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))


class Car:
    def __init__(self):
        # self.carIndex = carIndex
        self.orders = []
        self.distance = 1000
        self.centroid = {
            'lat': 0,
            'lon': 0
        }
        # self.deliveryStatus = False
        # self.isFull = False

    def add_order(self, order):
        self.orders.append(order)

    def take_out_order(self, order_index):
        self.orders.pop(order_index)

    def set_distance(self):
        self.distance = two_opt(self.orders, 0.1)

    def set_centroid(self):
        number_of_orders = len(self.orders)
        lat = 0
        lon = 0
        for order in self.orders:
            lat = lat + order.coordinate['lat']
            lon = lon + order.coordinate['lon']
        if number_of_orders > 0:
            self.centroid['lat'] = lat / number_of_orders
            self.centroid['lon'] = lon / number_of_orders


class Simulator:
    def __init__(self, init_car=None):
        if init_car:
            self.init_car = copy.deepcopy(init_car)
            self.cars = copy.deepcopy(init_car)
        self.all_cars_can_deliveried = False

    def reset(self):
        self.cars = copy.deepcopy(self.init_car)
        self.all_cars_can_deliveried = False
        print('reset simulator')

    def find_farthest_order(self, car_index):
        farthest_distance = 0
        farthest_distance_order_index = 0
        for i, order in enumerate(self.cars[car_index].orders):
            distance = compute_distance(self.cars[car_index].centroid['lat'], self.cars[car_index].centroid['lon'], order.coordinate['lat'],
                                             order.coordinate['lon'])
            if distance > farthest_distance:
                farthest_distance = distance
                farthest_distance_order_index = i
        # print('max distance is ', max_distance, 'order index is ', max_distance_order_index)
        return farthest_distance_order_index

    def find_nearest_car_and_order(self, lat, lon, car_index):
        min_distance = 1000
        nearest_car = 0
        nearest_order = 0
        for i, car in enumerate(self.cars):
            if i != car_index:
                if len(car.orders) > 0:
                    for j, order in enumerate(car.orders):
                        distance = compute_distance(lat, lon, order.coordinate['lat'], order.coordinate['lon'])

                        if distance < min_distance:
                            min_distance = distance
                            nearest_order = j
                            nearest_car = i
        return nearest_car, nearest_order

    def move_order(self, origin_car_index, destination_car_index, order_index):
        if len(self.cars[origin_car_index].orders) > 0:
            origin_car_orders = self.cars[origin_car_index].orders
            destination_car_orders = self.cars[destination_car_index].orders
            selected_order = origin_car_orders.pop(order_index)
            destination_car_orders.append(selected_order)
            self.set_distance_and_centroid_all_cars()
            # print('moved', order_index, 'from car ', origin_car_index, 'to car ', destination_car_index)

    def get_max_order_car_index(self):
        max_orders, car_index= 0, 0
        for i, car in enumerate(self.cars):
            number_of_order = len(car.orders)
            if number_of_order > max_orders:
                car_index = i
                max_orders = number_of_order
        return car_index

    def get_min_order_car_index(self):
        car_index = 0
        min_orders = CAR_CAPACITY
        for i, car in enumerate(self.cars):
            number_of_order = len(car.orders)
            if number_of_order <= min_orders:
                car_index = i
                min_orders = number_of_order
        return car_index

    def set_distance_and_centroid_all_cars(self):
        if len(self.cars) == 1:
            self.cars[0].distance = 1000
            self.cars[0].set_centroid()
        else:
            for car in self.cars:
                if len(car.orders) > ALL_ORDERS / 1.5:
                    car.set_centroid()
                else:
                    car.set_distance()
                    car.set_centroid()

    def get_min_volume_order(self):
        min_volume = CAR_VOLUME
        order_id = 0
        car_id = 0
        order_volume = 0
        for i, car in enumerate(self.cars):
            for i, order in enumerate(car.orders):
                order_volume = order.width * order.height * order.length
                if order_volume < min_volume:
                    min_volume = order_volume
                    order_id = i
                    car_id = i
        return order_volume, order_id, car_id

    # def get_cars_volume(self):
    #     cars_volume = []
    #     for car in self.cars:
    #         car_volume = 0
    #         for order in car.orders:
    #             order_volume = order.length * order.height * order.width
    #             car_volume = car_volume + order_volume
    #         cars_volume.append(car_volume)
    #     return cars_volume

    def is_full(self, car_index):
        car_volume = 0
        for order in self.cars[car_index].orders:
            order_volume = order.length * order.height * order.width
            car_volume = car_volume + order_volume
            if car_volume >= CAR_VOLUME:
                return True
            else:
                return False

    def is_full_all_cars(self):
        is_full = 0
        is_excess_volume = 0
        number_of_cars = len(self.cars)
        for car in self.cars:
            car_volume = 0
            for order in car.orders:
                order_volume = order.length * order.height * order.width
                car_volume = car_volume + order_volume
            if car_volume >= CAR_VOLUME:
                is_full = is_full + 1
                is_excess_volume = is_excess_volume + 1
            else:
                car_space = CAR_VOLUME - car_volume
                min_order_volume, min_order_id, min_order_car = self.get_min_volume_order()
                if car_space < min_order_volume:
                    is_full = is_full + 1
        if is_full < number_of_cars:
            if is_excess_volume < number_of_cars:
                state = '11'
            elif is_excess_volume == 0:
                state = '10'
            else:
                state = '12'
        elif is_full == 0:
            state = '00'
        else:
            if is_excess_volume < number_of_cars:
                state = '21'
            elif is_excess_volume == 0:
                state = '20'
            else:
                state = '22'
        return state

        # else:
        #     if is_excess_volume < 0:
        #         return True, False
        #     else:
        #         return True, True

    def is_delivery_all_car(self):
        is_delivery_check = 0
        for i, car in enumerate(self.cars):
            number_of_order = len(car.orders)
            is_delivery, total_distance = self.is_delivery(i)
            if is_delivery:
                is_delivery_check = is_delivery_check + 1

        if is_delivery_check < len(self.cars):
            state = '1'
        elif is_delivery == 0:
            state = '0'
        else:
            state = '2'
        return state

    def is_delivery(self, car_index):
        is_delivery = 0
        number_of_order = len(self.cars[car_index].orders)
        total_distance = self.cars[car_index].distance
        if 240 >= total_distance > 100:
            print(number_of_order,'order', 'tatal distance : ', total_distance, 'car', car_index, 'can delivery')
            return True, total_distance
        else:
            print(number_of_order,'order', 'tatal distance : ', total_distance, 'car', car_index, 'can not delivery')
            return False, total_distance

    def get_average_distance(self):
        distance = 0
        for car in self.cars:
            distance = distance + car.distance
        average_distance = distance / len(self.cars)
        return average_distance, distance

    def get_state(self):
        is_full_state = self.is_full_all_cars()
        is_delivery_state = self.is_delivery_all_car()
        state_string = is_full_state + is_delivery_state
        if state_string == '211':
            state = 0
        if state_string == '201':
            state = 1
        if state_string == '221':
            state = 2
        if state_string == '210':
            state = 3
        if state_string == '200':
            state = 4
        if state_string == '220':
            state = 5
        if state_string == '212':
            state = 6
        if state_string == '202':
            state = 7
        if state_string == '222':
            state = 8
        if state_string == '111':
            state = 9
        if state_string == '101':
            state = 10
        if state_string == '112':
            state = 11
        if state_string == '110':
            state = 12
        if state_string == '100':
            state = 13
        if state_string == '102':
            state = 14
        if state_string == '121':
            state = 15
        if state_string == '120':
            state = 16
        if state_string == '122':
            state = 17
        if state_string == '001':
            state = 18
        if state_string == '000':
            state = 19
        if state_string == '002':
            state = 20
        return state

    def take_action(self, action):
        if action == 0:
            reward = self.add_car()
            new_state = self.get_state()
        if action == 1:
            reward = self.move_farthest_order_from_most_orders_to_nearest_car()
            new_state = self.get_state()
        if action == 2:
            reward = self.move_nearest_order_of_least_order_car()
            new_state = self.get_state()
        if action == 3:
            reward = self.move_nearest_order_of_car_that_not_full_and_can_delivery()
            new_state = self.get_state()
        if action == 4:
            reward = self.move_most_distance_to_nearest()
            new_state = self.get_state()
        if action == 5:
            reward = self.delete_car()
            new_state = self.get_state()

        print('action : ', action)
        print('reward : ', reward)
        print('new state : ', new_state)
        print('#################################################################')

        return reward, new_state

    # New ACtion
    def add_car(self):
        is_full = self.is_full_all_cars()
        self.cars.append(Car())
        average_distance, all_distance= self.get_average_distance()
        if is_full == '21' or is_full == '20' or is_full == '22':
            # reward = -average_distance + 100
            reward = (- average_distance * 2) - all_distance + 1000
        else:
            # reward = -self.get_average_distance() - 100
            reward = (- average_distance * 2) - all_distance - 1000
        return reward

    def move_farthest_order_from_most_orders_to_nearest_car(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            most_order_car = self.get_max_order_car_index()
            farthest_order_index = self.find_farthest_order(most_order_car)
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[most_order_car].orders[farthest_order_index].coordinate['lat'], self.cars[most_order_car].orders[farthest_order_index].coordinate['lon'], most_order_car)
            self.move_order(most_order_car, nearest_car, farthest_order_index)
            avg_distance, all_distance = self.get_average_distance()
            reward = ((previous_avg_distance - avg_distance) * 2) + ((previous_all_distance - all_distance)* 2)
        else:
            reward = -1000
        return reward

    def move_nearest_order_of_least_order_car(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            least_order_car = self.get_min_order_car_index()
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[least_order_car].centroid['lat'], self.cars[least_order_car].centroid['lon'], least_order_car)
            self.move_order(nearest_car, least_order_car, nearest_order)
            avg_distance, all_distance = self.get_average_distance()
            reward = ((previous_avg_distance - avg_distance) * 2) + ((previous_all_distance - all_distance)* 2)
        else:
            reward = -1000
        return reward

    def move_nearest_order_of_car_that_not_full_and_can_delivery(self):
        # is_full_all_cars, is_excess = self.is_full_all_cars()
        # if not is_full_all_cars:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            min_order = 1000
            min_order_car_index = 0
            for i, car in enumerate(self.cars):
                is_delivery, total_distance = self.is_delivery(i)
                is_full = self.is_full(i)
                if is_delivery and not is_full:
                    number_of_order = len(car.orders)
                    if number_of_order < min_order:
                        min_order = number_of_order
                        min_order_car_index = i
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[min_order_car_index].centroid['lat'], self.cars[min_order_car_index].centroid['lon'], min_order_car_index)
            self.move_order(nearest_car, min_order_car_index, nearest_order)
            avg_distance, all_distance = self.get_average_distance()
            reward = ((previous_avg_distance - avg_distance) * 2) + ((previous_all_distance - all_distance)* 2)
        else:
            reward = -1000
        return reward

    def move_most_distance_to_nearest(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            max_distance, car_index_max = 0, 0
            for i, car in enumerate(self.cars):
                distance = car.distance
                if distance > max_distance:
                    car_index_max = i
                    max_distance = distance
            farthest_order = self.find_farthest_order(car_index_max)
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[car_index_max].centroid['lat'], self.cars[car_index_max].centroid['lon'], car_index_max)
            self.move_order(car_index_max, nearest_car, farthest_order)
            avg_distance, all_distance = self.get_average_distance()
            reward = ((previous_avg_distance - avg_distance) * 2) + ((previous_all_distance - all_distance)* 2)
        else:
            reward = -1000
        return reward

    def delete_car(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            average_distance, all_distance= self.get_average_distance()
            car_index = self.get_min_order_car_index()
            if len(self.cars[car_index].orders) > 0:
                for i, order in enumerate(self.cars[car_index].orders):
                    nearest_car, nearest_order = self.find_nearest_car_and_order(order.coordinate['lat'], order.coordinate['lon'], car_index)
                    self.cars[nearest_car].orders.append(order)
            self.cars.pop(car_index)
            self.set_distance_and_centroid_all_cars()
            reward = average_distance
        else:
            reward = -10000
        return reward



    # Old Action
    # def move_most_orders_to_least_orders(self):
    #     is_full, is_excess = self.is_full_all_cars()
    #     if not is_full:
    #         previous_distance = self.get_average_distance()
    #         car_index_max, car_index_min = self.get_max_min_car_index()
    #
    #         farthest_order = self.find_farthest_order(self.cars[car_index_max].orders)
    #         self.move_order(car_index_max, car_index_min, farthest_order)
    #         reward = previous_distance - self.get_average_distance()
    #     else:
    #         reward = -1000
    #     return reward
    #
    # def move_most_total_distance_to_least_total_distance(self):
    #     is_full, is_excess = self.is_full_all_cars()
    #     if not is_full:
    #         previous_distance = self.get_average_distance()
    #         max_distance, car_index_max, car_index_min = 0, 0, 0
    #         min_distance = 10000
    #         for i, car in enumerate(self.cars):
    #             # best_distance = two_opt(car.orders, 0.1)
    #             best_distance = car.distance
    #             if best_distance > max_distance:
    #                 car_index_max = i
    #                 max_distance = best_distance
    #
    #             if best_distance < min_distance:
    #                 car_index_min = i
    #                 min_distance = best_distance
    #
    #         farthest_order = self.find_farthest_order(self.cars[car_index_max].orders)
    #         self.move_order(car_index_max, car_index_min, farthest_order)
    #         reward = previous_distance - self.get_average_distance()
    #     else:
    #         reward = -1000
    #     return reward
    #
    # def move_farthest_to_nearest_car(self):
    #     is_full, is_excess = self.is_full_all_cars()
    #     if not is_full:
    #         previous_distance = self.get_average_distance()
    #         car_index, x = self.get_max_min_car_index()
    #         farthest_order_index = self.find_farthest_order(self.cars[car_index].orders)
    #         farthest_order = self.cars[car_index].orders[farthest_order_index]
    #         min_distance = 100000
    #         min_distance_order_index, min_distance_car_index = 0, 0
    #         for i, car in enumerate(self.cars):
    #             if i != car_index:
    #                 for j, order in enumerate(car.orders):
    #                     distance = compute_distance(farthest_order.coordinate['lat'],
    #                                                      farthest_order.coordinate['lon'], order.coordinate['lat'],
    #                                                      order.coordinate['lon'])
    #                     # print('distance : ', distance, 'min distance : ', min_distance)
    #                     if distance < min_distance:
    #                         min_distance_car_index = i
    #                         min_distance = distance
    #         self.move_order(car_index, min_distance_car_index, farthest_order_index)
    #         reward = previous_distance - self.get_average_distance()
    #     else:
    #         reward = -1000
    #     return reward
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
        self.epsilon = 0.5
        self.state_value = []

        self.all_epochs = []
        self.all_penalties = []
        self.q_table = np.zeros((21, 6))
        car = Car()
        for i in range(ALL_ORDERS):
            car.add_order(Order())
        car.set_centroid()
        self.env = Simulator(init_car=[car])

    def save_model(self):
        np.save(open('qtable.np', 'wb'), self.q_table)

    def load_model(self):
        self.q_table = np.load(open('qtable.np', 'rb'))

    def training(self):
        for i in range(1, 100000):
            self.env.reset()
            state = self.env.get_state()

            epochs, penalties, reward, = 0, 0, 0
            done = False

            while not done:
                if random.uniform(0, 1) < self.epsilon:
                    action = random.randint(0, 5)
                else:
                    action = np.argmax(self.q_table[state])  # Exploit learned values

                print(f'Current Action : {action} state : {state}')
                # print(f'Q table {self.q_table}')
                print('Q table')
                print(self.q_table)

                reward, next_state = self.env.take_action(action)

                print(f'Next State {next_state}')

                old_value = self.q_table[state, action]
                next_max = np.max(self.q_table[next_state])

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state, action] = new_value

                self.save_model()

                if reward == -10:
                    penalties += 1

                state = next_state
                epochs += 1

                if state == 7 or state == 16 or state == 20:
                    done = True

            self.epsilon = self.epsilon - 0.01

            if self.epsilon < 0.2:
                self.epsilon = 0.2

            if i % 100 == 0:
                clear_output(wait=True)
                print(f"Episode: {i}")

        print("Training finished.\n")
        print(f'Q table {self.q_table}')

    def predict(self):
        state = self.env.get_state()
        done = False

            while not done:
                action = np.argmax(self.q_table[state])  # Exploit learned values
                reward, next_state = self.env.take_action(action)

                print(next_state)
                print(self.env.cars)

                if state == 4 or state == 8:
                    done = True

if __name__ == "__main__":
    agent = QLearning()
    # agent.load_model()
    agent.training()

    # car = Car()
    # for i in range(ALL_ORDERS):
    #     car.add_order(Order())
    # car.set_centroid()
    # s = Simulator(init_car=[car])


