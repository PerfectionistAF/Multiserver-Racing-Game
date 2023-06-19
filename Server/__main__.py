import atexit

from GameServer import GameServer


def exit_handler():
    global gameServer
    gameServer.close()


if __name__ == '__main__':
    atexit.register(exit_handler)
    gameServer = GameServer()
    gameServer.start()
    gameServer.close()
