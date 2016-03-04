from struct import pack, unpack, calcsize


class NotiFireProtocol(object):   #TODO document
    #TODO consider going back to just sending the sender's name
    HEADER_TYPE = "!II"
    HEADER_SIZE = calcsize(HEADER_TYPE)

    def __init__(self, my_name):
        self.my_name = my_name

    def ping(self, connection, name):
        data = pack(self.HEADER_TYPE, len(name), len(self.my_name)) + name + self.my_name
        connection.send(data)

    def pong(self, connection):
        my_name_length, name_length = unpack(self.HEADER_TYPE, connection.receive(self.HEADER_SIZE))
        print "ponged lengths", my_name_length, name_length
        recipient = connection.receive(my_name_length)
        print "ponged recipient", recipient
        if recipient == self.my_name:
            return connection.receive(name_length)


def unit_test():
    class ConnectionMock(object):
        def send(self, data): self.data = data;
        def receive(self, len):
            ret, self.data = self.data[:len], self.data[len:]
            return ret

    name = "name_"
    c = ConnectionMock()
    p = NotiFireProtocol("Local")
    p.ping(c, name)
    got = p.pong(c)
    if name != got:
        raise Exception("got %s instead of %s" % (got, name))

    p2 = NotiFireProtocol("Other")
    p.ping(c, name)
    got = p2.pong(c)
    if got is not None:
        raise Exception("got %s, but shouldn't have" % (got,))


if __name__ == "__main__":
    unit_test()
