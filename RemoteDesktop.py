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
        print("Remote Desktop")
        self.screenConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ConnectScreen()
        self.screenThread = threading.Thread(target= self.LiveScreen)
        self.screenThread.start()
        
        self.mouseConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ConnectMouse()
        self.mouseThread = threading.Thread(target= self.MouseControlled)
        self.mouseThread.start()
    
    def ConnectScreen(self):
        self.screenConnection.connect((HOST, SERVER_PORT))
        
    def LiveScreen(self):
        while self.screenConnection:
            image = ImageGrab.grab()
            image_byte_array = io.BytesIO()
            image.save(image_byte_array, format='JPEG')
            image_byte_array = image_byte_array.getvalue()
            
            self.screenConnection.sendall(len(image_byte_array).to_bytes(4))
            self.screenConnection.sendall(image_byte_array)
            
            time.sleep(DELAY) 
       
    def ConnectMouse(self):
        self.mouseConnection.connect((HOST, SERVER_PORT))
        
    def MouseControlled(self):
        while True:
            buffer = self.mouseConnection.recv(19).decode()
            if not buffer:
                break
            command, x, y = buffer.split(",")
            if command == "clickLeft":
                button = 'left'
                print(buffer)
                # pag.click(x, y,button)
            if command == "clickRight":
                button = 'right'
                print(buffer)
                # pag.click(x, y, button)
            if command == "move":
                print(buffer)
                # pag.moveTo(x,y)
            if command == "scroll":
                print(buffer)
                # pag.scroll(x)
            buffer = ""
                   

#main
try:
    App = RemoteDesktop()
except:
    print("Error")
    

