from selectors import EVENT_READ
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

from GameFactory import GameFactory
from Protocols import *


class GameServer:
    def __init__(self) -> None:
        self.TCP_socket = socket(AF_INET, SOCK_STREAM)
        self.TCP_socket.bind((HOST, PORT))
        self.TCP_socket.listen()
        self.UDP_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_socket.bind((HOST, PORT))

        self.gameFactory = GameFactory()
        self.gameFactory.sel.register(self.TCP_socket, EVENT_READ, self.TCPHandler)
        self.gameFactory.sel.register(self.UDP_socket, EVENT_READ, self.UDPHandler)

    def TCPHandler(self, sock: socket, mask) -> None:
        client_socket, client_address = sock.accept()
        self.gameFactory.sel.register(client_socket, EVENT_READ, self.ChatHandler)
        self.gameFactory.AddressConnectionMap[client_address] = client_socket
        self.gameFactory.addPlayer(client_address)

    def ChatHandler(self, sock: socket, mask) -> None:
        try:
            data = sock.recv(4096)
            addr: Address = sock.getpeername()
            if data and addr in self.gameFactory.PlayerPlayersMap:
                self.Broadcast(data.decode(), addr, self.gameFactory.getPeers(addr))
        except Exception as e:
            print(f'player disconnected: {e}')
            self.gameFactory.removePlayer(sock)

    def Broadcast(
        self, message: str, fromAddress: Address, toList: list[Address]
    ) -> None:
        for client_address in toList:
            if (
                client_address != fromAddress
                and client_address in self.gameFactory.AddressConnectionMap
            ):
                client_socket = self.gameFactory.AddressConnectionMap[client_address]
                try:
                    client_socket.send(''.join(['b', message]).encode())
                except Exception as e:
                    print(f'error broadcasting message: {e}')
                    self.gameFactory.sel.unregister(client_socket)
                    client_socket.close()

    def UDPHandler(self, sock: socket, mask) -> None:
        addr: Address
        data, addr = sock.recvfrom(4096)
        game = self.gameFactory.AddressDispatchMap.get(addr)
        if game:
            movement = getData(data)
            game.move(movement, addr)

    def close(self) -> None:
        self.running = False
        self.TCP_socket.close()
        self.UDP_socket.close()
        self.gameFactory.close()
        self.gameFactory.join()
        print('server closed')

    def start(self) -> None:
        print('server started')
        self.gameFactory.start()
        self.running = True
        while self.running:
            events = self.gameFactory.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
