from threading import Thread
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from socket import create_connection, socket, AF_INET, SOCK_STREAM, SOCK_DGRAM

from Protocols import *


class Proxy(Thread):
    def __init__(
        self,
        mailBoxIn: list[str],
        mailBoxOut: list[str],
        addr: int = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(name='ServerProxy', *args, **kwargs)
        self._initProxy()
        self.addr = addr
        self.mailBoxIn = mailBoxIn
        self.mailBoxOut = mailBoxOut

    def close(self) -> None:
        self.running = False
        self.state = GameState.GameEnd

    def move(self, movement: Movement) -> None:
        self.movement = movement

    def TCPHandel(self, sock: socket, mask):
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
            except Exception as e:
                print(f'connection to server lost: {e}')
                self.close()

    def connectToServer(self, sock: socket, mask):
        try:
            data = sock.recv(4096)
            if data:
                self.playerCount: int = int.from_bytes(data)
                self.sel.modify(sock, EVENT_READ | EVENT_WRITE, self.TCPHandel)
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
        self.running = True
        try:
            self._initSockets()
            while self.running:
                events = self.sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
            self.TCP_socket.close()
            self.UDP_socket.close()
        except Exception as e:
            print(f'cannot connect to server: {e}')
            self.close()
        finally:
            self.sel.close()

    def _initSockets(self):
        self.TCP_socket = create_connection(
            address=(HOST, PORT),
            timeout=10,
            source_address=self.addr,
        )
        self.UDP_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_socket.bind(self.TCP_socket.getsockname())
        self.sel.register(self.TCP_socket, EVENT_READ, self.connectToServer)
        self.sel.register(self.UDP_socket, EVENT_READ | EVENT_WRITE, self.UDPHandle)

    def _initProxy(self):
        self.movement: Movement = [0, 0]
        self.running = False
        self.playerCount: int = None
        self.state = GameState.MainMenu
        self.sel = DefaultSelector()
