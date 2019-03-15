from pymongo import MongoClient


def init(user, passwd):
    client = MongoClient("mongodb+srv://mrvansork:B00le@cluster0-ajhuk.mongodb.net/test?retryWrites=true")
    return client.axon
