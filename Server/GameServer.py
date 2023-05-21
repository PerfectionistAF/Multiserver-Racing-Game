from socket import socket
from socketserver import UDPServer, DatagramRequestHandler
from weakref import WeakValueDictionary

from Game import Game
from Protocols import GameState, getData


class GameServer(UDPServer):
    allow_reuse_address = True
    allow_reuse_port = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.PlayerList: WeakValueDictionary[
            tuple[str, int], Game
        ] = WeakValueDictionary()
        self.gameInSetup: Game = None

    def verify_request(
        self, request: tuple[bytes, socket], client_address: tuple[str, int]
    ) -> bool:
        if client_address not in self.PlayerList:
            if (
                self.gameInSetup is None
                or not self.gameInSetup.is_alive()
                or self.gameInSetup.state is not GameState.GameSetup
            ):
                self.gameInSetup = Game()
                self.gameInSetup.start()
            self.gameInSetup.addPlayer(client_address)
            self.PlayerList[client_address] = self.gameInSetup
        if self.PlayerList[client_address].state is not GameState.GamePlay:
            return False
        return True

    def server_close(self) -> None:
        if self.PlayerList:
            for thread in self.PlayerList.values():
                thread.join()


class Dispatcher(DatagramRequestHandler):
    def handle(self) -> None:
        gameServer: GameServer = self.server
        game = gameServer.PlayerList[self.client_address]
        state, data = getData(self.rfile.readline().strip())
        if state is GameState.GamePlay:
            game.move(data, self.client_address)
