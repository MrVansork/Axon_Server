from mongo import Mongo
from constants import BIG_TITLE
from server import Server

import bcrypt


def main():
    print("__________________________________")
    print(BIG_TITLE)
    print("__________________________________\n")
    Mongo.init("mrvansork", "B00le")
    server = Server(8192)
    server.start()


if __name__ == "__main__":
    main()
