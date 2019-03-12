from threading import Thread
from constants import *


def process(message):
    if message.startswith(LOGIN_TAG):
        try:
            user = message.split(LOGIN_TAG)[1]
            print(user)
        except:
            print("Error receiving login data")

    elif message.startswith(SIGNUP_TAG):
        new_user = message.split(SIGNUP_TAG)[1]
        print(new_user)


class ServerClient:
    def __init__(self, sock, cid):
        self.sock = sock
        self.cid = cid
        self.running = True
        self.send_str("@@ID@@"+str(cid))
        self.send_str("@@LEN@@"+str(BUFFSIZE))
        Thread(target=self.receive()).start()

    def receive(self):
        while self.running:
            message = self.sock.recv(BUFFSIZE).decode("utf8")
            print("Client[" + str(self.cid) + "]: " + message)
            process(message)

    def send_str(self, message):
        self.send_bytes(bytes())
        self.send_bytes(bytes(message, "utf8"))

    def send_bytes(self, data):
        self.sock.send(data)
