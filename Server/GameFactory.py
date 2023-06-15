from time import time
from random import randint
from socket import socket
from threading import Thread
from selectors import DefaultSelector

from Game import Game
from Player import Player
from Protocols import *


class GameFactory(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='GameFactory', *args, **kwargs)
        self.running = True
        self.queueStartTime = float('inf')
        self.sel = DefaultSelector()
        self.AddressDispatchMap: dict[Address, Game] = {}
        self.AddressSocketMap: dict[Address, socket] = {}
        self.PlayerPlayersMap: dict[Address, list[Address]] = {}
        self.playerQueue: list[Address] = []

    def addPlayer(self, addr: Address) -> None:
        if addr not in self.AddressDispatchMap and addr not in self.playerQueue:
            if len(self.playerQueue) == 0:
                self.queueStartTime = time()
            self.playerQueue.append(addr)
        else:
            self.signalGameStart(addr)

    def getPeers(self, addr: Address) -> list[Address]:
        return self.PlayerPlayersMap[addr]

    def signalGameStart(self, *players: Address):
        playerCount = len(players)
        for addr in players:
            conn = self.AddressSocketMap[addr]
            conn.send(playerCount.to_bytes(2))

    def gameClose(self, result: dict[Address, Player]):
        # TO-DO: implement logic to find the player with the highest score
        winner = randint(0, len(result) - 1)
        print('Game Ended')
        for addr in result.keys():
            conn = self.AddressSocketMap[addr]
            try:
                conn.send(''.join(['w', str(winner)]).encode())
            except Exception as e:
                print(f'player at {addr} cannot be reached: {e}')
            conn.close()
            self.sel.unregister(conn)
            del self.AddressSocketMap[addr]
            del self.AddressDispatchMap[addr]
            del self.PlayerPlayersMap[addr]

    def gameError(self, e: Exception):
        print(f'Game Error: {e}')

    def close(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            if len(self.playerQueue) >= MAX_PLAYERS or (
                time() - self.queueStartTime >= QUEUE_MAX_TIME
            ):
                print('creating game')
                players = self.playerQueue[:MAX_PLAYERS]
                self.playerQueue = self.playerQueue[MAX_PLAYERS:]
                game = Game(
                    playerAddresses=players,
                    callback=self.gameClose,
                    error_callback=self.gameError,
                )
                game.start()
                dispatchers = {addr: game for addr in players}
                self.AddressDispatchMap.update(dispatchers)
                for addr in players:
                    self.PlayerPlayersMap[addr] = players
                self.signalGameStart(*players)
                self.queueStartTime = float('inf')
