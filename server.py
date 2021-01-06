import socket
import threading
import queue
import time

NB_CLIENTS = 3


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", clientAddress)
        self.csocket.send(bytes("Hi, This is from Server..", 'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'bye':
                break
            if msg.isnumeric():
                idQ.put(int(msg))
                idQ.task_done()
            print("Message from client: ", msg)
            if leaderID != -1:
                self.csocket.send(bytes(str(leaderID), 'UTF-8'))
        print("Client at ", clientAddress, " disconnected...")


LOCALHOST = "127.0.0.1"
PORT = 8080
idQ = queue.Queue(NB_CLIENTS)
listIDs = []
leaderID = -1
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
server.listen(5)
while True:
    clientSock, clientAddress = server.accept()
    newThread = ClientThread(clientAddress, clientSock)
    newThread.start()
    while not idQ.empty():
        item = idQ.get()
        listIDs.append(int(item))
    if len(listIDs) == (NB_CLIENTS - 1):
        time.sleep(1)
        leaderID = max(listIDs)
        print("The leader is : " + str(leaderID))
server.close()
