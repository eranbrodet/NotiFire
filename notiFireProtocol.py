from struct import pack, unpack, calcsize


class NotiFireProtocol(object):   #TODO document
    #TODO consider going back to just sending the sender's name
    HEADER_TYPE = "!II"
    HEADER_SIZE = calcsize(HEADER_TYPE)

    def __init__(self, my_name):
        self.my_name = my_name

    def ping(self, connection, name):
        #TODO can't handle unicode
        data = pack(self.HEADER_TYPE, len(name), len(self.my_name)) + name + self.my_name
        connection.send(data)

    def pong(self, connection):
        recipient_length, sender_length = unpack(self.HEADER_TYPE, connection.receive(self.HEADER_SIZE))
        recipient = connection.receive(recipient_length)
        sender = connection.receive(sender_length)
        print "Ponged from %s to %s" % (sender, recipient)
        return recipient

def unit_test():
    class ConnectionMock(object):
        def send(self, data): self.data = data;
        def receive(self, len):
            ret, self.data = self.data[:len], self.data[len:]
            return ret

    sender = "sender"
    c = ConnectionMock()
    p = NotiFireProtocol(sender)
    p.ping(c, sender)
    got = p.pong(c)
    if sender != got:
        raise Exception("got %s instead of %s" % (got, sender))


if __name__ == "__main__":
    unit_test()
