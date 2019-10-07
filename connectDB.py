from pymongo import MongoClient

_db = None


def connectDB():
    global _db
    if _db is not None:
        return _db
    else:
        connect = MongoClient("localhost", 27017)
        _db = connect.get_database("orderDB")
        return _db
