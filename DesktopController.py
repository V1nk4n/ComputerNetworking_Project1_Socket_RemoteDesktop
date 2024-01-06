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
        # Đặt tên cho cửa sổ
        self.window.title("Remote Desktop Controller")
        
        # Tạo 1 socket để nhận kết nối
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.bind((HOST, SERVER_PORT))
        self.sk.listen()
        print("Controller")
        
        # canvas dùng để vẽ lên cửa sổ -> chuẩn bị cho livescreen
        self.canvas = Canvas(self.window, width=1920, height=1080)
        self.canvas.pack()
        
        # Khởi tạo socket (Connection), địa chỉ (Addr) (Cái này không sử dụng chỉ truyền cho đủ tham số của hàm accept của socket),
        # luồng (Thread) để truyền chuột, bàn phím, màn hình
        self.screenConnection = None
        self.screenAddr = None
        self.screenThread = None
        
        self.keyConnection = None
        self.keyAddr = None
        self.keyThread = None
        
        self.mouseConnection = None
        self.mouseAddr = None
        self.mouseThread = None
        
        # Thiết lập socket chấp nhận kết nối để nhận màn hình từ máy Remote
        self.screenConnection, self.screenAddr = self.sk.accept()
        #Thiết lập luồng để truyền màn hình với hàm xử lý LiveScreen
        #self.LiveScreen = LiveScreen(self) (OOP)
        self.screenThread = threading.Thread(target = self.LiveScreen)
        #.start là để bắt đầu luồng
        self.screenThread.start()
        
        #Tương tự dành cho bàn phím
        self.keyConnection, self.keyAddr = self.sk.accept()
        self.keyThread = threading.Thread(target = self.KeyControl)
        self.keyThread.start()
        
        #Hàm chuột đang lỗi
        self.mouseConnection, self.mouseAddr = self.sk.accept()
        self.mouseThread = threading.Thread(target = self.MouseControl)
        self.mouseThread.start()
        
        self.MacConnection = None
        self.MacAddr = None
        self.MacThread = None
        
        self.MacConnection, self.MacAddr = self.sk.accept()
        self.MacThread = threading.Thread(target = self.MacAd)
        self.MacThread.start()
   
    
    def LiveScreen(self):
        while self.screenConnection:
            #Nhận chiều dài của hình ảnh ở kiểu byte
            length_bytes = self.screenConnection.recv(4)
            #Độ dài của hình ảnh ở kiểu int
            length_ints = int.from_bytes(length_bytes)
        
            #Khởi tạo 1 mảng chứa hình ảnh ở kiểu byte
            image_byte_array = b""
            while len(image_byte_array) < length_ints:
                    buffer = self.screenConnection.recv(BUFFERSIZE)
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
        self.keyConnection.sendall(buffer.encode(FORMAT))
        buffer = self.keyConnection.recv(BUFFERSIZE).decode()
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
        self.mouseConnection.sendall(buffer.encode())
        buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
        buffer =""
    def clickRight(self, event):
        #Nhấn bên phải
        buffer = f"clickRight,{event.x},{event.y}"
        self.mouseConnection.sendall(buffer.encode())
        buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
        buffer =""
    def move(self, event):
        #Di chuyển chuột
        buffer = f"move,{event.x},{event.y}"
        print(buffer)
        self.mouseConnection.sendall(buffer.encode())
        buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
        buffer =""
    def scroll(self, event):
        #Cuộn chuột
        buffer = f"move,{event.x},{event.y}"
        self.mouseConnection.sendall(buffer.encode())
        buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
        buffer =""
        
    def MacAd(self):
        result = self.MacConnection.recv(BUFFERSIZE).decode(FORMAT)
        result = result[2:].upper()
        result = ':'.join(result[i:i + 2] for i in range(0, len(result), 2))
        print(result)
 
#main   
try:
    # Tạo cửa sổ ứng dụng
    window = tk.Tk()
    # Khởi động ứng dụng
    App = DesktopController(window)
    window.mainloop()
except:
    print("Error")


