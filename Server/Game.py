from time import time
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

from Player import Player
from Protocols import *


class Game(Thread):
    def __init__(
        self,
        playerAddresses: list[Address],
        callback=None,
        error_callback=None,
        *args,
        **kwargs
    ):
        super().__init__(name='Game',*args, **kwargs)
        self.addressList: list[Address] = playerAddresses
        self.callback = callback
        self.error_callback = error_callback

    def createSnapshot(self) -> GameSnapshot:
        return [
            [player.x, player.y, player.deg]
            for player in self.AddressPlayerMap.values()
        ]

    def move(self, movement: Movement, addr: Address) -> None:
        player = self.AddressPlayerMap[addr]
        player.move(movement)

    def run(self):
        try:
            self.AddressPlayerMap: dict[Address, Player] = {
                addr: Player(id) for id, addr in enumerate(self.addressList)
            }
            soc = socket(AF_INET, SOCK_DGRAM)
            gameTimeDelta = 0.0
            gameStartTime = time()
            while gameTimeDelta <= GAME_TIME:
                data = dumpData(self.createSnapshot())
                for addr in self.addressList:
                    soc.sendto(data, addr)
                gameTimeDelta = time() - gameStartTime
            if self.callback:
                self.callback(self.AddressPlayerMap)
        except Exception as e:
            if self.error_callback:
                self.error_callback(e)
