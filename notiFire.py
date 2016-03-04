from multiprocessing import Process, freeze_support
from socket import gethostname
from time import sleep
from notiFireDb import NotiFireDb
from notiFireClient import NotiFireClient
from notifireServer import NotifireServer
from screenSplasher import splash


def run_server():
    server = NotifireServer(60053, "Eran", splash.show)  #TODO configurable name
    server.start()


def register():
    while True:
        NotiFireDb.register("Eran", gethostname())
        sleep(3600)  #TODO configurable time


if __name__ == "__main__":
    #TODO use logger instead of print
    freeze_support()  #TODO needed? what does it do?
    Process(target=register).start()
    Process(target=run_server).start()
    #TODO Run UI that lists available clients and allows to ping them
