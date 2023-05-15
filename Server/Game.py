from time import time
from math import sin, cos, radians
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, SO_REUSEADDR, SOL_SOCKET

from Player import Player
from Protocols import GameSnapshot, dumpGameSnapshotData, TICK_RATE, HOST, PORT


class Game(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.playerList: dict[tuple[str, int], Player] = {}
        self.soc = socket(AF_INET, SOCK_DGRAM)
        self.soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.soc.bind((HOST, PORT))

    def addPlayer(self, addr: tuple[str, int]) -> Player:
        player = Player(self.counter)
        self.playerList[addr] = player
        self.counter += 1
        return player

    def _createSnapshot(self) -> GameSnapshot:
        l = sorted(self.playerList.values(), key=lambda player: player.id)
        return [(player.x, player.y, player.deg) for player in l]

    def run(self) -> None:
        prevTime = time()
        while self.playerList:
            currTime = time()
            if currTime - prevTime >= 1000 / TICK_RATE:
                snapshot = self._createSnapshot()
                data = dumpGameSnapshotData(snapshot)
                for addr in self.playerList.keys():
                    self.soc.sendto(data, addr)
                prevTime = currTime
