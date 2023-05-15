from socket import socket
from socketserver import UDPServer, DatagramRequestHandler
from weakref import WeakValueDictionary

from Player import Player
from Game import Game
from Protocols import Movement, getMovementData, MAX_PLAYERS


class GameServer(UDPServer):
    allow_reuse_address = True
    allow_reuse_port = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.PlayerList: WeakValueDictionary[tuple[str, int], Player] = WeakValueDictionary()
        self.gameInSetup: Game = None

    def verify_request(
        self, request: tuple[bytes, socket], client_address: tuple[str, int]
    ) -> bool:
        if client_address not in self.PlayerList:
            if self.gameInSetup is None:
                self.gameInSetup = Game(daemon=False)
                self.gameInSetup.start()
            player = self.gameInSetup.addPlayer(client_address)
            self.PlayerList[client_address] = player
            if player.id == MAX_PLAYERS-1:
                self.gameInSetup = None
        return True

    def server_close(self) -> None:
        if self.PlayerList:
            for thread in self.PlayerList.values():
                thread.join()


class Dispatcher(DatagramRequestHandler):
    def handle(self) -> None:
        gameServer: GameServer = self.server
        movement: Movement = getMovementData(self.rfile.readline().strip())
        player = gameServer.PlayerList[self.client_address]
        player.move(movement)
        self.wfile.write(player.id.to_bytes(2, "big"))
