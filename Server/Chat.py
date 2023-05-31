import socket
import threading

class Server:
    def _init_(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        self.accept_connections()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_messages, args=(client_socket,)).start()

    def handle_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Received message: {message}")
                    self.broadcast(message, client_socket)
            except Exception as e:
                print(f"Error handling message: {str(e)}")
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def broadcast(self, message, sender_socket):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode())
                except Exception as e:
                    print(f"Error broadcasting message: {str(e)}")
                    client_socket.close()
                    self.clients.remove(client_socket)

if __name__ == '_main_':
    server = Server('localhost', 12345)
    server.start()