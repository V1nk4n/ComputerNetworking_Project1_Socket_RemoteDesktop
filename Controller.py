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
   
    
# def recvImage(conn):
#     length_bytes = conn.recv(4)
#     image_length = int.from_bytes(length_bytes)
    
#     image_byte_array = b""
#     remaining_length = image_length
#     while remaining_length > 0:
#             chunk = conn.recv(min(BUFFERSIZE, remaining_length))
#             if not chunk:
#                 break
#             image_byte_array += chunk
#             remaining_length -= len(chunk)


#     if len(image_byte_array) == image_length:
#         image_byte_io = io.BytesIO(image_byte_array)
#         image = Image.open(image_byte_io)
#         return image
#     else:
#         print("Chua nhan du du lieu")
#         return None

def recvLiveScreen(conn, window):
    
    canvas = Canvas(window, width=1920, height=1080) #Canvas cho phep ve len cua so
    canvas.pack() #Them canvas vao Tk
    
    while True:
        image = recvImage(conn)
        if image:
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            window.update()
      
global buffer
buffer = []

def on_key(key):
    try:
        key_value = key.char
    except:
        key_value = str(key)
    print({key_value})
    buffer.append(key_value)

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
    


class Controller:
    def __init__(self, window):
        self.window = window
        self.window.title("Remote Desktop Controller")
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, SERVER_PORT))
        self.socket.listen()
        print("Controller")
        self.connection = None
        
        self.canvas = Canvas(self.window, width=1920, height=1080)
        self.canvas.pack()
        
        mouseThread = threading.Thread(target = self.MouseControl)
        mouseThread.start()
        
        screenThread = threading.Thread(target = self.LiveScreen)
        screenThread.start()
        
        self.ConnectSocket()
        
    def ConnectSocket(self):
        self.connection, self.address = self.socket.accept()   
            
    def MouseControl(self):
        self.window.bind("<Motion>", self.move)
        self.window.bind("<Button-1>", self.clickLeft)
        self.window.bind("<Button-3>", self.clickRight)
        self.window.bind("<MouseWheel>", self.scroll)
        
    def clickLeft(self, event):
        self.connection.sendall(f"clickLeft,{event.x},{event.y}".encode())
    def clickRight(self, event):
        self.connection.sendall(f"clickRight,{event.x},{event.y}".encode())
    def move(self, event):
        self.connection.sendall(f"move,{event.x},{event.y}".encode())
    def scroll(self, event):
        self.connection.sendall(f"scroll,{event.delta}, 0".encode())
    
    def LiveScreen(self):
       self.updateScreen()
            
    def updateScreen(self):
        image = self.recvImage(self)
        if image:
                photo = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                window.update()
                self.window.after(10, self.update_screen)
                
    def recvImage(self):
        length_bytes = self.connection.recv(4)
        image_length = int.from_bytes(length_bytes)
        
        image_byte_array = b""
        remaining_length = image_length
        while remaining_length > 0:
                chunk = self.connection.recv(min(BUFFERSIZE, remaining_length))
                if not chunk:
                    break
                image_byte_array += chunk
                remaining_length -= len(chunk)


        if len(image_byte_array) == image_length:
            image_byte_io = io.BytesIO(image_byte_array)
            image = Image.open(image_byte_io)
            return image
        else:
            print("Chua nhan du du lieu")
            return None
        
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, SERVER_PORT))
# s.listen()
# print("SERVER SIDE")
# print("server: ", HOST, SERVER_PORT)
# print("Waiting for Client")

try:
    window = tk.Tk()
    App = Controller(window)
    window.mainloop()

except:
    print("Error")


