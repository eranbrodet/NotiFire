from multiprocessing import Process, freeze_support, Value, Array
from random import randint
from socket import gethostname
from time import sleep
from notiFireDb import NotiFireDb
from notiFireClient import NotiFireClient
from notifireServer import NotifireServer
from screenSplasher import splash
from windowsUI import MainWindow


class NotiFire(object):
    def _run_server(self):
        server = NotifireServer(self.port.value, self.name.value, splash.show)
        server.start()

    def _register(self, name, port):
        my_address = gethostname()
        NotiFireDb.register(name, my_address, port, old_name=self.name.value)
        self.name.value = name
        print "new name", self.name.value

    def _register_infinite(self):
        while True:
            try:
                print "_register_infinite running with ", self.name.value, self.port.value
                self._register(self.name.value, self.port.value)
            except ValueError:
                pass  # Ignoring when we are trying to register the same name again
            finally:
                sleep(10)  #TODO configurable time

    def _register_once(self, name, port):
        try:
            self._register(name, port)
            return True
        except ValueError:
            splash.warning("Name already take")
            return False

    def _pinger(self, recipient):
        try:
            address, port = NotiFireDb.get_address(recipient)
            port = int(port)
            NotiFireClient(self.name.value).ping_user(port, address, recipient)
            return True
        except KeyError:
            NotiFireDb.remove(recipient)
            return False

    def main(self):
        self.name = Array('c', "Anonymous_%s" % (randint(0, 1024),))
        self.port = Value('i', 60053)
        #TODO use logger instead of print
        freeze_support()  #TODO needed? what does it do?
        #TODO will it always register the same name here?

        self._register_once(self.name.value, self.port.value)  # Ensure we registered before starting the server
        register_process = Process(target=self._register_infinite)  #TODO variables aren't shared accross processes
        server_process = Process(target=self._run_server)
        register_process.start()
        server_process.start()

        MainWindow(self.port.value, self.name.value, self._register_once, self._pinger).show()

        print "Shutting down"
        register_process.terminate()
        server_process.terminate()
        NotiFireDb.remove(self.name.value)


if __name__ == "__main__":
    NotiFire().main()