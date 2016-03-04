from contextlib import closing
from socket import socket
from notiFireProtocol import NotiFireProtocol


class NotiFireClient(object):
    def __init__(self, port, my_name):
        self.port = port
        self.protocol = NotiFireProtocol(my_name)

    def ping_user(self, recipient_address, recipient_name):
        with closing(socket()) as connection:
            connection.connect((recipient_address, self.port))
            self.protocol.ping(connection, recipient_name)
        print "Pinged " + recipient_name
