import socket
import threading
import pyautogui as pag
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import Label, Canvas
from pynput import keyboard 
import time

HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 0.0001
   
    

def listen():
    with keyboard.Listener(on_press = on_key) as listener:
        listener.join()
    
def sendKey(conn):
    listen()
    while True:
        conn.sendall(buffer.encode(FORMAT))
        buffer = " "

def sendMouse(conn):
    while True:
        x, y = pag.position()
        # x = root.winfo_pointerx()
        # y = root.winfo_pointery()
        conn.sendall(f"{x},{y}".encode())
        time.sleep(1)
    

class DesktopController:
    def __init__(self, window):
        self.window = window
        self.window.title("Remote Desktop Controller")
        
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.bind((HOST, SERVER_PORT))
        self.sk.listen()
        print("Controller")
        
        self.canvas = Canvas(self.window, width=1920, height=1080)
        self.canvas.pack()
        
        self.screenConnection = None
        self.screenAddr = None
        self.screenThread = None
        
        self.mouseConnection = None
        self.mouseAddr = None
        self.mouseThread = None
        
        

        self.screenConnection, self.screenAddr = self.sk.accept()
        self.screenThread = threading.Thread(target = self.LiveScreen)
        self.screenThread.start()
        
        self.keyConnection, self.keyAddr = self.sk.accept()
        self.keyThread = threading.Thread(target = self.KeyControl)
        self.keyThread.start()
        
        # self.mouseConnection, self.mouseAddr = self.sk.accept()
        # self.mouseThread = threading.Thread(target = self.MouseControl)
        # self.mouseThread.start()
        
    def ConnectScreen(self):
        return self.sk.accept()
    
    def ConnectMouse(self):
        return self.sk.accept()
    
# while self.mouseConnection:
        #     window.update_idletasks()
        #     time.sleep(2*DELAY)
        
    def KeyControl(self):
        self.window.bind("<Key>", self.press)
    
    def press(self, event):
        key = event.char
        self.keyConnection.sendall(f"{key}".encode())
    
    def MouseControl(self):
        self.window.bind("<Motion>", self.move)
        self.window.bind("<Button-1>", self.clickLeft)
        self.window.bind("<Button-3>", self.clickRight)
        self.window.bind("<MouseWheel>", self.scroll)
        
    def clickLeft(self, event):
        buffer = f"clickLeft,{event.x},{event.y},"
        self.mouseConnection.sendall(buffer.encode())
    def clickRight(self, event):
        self.mouseConnection.sendall(f"clickRight,{event.x},{event.y}".encode())
    def move(self, event):
        buffer = f"move,{event.x},{event.y},"
        print(buffer)
        self.mouseConnection.sendall(buffer.encode())
        buffer =""
    def scroll(self, event):
        self.mouseConnection.sendall(f"scroll,{event.delta},0".encode())
    
    def LiveScreen(self):
        while self.screenConnection:
            length_bytes = self.screenConnection.recv(4)
            image_length = int.from_bytes(length_bytes)
        
            image_byte_array = b""
            while len(image_byte_array) < image_length:
                    buffer = self.screenConnection.recv(BUFFERSIZE)
                    if not buffer:
                        break
                    image_byte_array += buffer

            image_byte_io = io.BytesIO(image_byte_array)
            image = Image.open(image_byte_io) 
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.window.update_idletasks()
            
                    
                
    def recvImage(self):
        length_bytes = self.connection.recv(4)
        image_length = int.from_bytes(length_bytes)
        
        image_byte_array = b""
        while len(image_byte_array) < length_bytes:
                buffer = self.connection.recv(BUFFERSIZE)
                if not buffer:
                    break
                image_byte_array += buffer


        if len(image_byte_array) == image_length:
            image_byte_io = io.BytesIO(image_byte_array)
            image = Image.open(image_byte_io)
            return image
        else:
            print("Chua nhan du du lieu")
            return None
    
    def on_key(self, key):
        try:
            key_value = key.char
        except:
            key_value = str(key)
        self.connection.sendall(key.encode(FORMAT))
    

    def listen_keyboard():
        with keyboard.Listener(on_press = on_key) as listener:
            listener.join()
    
        
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, SERVER_PORT))
# s.listen()
# print("SERVER SIDE")
# print("server: ", HOST, SERVER_PORT)
# print("Waiting for Client")

try:
    window = tk.Tk()
    App = DesktopController(window)
    window.mainloop()
except:
    print("Error")


