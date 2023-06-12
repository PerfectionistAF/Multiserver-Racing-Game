from time import time
from threading import Thread
from multiprocessing.connection import Connection
from socket import socket, AF_INET, SOCK_DGRAM

from Player import Player
from Protocols import *


def createSnapshot(AddressPlayerMap: dict[Address, Player]) -> GameSnapshot:
    return [(player.x, player.y, player.deg) for player in AddressPlayerMap.values()]


def move(AddressPlayerMap: dict[Address, Player], pipe: Connection) -> None:
    while not pipe.closed:
        try:
            movement, addr = pipe.recv()
            player = AddressPlayerMap[addr]
            player.move(movement)
        except EOFError:
            pass


def run(playerList: list[Address], pipe: Connection) -> dict[Address, Player]:
    AddressPlayerMap: dict[Address, Player] = {
        itr[1]: Player(itr[0]) for itr in enumerate(playerList)
    }
    pipeHandler = Thread(target=move, args=(AddressPlayerMap, pipe), daemon=False)
    pipeHandler.start()
    soc = socket(AF_INET, SOCK_DGRAM)
    gameStartTime = time()
    while True:
        data = dumpData(createSnapshot(AddressPlayerMap))
        for addr in AddressPlayerMap:
            soc.sendto(data, addr)
        gameTimeDelta = time() - gameStartTime
        if gameTimeDelta >= GAME_TIME:
            pipe.close()
            break
    pipeHandler.join()
    return AddressPlayerMap
