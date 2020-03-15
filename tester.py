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
            print("--- %s seconds (tester predict) ---" % (time.time() - start_time))


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
            print("--- %s seconds (model predict) ---" % (time.time() - start_time))


def print_result(agent):
    for i, car in enumerate(agent.env.cars):
        print('car : ', i)
        print('volume : \t',  car.volume)
        print('distance : \t', car.distance)


if __name__ == "__main__":
    agent = QLearning(False)

    print('model predict')
    model_predict(agent)
    print_result(agent)

    print('tester predict')
    tester_predict(agent)
    print_result(agent)


