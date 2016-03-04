from select import select
from socket import socket, AF_INET, SOCK_DGRAM
from notiFireProtocol import NotiFireProtocol


class UdpReceiver(object):
    def __init__(self, s):
        self.data = s.recv(1024)
        print "Received data size %s" % (len(self.data),)

    def receive(self, size):
        print "Receive with size %s" % (size,)
        ret = self.data[:size]
        self.data = self.data[size:]
        return ret


class NotifireServer(object):
    def __init__(self, port, my_name, callback):
        self.port = port
        self.protocol = NotiFireProtocol(my_name)
        self.callback = callback

    def start(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', self.port))
        self.socket.setblocking(0)

        while True:
            result = select([self.socket], [], [])
            self.handle_result(result)

    def handle_result(self, select_result):
        sender = self.protocol.pong(UdpReceiver(select_result[0][0]))
        if sender is not None:
            self.callback(sender)
