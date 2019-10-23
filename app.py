from flask import Flask,Response,request
from connectDB import connectDB
from cluster import clusterByKmean
from bson.json_util import dumps
import traceback

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def path():
    try:
        data = request.form
        print(data)
        db = connectDB()
        orders = db['orders'].find()

        if (data['solution'] == 'kmean'):
            coordinates = []
            for order in orders:
                coordinates.append({
                    'id': order['_id'],
                    'coor': order['coordinates']
                })
            n = int(data['numberOfCars'])
            cars = clusterByKmean(coordinates,n)

        db = connectDB()
        for c in cars:
            db['orders'].update_one({"_id": c['id']}, {"$set": {"carNumber": int(c['carNumber'])}})

        return 'success'

    except Exception as e: print(e)
if __name__ == '__main__':
    app.run()
