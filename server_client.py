from threading import Thread
from constants import *
from mongo import Mongo
import bcrypt

import json
import datetime


class ServerClient:
    def __init__(self, sock, cid, server):
        self.sock = sock
        self.cid = cid
        self.server = server
        self.running = True
        self.send_str("@@ID@@" + str(cid))
        Thread(target=self.receive()).start()

    def process(self, message):
        if message.startswith(LOGIN_TAG):
            self.check_user(message)
        elif message.startswith(SIGNUP_TAG):
            self.new_user(message)
        elif message.startswith(P_KEY_TAG):
            print("KEY: {}".format(message.split(P_KEY_TAG)[1]))
        else:
            print(message)

    def new_user(self, message):
        new_user = message.split(SIGNUP_TAG)[1]
        new_user = json.loads(new_user)
        db = Mongo.DB
        count = db.user.count({"username": {"$regex": "^" + new_user['username'] + "$", "$options": "i"}})
        if count == 0:
            db.user.insert_one({
                "username": new_user['username'],
                "password": bcrypt.hashpw(new_user['password'].encode("utf8"), bcrypt.gensalt()),
                "email": new_user['email'],
                "signUpDate": datetime.datetime.utcnow()})
            self.send_str(SIGNUP_TAG + OK_TAG)
        else:
            self.send_str(SIGNUP_TAG + FAILED_TAG)

    def check_user(self, message):
        data = message.split(LOGIN_TAG)[1]
        data = json.loads(data)
        print("DATA: " + str(data))
        _user = data['username']
        _password = data['password']
        results = Mongo.DB['user'].find_one({"username": {"$regex": "^" + _user + "$", "$options": "i"}})
        print("Client: {}".format(_password.encode("utf8")))
        print("Real: {}".format(results['password']))
        if results is not None:
            if _password.encode("utf8") == results['password']:
                self.send_str(LOGIN_TAG + OK_TAG)
            else:
                print("Password incorrect")
                self.send_str(LOGIN_TAG + FAILED_TAG)
        else:
            print("Username incorrect")
            self.send_str(LOGIN_TAG + FAILED_TAG)

    def receive(self):
        try:
            while self.running:
                message = self.sock.recv(BUFFSIZE).decode("utf8")
                self.process(message)
        except ConnectionResetError:
            self.disconnect()

    def disconnect(self):
        try:
            del self.server.clients["testing"]
        except KeyError:
            print("Client with ID: {}, not found".format(str(self.cid)))
        print(str(self.sock.getsockname()) + " disconnected!")

    def send_str(self, message):
        self.sock.sendall(bytes(message + "\n", "utf8"))
