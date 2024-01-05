import socket

HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 0.0001

# sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sk.bind((HOST, SERVER_PORT))
# sk.listen()
# print("Controller")
# MouseThread, Mouseaddr = sk.accept()
# ScreenThread, Screenaddr = sk.accept()

# MouseThread.sendall("Mouse".encode(FORMAT))
# Screen = ScreenThread.recv(BUFFERSIZE).decode(FORMAT)
# print(Screen)
# input()
