from travellingSales import two_opt

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
        # self.deliveryStatus = False
        # self.isFull = False

    def add_order(self, order):
        self.orders.append(order)

    def take_out_order(self, order_index):
        self.orders.pop(order_index)

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

    def set_volume(self):
        volume = 0
        for order in self.orders:
            volume = volume + (order.width * order.height * order.length)
