from clusterByKmean import clusterByKmean
from orders import Order
from travellingSales import two_opt
import random
import numpy as np
from q_learning_edit_std_volume_and_state import QLearning
import time
import math

VOLUME_STD = 2.3


def predict(all_orders):
    orders = []
    sum_volume = 0
    for order in all_orders:
        orders.append(Order(order))

    for order in orders:
        sum_volume = sum_volume + order.volume
    number_of_cars = math.ceil(sum_volume / 6500000)
    print('number of cars : ', number_of_cars)
    done = False

    orders_clustered = clusterByKmean(orders, number_of_cars)
    cars = []
    for i in range(number_of_cars):
        car_orders = []
        for order in orders_clustered:
            if order.carNumber == i:
                car_orders.append(order)
        cars.append(car_orders)

    routes = []
    distance = []
    volume = []
    for i, car_orders in enumerate(cars):
        finish_distance, finish_route = two_opt(orders=car_orders, improvement_threshold=0.1, solution='kmean')
        car_volume = 0
        for order in car_orders:
            car_volume = car_volume + order.volume
        print('car: ', i,'distance: ', finish_distance, 'volume: ', car_volume)
        if 50 <= finish_distance <= 240:
            routes.append(finish_route)
            distance.append(finish_distance)
            if car_volume <= 699200:
                volume.append(car_volume)

    agent = QLearning(is_train=False, orders=all_orders)
    agent.env.reset()
    for i, car in enumerate(cars):
        if i == 0:
            agent.env.cars[0].orders = car
        else:
            agent.env.add_car()
            agent.env.cars[i].orders = car


    while not done:
        start_time = time.time()
        agent.load_model('q-table_edit_std_volume_and_state_3rd.np')
        print(agent.q_table)
        agent.env.set_distance_and_centroid_and_volume_all_cars()
        done = False
        state = agent.env.get_state()
        loop = 2
        count = 0
        while not done:
            if state == 15:
                if agent.env.std_volume < VOLUME_STD:
                    time_use = time.time() - start_time
                    print('time : ', time_use)
                    print('standard volume', agent.env.std_volume)
                    done = True
                    return 'finish', agent.env.cars

            history_number = len(agent.env.move_history)
            if history_number >= 6:
                start = history_number - 6
                end = history_number
                if start + 5 < end:
                    if agent.env.move_history[start] == agent.env.move_history[start + 2] == agent.env.move_history[start + 4]:
                        if agent.env.move_history[start + 1] == agent.env.move_history[start + 3] == agent.env.move_history[start + 5]:
                            loop = loop + 1
                            print('loop ***********************************************', loop)
                            print(agent.q_table)
                            agent.env.move_history = []
                        if loop >= 20:
                            return 'reject', agent.env.cars

            if loop % 2 == 0:
                action = np.argmax(agent.q_table[state])
            else:
                if state == 0 or state == 4 or state == 8 or state == 12:
                    loop = loop + 1
                else:
                    max_index = np.argmax(agent.q_table[state])
                    max_value = agent.q_table[state][max_index]
                    min_diff = max_value
                    for i, q_value in enumerate(agent.q_table[state]):
                        diff = max_value - q_value
                        if diff != 0 and diff < min_diff:
                            min_diff = diff
                            action = i
                    print('old action: ', max_index, 'new_action: ', action)

            next_state = agent.env.take_action(action)
            print('state : ', state, 'action : ', action, 'next state: ', next_state)
            print('-------------------------------------------------------------------')
            if action == 0:
                loop = loop + 1
            state = next_state
