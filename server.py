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
DELAY = 0.1

def recvList(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    
    while (item != "end"):
        
        list.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
        
    return list

def handleClient(conn: socket, addr):
    print("client address: ", addr)
    print("conn: ", conn.getsockname())

    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client ",addr,"says",msg)
        # msg = input("Server: ")
        # server.sendall(msg.encode(FORMAT))
        if (msg == "list"):
            conn.sendall(msg.encode(FORMAT))
            list = recvList(conn)
            
            print("received: ")
            print(list)
            
            
    print("client", addr, "finished")   
    print(conn.getsockname(), "closed")
    conn.close()

def recvImage(conn):
    length_bytes = conn.recv(4)
    image_length = int.from_bytes(length_bytes)
    
    image_byte_array = b""
    remaining_length = image_length
    while remaining_length > 0:
            chunk = conn.recv(min(BUFFERSIZE, remaining_length))
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

def recvLiveScreen(conn):
    root = tk.Tk() #tao ra 1 Tk (Tk la 1 cua so)
    root.title("Live Screen")
    
    canvas = Canvas(root, width=1920, height=1080) #Canvas cho phep ve len cua so
    canvas.pack() #Them canvas vao Tk
    
    while True:
        image = recvImage(conn)
        if image:
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            root.update()
      
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
    # threading.Thread(targer = listen).start()
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
    

        
s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server: ", HOST, SERVER_PORT)
print("Waiting for Client")

# nclient = 0
# while (nclient < 3):
#     try:
#         conn, addr = s.accept()
        
#         thr = threading.Thread(target=handleClient, args = (conn, addr))
#         thr.daemon = False
#         thr.start()
         
#     except:
#         print("Error")

#     nclient += 1
try:
    conn, addr = s.accept()
    
    mouseThread = threading.Thread(target = sendMouse, agrs = conn)
    screenThread = threading.Thread(target= recvLiveScreen, agrs = conn)
    
    mouseThread.start()
    screenThread.start()
    
    mouseThread.join()
    screenThread.join()
    

except:
    print("Error")

print("End")
input()

s.close();

