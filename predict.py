import random
import numpy as np

random.seed(5555)
np.random.seed(5555)

from qLearning import QLearning
import time


def model_predict(agent):
    start_time = time.time()
    agent.load_model('1st_qtable.np')
    done = False
    state = agent.env.get_state()
    while not done:
        action = agent.predict(state)
        reward, next_state = agent.env.take_action(action)
        state = next_state

        if state == 8:
            done = True
            time_use = time.time() - start_time
            print("model predict ", time_use, ' seconds')


def print_result(agent):
    for i, car in enumerate(agent.env.cars):
        print('car : ', i)
        print('volume : \t',  car.volume)
        print('distance : \t', car.distance)


def predict(orders):
    agent = QLearning(False, orders)
    agent.env.reset()
    model_predict(agent)

    for i, car in enumerate(agent.env.cars):
        for j in range(len(car.route)):
            delivery_index = car.route[j]
            for k, order in enumerate(car.orders):
                if k == delivery_index:
                    order.deliveryOrder = j

    return agent.env.cars


if __name__ == "__main__":
    agent = QLearning(False)
    agent.env.reset()

    print('model predict')
    model_predict(agent)
    print_result(agent)
