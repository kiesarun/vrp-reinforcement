import numpy as np
import random
import string
import winsound
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


CAR_WIDTH = 152
CAR_LENGTH = 230
CAR_HEIGHT = 200
CAR_VOLUME = CAR_LENGTH * CAR_HEIGHT * CAR_WIDTH

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 3000  # Set Duration To 1000 ms == 1 second


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
        self.width = random.uniform(10, 50)
        self.height = random.uniform(2, 80)
        self.length = random.uniform(15, 80)
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
        self.distance = 0
        self.centroid = {
            'lat': 0,
            'lon': 0
        }
        self.volume = 0
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

    def set_volume(self):
        volume = 0
        for order in self.orders:
            volume = volume + (order.width * order.height * order.length)


class Simulator:
    def __init__(self, init_car=None):
        if init_car:
            self.init_car = copy.deepcopy(init_car)
            self.cars = copy.deepcopy(init_car)
        self.can_delivery_cars = 0
        # self.not_full_cars = 0
        self.not_excess_cars = 0

    def reset(self):
        self.cars = copy.deepcopy(self.init_car)
        self.can_delivery_cars = 0
        # self.not_full_cars = 0
        self.not_excess_cars = 0
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
        min_centroid_distance = 1000
        nearest_car = 0
        nearest_order = 0
        if len(self.cars) > 1:
            for i, car in enumerate(self.cars):
                if i != car_index:
                    centroid_distance = compute_distance(lat, lon, car.centroid['lat'], car.centroid['lon'])
                    if centroid_distance < min_centroid_distance:
                        min_centroid_distance = centroid_distance
                        nearest_car = i

        if len(self.cars[nearest_car].orders) > 0:
            for j, order in enumerate(self.cars[nearest_car].orders):
                distance = compute_distance(lat, lon, order.coordinate['lat'], order.coordinate['lon'])

                if distance < min_distance:
                    min_distance = distance
                    nearest_order = j
        return nearest_car, nearest_order

    def move_order(self, origin_car_index, destination_car_index, order_index):
        if len(self.cars[origin_car_index].orders) > 0:
            origin_car_orders = self.cars[origin_car_index].orders
            destination_car_orders = self.cars[destination_car_index].orders
            selected_order = origin_car_orders.pop(order_index)
            destination_car_orders.append(selected_order)
            self.set_distance_and_centroid_and_volume(origin_car_index)
            self.set_distance_and_centroid_and_volume(destination_car_index)
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

    def set_distance_and_centroid_and_volume(self, car_index):
        if len(self.cars[car_index].orders) < ALL_ORDERS / 1.5:
            self.cars[car_index].set_distance()
        else:
            self.cars[car_index].distance = 1000
        self.cars[car_index].set_centroid()
        self.cars[car_index].set_volume()


    def set_distance_and_centroid_and_volume_all_cars(self):
        if len(self.cars) == 1:
            self.cars[0].distance = 1000
            self.cars[0].set_centroid()
            self.cars[0].set_volume()
        else:
            for car in self.cars:
                if len(car.orders) > ALL_ORDERS / 1.5:
                    car.distance = 1000
                else:
                    car.set_distance()
                car.set_centroid()
                car.set_volume()

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

    def get_avg_volume(self):
        volume = 0
        for car in self.cars:
            volume = volume + car.volume
        return volume / len(self.cars)

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
        # is_full = 0
        is_excess_volume = 0
        number_of_cars = len(self.cars)
        print('CAR VOLUME', CAR_VOLUME)
        for i, car in enumerate(self.cars):
            car_volume = 0
            for order in car.orders:
                order_volume = order.length * order.height * order.width
                car_volume = car_volume + order_volume
            if car_volume >= CAR_VOLUME:
                is_excess_volume = is_excess_volume + 1
                print('car', i, 'volume: ', car_volume, 'FULL')
            else:
                print('car', i, 'volume: ', car_volume)
        if is_excess_volume == 0:
            state = '0'
        elif is_excess_volume < len(self.cars):
            state = '1'
        else:
            state = '2'
        # if is_full == 0:
        #     state = '00'
        # elif is_full < number_of_cars:
        #     if is_excess_volume == 0:
        #         state = '10'
        #     elif is_excess_volume < number_of_cars:
        #         state = '11'
        #     else:
        #         state = '12'
        # else:
        #     if is_excess_volume == 0 :
        #         state = '20'
        #     elif is_excess_volume < number_of_cars:
        #         state = '21'
        #     else:
        #         state = '22'
        # self.not_full_cars = number_of_cars - is_full
        self.not_excess_cars = number_of_cars - is_excess_volume
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
            is_delivery= self.is_delivery(i)
            if is_delivery:
                is_delivery_check = is_delivery_check + 1

        if is_delivery_check == 0:
            state = '0'
        elif is_delivery_check < len(self.cars):
            state = '1'
        else:
            state = '2'
        self.can_delivery_cars = is_delivery_check
        return state

    def is_delivery(self, car_index):
        # is_delivery = 0
        number_of_order = len(self.cars[car_index].orders)
        total_distance = self.cars[car_index].distance
        if 240 >= total_distance >= 50:
            print(number_of_order,'order', 'tatal distance : ', total_distance, 'car', car_index, 'can delivery')
            return True
        else:
            print(number_of_order,'order', 'tatal distance : ', total_distance, 'car', car_index)
            return False

    def get_finish_cars(self):
        finish_cars = 0
        for i, car in enumerate(self.cars):
            if not self.is_full(i) and self.is_delivery(i):
                finish_cars = finish_cars + 1
        return finish_cars

    def get_average_distance(self):
        distance = 0
        for car in self.cars:
            distance = distance + car.distance
        average_distance = distance / len(self.cars)
        return average_distance, distance

    def get_state(self):
        is_full_state = self.is_full_all_cars()
        is_delivery_state = self.is_delivery_all_car()
        state_string = is_delivery_state + is_full_state
        if state_string == '00':
            state = 2
        elif state_string == '01':
            state = 1
        elif state_string == '02':
            state = 0
        elif state_string == '10':
            state = 5
        elif state_string == '11':
            state = 4
        elif state_string == '12':
            state = 3
        elif state_string == '20':
            state = 8
        elif state_string == '21':
            state = 7
        else:
            state = 6
        return state

    def take_action(self, action):
        if action == 0:
            reward = self.add_car()
        elif action == 1:
            reward = self.move_farthest_order_from_most_orders_to_nearest_car()
        elif action == 2:
            reward = self.move_nearest_order_of_least_order_car()
        elif action == 3:
            reward = self.move_nearest_order_of_car_that_not_full_and_can_delivery()
        elif action == 4:
            reward = self.move_most_distance_to_nearest()
        elif action == 5:
            reward = self.move_from_full_car_and_can_not_delivery_to_nearest_car()
        else:
            reward = self.delete_car()

        new_state = self.get_state()
        reward = np.tanh(reward)

        # print('action : ', action)
        # print('reward : ', reward)
        # print('new state : ', new_state)
        # print('#################################################################')

        return reward, new_state

    # New ACtion
    def add_car(self):
        is_full_state = self.is_full_all_cars()
        is_delivery = self.is_delivery_all_car()
        previous_avg_distance, previous_all_distance = self.get_average_distance()
        previous_avg_volume = self.get_avg_volume()
        self.cars.append(Car())
        new_car = len(self.cars) - 1
        average_distance, all_distance = self.get_average_distance()
        most_order_car = self.get_max_order_car_index()
        farthest_order_index = self.find_farthest_order(most_order_car)
        self.move_order(most_order_car, new_car, farthest_order_index)
        current_volume = self.get_avg_volume()
        if is_full_state == '2' or is_delivery != '2':
            number_of_cars = len(self.cars)
            finish_cars = self.get_finish_cars()
            # reward = - ((all_distance - previous_all_distance) * (cant_delivery_car + excess_cars + 1)) - 100
            # reward = - ((all_distance - previous_all_distance) * (cant_delivery_car + 1)) + ((current_volume - previous_avg_volume) * (excess_cars + 1)) - 100
            reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * finish_cars - 50
        else:
            reward = -10000
        return reward

    def move_farthest_order_from_most_orders_to_nearest_car(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            previous_avg_volume = self.get_avg_volume()
            most_order_car = self.get_max_order_car_index()
            farthest_order_index = self.find_farthest_order(most_order_car)
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[most_order_car].orders[farthest_order_index].coordinate['lat'], self.cars[most_order_car].orders[farthest_order_index].coordinate['lon'], most_order_car)
            if nearest_car != most_order_car:
                self.move_order(most_order_car, nearest_car, farthest_order_index)
            avg_distance, all_distance = self.get_average_distance()
            current_volume = self.get_avg_volume()
            # reward = ((previous_all_distance - all_distance) * (self.can_delivery_cars + self.not_excess_cars + 1))
            finish_cars = self.get_finish_cars()
            if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * finish_cars
            else:
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * finish_cars - 100
        else:
            reward = -10000
        return reward

    def move_nearest_order_of_least_order_car(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            previous_avg_volume = self.get_avg_volume()
            least_order_car = self.get_min_order_car_index()
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[least_order_car].centroid['lat'], self.cars[least_order_car].centroid['lon'], least_order_car)
            if nearest_car != least_order_car:
                self.move_order(nearest_car, least_order_car, nearest_order)
            avg_distance, all_distance = self.get_average_distance()
            current_volume = self.get_avg_volume()
            # reward = ((previous_all_distance - all_distance) * (self.can_delivery_cars + self.not_excess_cars + 1))
            finish_cars = self.get_finish_cars()
            if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1)
            else:
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1) - 100
        else:
            reward = -10000
        return reward

    def move_nearest_order_of_car_that_not_full_and_can_delivery(self): # not check delivery anymore
        # is_full_all_cars, is_excess = self.is_full_all_cars()
        # if not is_full_all_cars:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            previous_avg_volume = self.get_avg_volume()
            min_order = 1000
            min_order_car_index = 0
            for i, car in enumerate(self.cars):
                # is_delivery = self.is_delivery(i)
                is_full = self.is_full(i)
                if not is_full:
                    number_of_order = len(car.orders)
                    if number_of_order < min_order:
                        min_order = number_of_order
                        min_order_car_index = i
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[min_order_car_index].centroid['lat'], self.cars[min_order_car_index].centroid['lon'], min_order_car_index)
            if nearest_car != min_order_car_index:
                self.move_order(nearest_car, min_order_car_index, nearest_order)
            avg_distance, all_distance = self.get_average_distance()
            current_volume = self.get_avg_volume()
            # reward = ((previous_avg_distance - avg_distance) * 2) + ((previous_all_distance - all_distance)* 2)
            # reward = ((previous_all_distance - all_distance) * (self.can_delivery_cars + self.not_excess_cars + 1))
            finish_cars = self.get_finish_cars()
            if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1)
            else:
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1) - 100
        else:
            reward = -10000
        return reward

    def move_most_distance_to_nearest(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            previous_avg_volume = self.get_avg_volume()
            max_distance, car_index_max = 0, 0
            for i, car in enumerate(self.cars):
                distance = car.distance
                if distance > max_distance:
                    car_index_max = i
                    max_distance = distance
            farthest_order = self.find_farthest_order(car_index_max)
            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[car_index_max].centroid['lat'], self.cars[car_index_max].centroid['lon'], car_index_max)
            if nearest_car != car_index_max:
                self.move_order(car_index_max, nearest_car, farthest_order)
            avg_distance, all_distance = self.get_average_distance()
            current_volume = self.get_avg_volume()
            # reward = ((previous_avg_distance - avg_distance) * 2) + ((previous_all_distance - all_distance)* 2)
            # reward = ((previous_all_distance - all_distance) * (self.can_delivery_cars + self.not_excess_cars + 1))
            finish_cars = self.get_finish_cars()
            if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1)
            else:
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1) - 100
        else:
            reward = -10000
        return reward

    def move_from_full_car_and_can_not_delivery_to_nearest_car(self):
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            previous_avg_volume = self.get_avg_volume()
            most_orders = 0
            most_orders_car = 0
            for i, car in enumerate(self.cars):
                is_full = self.is_full(i)
                is_delivery = self.is_delivery(i)
                if is_full and not is_delivery:
                    number_of_orders = len(self.cars[i].orders)
                    if number_of_orders > most_orders:
                        most_orders = number_of_orders
                        most_orders_car = i
            farthest_order = self.find_farthest_order(most_orders_car)
            nearest_car, nearest_orders = self.find_nearest_car_and_order(self.cars[most_orders_car].orders[farthest_order].coordinate['lat'], self.cars[most_orders_car].orders[farthest_order].coordinate['lon'], most_orders_car)
            if nearest_car != most_orders_car:
                self.move_order(most_orders_car, nearest_car, farthest_order)
            avg_distance, all_distance = self.get_average_distance()
            current_volume = self.get_avg_volume()
            # reward = ((previous_avg_distance - avg_distance) * 2) + ((previous_all_distance - all_distance)* 2)
            # reward = ((previous_all_distance - all_distance) * (self.can_delivery_cars + self.not_excess_cars + 1))
            finish_cars = self.get_finish_cars()
            if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1)
            else:
                reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1) - 100
        else:
            reward = -10000
        return reward

    def delete_car(self):
        # is_full, is_excess = self.is_full_all_cars()
        # if not is_full:
        if len(self.cars) > 1:
            previous_avg_distance, previous_all_distance = self.get_average_distance()
            previous_avg_volume = self.get_avg_volume()
            average_distance, all_distance= self.get_average_distance()
            car_index = self.get_min_order_car_index()
            min_order = 1000
            for i, car in enumerate(self.cars):
                orders_number = len(car.orders)
                if not self.is_delivery(i):
                    if orders_number < min_order:
                        min_order = orders_number
                        car_index = i
            if len(self.cars[car_index].orders) > 0:
                for i, order in enumerate(self.cars[car_index].orders):
                    nearest_car, nearest_order = self.find_nearest_car_and_order(order.coordinate['lat'], order.coordinate['lon'], car_index)
                    if nearest_car != car_index:
                        self.cars[nearest_car].orders.append(order)
            self.cars.pop(car_index)
            self.set_distance_and_centroid_and_volume_all_cars()
            is_full = self.is_full_all_cars()
            is_delivery = self.is_delivery_all_car()
            # avg_distance, all_distance = self.get_average_distance()
            current_volume = self.get_avg_volume()
            if is_full != '2':
                finish_cars = self.get_finish_cars()
                if is_delivery == '2':
                    # reward = - ((all_distance - previous_all_distance) * (cant_delivery_car + excess_cars + 1)) + 500
                    reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1) + 50
                else:
                    # reward = - ((all_distance - previous_all_distance) + () * (cant_delivery_car + excess_cars + 1)) + 100
                    reward = (((previous_all_distance - all_distance) * (self.can_delivery_cars + 1)) + ((previous_avg_volume - current_volume) * (self.not_excess_cars + 1))) * (finish_cars + 1) + 10
                # reward = ((previous_all_distance - all_distance) * (self.can_delivery_cars + self.not_excess_cars + 1)) * (1 / len(self.cars)) + 100
            else:
                reward = -10000
        else:
            reward = -10000
        return reward

class QLearning:
    def __init__(self, learning_rate=0.1):
        self.alpha = learning_rate
        self.gamma = 0.89
        self.epsilon = 0.5
        self.state_value = []

        self.all_epochs = []
        self.all_penalties = []
        self.q_table = np.zeros((9, 7))
        car = Car()
        for i in range(ALL_ORDERS):
            car.add_order(Order())
        self.env = Simulator(init_car=[car])

    def save_model(self, file_name):
        np.save(open(file_name, 'wb'), self.q_table)

    def load_model(self):
        self.q_table = np.load(open('file_name', 'rb'))

    def training(self):
        for i in range(1, 1000):
            self.env.reset()
            self.env.set_distance_and_centroid_and_volume_all_cars()
            state = self.env.get_state()

            epochs, penalties, reward, = 0, 0, 0
            done = False

            file_name = 'qtable0.np'
            while not done:
                if random.uniform(0, 1) < self.epsilon:
                    action = random.randint(0, 6)
                else:
                    action = np.argmax(self.q_table[state])  # Exploit learned values

                # print(f'Current Action : {action} state : {state}')
                # print(f'Q table {self.q_table}')
                print(f'State : {state} action : {action}')

                reward, next_state = self.env.take_action(action)

                print(f'Reward {reward}')
                print(f'Next State {next_state}')

                print('number of cars: ', len(self.env.cars))
                # print('not full : ', self.env.not_full_cars)
                print('not_excess : ', self.env.not_excess_cars)
                print('is_delivery : ', self.env.can_delivery_cars)

                old_value = self.q_table[state, action]
                next_max = np.max(self.q_table[next_state])

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state, action] = new_value

                self.save_model(file_name)
                print('Q table')
                print(self.q_table)
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

                # if reward == -10:
                #     penalties += 1

                state = next_state
                epochs += 1

                if state == 8:
                    print('GOAL!!!!!!!!!!!!!!')
                    print('GOAL!!!!!!!!!!!!!!')
                    print('GOAL!!!!!!!!!!!!!!')
                    print('GOAL!!!!!!!!!!!!!!')
                    winsound.Beep(frequency, duration)
                    file_name = 'qtable' + str(i) + '.np'
                    done = True

            self.epsilon = self.epsilon - 0.01

            if self.epsilon < 0.2:
                self.epsilon = 0.2

            if i % 100 == 0:
                clear_output(wait=True)
                print(f"Episode: {i}")
                # print(self.q_table)

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


