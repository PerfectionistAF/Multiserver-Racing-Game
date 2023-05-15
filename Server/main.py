from GameServer import GameServer, Dispatcher
from Protocols import HOST, PORT


if __name__ == "__main__":
    with GameServer((HOST, PORT), Dispatcher) as gameServer:
        gameServer.serve_forever()
