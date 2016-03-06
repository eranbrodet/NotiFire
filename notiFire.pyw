from functools import partial
from multiprocessing import Process, freeze_support
from socket import gethostname
from time import sleep

from logger import logger
from notiFireClient import NotiFireClient
from notiFireDb import NotiFireDb
from notiFireServer import NotiFireServer
from screenSplasher import splash
from windowsUI import UI


class NotiFire(object):
    def __init__(self):
        self.name = None

    def _run_server(self, name, port):
        server = NotiFireServer(port, name, splash.info)
        server.start()

    def _register(self, name, port):
        my_address = gethostname()
        NotiFireDb.register(name, my_address, port, old_name=self.name)
        self.name = name
        logger.info("new name %s" % (name,))

    def _register_infinite(self, name, port):
        while True:
            try:
                logger.info("_register_infinite running with %s %s" % (name, port))
                self._register(name, port)
            except ValueError:
                pass  # Ignoring when we are trying to register the same name again
            finally:
                sleep(3600)  #TODO configurable time

    def _register_once(self, name, port):
        try:
            self._register(name, port)
            return True
        except ValueError:
            splash.warning("Name already taken")
            return False

    @staticmethod
    def _pinger(name, recipient):
        try:
            address, port = NotiFireDb.get_address(recipient)
            port = int(port)
            NotiFireClient(name).ping_user(port, address, recipient)
            return True
        except KeyError:
            NotiFireDb.remove(recipient)
            return False

    def main(self):
        freeze_support()  #TODO needed? what does it do?
        #TODO fail gracefully if port is taken
        logger.info("Starting")

        port = 60053
        name = ""
        registered = False
        try:
            while not registered:
                name = UI().get_name()
                if name is None:
                    return
                registered = self._register_once(name, port)  # Ensure we registered before starting the server
            # We set a process to register every so often in order to update in case of address change
            register_process = Process(target=self._register_infinite, args=(name, port))
            server_process = Process(target=self._run_server, args=(name, port))
            register_process.start()
            server_process.start()

            UI().main_window(name, partial(self._pinger, name))
            logger.info("After UI")
            register_process.terminate()
            server_process.terminate()
        finally:
            if name is not None:
                NotiFireDb.remove(name)
            logger.info("Bye bye")


if __name__ == "__main__":
    NotiFire().main()
