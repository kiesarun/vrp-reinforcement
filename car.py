from travellingSales import two_opt
import numpy as np

class Car:
    def __init__(self):
        # self.carIndex = carIndex
        self.orders = []
        self.distance = 0
        self.centroid = {
            'lat': 0,
            'lon': 0
        }
        self.volume = 0
        self.route = []
        # self.deliveryStatus = False
        # self.isFull = False

    def add_order(self, order):
        self.orders.append(order)
        self.volume = self.volume + order.volume


    def take_out_order(self, order_index):
        self.volume = self.volume - self.orders[order_index].volume
        order = self.orders.pop(order_index)
        return order

    def set_distance(self):
        self.distance = two_opt(self.orders, 0.1)

    def set_centroid(self):
        number_of_orders = len(self.orders)
        lat = 0
        lon = 0
        for order in self.orders:
            lat = lat + order.coordinate['lat']
            lon = lon + order.coordinate['lon']
        if number_of_orders > 0:
            self.centroid['lat'] = lat / number_of_orders
            self.centroid['lon'] = lon / number_of_orders

