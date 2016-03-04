from contextlib import closing
from socket import socket
from notiFireProtocol import NotiFireProtocol


class NotiFireClient(object):
    def __init__(self, my_name):
        self.protocol = NotiFireProtocol(my_name)

    def ping_user(self, port, recipient_address, recipient_name):
        print recipient_address, port, recipient_name
        with closing(socket()) as connection:
            connection.connect((recipient_address, port))
            self.protocol.ping(connection, recipient_name)
        print "Pinged " + recipient_name
