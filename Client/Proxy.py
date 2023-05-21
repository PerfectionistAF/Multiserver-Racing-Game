from select import select
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, SO_REUSEADDR, SOL_SOCKET

from Protocols import (
    GameState,
    HOST,
    PORT,
    Movement,
    GameSnapshot,
    dumpData,
    getData,
)


class Proxy(Thread):
    def __init__(self, addr=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        if addr:
            self.sock.bind((HOST, addr))
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        data = dumpData((GameState.GameSetup, 0))
        self.sock.sendto(data, (HOST, PORT))
        self.LatestSnapshot: GameSnapshot = GameSnapshot

    def waitOtherPlayers(self) -> bool:
        readyToRead, _, _ = select([self.sock], [], [], 20 / 1000)
        if readyToRead:
            data, _ = self.sock.recvfrom(1024)
            if data:
                s, self.LatestSnapshot = getData(data)
                return True
        return False

    def move(self, movement: Movement) -> None:
        data = dumpData((GameState.GamePlay, movement))
        self.sock.sendto(data, (HOST, PORT))

    def run(self) -> None:
        sock = self.sock.dup()
        ticks = 0
        while ticks < 10:
            data, _ = sock.recvfrom(4096)
            if data:
                ticks = 0
                packet = getData(data)
                if packet[0] is GameState.GameEnd:
                    packet[1]
                    break
                self.LatestSnapshot = packet[1]
            else:
                ticks = ticks + 1
