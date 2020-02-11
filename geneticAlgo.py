import numpy as np
import random 
from matplotlib import pyplot as plt
from math import cos, asin, sqrt, ceil

CAR_CAPACITY = 30
ROOT_NODE = [13.72919, 100.77564]
# CAR_WIDTH = 150
# CAR_LENGTH = 180
# CAR_HEIGHT = 150

class Genetic :
  def __init__(self, orders):
    self.orders_input = orders
    
    self.new_population = self.createRandomPopulation()
    print(self.new_population)
    
  def createRandomPopulation(self):
    number_of_orders = self.orders_input.count() 
    sol_per_pop = ceil(number_of_orders / CAR_CAPACITY)
    num_weights = random.randint(0, CAR_CAPACITY)
    print('number of order in car 1 :', num_weights)                                      # จะเอากี่ order , 0 - 30 => 25

    pop_size = (sol_per_pop, CAR_CAPACITY)                                 
    print('zeros')
    
    new_population = np.zeros(pop_size, dtype=int)
    print(new_population)
    random_index_car = random.sample(range(CAR_CAPACITY), num_weights)                    # 0 - 30 =>  25 number 
    random_index_order = random.sample(range(number_of_orders), num_weights)              # 0 - 49 =>  25 number
    print('index of car 1', random_index_car)
    print('order index of car 1', random_index_order)

    for i in range(num_weights):
      new_population[0][random_index_car[i]] = self.orders_input[random_index_order[i]]['index']
    

    return new_population

  def availableOrder(self):
    for order in self.orders_input:
      if order in self.new_population[0]:
        print('not')   
      else:
        print('yes')  




