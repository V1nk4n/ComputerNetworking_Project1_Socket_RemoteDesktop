# import socket

# HOST = "127.0.0.1"
# SERVER_PORT = 61000
# FORMAT = "utf8"
# BUFFERSIZE = 1024*1024
# DELAY = 0.0001

# MouseThread = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Mouse")
# MouseThread.connect((HOST, SERVER_PORT))


# ScreenThread = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Screen")
# ScreenThread.connect((HOST, SERVER_PORT))

# Mouse = MouseThread.recv(BUFFERSIZE).decode(FORMAT)
# print(Mouse)

# ScreenThread.sendall("Screen".encode(FORMAT))
# input()
# input()

# def sendImage(client):
#     image = pag.screenshot()
#     image_byte_array = io.BytesIO()
#     image.save(image_byte_array, format='JPEG')
#     image_byte_array = image_byte_array.getvalue()
    
#     client.sendall(len(image_byte_array).to_bytes(4))
#     for i in range(0, len(image_byte_array), BUFFERSIZE):
#         client.sendall(image_byte_array[i:i+BUFFERSIZE])
    

# global buffer
# buffer = []

# def recvKey(client):
#     buffer = client.recv(BUFFERSIZE).decode(FORMAT)
#     pag.typewrite(buffer,DELAY)

# def recvMouse(client):
#     while True:
#         buffer = client.recv(BUFFERSIZE).decode()
#         if "clickLeft" in buffer:
#             buffer = buffer.replace("clickLeft,", "")
#             x ,y = buffer.split(",")
#             clicks = 1
#             interval = 0.1
#             button = "left"
#             pag.moveTo(x,y)
#             pag.click(x, y, clicks, interval, button)
#         else:
#             x, y = map(int, buffer.split(","))
#             print(f"{x},{y}")
#             pag.moveTo(x,y)

import socket
import threading
import pyautogui as pag
import time
import io
import tkinter as tk
from tkinter import Label, Canvas
from pynput import keyboard 
from PIL import Image, ImageTk
from uuid import getnode as get_mac


HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 10

class RemoteDesktop:
    def __init__(self):
        
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.bind((HOST, SERVER_PORT))
        self.sk.listen()
        print("Remote Desktop")
        
        # Khởi tạo socket (Connection), địa chỉ (Addr) (Cái này không sử dụng chỉ truyền cho đủ tham số của hàm accept của socket),
        # luồng (Thread) để truyền chuột, bàn phím, màn hình
        self.Socket = None
        self.SocAddr = None
        self.screenThread = None
        
        self.keyConnection = None
        self.keyAddr = None
        self.keyThread = None
        
        self.mouseConnection = None
        self.mouseAddr = None
        self.mouseThread = None
        
        self.MacConnection = None
        self.MacAddr = None
        self.MacThread = None
        
        # Thiết lập socket chấp nhận kết nối để nhận màn hình từ máy Remote
        self.Socket, self.SocAddr = self.sk.accept()
        #Thiết lập luồng để truyền màn hình với hàm xử lý LiveScreen
        #self.LiveScreen = LiveScreen(self) (OOP)
        self.screenThread = threading.Thread(target = self.LiveScreen)
        #.start là để bắt đầu luồng
        self.screenThread.start()
        
        #Tương tự dành cho bàn phím
        
        self.keyThread = threading.Thread(target = self.KeyControlled)
        self.keyThread.start()
        
        #Hàm chuột đang lỗi
        
        self.mouseThread = threading.Thread(target = self.MouseControlled)
        self.mouseThread.start()
        
        
        self.MacThread = threading.Thread(target = self.mac_address)
        self.MacThread.start()
    
    def LiveScreen(self):
        while self.Socket:
            #Chụp màn hình
            image = pag.screenshot()
            #Tạo BytesIO lưu hình ảnh ở dạng byte
            image_byte_array = io.BytesIO()
            #Lưu hình ảnh vào image_byte_array dưới dạng JPEG
            image.save(image_byte_array, format='JPEG')
            #Đổi thành dạng byte
            image_byte_array = image_byte_array.getvalue()
            
            #Gửi độ dài của hình ảnh
            self.Socket.sendall(len(image_byte_array).to_bytes(4))
            #Gửi hình ảnh
            self.Socket.sendall(image_byte_array)
            
           
                
    def KeyControlled(self):
        while True:
            #Nhận dữ liệu bàn phím
            buffer = self.Socket.recv(BUFFERSIZE).decode()
            
            if not buffer:
                break
            
            print(buffer)
            
            self.Socket.sendall(buffer.encode(FORMAT))
            buffer=""
        
        
    def MouseControlled(self):
        while True:
            #Nhận dữ liệu chuột
            buffer = self.Socket.recv(BUFFERSIZE).decode()
            
            if not buffer:
                break
            
            #Lệnh có dạng: move,123,456 (di chuyển chuột đến tọa độ (123,456))
            #Tách lệnh trên ra thành 3 thành phần command, x, y
            command, x, y = buffer.split(",")
            
            #Nếu lệnh là nhấp trái
            if command == "clickLeft":
                button = 'left'
                print("ClickLeft ",x,y)
                # pag.click(x, y,button)
            #Nếu lệnh là nhấp phải
            if command == "clickRight":
                button = 'right'
                print("ClickRight ",x,y)
                # pag.click(x, y, button)
            #Nếu lệnh là di chuyển
            if command == "move":
                print(x,y)
                # pag.moveTo(x,y)
            #Nếu lệnh là cuộn
            if command == "scroll":
                print("Scroll ",x,y)
                # pag.scroll(x)
            self.Socket.sendall(buffer.encode())
            #Dọn buffer
            buffer=""

    def mac_address(self):
        mac = get_mac()
        self.Socket.sendall(hex(mac).encode(FORMAT))
        return
                   

#main
try:
    #Khởi động ứng dụng
    App = RemoteDesktop()
except:
    print("Error")
    

