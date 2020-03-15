import string
import random


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class Order:
    def __init__(self):
        self.id = random_string()
        self.coordinate = {
            'lat': random.uniform(13.6, 13.9),
            'lon': random.uniform(100.1, 100.5)
        }
        self.width = random.uniform(10, 50)
        self.height = random.uniform(2, 80)
        self.length = random.uniform(15, 80)
        self.carNumber = 0
        self.deliveryOrder = 0
        # self.index = index

