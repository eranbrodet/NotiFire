from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from notiFireProtocol import NotiFireProtocol


class UdpBroadcaster(object):
    def __init__(self, s, port):
        self._port = port
        self.socket = s

    def send(self, data):
        self.socket.sendto(data, ('<broadcast>', self._port))


class NotiFireClient(object):
    def __init__(self, my_name, port):
        self.port = port
        self.protocol = NotiFireProtocol(my_name)

    def ping_user(self, recipient):
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.protocol.ping(UdpBroadcaster(s, self.port), recipient)
        print "Pinged " + recipient
