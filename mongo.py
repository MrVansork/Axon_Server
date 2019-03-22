from pymongo import MongoClient


class Mongo:
    DB = None

    @staticmethod
    def init(user, passwd):
        client = MongoClient(
            "mongodb+srv://" + user + ":" + passwd + "@cluster0-ajhuk.mongodb.net/test?retryWrites=true")
        Mongo.DB = client.axon
        print("Mongo connection initialized")
        return client.axon
