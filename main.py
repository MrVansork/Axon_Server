from server import Server
from constants import BIG_TITLE

def main():
    print("__________________________________")
    print(BIG_TITLE)
    print("__________________________________\n")
    server = Server(8192)
    server.start()


if __name__ == "__main__":
    main()
