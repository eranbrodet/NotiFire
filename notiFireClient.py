from contextlib import closing
from socket import socket
from logger import logger
from notiFireProtocol import NotiFireProtocol


class NotiFireClient(object):
    def __init__(self, my_name):
        self.protocol = NotiFireProtocol(my_name)
        logger.debug("Creating client with name %s" % (my_name,))

    def ping_user(self, port, recipient_address, recipient_name):
        logger.debug("Called with %s %s %s" % (recipient_address, port, recipient_name))
        with closing(socket()) as connection:
            connection.connect((recipient_address, port))
            self.protocol.ping(connection, recipient_name)
        logger.info("Pinged %s" % (recipient_name))
