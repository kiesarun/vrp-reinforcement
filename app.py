from dotenv import load_dotenv

load_dotenv()
from flask import Flask, Response, request
from connectDB import connectOrdersDB
from clusterByKmean import clusterByKmean
from predict import predict
from travellingSales import two_opt
from orders import Order
from prepareData import prepareData
app = Flask(__name__)


@app.route('/', methods=['POST'])
def path():
    try:
        data = request.form
        db = connectOrdersDB()
        all_orders = db['orders'].find()

        orders = []
        for order in all_orders:
            orders.append(Order(order))

        if data['solution'] == 'kmean':
            number_of_cars = int(data['numberOfCars'])
            orders_clustered = clusterByKmean(orders, number_of_cars)

            cars = []
            for i in range(number_of_cars):
                car_orders = []
                for order in orders_clustered:
                    if order.carNumber == i:
                        car_orders.append(order)
                cars.append(car_orders)
            print('prepared')

            routes = []
            for car_orders in cars:
                finish_distance, finish_route = two_opt(car_orders, 0.1)
                routes.append(finish_route)

            for i, car_orders in enumerate(cars):
                for j in range(len(routes[i])):
                    for k in range(len(car_orders)):
                        if routes[i][j] == k:
                            car_orders[k].deliveryOrder = j

                # for j, order in enumerate(car_orders):
                #     for
                #     order.deliveryOrder = route[i][j]
                    # print(route[i][j])

        elif data['solution'] == 'qlearning':
            cars = predict(orders)

        db = connectOrdersDB()
        # for i in range(len(completed_data)):
        for car_orders in cars:
            for order in car_orders:
                db['orders'].update_one({"_id": order.id}, {"$set": {"carNumber": int(order.carNumber)}})
                db['orders'].update_one({"_id": order.id}, {"$set": {"deliveryOrder": int(order.deliveryOrder)}})

        return 'success'

    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
