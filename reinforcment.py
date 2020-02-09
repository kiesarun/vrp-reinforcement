import numpy as np

CAR_CAPACITY = 10
# CAR_WIDTH = 150
# CAR_LENGTH = 180
# CAR_HEIGHT = 150

class State:
    def __init__(self, orders):
        self.cars = []
        self.cars.append(orders)
        # self.cars.append(np.zeros(CAR_CAPACITY, dtype=int))
        print(self.cars)
        self.finish = False

    def CarDeliverableCheck(self):
        if len(self.cars[0]) <= CAR_CAPACITY:
            self.finish = True 
            
# if __name__ == "__main__":
#     s1 = State()