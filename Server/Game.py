from time import time
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

from Player import Player
from Protocols import GameState, TICK_RATE, MAX_PLAYERS, Movement, GameSnapshot, dumpData


class Game(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.daemon = False
        self.playerCount = 0
        self.state:GameState = GameState.GameSetup
        self.playerList: dict[tuple[str, int], Player] = {}
        self.soc = socket(AF_INET, SOCK_DGRAM)

    def addPlayer(self, addr: tuple[str, int]) -> None:
        player = Player(self.playerCount)
        self.playerList[addr] = player
        self.playerCount += 1

    def _createSnapshot(self) -> GameSnapshot:
        l = sorted(self.playerList.values(), key=lambda player: player.id)
        return [(player.x, player.y, player.deg) for player in l]

    def move(self, movement: Movement, addr: tuple[str, int]) -> None:
        player = self.playerList[addr]
        player.move(movement)

    def run(self) -> None:
        gameStartTime = time()
        while True:
            curr = time()
            delta = curr - gameStartTime
            match self.state:
                case GameState.GameSetup:
                    if self.playerCount == MAX_PLAYERS or delta >= 30:
                        self.state = GameState.GamePlay
                case GameState.GamePlay:
                    snapshot = self._createSnapshot()
                    data = dumpData(snapshot)
                    for addr in self.playerList.keys():
                        self.soc.sendto(data, addr)
                    if delta >= 90:
                        self.state = GameState.GameEnd
                case GameState.GameEnd:
                    break