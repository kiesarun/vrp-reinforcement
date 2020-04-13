import string
import random


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class Order:
    def __init__(self, order=None):
        if order is None:
            self.id = random_string()
            self.coordinate = {
                'lat': random.uniform(13.6, 13.9),
                'lon': random.uniform(100.1, 100.5)
            }
            self.width = random.uniform(10, 50)
            self.height = random.uniform(2, 100)
            self.length = random.uniform(15, 100)
        else:
            print(order)
            self.id = order['_id']
            self.coordinate = {
                'lat': order['coordinates']['lat'],
                'lon': order['coordinates']['lon']
            }
            self.width = order['width']
            self.height = order['height']
            self.length = order['length']
        self.volume = self.width * self.height * self.length
        self.carNumber = 0
        self.deliveryOrder = 0




