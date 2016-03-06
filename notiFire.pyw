from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
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

    def main(self):
        args = self._parse_args()
        freeze_support()  #TODO needed? what does it do?
        #TODO fail gracefully if port is taken
        logger.info("Starting")

        port = 60053
        name = args.name
        registered = False
        try:
            while not registered:
                if not args.name:
                    name = UI().get_name()
                if name is None:
                    return
                registered = self._register_once(name, port)  # Ensure we registered before starting the server
                if not registered and args.name:
                    logger.error("Can't register name: " + args.name)
                    return
            if args.ping:
                try:
                    self._pinger(args.name, args.ping)
                except:
                    logger.error("Can't ping: " + args.ping)
                if not args.start_server:
                    return
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

    @staticmethod
    def _parse_args():
        parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-n", "--name", type=str, metavar="your name", default="")
        features_group = parser.add_argument_group("Features")
        features_group = features_group.add_mutually_exclusive_group()
        features_group.add_argument("--ping", "-p", type=str, metavar="person_name")
        features_group.add_argument("--start_server", "-s", action="store_true")
        args = parser.parse_args()
        if not args.name and (args.ping or args.start_server):
            parser.error("Please supply your name")
        if args.name and (not args.ping) and (not args.start_server):
            parser.error("Please choose a feature to run")
        return args


if __name__ == "__main__":
    NotiFire().main()
