from bson.json_util import dumps

from constants import BIG_TITLE
from server import Server

import mongo

def main():
    print("__________________________________")
    print(BIG_TITLE)
    print("__________________________________\n")
    # server = Server(8192)
    # server.start()
    db = mongo.init("mrvansork", "B00le")
    user = dumps(db.user.find_one())
    print(user)



if __name__ == "__main__":
    main()
