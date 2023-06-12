from time import time
from socket import socket
from random import randint
from threading import Thread
from multiprocessing import Pipe
from multiprocessing.pool import AsyncResult, Pool
from multiprocessing.connection import Connection
from selectors import DefaultSelector

import Game
from Player import Player
from Protocols import *


class GameFactory(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name="GameFactory",*args, **kwargs)
        self.running = True
        self.sel = DefaultSelector()
        self.AddressGameMap: dict[Address, Connection] = {}
        self.AddressSocketMap: dict[Address, socket] = {}
        self.playerQueue: list[Address] = []

    def addPlayer(self, addr: Address) -> None:
        if addr not in self.AddressGameMap and addr not in self.playerQueue:
            self.playerQueue.append(addr)
        else:
            self.openGame(addr)

    def getPlayers(self, addr: Address) -> list[Address]:
        players: list[Address] = []
        playerGame = self.AddressGameMap.get(addr)
        if playerGame:
            players = [
                player
                for player, game in self.AddressGameMap.items()
                if game == playerGame
            ]
        return players

    def openGame(self, *players: Address):
        playerCount = len(players)
        for addr in players:
            conn = self.AddressSocketMap[addr]
            conn.send(playerCount.to_bytes(2))

    def closeGame(self, result: AsyncResult[dict[Address, Player]]):
        # TO-DO: implement logic to find the player with the highest score
        winner = randint(0, len(result))
        for addr in result.keys():
            conn = self.AddressSocketMap[addr]
            pipe = self.AddressGameMap[addr]
            try:
                conn.sendall(("w" + str(winner)).encode())
            except:
                pass
            self.sel.unregister(conn)
            conn.close()
            pipe.close()
            del self.AddressGameMap[addr]
            del self.AddressSocketMap[addr]

    def close(self) -> None:
        self.running = False

    def run(self) -> None:
        gamePool = Pool(processes=2)
        lastGameCreated = time()
        FORCE_START_TIMER = 10
        while self.running:
            curr = time()
            delta = curr - lastGameCreated
            if len(self.playerQueue) >= MAX_PLAYERS or (
                delta >= FORCE_START_TIMER and len(self.playerQueue) > 0
            ):
                p1, p2 = Pipe(duplex=False)
                players = self.playerQueue[:MAX_PLAYERS]
                self.playerQueue = self.playerQueue[MAX_PLAYERS:]
                self.openGame(*players)
                gamePool.apply_async(
                    func=Game.run,
                    args=(players, p1),
                    callback=self.closeGame,
                )
                for addr in players:
                    self.AddressGameMap[addr] = p2
                lastGameCreated = time()
        gamePool.join()
