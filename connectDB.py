from pymongo import MongoClient
import os

_db = None

db_host = os.getenv('DBHOST', 'localhost:27017')
db_user = os.getenv('DBUSER')
db_pass = os.getenv('DBPASS')
db_database = os.getenv('DBDATABASE', 'vrpProjectDB')
db_poolsize = os.getenv('POOLSIZE', 5)
db_authdb = os.getenv('AUTHDB')


def connectOrdersDB():
    global _db
    if _db is not None:
        return _db
    else:
        db_uri = f"mongodb://{db_user}:{db_pass}@{db_host}"
        print(db_uri)
        if db_user:
            connect = MongoClient(
                f"mongodb://{db_user}:{db_pass}@{db_host}", authSource=db_database)
        else:
            connect = MongoClient(f"mongodb://{db_host}")
        _db = connect.get_database(db_database)
        return _db
