from time import time
from random import randint
from socket import socket, SHUT_RDWR
from threading import Thread
from selectors import DefaultSelector
from weakref import WeakValueDictionary

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
        self.AddressConnectionMap: dict[Address, socket] = WeakValueDictionary()
        self.PlayerPlayersMap: dict[Address, list[Address]] = {}
        self.playerQueue: list[Address] = []

    def addPlayer(self, addr: Address) -> None:
        if addr not in self.playerQueue:
            if addr not in self.AddressDispatchMap:
                print(f'New player from {addr}')
                self.playerQueue.append(addr)
                if len(self.playerQueue) == 1:
                    self.queueStartTime = time()
            else:
                playerCount = len(self.PlayerPlayersMap[addr])
                self.signalGameStart(addr, playerCount=playerCount)

    def removePlayer(self, sock: socket):
        self.sel.unregister(sock)
        sock.shutdown(SHUT_RDWR)
        sock.close()

    def getPeers(self, addr: Address) -> list[Address]:
        return self.PlayerPlayersMap[addr]

    def signalGameStart(self, *players: Address, playerCount: int):
        for addr in players:
            conn = self.AddressConnectionMap.get(addr)
            if conn:
                conn.send(playerCount.to_bytes(2))

    def gameClose(self, result: dict[Address, Player]):
        # TO-DO: implement logic to find the player with the highest score
        winner = randint(0, len(result) - 1)
        for addr in result.keys():
            print(f'Game Ended for {addr}')
            conn = self.AddressConnectionMap.get(addr)
            if conn:
                try:
                    conn.send(''.join(['w', str(winner)]).encode())
                except Exception as e:
                    print(f'player at {addr} cannot be reached: {e}')
                self.removePlayer(conn)
                del self.AddressConnectionMap[addr]
            del self.AddressDispatchMap[addr]
            del self.PlayerPlayersMap[addr]

    def gameError(self, e: Exception):
        print(f'game error: {e}')

    def close(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            playersInQueue = len(self.playerQueue)
            if playersInQueue >= MAX_PLAYERS or (
                (time() - self.queueStartTime) >= QUEUE_MAX_TIME
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
                self.signalGameStart(*players, playerCount=len(players))
                self.queueStartTime = float('inf')
