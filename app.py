from dotenv import load_dotenv

load_dotenv()
from flask import Flask, Response, request
from connectDB import connectOrdersDB
from clusterByKmean import clusterByKmean
from travellingSales import travellingSales
from prepareData import prepareData
app = Flask(__name__)


@app.route('/', methods=['POST'])
def path():
    try:
        data = request.form
        db = connectOrdersDB()
        orders = db['orders'].find()

        # s1 = State(orders)
        # s1.take_action()

        # g = Genetic(orders)

        if data['solution'] == 'kmean':
            coordinates = []
            completed_data = []
            for order in orders:
                coordinates.append({
                    'id': order['_id'],
                    'coor': order['coordinates']
                })
            number_of_cars = int(data['numberOfCars'])
            grouped_cars = clusterByKmean(coordinates, number_of_cars) 

            prepared_data = prepareData(grouped_cars,number_of_cars)
            completed_data = travellingSales(prepared_data)

            db = connectOrdersDB()
            for i in range(len(completed_data)):
              print('round', i)
              for order in completed_data[i]:
                print(order)
                db['orders'].update_one({"_id": order['id']}, {"$set": {"carNumber": int(order['carNumber'])}})
                db['orders'].update_one({"_id": order['id']}, {"$set": {"deliveryOrder": int(order['delivery'])}})

        return 'success'

    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
