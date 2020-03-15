import random
import numpy as np

random.seed(5555)
np.random.seed(5555)

from qLearning import QLearning
import time


def tester(state):
    if state == 0:
        action = 0
    elif state == 1:
        action = 5
    elif state == 2:
        action = 2
    elif state == 3:
        action = 0
    elif state == 4:
        action = 5
    elif state == 5:
        action = 5
    elif state == 6:
        action = 0
    elif state == 7:
        action = 6
    else:
        action = 6
    return action


def tester_predict(agent):
    start_time = time.time()
    done = False
    state = agent.env.get_state()
    while not done:
        action = tester(state)
        reward, next_state = agent.env.take_action(action)
        state = next_state

        if state == 8:
            done = True
            time_use = time.time() - start_time
            print("model predict ", time_use, 'seconds')


def print_result(agent):
    for i, car in enumerate(agent.env.cars):
        print('car : ', i)
        print('volume : \t',  car.volume)
        print('distance : \t', car.distance)


if __name__ == "__main__":
    agent = QLearning(False)

    print('tester predict')
    tester_predict(agent)
    print_result(agent)


