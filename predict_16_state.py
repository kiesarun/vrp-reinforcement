import random
import numpy as np

# random.seed(5555)
# np.random.seed(5555)

from q_learning_edit_std_volume_and_state import QLearning
import time

VOLUME_STD = 2.3


def model_predict(agent):
    start_time = time.time()
    agent.load_model('q-table_edit_std_volume_and_state_3rd.np')
    print(agent.q_table)
    agent.env.set_distance_and_centroid_and_volume_all_cars()
    done = False
    state = agent.env.get_state()
    loop = 2
    count = 0
    while not done:
        history_number = len(agent.env.move_history)
        if history_number >= 8:
            start = history_number - 8
            end = history_number
            if start + 7 < end:
                if agent.env.move_history[start] == agent.env.move_history[start + 2] or agent.env.move_history[start + 2] == agent.env.move_history[start + 4]:
                    if agent.env.move_history[start + 1] == agent.env.move_history[start + 3] or agent.env.move_history[start + 3] == agent.env.move_history[start + 5]:
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
        if state == next_state:
            count = count + 1
        else:
            count = 0
        state = next_state


        if state == 15:
            if agent.env.std_volume < VOLUME_STD:
                time_use = time.time() - start_time
                print('time : ', time_use)
                print('standard volume', agent.env.std_volume)
                done = True
                return 'finish', agent.env.cars


def print_result(agent):
    print(agent.env.sum_volume)
    for i, car in enumerate(agent.env.cars):
        print('car : ', i)
        print('volume : \t',  car.volume)
        print('distance : \t', car.distance)


def predict(orders):
    agent = QLearning(is_train=False, orders=orders)
    agent.env.reset()
    status, result = model_predict(agent)

    for i, car in enumerate(result):
        for j in range(len(car.route)):
            delivery_index = car.route[j]
            for k, order in enumerate(car.orders):
                if k == delivery_index:
                    order.deliveryOrder = j
                    order.carNumber = i

    return status, result


if __name__ == "__main__":
    agent = QLearning(is_train=False)
    agent.env.reset()

    print('model predict')
    model_predict(agent)
    print_result(agent)

