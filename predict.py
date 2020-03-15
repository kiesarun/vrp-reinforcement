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
            print("--- %s seconds (model predict) ---" % (time.time() - start_time))


def print_result(agent):
    for i, car in enumerate(agent.env.cars):
        print('car : ', i)
        print('volume : \t',  car.volume)
        print('distance : \t', car.distance)


if __name__ == "__main__":
    agent = QLearning(False)
    agent.env.reset()

    print('model predict')
    model_predict(agent)
    print_result(agent)
