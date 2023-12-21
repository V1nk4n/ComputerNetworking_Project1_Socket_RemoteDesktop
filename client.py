import socket
import threading
import pyautogui as pag
import pyautogui as pag
from PIL import ImageGrab
import io
import time

HOST = "10.131.3.147"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 0.1


def sendList(client, list):
    
    for item in list:
        client.sendall(item.encode(FORMAT))
        client.recv(1024)
        
    msg = "end"
    client.send(msg.encode(FORMAT))

def sendImage(client):
    image = pag.screenshot()
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format='JPEG')
    image_byte_array = image_byte_array.getvalue()
    
    client.sendall(len(image_byte_array).to_bytes(4))
    for i in range(0, len(image_byte_array), BUFFERSIZE):
        client.sendall(image_byte_array[i:i+BUFFERSIZE])
    
def liveScreen(client):
    while True:
        sendImage(client)
        
        time.sleep(DELAY) 

global buffer
buffer = []
def recvKey(client):
    buffer = client.recv(BUFFERSIZE).decode(FORMAT)
    pag.typewrite(buffer,DELAY)

def recvMouse(client):
    while True:
        buffer = client.recv(BUFFERSIZE).decode()
        x, y = map(int, buffer.split(","))
        print(f"{x},{y}")
        pag.moveTo(x,y)
    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")
    
try:
    client.connect((HOST, SERVER_PORT))
    print("client address: ", client.getsockname())
    recvMouse(client)
    liveScreen(client)
    # list = ["vinhan","19","nam"]

    # msg = None
    # while (msg!= "x"):
    #     msg = input("Client: ")
    #     client.sendall(msg.encode(FORMAT))
    #     # msg = client.recv(1024).decode(FORMAT)
    #     # print("Server: ",msg)
    #     if (msg == "list"):
    #         client.recv(1024)
    #         sendList(client, list)
        
except:
    print("Error")
    

input()
client.close()