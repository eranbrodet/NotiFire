from contextlib import closing
from socket import socket, gethostname
from notiFireProtocol import NotiFireProtocol


class Receiver(object):
    def __init__(self, connection):
        self.connection = connection

    def receive(self, size):
        return self.connection.recv(size)


class NotifireServer(object):
    def __init__(self, port, my_name, callback):
        self.port = port
        self.protocol = NotiFireProtocol(my_name)
        self.callback = callback

    def start(self):
        with closing(socket()) as self.socket:
            host = gethostname()
            self.socket.bind((host, self.port))        # Bind to the port
            self.socket.listen(5)                 # Now wait for client connection.
            while True:
               connection, addr = self.socket.accept()     # Establish connection with client.
               self.handle_result(connection)

    def handle_result(self, connection):
        sender = self.protocol.pong(Receiver(connection))
        if sender is not None:
            self.callback(sender)
