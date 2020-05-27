import random
import numpy as np

# random.seed(5555)
# np.random.seed(5555)

import copy
from math import cos, asin, sqrt
from car import Car

CAR_CAPACITY = 30
ROOT_NODE = {
    'lat': 13.72919,
    'lon': 100.77564
}

CAR_WIDTH = 152
CAR_LENGTH = 230
CAR_HEIGHT = 200
CAR_VOLUME = CAR_LENGTH * CAR_HEIGHT * CAR_WIDTH
MIN_DISTANCE = 50
MAX_DISTANCE = 240

VOLUME_STD = 2.3


def compute_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
        cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin... as km.


def scale_volume(volume):
    return volume / 1000000


class Simulator:
    def __init__(self, init_car=None, is_train=True):
        if init_car:
            self.init_car = copy.deepcopy(init_car)
            self.cars = copy.deepcopy(init_car)
        self.can_delivery_cars = 0
        self.not_excess_cars = 0
        self.all_order = len(self.cars[0].orders)
        self.std_volume = 0
        self.is_train = is_train
        self.ori_is_train = is_train
        self.sum_volume = 0
        self.move_history = []

    def reset(self):
        self.cars = copy.deepcopy(self.init_car)
        self.can_delivery_cars = 0
        self.not_excess_cars = 0
        self.std_volume = 0
        self.all_order = len(self.cars[0].orders)
        self.is_train = self.ori_is_train
        self.sum_volume = 0
        print('reset simulator')

    def find_nearest_other_car_order(self, car_index):
        nearest_distance = 10000
        nearest_distance_order_index = ''
        nearest_car = ''
        for i, order in enumerate(self.cars[car_index].orders):
            for index, car in enumerate(self.cars):
                if index != car_index:
                    distance = compute_distance(self.cars[index].centroid['lat'], self.cars[index].centroid['lon'], order.coordinate['lat'],
                                                     order.coordinate['lon'])
                    if distance <= nearest_distance:
                        nearest_distance = distance
                        nearest_distance_order_index = i
                        nearest_car = index
        # print('max distance is ', max_distance, 'order index is ', max_distance_order_index)
        return nearest_distance_order_index, nearest_car

    def find_farthest_of_other_cars_order(self, car_index):
        farthest_distance = 0
        farthest_distance_order_index = 0
        for i, order in enumerate(self.cars[car_index].orders):
            for index, car in enumerate(self.cars):
                if index != car_index:
                    distance = compute_distance(self.cars[index].centroid['lat'], self.cars[index].centroid['lon'], order.coordinate['lat'],
                                                     order.coordinate['lon'])
                    if distance >= farthest_distance:
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
                    if centroid_distance <= min_centroid_distance:
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
            self.move_history.append([origin_car_index, destination_car_index, self.cars[origin_car_index].orders[order_index]])
            origin_car_orders = self.cars[origin_car_index].orders
            destination_car_orders = self.cars[destination_car_index].orders
            selected_order = origin_car_orders.pop(order_index)
            destination_car_orders.append(selected_order)

            self.set_distance_and_centroid_and_volume(origin_car_index)
            self.set_distance_and_centroid_and_volume(destination_car_index)
            # print('moved', order_index, 'from car ', origin_car_index, 'to car ', destination_car_index)

    def get_max_order_car_index(self):
        max_orders, car_index = 0, 0
        for i, car in enumerate(self.cars):
            number_of_order = len(car.orders)
            if number_of_order > max_orders:
                car_index = i
                max_orders = number_of_order
        return car_index

    def get_max_order(self):
        max_orders = 0
        for car in self.cars:
            number_of_order = len(car.orders)
            if number_of_order > max_orders:
                max_orders = number_of_order
        return max_orders

    def get_max_volume_car_index(self):
        max_volume, car_index = 0, 0
        for i, car in enumerate(self.cars):
            volume = car.volume
            if volume > max_volume:
                max_volume = volume
                car_index = i
        return car_index

    def get_min_volume_car_index(self):
        car_index = 0
        min_volume = 100000000
        for i, car in enumerate(self.cars):
            car_volume = car.volume
            if car_volume < min_volume:
                car_index = i
                min_volume = car_volume
        return car_index

    def get_sum_volume(self):
        sum_volume = 0
        for car in self.cars:
            sum_volume = sum_volume + car.volume
        return sum_volume

    def set_car_volume(self, car_index):
        volume = 0
        for order in self.cars[car_index].orders:
            volume = volume + order.volume
        self.cars[car_index].volume = volume

    def set_distance_and_centroid_and_volume(self, car_index):
        if len(self.cars[car_index].orders) < 160: #self.all_order / 1.8
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
            for i, car in enumerate(self.cars):
                if len(car.orders) > 160: #self.all_order / 1.8
                    car.distance = 1000
                else:
                    car.set_distance()
                car.set_centroid()
                car.set_volume()
        self.sum_volume = self.get_sum_volume()

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
        car_volume = self.cars[car_index].volume
        if car_volume >= CAR_VOLUME:
            return True
        else:
            return False

    def is_full_all_cars(self):
        is_excess_volume = 0
        number_of_cars = len(self.cars)
        print('CAR VOLUME', CAR_VOLUME)
        for i, car in enumerate(self.cars):
            car_volume = self.cars[i].volume
            if car_volume >= CAR_VOLUME:
                is_excess_volume = is_excess_volume + 1
                print('car', i, 'volume: ', car_volume, 'FULL')
            else:
                print('car', i, 'volume: ', car_volume)

        print('full cars check : ', is_excess_volume)

        if is_excess_volume == 0:
            state = '0'
        elif is_excess_volume == 1:
            if number_of_cars == 1:
                state = '3'
            if number_of_cars > 1:
                state = '1'
        elif is_excess_volume < len(self.cars):
            state = '2'
        else:
            state = '3'
        self.not_excess_cars = number_of_cars - is_excess_volume
        return state

    def is_delivery_all_car(self):
        number_of_cars = len(self.cars)
        is_not_delivery_check = 0
        for i, car in enumerate(self.cars):
            is_delivery = self.is_delivery(i)
            if not is_delivery:
                is_not_delivery_check = is_not_delivery_check + 1

        print('not delivery check : ', is_not_delivery_check)

        if is_not_delivery_check == 0:
            state = '3'
        elif is_not_delivery_check == 1:
            if number_of_cars == 1:
                state = '0'
            if number_of_cars > 1:
                state = '1'
        elif is_not_delivery_check < number_of_cars:
            state = '2'
        else:
            state = '0'
        self.can_delivery_cars = number_of_cars - is_not_delivery_check
        return state

    def is_delivery(self, car_index):
        # is_delivery = 0
        number_of_order = len(self.cars[car_index].orders)
        total_distance = self.cars[car_index].distance
        if MAX_DISTANCE >= total_distance >= MIN_DISTANCE:
            print(number_of_order,'order', 'total distance : ', total_distance, 'car', car_index, 'can delivery')
            return True
        else:
            print(number_of_order,'order', 'total distance : ', total_distance, 'car', car_index)
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

    def get_std_deviation_distance(self):
        mean, all_ = self.get_average_distance()
        sum_diff = 0
        for car in self.cars:
            sum_diff = sum_diff + (car.distance - mean) ** 2
        variance = sum_diff / len(self.cars)
        std = sqrt(variance)
        return std

    def get_std_deviation_volume(self):
        mean = self.get_avg_volume()
        mean = scale_volume(mean)
        sum_diff = 0
        for car in self.cars:
            car_volume = scale_volume(car.volume)
            sum_diff = sum_diff + (car_volume - mean) ** 2
        variance = sum_diff / len(self.cars)
        std = sqrt(variance)
        return std

    def get_state(self):
        is_full_state = self.is_full_all_cars()
        is_delivery_state = self.is_delivery_all_car()
        state_string = is_delivery_state + is_full_state

        volume_std = self.get_std_deviation_volume()
        self.std_volume = volume_std

        if state_string == '00':
            state = 3
        elif state_string == '01':
            state = 1
        elif state_string == '02':
            state = 2
        elif state_string == '03':
            state = 0
        elif state_string == '10':
            state = 7
        elif state_string == '11':
            state = 5
        elif state_string == '12':
            state = 6
        elif state_string == '13':
            state = 4
        elif state_string == '20':
            state = 11
        elif state_string == '21':
            state = 9
        elif state_string == '22':
            state = 10
        elif state_string == '23':
            state = 8
        elif state_string == '30':
            state = 15
        elif state_string == '31':
            state = 13
        elif state_string == '32':
            state = 14
        else:
            state = 12
        return state

    def take_action(self, action):
        if self.is_train:
            if action == 0:
                reward = self.add_car()
            elif action == 1:
                reward = self.move_farthest_order_from_most_orders_to_nearest_car()
            elif action == 2:
                reward = self.move_nearest_order_of_least_order_car()
            elif action == 3:
                reward = self.move_nearest_order_of_car_that_not_full_and_not_delivery()
            elif action == 4:
                reward = self.move_most_distance_to_nearest()
            elif action == 5:
                reward = self.move_from_full_car_and_can_not_delivery_to_nearest_car()
            else:
                reward = self.delete_car()
            new_state = self.get_state()
            reward = np.tanh(reward)
            return reward, new_state
        else:
            if action == 0:
                self.add_car()
            elif action == 1:
                self.move_farthest_order_from_most_orders_to_nearest_car()
            elif action == 2:
                self.move_nearest_order_of_least_order_car()
            elif action == 3:
                self.move_nearest_order_of_car_that_not_full_and_not_delivery()
            elif action == 4:
                self.move_most_distance_to_nearest()
            elif action == 5:
                self.move_from_full_car_and_can_not_delivery_to_nearest_car()
            else:
                self.delete_car()
            new_state = self.get_state()
            return new_state

    def get_reward(self, pre_delivery_cars, pre_not_full_cars):
        curr_delivery = self.can_delivery_cars
        curr_not_full = self.not_excess_cars

        diff_delivery = curr_delivery - pre_delivery_cars
        diff_not_full = curr_not_full - pre_not_full_cars

        finish_rate = self.get_finish_cars() / len(self.cars)
        reward = diff_delivery + diff_not_full + (finish_rate * 2)
        return reward

    def add_new_empty_car(self):
        self.cars.append(Car())

    # New ACtion
    def add_car(self):
        if self.is_train:
            is_full_state = self.is_full_all_cars()
            is_delivery = self.is_delivery_all_car()
            pre_delivery_cars = self.can_delivery_cars
            pre_not_full_cars = self.not_excess_cars

            # do
            self.cars.append(Car())
            new_car = len(self.cars) - 1
            most_order_car = self.get_max_volume_car_index()
            farthest_order_index = self.find_farthest_of_other_cars_order(most_order_car)
            self.move_order(most_order_car, new_car, farthest_order_index)
            #

            if is_full_state == '3' and is_delivery == '0':
                if not self.is_full(most_order_car) or self.is_delivery(most_order_car):
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) + 2
                else:
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) - 1
            elif is_full_state == '3' or is_delivery == '0':
                reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) - 2
            else:
                reward = -10000
            return reward
        else:
            self.cars.append(Car())
            new_car = len(self.cars) - 1
            most_order_car = self.get_max_volume_car_index()
            farthest_order_index = self.find_farthest_of_other_cars_order(most_order_car)
            self.move_order(most_order_car, new_car, farthest_order_index)

    def move_farthest_order_from_most_orders_to_nearest_car(self):
        if self.is_train:
            if len(self.cars) > 1:
                pre_delivery_cars = self.can_delivery_cars
                pre_not_full_cars = self.not_excess_cars

                most_order_car = self.get_max_volume_car_index()
                farthest_order_index, nearest_car = self.find_nearest_other_car_order(most_order_car)
                # nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[most_order_car].orders[farthest_order_index].coordinate['lat'], self.cars[most_order_car].orders[farthest_order_index].coordinate['lon'], most_order_car)
                if nearest_car != most_order_car:
                    self.move_order(most_order_car, nearest_car, farthest_order_index)

                if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars)
                else:
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) - 2
            else:
                reward = -10000
            return reward
        else:
            if len(self.cars) > 1:
                most_order_car = self.get_max_volume_car_index()
                farthest_order_index, nearest_car = self.find_nearest_other_car_order(most_order_car)
                # nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[most_order_car].orders[farthest_order_index].coordinate['lat'], self.cars[most_order_car].orders[farthest_order_index].coordinate['lon'], most_order_car)
                if nearest_car != most_order_car:
                    self.move_order(most_order_car, nearest_car, farthest_order_index)

    def move_nearest_order_of_least_order_car(self):
        if self.is_train:
            if len(self.cars) > 1:
                previous_avg_distance, previous_all_distance = self.get_average_distance()
                previous_avg_volume = self.get_avg_volume()

                pre_delivery_cars = self.can_delivery_cars
                pre_not_full_cars = self.not_excess_cars

                least_order_car = self.get_min_volume_car_index()
                nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[least_order_car].centroid['lat'], self.cars[least_order_car].centroid['lon'], least_order_car)
                if nearest_car != least_order_car:
                    self.move_order(nearest_car, least_order_car, nearest_order)

                if not self.is_full(least_order_car) and self.is_delivery(least_order_car):
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars)
                else:
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) - 2
            else:
                reward = -10000
            return reward
        else:
            if len(self.cars) > 1:
                least_order_car = self.get_min_volume_car_index()
                nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[least_order_car].centroid['lat'], self.cars[least_order_car].centroid['lon'], least_order_car)
                if nearest_car != least_order_car:
                    self.move_order(nearest_car, least_order_car, nearest_order)

    def move_nearest_order_of_car_that_not_full_and_not_delivery(self):
        if self.is_train:
            if len(self.cars) > 1:
                if self.is_full_all_cars() != '3':
                    pre_delivery_cars = self.can_delivery_cars
                    pre_not_full_cars = self.not_excess_cars

                    min_order = 1000
                    min_order_car_index = 0
                    check = 0
                    for i, car in enumerate(self.cars):
                        is_full = self.is_full(i)
                        if not is_full and not self.is_delivery(i):
                            number_of_order = len(car.orders)
                            check = check + 1
                            if number_of_order < min_order:
                                min_order = number_of_order
                                min_order_car_index = i
                    if check > 0:
                        if self.cars[min_order_car_index].distance < MIN_DISTANCE:
                            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[min_order_car_index].centroid['lat'], self.cars[min_order_car_index].centroid['lon'], min_order_car_index)
                            if nearest_car != min_order_car_index:
                                self.move_order(nearest_car, min_order_car_index, nearest_order)
                        elif self.cars[min_order_car_index].distance > MAX_DISTANCE:
                            farthest_order_index, nearest_car = self.find_nearest_other_car_order(min_order_car_index)
                            lat = self.cars[min_order_car_index].orders[farthest_order_index].coordinate['lat']
                            lon = self.cars[min_order_car_index].orders[farthest_order_index].coordinate['lon']
                            # nearest_car, nearest_order = self.find_nearest_car_and_order(lat, lon, min_order_car_index)
                            if nearest_car != min_order_car_index:
                                self.move_order(min_order_car_index, nearest_car, farthest_order_index)
                        else:
                            pass

                        if not self.is_full(min_order_car_index) and self.is_delivery(min_order_car_index):
                            if self.is_delivery_all_car() == '1' and self.is_full_all_cars() == '1':
                                reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) + 1
                            else:
                                reward = self.get_reward(pre_delivery_cars, pre_not_full_cars)
                        else:
                            reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) - 2
                    else:
                        reward = -10000
                else:
                    reward = -10000
            else:
                reward = -10000
            return reward
        else:
            if len(self.cars) > 1:
                if self.is_full_all_cars() != '3':
                    min_order = 1000
                    min_order_car_index = 0
                    check = 0
                    for i, car in enumerate(self.cars):
                        is_full = self.is_full(i)
                        if not is_full and not self.is_delivery(i):
                            number_of_order = len(car.orders)
                            check = check + 1
                            if number_of_order < min_order:
                                min_order = number_of_order
                                min_order_car_index = i
                    if check > 0:
                        if self.cars[min_order_car_index].distance < MIN_DISTANCE:
                            nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[min_order_car_index].centroid['lat'], self.cars[min_order_car_index].centroid['lon'], min_order_car_index)
                            if nearest_car != min_order_car_index:
                                self.move_order(nearest_car, min_order_car_index, nearest_order)
                        if self.cars[min_order_car_index].distance > MAX_DISTANCE:
                            farthest_order_index, nearest_car = self.find_nearest_other_car_order(min_order_car_index)
                            lat = self.cars[min_order_car_index].orders[farthest_order_index].coordinate['lat']
                            lon = self.cars[min_order_car_index].orders[farthest_order_index].coordinate['lon']
                            nearest_car, nearest_order = self.find_nearest_car_and_order(lat, lon, min_order_car_index)
                            if nearest_car != min_order_car_index:
                                self.move_order(min_order_car_index, nearest_car, nearest_order)
                        else:
                            pass

    def move_most_distance_to_nearest(self):
        if self.is_train:
            if len(self.cars) > 1:
                pre_delivery_cars = self.can_delivery_cars
                pre_not_full_cars = self.not_excess_cars

                max_distance, car_index_max = 0, 0
                for i, car in enumerate(self.cars):
                    distance = car.distance
                    if distance > max_distance:
                        car_index_max = i
                        max_distance = distance
                farthest_order, nearest_car = self.find_nearest_other_car_order(car_index_max)
                # nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[car_index_max].centroid['lat'], self.cars[car_index_max].centroid['lon'], car_index_max)
                if nearest_car != car_index_max:
                    self.move_order(car_index_max, nearest_car, farthest_order)

                if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars)
                else:
                    reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) - 2
            else:
                reward = -10000
            return reward
        else:
            if len(self.cars) > 1:
                max_distance, car_index_max = 0, 0
                for i, car in enumerate(self.cars):
                    distance = car.distance
                    if distance > max_distance:
                        car_index_max = i
                        max_distance = distance
                farthest_order, nearest_car = self.find_nearest_other_car_order(car_index_max)
                # nearest_car, nearest_order = self.find_nearest_car_and_order(self.cars[car_index_max].centroid['lat'], self.cars[car_index_max].centroid['lon'], car_index_max)
                if nearest_car != car_index_max:
                    self.move_order(car_index_max, nearest_car, farthest_order)

    def move_from_full_car_and_can_not_delivery_to_nearest_car(self):
        if self.is_train:
            if len(self.cars) > 1:
                if self.is_full_all_cars() != '0' or self.is_delivery_all_car() != '3':
                    pre_delivery_cars = self.can_delivery_cars
                    pre_not_full_cars = self.not_excess_cars

                    compare_orders = 0
                    compare_orders_car = 0
                    check = False
                    for i, car in enumerate(self.cars):
                        is_full = self.is_full(i)
                        is_delivery = self.is_delivery(i)
                        if is_full and not is_delivery:
                            check = True
                            number_of_orders = len(self.cars[i].orders)
                            if number_of_orders > compare_orders:
                                compare_orders = number_of_orders
                                compare_orders_car = i
                    if check:
                        farthest_order, nearest_car = self.find_nearest_other_car_order(compare_orders_car)
                        lat = self.cars[compare_orders_car].orders[farthest_order].coordinate['lat']
                        lon = self.cars[compare_orders_car].orders[farthest_order].coordinate['lon']
                        # nearest_car, nearest_orders = self.find_nearest_car_and_order(lat, lon, compare_orders_car)
                        if nearest_car != compare_orders_car:
                            self.move_order(compare_orders_car, nearest_car, farthest_order)

                        if not self.is_full(nearest_car) and self.is_delivery(nearest_car):
                            if self.is_delivery_all_car() == '1' and self.is_full_all_cars() == '1':
                                reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) + 1
                            else:
                                reward = self.get_reward(pre_delivery_cars, pre_not_full_cars)
                        else:
                            reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) - 2
                    else:
                        reward = -10000
                else:
                    reward = -10000

            else:
                reward = -10000
            return reward
        else:
            if len(self.cars) > 1:
                if self.is_full_all_cars() != '0' or self.is_delivery_all_car() != '3':
                    compare_orders = 0
                    compare_orders_car = 0
                    check = False
                    for i, car in enumerate(self.cars):
                        is_full = self.is_full(i)
                        is_delivery = self.is_delivery(i)
                        if is_full and not is_delivery:
                            check = True
                            number_of_orders = len(self.cars[i].orders)
                            if number_of_orders > compare_orders:
                                compare_orders = number_of_orders
                                compare_orders_car = i
                    if check:
                        farthest_order, nearest_car = self.find_nearest_other_car_order(compare_orders_car)
                        lat = self.cars[compare_orders_car].orders[farthest_order].coordinate['lat']
                        lon = self.cars[compare_orders_car].orders[farthest_order].coordinate['lon']
                        # nearest_car, nearest_orders = self.find_nearest_car_and_order(lat, lon, compare_orders_car)
                        if nearest_car != compare_orders_car:
                            self.move_order(compare_orders_car, nearest_car, farthest_order)

    def delete_car(self): # delete min order car that can't delivery
        if self.is_train:
            if len(self.cars) > 1:
                pre_delivery_cars = self.can_delivery_cars
                pre_not_full_cars = self.not_excess_cars

                car_index = self.get_min_volume_car_index()
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
                if is_full != '3':
                    if is_delivery == '3':
                        reward = self.get_reward(pre_delivery_cars, pre_not_full_cars) + 2
                    else:
                        reward = self.get_reward(pre_delivery_cars, pre_not_full_cars)
                else:
                    reward = -10000
            else:
                reward = -10000
            return reward
        else:
            if len(self.cars) > 1:
                # car_index = self.get_min_volume_car_index()
                # min_order = 1000
                # for i, car in enumerate(self.cars):
                #     orders_number = len(car.orders)
                #     if not self.is_delivery(i):
                #         if orders_number < min_order:
                #             min_order = orders_number
                #             car_index = i
                car_index = self.get_max_volume_car_index()
                if len(self.cars[car_index].orders) > 0:
                    for i, order in enumerate(self.cars[car_index].orders):
                        nearest_car, nearest_order = self.find_nearest_car_and_order(order.coordinate['lat'], order.coordinate['lon'], car_index)
                        if nearest_car != car_index:
                            self.cars[nearest_car].orders.append(order)
                self.cars.pop(car_index)
                self.set_distance_and_centroid_and_volume_all_cars()

