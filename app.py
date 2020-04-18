from dotenv import load_dotenv

load_dotenv()
from flask import Flask, Response, request, jsonify
from connectDB import connectOrdersDB
from waitress import serve
from clusterByKmean import clusterByKmean
from predict_last import predict
from travellingSales import two_opt
from bson.objectid import ObjectId
from orders import Order

app = Flask(__name__)


@app.route('/', methods=['POST'])
def path():
    # try:
    print('YAY')
    data = request.form
    db = connectOrdersDB()
    request_id = data['id']

    request_obj = db['requests'].find_one({'_id': ObjectId(request_id)})

    all_orders = request_obj['orders']

    if data['solution'] == 'kmean':
        orders = []
        for order in all_orders:
            orders.append(Order(order))
        number_of_cars = int(data['numberOfCars'])
        orders_clustered = clusterByKmean(orders, number_of_cars)
        cars = []
        for i in range(number_of_cars):
            car_orders = []
            for order in orders_clustered:
                if order.carNumber == i:
                    car_orders.append(order)
            cars.append(car_orders)

        routes = []
        distance = []
        volume = []
        for car_orders in cars:
            finish_distance, finish_route = two_opt(orders=car_orders, improvement_threshold=0.1, solution=data['solution'])
            routes.append(finish_route)
            distance.append(finish_distance)
            car_volume = 0
            for i, order in enumerate(car_orders):
                car_volume = car_volume + order.volume
            volume.append(car_volume)

        for i, car_orders in enumerate(cars):
            for j in range(len(routes[i])):
                for k in range(len(car_orders)):
                    if routes[i][j] == k:
                        car_orders[k].deliveryOrder = j
        status = 'finish'

    if data['solution'] == 'qlearning':
        status, result = predict(all_orders)
        distance = []
        volume = []
        cars = []
        routes = []
        for car in result:
            distance.append(car.distance)
            volume.append(car.volume)
            cars.append(car.orders)
            routes.append(car.route)
            print(car.route)

        for i, car_orders in enumerate(cars):
            for j in range(len(routes[i])):
                for k in range(len(car_orders)):
                    if routes[i][j] == k:
                        car_orders[k].deliveryOrder = j

    db = connectOrdersDB()

    def find_order_by_id(order_id):
        for index, order in enumerate(all_orders):
            if order['_id'] == order_id:
                return index

    print('request id', request_id)

    for car_orders in cars:
        for order in car_orders:
            order_index = find_order_by_id(order.id)
            all_orders[order_index]['carNumber'] = int(order.carNumber)
            all_orders[order_index]['deliveryOrder'] = int(order.deliveryOrder)
            all_orders[order_index]['width'] = order.width
            all_orders[order_index]['height'] = order.height
            all_orders[order_index]['length'] = order.length
            all_orders[order_index]['coordinates'] = order.coordinate
            print('car number: ', order.carNumber, 'deliveryOrder: ', order.deliveryOrder, 'width', order.width)
            if order.carNumber == -1:
                print('error')

    print('all_orders: ', all_orders)

    db['requests'].find_one_and_update({'_id': ObjectId(request_id)}, {'$set': {'orders': all_orders, 'status': status, 'distance': distance, 'volume': volume}})

    return jsonify({
        "finish_distance": distance
    })

    # except Exception as e:
    #     print(e)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
