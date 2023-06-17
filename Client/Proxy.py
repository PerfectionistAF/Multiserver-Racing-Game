from time import sleep
from sys import argv
from threading import Thread
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, SO_REUSEADDR, SOL_SOCKET

from Protocols import *


class Proxy(Thread):
    def __init__(
        self,
        mailBoxIn: list[str],
        mailBoxOut: list[str],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(name='ServerProxy', *args, **kwargs)
        self._initProxy()
        self.addr: Address = (
            ('localhost', int(argv[1])) if len(argv) == 2 else ('localhost', 0)
        )
        self.mailBoxIn = mailBoxIn
        self.mailBoxOut = mailBoxOut

    def close(self) -> None:
        if self.running:
            self.running = False
            self.sel.unregister(self.TCP_socket)
            self.sel.unregister(self.UDP_socket)
            if self.state is not GameState.GameEnd:
                self.TCP_socket.detach()
            else:
                # wait shutdown signal from server to avoid [WinError 10048]
                sleep(3)
            self.UDP_socket.close()
            self.sel.close()
        self.closed = True
        self.state = GameState.GameEnd

    def move(self, movement: Movement) -> None:
        self.movement = movement

    def TCPHandle(self, sock: socket, mask):
        if self.mailBoxOut and mask & EVENT_WRITE:
            try:
                for message in self.mailBoxOut:
                    sock.send(message.encode())
                self.mailBoxOut.clear()
            except Exception as e:
                print(f'failed to send message: {e}')
        if mask & EVENT_READ:
            try:
                data = sock.recv(4096)
                if data:
                    messageType, message = decodeMessage(data)
                    if messageType == 'b':
                        self.mailBoxIn.append(message)
                    elif messageType == 'w':
                        winner = message
                        print(f'THE WINNER IS : {winner}')
                        self.state = GameState.GameEnd
                        self.close()
            except Exception as e:
                print(f'connection to server lost: {e}')
                self.close()

    def connectToServer(self, sock: socket, mask):
        try:
            data = sock.recv(4096)
            if data:
                self.playerCount: int = int.from_bytes(data)
                self.sel.modify(sock, EVENT_READ | EVENT_WRITE, self.TCPHandle)
                self.LatestSnapshot: GameSnapshot = [
                    [100, 100 + i * 10, 0] for i in range(self.playerCount)
                ]
                self.state = GameState.GameSetup
        except Exception as e:
            print(f'cannot connect to server: {e}')
            self.close()

    def UDPHandle(self, sock: socket, mask):
        if mask & EVENT_READ:
            data, _ = sock.recvfrom(4096)
            if data:
                self.LatestSnapshot = getData(data)
        if mask & EVENT_WRITE:
            if self.movement != [0, 0]:
                data = dumpData(self.movement)
                sock.sendto(data, (HOST, PORT))
                self.movement = [0, 0]

    def run(self) -> None:
        try:
            self._initSockets()
            self.running = True
            while self.running:
                events = self.sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        except Exception as e:
            print(f'cannot connect to server: {e}')
        finally:
            self.close()

    def _initSockets(self):
        self.TCP_socket = socket(AF_INET, SOCK_STREAM)
        self.TCP_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.TCP_socket.bind(self.addr)
        self.TCP_socket.connect((HOST, PORT))
        self.sel.register(self.TCP_socket, EVENT_READ, self.connectToServer)

        self.UDP_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.UDP_socket.bind(self.TCP_socket.getsockname())
        self.sel.register(self.UDP_socket, EVENT_READ | EVENT_WRITE, self.UDPHandle)

    def _initProxy(self):
        self.movement: Movement = [0, 0]
        self.running = False
        self.closed = False
        self.playerCount: int = None
        self.state = GameState.MainMenu
        self.sel = DefaultSelector()
