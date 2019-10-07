from flask import Flask,Response
from connectDB import connectDB
from cluster import cluster
from bson.json_util import dumps

app = Flask(__name__)


@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/')
def bestpath():
    db = connectDB()
    orders = db['orders'].find()
    coordinates = []
    for order in orders:
        coordinates.append(order["coordinates"])

    print(coordinates)
    cluster(coordinates)
    return 'bestpath'

if __name__ == '__main__':
    app.run()
