from contextlib import closing
from socket import socket, gethostname
from notiFireProtocol import NotiFireProtocol


class NotiFireClient(object):
    def __init__(self, port, my_name):
        self.port = port
        self.protocol = NotiFireProtocol(my_name)

    def ping_user(self, recipient):
        with closing(socket()) as connection:
            connection.connect((gethostname(), self.port)) #TODO get actual host
            self.protocol.ping(connection, recipient)
        print "Pinged " + recipient
