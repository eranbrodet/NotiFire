from contextlib import closing
from socket import socket, gethostname
from logger import logger
from notiFireProtocol import NotiFireProtocol


class ReceiveAdapter(object):
    """
        We use an adapter since our protocol requires a receive method instead of recv
    """
    def __init__(self, connection):
        self.connection = connection

    def receive(self, size):
        return self.connection.recv(size)


class NotiFireServer(object):
    def __init__(self, port, my_name, callback):
        self.port = port
        self.protocol = NotiFireProtocol(my_name)
        self.callback = callback
        logger.debug("Creating server with name %s" % (my_name,))

    def start(self):
        logger.info("Starting Server")
        with closing(socket()) as self.socket:
            host = gethostname()
            self.socket.bind((host, self.port))
            self.socket.listen(5)
            while True:
                 connection, addr = self.socket.accept()
                 self.handle_request(connection)

    def handle_request(self, connection):
        logger.debug("Handling request")
        sender = self.protocol.pong(ReceiveAdapter(connection))
        if sender is not None:
            self.callback(sender)
