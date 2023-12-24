import socket
import threading
import pyautogui as pag
from PIL import ImageGrab
import io
import time

HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 0.0001

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

class RemoteDesktop:
    def __init__(self):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Remote Desktop")
        self.sk.connect((HOST, SERVER_PORT))
        
        self.mouseThread = None
        self.screenThread = None
        
        self.ConnectScreen()
        self.screenThread.start()
        
        self.ConnectMouse()
        self.mouseThread.start()
        
    def ConnectMouse(self):
        self.mouseThread = threading.Thread(target= self.MouseControlled, args = (self,))    
        
    def MouseControlled(self):
        while True:
            buffer = self.sk.recv(BUFFERSIZE).decode()
            if not buffer:
                break
            command, x, y = buffer.split(",")
            if command == "clickLeft":
                button = 'left'
                pag.click(x, y,button)
            if command == "clickRight":
                button = 'right'
                pag.click(x, y, button)
            if command == "move":
                pag.moveTo(x,y)
            if command == "scroll":
                pag.scroll(x)
    
    def ConnectScreen(self):
        self.screenThread = threading.Thread(target= self.LiveScreen, args = (self,))
        
    def LiveScreen(self):
        while True:
            sendImage(self.sk)
            time.sleep(DELAY) 
    
    def sendImage(client):
        image = pag.screenshot()
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format='JPEG')
        image_byte_array = image_byte_array.getvalue()
        
        client.sendall(len(image_byte_array).to_bytes(4))
        for i in range(0, len(image_byte_array), BUFFERSIZE):
            client.sendall(image_byte_array[i:i+BUFFERSIZE])
                

#main
try:
    App = RemoteDesktop()
except:
    print("Error")
    

