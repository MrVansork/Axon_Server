from threading import Thread
from constants import *
from mongo import Mongo
from bson.json_util import dumps
import bcrypt

import json
import datetime


class ServerClient:
    def __init__(self, sock, cid, server):
        self.sock = sock
        self.username = None
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
        elif message.startswith(QUIT_TAG):
            self.send_str(QUIT_TAG)
            self.disconnect()
        else:
            print("Unknown: "+message)

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
        _user = data['username']
        _password = data['password']
        results = Mongo.DB['user'].find_one({"username": {"$regex": "^" + _user + "$", "$options": "i"}})
        if results is not None:
            if bcrypt.checkpw(_password.encode(), results['password']):
                self.username = _user
                self.send_str(LOGIN_TAG + OK_TAG)
                nets = self.get_nets()

                self.send_str("@@NET@@")
            else:
                self.send_str(LOGIN_TAG + FAILED_TAG)
        else:
            self.send_str(LOGIN_TAG + FAILED_TAG)

    def get_nets(self):
        results = Mongo.DB['neuralNet'].find({"collaborators": {"$regex": "^"+self.username+"$", "$options": "i"}})
        return results

    def receive(self):
        try:
            while self.running:
                message = self.sock.recv(BUFFSIZE).decode("utf8")
                self.process(message)
        except ConnectionResetError:
            self.disconnect()

    def disconnect(self):
        try:
            self.running = False
            del self.server.clients["testing"]
        except KeyError:
            print("Client with ID: {}, not found".format(str(self.cid)))
        print(str(self.sock.getsockname()) + " disconnected!")

    def send_str(self, message):
        self.sock.sendall(bytes(message + "\n", "utf8"))
