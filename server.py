from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from server_client import ServerClient


class Server:
    clients = {}
    addresses = {}

    def __init__(self, port):
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('', port))

    def start(self):
        self.sock.listen(5)
        print("Server started")
        accept_thread = Thread(target=self.accept_incoming_connections)
        accept_thread.start()

    def close(self):
        self.sock.close()

    def accept_incoming_connections(self):
        while True:
            client, client_address = self.sock.accept()
            print("%s:%s has connected" % client_address)
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, sock):
        cid = len(self.clients)
        client = ServerClient(sock, cid)
        self.clients[cid] = client

    def broadcast(self, msg):
        for client in self.clients:
            client.send_str(msg)
