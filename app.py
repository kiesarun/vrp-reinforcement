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
        db = connectOrdersDB()
        orders = db['orders'].find()

        if data['solution'] == 'kmean':
            coordinates = []
            # prepared_data = []
            for order in orders:
                coordinates.append({
                    'id': order['_id'],
                    'coor': order['coordinates']
                })
            number_of_cars = int(data['numberOfCars'])
            grouped_cars = clusterByKmean(coordinates, number_of_cars) 

            for num in range(number_of_cars):    
                # prepared_data.append(prepareData(grouped_cars,num))
                prepared_data = prepareData(grouped_cars,num)
                # print('preeeeeeeeepareeeeeeedddd :::::::::::::: ', preoared_data)
                travellingSales(prepared_data)

            db = connectOrdersDB()
            # for c in grouped_cars:
                # db['orders'].update_one({"_id": c['id']}, {"$set": {"carNumber": int(c['carNumber'])}})

            # for i in range(number_of_cars):
            #     delivery = 0
            #     for c in grouped_cars:
            #         if c['carNumber'] == i:
            #             delivery = delivery+1
            #             print(c['carNumber'], i)
            #             db['orders'].update_one({"_id": c['id']}, {"$set": {"carNumber": int(c['carNumber'])}})
            #             db['orders'].update_one({"_id": c['id']}, {"$set": {"deliveryOrder": delivery}})

        return 'success'

    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
