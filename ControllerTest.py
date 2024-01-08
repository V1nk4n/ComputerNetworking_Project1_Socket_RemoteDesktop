# import socket

# HOST = "127.0.0.1"
# SERVER_PORT = 61000
# FORMAT = "utf8"
# BUFFERSIZE = 1024*1024
# DELAY = 0.0001

# def listen():
#     with keyboard.Listener(on_press = on_key) as listener:
#         listener.join()
    
# def sendKey(conn):
#     listen()
#     while True:
#         conn.sendall(buffer.encode(FORMAT))
#         buffer = " "

# def sendMouse(conn):
#     while True:
#         x, y = pag.position()
#         # x = root.winfo_pointerx()
#         # y = root.winfo_pointery()
#         conn.sendall(f"{x},{y}".encode())
#         time.sleep(1)


    # def ConnectScreen(self):
    #     return self.sk.accept()
    
    # def ConnectMouse(self):
    #     return self.sk.accept()
    
    # while self.mouseConnection:
        #     window.update_idletasks()
        #     time.sleep(2*DELAY)
        
        
# sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sk.bind((HOST, SERVER_PORT))
# sk.listen()
# print("Controller")
# MouseThread, Mouseaddr = sk.accept()
# ScreenThread, Screenaddr = sk.accept()

# MouseThread.sendall("Mouse".encode(FORMAT))
# Screen = ScreenThread.recv(BUFFERSIZE).decode(FORMAT)
# print(Screen)
# input()

    # def recvImage(self):
    #     length_bytes = self.connection.recv(4)
    #     image_length = int.from_bytes(length_bytes)
        
    #     image_byte_array = b""
    #     while len(image_byte_array) < length_bytes:
    #             buffer = self.connection.recv(BUFFERSIZE)
    #             if not buffer:
    #                 break
    #             image_byte_array += buffer


    #     if len(image_byte_array) == image_length:
    #         image_byte_io = io.BytesIO(image_byte_array)
    #         image = Image.open(image_byte_io)
    #         return image
    #     else:
    #         print("Chua nhan du du lieu")
    #         return None  
    
    # def on_key(self, key):
    #     try:
    #         key_value = key.char
    #     except:
    #         key_value = str(key)
    #     self.connection.sendall(key.encode(FORMAT))
    

    # def listen_keyboard():
    #     with keyboard.Listener(on_press = on_key) as listener:
    #         listener.join()
    
import socket
import threading
import pyautogui as pag
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import Label, Canvas
from pynput import keyboard 
import time
from uuid import getnode as get_mac


HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 10

class DesktopController:
    # Hàm khởi tạo
    def __init__(self, window):
        # Gán cửa sổ đã tạo ở main cho self.window
        self.window = window
        # # Đặt tên cho cửa sổ
        self.window.title("Remote Desktop Controller")

        print("Controller")
        
        # canvas dùng để vẽ lên cửa sổ -> chuẩn bị cho livescreen
        self.canvas = Canvas(self.window, width=1920, height=1080)
        self.canvas.pack()
        
        # Khởi tạo socket (Connection), địa chỉ (Addr) (Cái này không sử dụng chỉ truyền cho đủ tham số của hàm accept của socket),
        # luồng (Thread) để truyền chuột, bàn phím, màn hình
        
        #Thiết lập socket để truyền màn hình
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Lệnh connect để kết nối tới socket screenConnection ở máy Controller
        self.Socket.connect((HOST, SERVER_PORT))
        #Tạo luồng LiveScreen
        self.screenThread = threading.Thread(target = self.LiveScreen)
        #.start() để bắt đầu luồng màn hình
        self.screenThread.start()
        
        #Tương tự
       
        self.keyThread = threading.Thread(target = self.KeyControl)
        self.keyThread.start()
        
    
        self.mouseThread = threading.Thread(target = self.MouseControl)
        self.mouseThread.start()
        

        self.MacThread = threading.Thread(target = self.MacAd)
        self.MacThread.start()
   
    
    def LiveScreen(self):
        while self.Socket:
            #Nhận chiều dài của hình ảnh ở kiểu byte
            length_bytes = self.Socket.recv(4)
            #Độ dài của hình ảnh ở kiểu int
            length_ints = int.from_bytes(length_bytes)
        
            #Khởi tạo 1 mảng chứa hình ảnh ở kiểu byte
            image_byte_array = b""
            while len(image_byte_array) < length_ints:
                    buffer = self.Socket.recv(BUFFERSIZE)
                    if not buffer:
                        break
                    image_byte_array += buffer

            #Tạo 1 BytesIO cho phép đọc dữ liệu dạng byte
            image_byte_io = io.BytesIO(image_byte_array)
            #Mở hình ảnh
            image = Image.open(image_byte_io)
            #Tạo đối tượng PhotoImage để đưa lên window
            photo = ImageTk.PhotoImage(image)
            #Đưa hình ảnh lên canvas đã tạo ở __init__
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            #Cập nhật liên tục
            self.window.update_idletasks()
                                    
    def KeyControl(self):
        #Lắng nghe bàn phím
        self.window.bind("<Key>", self.press)
    
    def press(self, event):
        #Truyền phím nhập
        buffer = event.char
        self.Socket.sendall(buffer.encode(FORMAT))
        buffer = self.Socket.recv(BUFFERSIZE).decode()
        buffer =""
    
    def MouseControl(self):
        #Lắng nghe chuột
        self.window.bind("<Motion>", self.move)
        self.window.bind("<Button-1>", self.clickLeft)
        self.window.bind("<Button-3>", self.clickRight)
        self.window.bind("<MouseWheel>", self.scroll)
        # self.window.update_idletasks()
        
    def clickLeft(self, event):
        #Nhấn bên trái
        buffer = f"clickLeft,{event.x},{event.y}"
        self.Socket.sendall(buffer.encode())
        buffer = self.Socket.recv(BUFFERSIZE).decode()
        buffer =""
    def clickRight(self, event):
        #Nhấn bên phải
        buffer = f"clickRight,{event.x},{event.y}"
        self.Socket.sendall(buffer.encode())
        buffer = self.Socket.recv(BUFFERSIZE).decode()
        buffer =""
    def move(self, event):
        #Di chuyển chuột
        buffer = f"move,{event.x},{event.y}"
        print(buffer)
        self.Socket.sendall(buffer.encode())
        buffer = self.Socket.recv(BUFFERSIZE).decode()
        buffer =""
    def scroll(self, event):
        #Cuộn chuột
        buffer = f"move,{event.x},{event.y}"
        self.Socket.sendall(buffer.encode())
        buffer = self.Socket.recv(BUFFERSIZE).decode()
        buffer =""
        
    def MacAd(self):
        result = self.Socket.recv(BUFFERSIZE).decode(FORMAT)
        result = result[2:].upper()
        result = ':'.join(result[i:i + 2] for i in range(0, len(result), 2))
        print(result)
 
#main   
try:
    #Tạo cửa sổ ứng dụng
    window = tk.Tk()
    # Khởi động ứng dụng
    App = DesktopController(window)
    window.mainloop()
except:
    print("Error")


