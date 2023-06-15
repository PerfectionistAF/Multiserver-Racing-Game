from selectors import EVENT_READ
from socket import create_server, socket, AF_INET, SOCK_DGRAM

from GameFactory import GameFactory
from Protocols import *


class GameServer:
    def __init__(self) -> None:
        self.TCP_socket = create_server(address=(HOST, PORT), family=AF_INET)
        self.UDP_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_socket.bind((HOST, PORT))

        self.gameFactory = GameFactory()
        self.gameFactory.sel.register(self.TCP_socket, EVENT_READ, self.TCPHandler)
        self.gameFactory.sel.register(self.UDP_socket, EVENT_READ, self.UDPHandler)

    def TCPHandler(self, sock: socket, mask) -> None:
        client_socket, client_address = sock.accept()

        if client_address not in self.gameFactory.AddressSocketMap:
            print(f'New player from {client_address}')
        else:
            sock = self.gameFactory.AddressSocketMap[client_address]
            sock.close()
            self.gameFactory.sel.unregister(sock)

        self.gameFactory.addPlayer(client_address)
        self.gameFactory.AddressSocketMap[client_address] = client_socket
        self.gameFactory.sel.register(client_socket, EVENT_READ, self.ChatHandler)

    def ChatHandler(self, sock: socket, mask) -> None:
        try:
            data = sock.recv(4096)
            if data:
                addr: Address = sock.getpeername()
                if addr in self.gameFactory.PlayerPlayersMap:
                    self.Broadcast(data.decode(), addr, self.gameFactory.getPeers(addr))
        except Exception as e:
            print(f'Error receiving message: {str(e)}')
            sock.close()
            self.gameFactory.sel.unregister(sock)

    def Broadcast(
        self, message: str, fromAddress: Address, toList: list[Address]
    ) -> None:
        for client_address in toList:
            if (
                client_address != fromAddress
                and client_address in self.gameFactory.AddressSocketMap
            ):
                client_socket = self.gameFactory.AddressSocketMap[client_address]
                try:
                    client_socket.send(''.join(['b', message]).encode())
                except Exception as e:
                    print(f'Error broadcasting message: {str(e)}')
                    client_socket.close()
                    self.gameFactory.sel.unregister(client_socket)

    def UDPHandler(self, sock: socket, mask) -> None:
        addr: Address
        data, addr = sock.recvfrom(4096)
        if addr in self.gameFactory.AddressDispatchMap:
            movement = getData(data)
            game = self.gameFactory.AddressDispatchMap[addr]
            game.move(movement, addr)

    def close(self) -> None:
        self.gameFactory.sel.close()
        self.gameFactory.close()
        self.gameFactory.join()
        print('server closed')

    def start(self) -> None:
        print('server started')
        self.gameFactory.start()
        while True:
            events = self.gameFactory.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
