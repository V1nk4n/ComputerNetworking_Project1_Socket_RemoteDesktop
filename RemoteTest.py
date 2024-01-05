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

def sendImage(client):
    image = pag.screenshot()
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format='JPEG')
    image_byte_array = image_byte_array.getvalue()
    
    client.sendall(len(image_byte_array).to_bytes(4))
    for i in range(0, len(image_byte_array), BUFFERSIZE):
        client.sendall(image_byte_array[i:i+BUFFERSIZE])
    

global buffer
buffer = []

def recvKey(client):
    buffer = client.recv(BUFFERSIZE).decode(FORMAT)
    pag.typewrite(buffer,DELAY)

def recvMouse(client):
    while True:
        buffer = client.recv(BUFFERSIZE).decode()
        if "clickLeft" in buffer:
            buffer = buffer.replace("clickLeft,", "")
            x ,y = buffer.split(",")
            clicks = 1
            interval = 0.1
            button = "left"
            pag.moveTo(x,y)
            pag.click(x, y, clicks, interval, button)
        else:
            x, y = map(int, buffer.split(","))
            print(f"{x},{y}")
            pag.moveTo(x,y)
