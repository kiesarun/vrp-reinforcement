import numpy as np
import random
# import winsound
# from IPython.display import clear_output
from orders import Order
from car import Car
from simulator_edit_std_volume_and_state import Simulator

ALL_ORDERS = 300

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 3000  # Set Duration To 1000 ms == 1 second

VOLUME_STD = 1.8


class QLearning:
    def __init__(self, learning_rate=0.1, is_train=True, orders=None):
        self.alpha = learning_rate
        self.gamma = 0.89
        self.epsilon = 0.5
        self.state_value = []

        self.all_epochs = []
        self.all_penalties = []
        self.q_table = np.zeros((16, 7))
        car = Car()
        if orders is None:
            for i in range(ALL_ORDERS):
                car.add_order(Order())
        else:
            for order in orders:
                car.add_order(order)

        self.env = Simulator(init_car=[car], is_train=is_train)

    def save_model(self, file_name):
        np.save(open(file_name, 'wb'), self.q_table)

    def load_model(self, file_name):
        self.q_table = np.load(open(file_name, 'rb'))

    def training(self):
        for i in range(1, 200):
            self.env.reset()
            self.env.set_distance_and_centroid_all_cars()
            state = self.env.get_state()

            epochs, penalties, reward, = 0, 0, 0
            done = False

            file_name = 'q-table_edit_std_volume_and_state.np'
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
                print('not full : ', self.env.not_excess_cars)
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

                if state == 15:
                    if self.env.std_volume < VOLUME_STD:
                        print('GOAL!!!!!!!!!!!!!!')
                        file = open('Goal_edit_std_volume_and_state.txt', 'a')
                        file.write('\nGoal_' + str(i) + '\n')
                        file.write('standard volume: ' + str(self.env.std_volume) + '\n')
                        file.write(str(self.q_table))
                        file.write('\n\n')
                        for j, car in enumerate(self.env.cars):
                            file.write('car_' + str(j) + '\tvolume: ' + str(car.volume) + '\tdistance: ' + str(car.distance) + '\n')
                        file.write('###################################################################')
                        file.close()
                        done = True

            self.epsilon = self.epsilon - 0.01

            if self.epsilon < 0.2:
                self.epsilon = 0.2

            if i % 100 == 0:
                # clear_output(wait=True)
                print(f"Episode: {i}")
                # print(self.q_table)

        print("Training finished.\n")
        print(f'Q table {self.q_table}')

    def predict(self, state):
        state = self.env.get_state()
        done = False

        action = np.argmax(self.q_table[state])  # Exploit learned values
        return action


if __name__ == "__main__":
    agent = QLearning()
    agent.training()



