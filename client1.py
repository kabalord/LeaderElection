import socket
import random


SERVER = "127.0.0.1"
PORT = 7777
ID = random.randint(0, 100)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes(str(ID), 'UTF-8'))
while True:
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())
    out_data = input()
    client.sendall(bytes(out_data, 'UTF-8'))
    if out_data == 'bye':
        break
client.close()
