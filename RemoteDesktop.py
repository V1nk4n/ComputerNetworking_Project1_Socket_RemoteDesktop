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
        self.screenConnection = None
        self.screenAddr = None
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
        self.screenConnection, self.screenAddr = self.sk.accept()
        #Thiết lập luồng để truyền màn hình với hàm xử lý LiveScreen
        #self.LiveScreen = LiveScreen(self) (OOP)
        self.screenThread = threading.Thread(target = self.LiveScreen)
        #.start là để bắt đầu luồng
        self.screenThread.start()
        
        #Tương tự dành cho bàn phím
        self.keyConnection, self.keyAddr = self.sk.accept()
        self.keyThread = threading.Thread(target = self.KeyControlled)
        self.keyThread.start()
        
        #Hàm chuột đang lỗi
        self.mouseConnection, self.mouseAddr = self.sk.accept()
        self.mouseThread = threading.Thread(target = self.MouseControlled)
        self.mouseThread.start()
        
        self.MacConnection, self.MacAddr = self.sk.accept()
        self.MacThread = threading.Thread(target = self.mac_address)
        self.MacThread.start()
    
    def LiveScreen(self):
        while self.screenConnection:
            #Chụp màn hình
            image = pag.screenshot()
            #Tạo BytesIO lưu hình ảnh ở dạng byte
            image_byte_array = io.BytesIO()
            #Lưu hình ảnh vào image_byte_array dưới dạng JPEG
            image.save(image_byte_array, format='JPEG')
            #Đổi thành dạng byte
            image_byte_array = image_byte_array.getvalue()
            
            #Gửi độ dài của hình ảnh
            self.screenConnection.sendall(len(image_byte_array).to_bytes(4))
            #Gửi hình ảnh
            self.screenConnection.sendall(image_byte_array)
            
            time.sleep(DELAY) 
                
    def KeyControlled(self):
        while True:
            #Nhận dữ liệu bàn phím
            buffer = self.keyConnection.recv(BUFFERSIZE).decode()
            
            if not buffer:
                break
            
            print(buffer)
            
            self.keyConnection.sendall(buffer.encode(FORMAT))
            buffer=""
        
        
    def MouseControlled(self):
        while True:
            #Nhận dữ liệu chuột
            buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
            
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
            self.mouseConnection.sendall(buffer.encode())
            #Dọn buffer
            buffer=""

    def mac_address(self):
        mac = get_mac()
        self.MacConnection.sendall(hex(mac).encode(FORMAT))
        return
                   

#main
try:
    #Khởi động ứng dụng
    App = RemoteDesktop()
except:
    print("Error")
    

