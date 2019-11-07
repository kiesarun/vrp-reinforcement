from dotenv import load_dotenv

load_dotenv()
from flask import Flask, Response, request
from connectDB import connectOrdersDB
from clusterByKmean import clusterByKmean
from travellingSales import travellingSales
from prepareData import prepareData
from bson.json_util import dumps
import traceback

app = Flask(__name__)


@app.route('/', methods=['POST'])
def path():
    try:
        data = request.form
        print(data)
        db = connectOrdersDB()
        orders = db['orders'].find()

        if data['solution'] == 'kmean':
            coordinates = []
            for order in orders:
                coordinates.append({
                    'id': order['_id'],
                    'coor': order['coordinates']
                })
            n = int(data['numberOfCars'])
            cars = clusterByKmean(coordinates, n)
            # print(cars)
            # for i in range(n):
            #     prepared_data = prepareData(cars,i)
            #     # print('prepared_data:', prepared_data)
            #     delivery_order = travellingSales(prepared_data)
            #     # print('delivery_order:', delivery_order)

            db = connectOrdersDB()
            for c in cars:
                db['orders'].update_one({"_id": c['id']}, {"$set": {"carNumber": int(c['carNumber'])}})
                # db['orders'].update_one({"_id": c['id']}, {"$set": {"carNumber": int(c['carNumber'])},{"deliveryNo": int(c['delivery_No'])}})

        return 'success'

    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
