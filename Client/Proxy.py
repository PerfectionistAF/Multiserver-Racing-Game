from threading import Thread
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from socket import create_connection, socket, AF_INET, SOCK_STREAM, SOCK_DGRAM

from Protocols import *


class Proxy(Thread):
    def __init__(self, addr: int = None, *args, **kwargs) -> None:
        super().__init__(name="ServerProxy",*args, **kwargs)
        self.addr = addr
        self.playerCount: int = None
        self.running = False
        self.state = GameState.MainMenu
        self.messagesQueue = []
        self.movement: Movement = [0, 0]
        self.sel = DefaultSelector()

    def close(self) -> None:
        self.running = False

    def move(self, movement: Movement) -> None:
        self.movement = movement

    def TCPHandel(self, sock: socket, mask):
        try:
            data = sock.recv(4096)
            if data:
                packet = data.decode(errors="ignore")
                messageType = packet[0]
                message = packet[1:]
                if messageType == "b":
                    self.messagesQueue.append(message)
                elif message == "w":
                    winner = message
                    self.state = GameState.GameEnd
        except:
            print("connection to server lost?")

    def connectToServer(self, sock: socket, mask):
        data = sock.recv(4096)
        if data:
            self.playerCount: int = int.from_bytes(data)
            self.sel.modify(sock, EVENT_READ, self.TCPHandel)
            self.LatestSnapshot: GameSnapshot = [
                (100, 100 + i * 10, 0) for i in range(self.playerCount)
            ]
            self.state = GameState.GameSetup

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
        self.running = True
        try:
            self.TCP_socket = create_connection(
                address=(HOST, PORT),
                timeout=10,
                source_address=self.addr,
            )
            self.UDP_socket = socket(AF_INET, SOCK_DGRAM)
            self.UDP_socket.bind(self.TCP_socket.getsockname())
            self.sel.register(self.TCP_socket, EVENT_READ, self.connectToServer)
            self.sel.register(self.UDP_socket, EVENT_READ | EVENT_WRITE, self.UDPHandle)
        except Exception as e:
            print("server not available")
        while self.running:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
        self.TCP_socket.close()
        self.UDP_socket.close()
        self.sel.close()
