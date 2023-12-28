import socket

HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 0.0001

MouseThread = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Mouse")
MouseThread.connect((HOST, SERVER_PORT))


ScreenThread = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Screen")
ScreenThread.connect((HOST, SERVER_PORT))

Mouse = MouseThread.recv(BUFFERSIZE).decode(FORMAT)
print(Mouse)

ScreenThread.sendall("Screen".encode(FORMAT))
input()
input()
