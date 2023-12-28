import socket
import threading
import pyautogui as pag
from PIL import Image
import io
from PIL import ImageGrab
import tkinter as tk

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

def sendList(client, list):
    for item in list:
        client.sendall(item.encode(FORMAT))
        client.recv(1024)
        
    msg = "end"
    client.send(msg.encode(FORMAT))

def move(event):
    print(f"{event.x},{event.y}")
def clickLeft(event):
    print(f"clickLeft,{event.x},{event.y}")
def clickRight(event):
    print(f"clickRight,{event.x},{event.y}")
def scroll(event):
    print(f"scroll,{event.delta}, 0")

    
event_x = 1223  # Thay bằng giá trị nguyên cụ thể của event.x
event_y = 4256  # Thay bằng giá trị nguyên cụ thể của event.y

message = f"clickLeft,{event_x},{event_y}"
length_in_bytes = len(message.encode('utf-8'))
print(f"Độ dài của chuỗi là: {length_in_bytes} bytes")
