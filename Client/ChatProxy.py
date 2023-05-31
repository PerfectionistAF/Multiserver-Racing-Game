import socket
import threading

class Client:
    def _init_(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(f"Received message: {message}")  # Update GUI here
            except Exception as e:
                print(f"Error receiving message: {str(e)}")
                self.client_socket.close()
                break

    def send_message(self, message):
        try:
            encoded_message = message.encode('utf-8')
            message_length = len(encoded_message).to_bytes(4, byteorder='big')  # Include message length for server to handle incoming messages
            self.client_socket.sendall(message_length + encoded_message)
        except Exception as e:
            print(f"Error sending message: {str(e)}")

if __name__ == '_main_':
    client = Client('localhost', 12345)
    client.connect()
    while True:
        message = input("Enter a message: ")
        client.send_message(message)