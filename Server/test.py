import socket
import pickle

movement = [1, 0]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 3333))
sock.connect(("localhost", 8888))
data = pickle.dumps(movement)
with sock:
    sock.send(data)
    data = sock.recv(1024)
    print(data)
