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

class RemoteDesktop:
    def __init__(self):
        print("Remote Desktop")
        
        #Thiết lập socket để truyền màn hình
        self.screenConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Lệnh connect để kết nối tới socket screenConnection ở máy Controller
        self.screenConnection.connect((HOST, SERVER_PORT))
        #Tạo luồng LiveScreen
        self.screenThread = threading.Thread(target = self.LiveScreen)
        #.start() để bắt đầu luồng màn hình
        self.screenThread.start()
        
        #Tương tự
        self.keyConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keyConnection.connect((HOST, SERVER_PORT))
        self.keyThread = threading.Thread(target = self.KeyControlled)
        self.keyThread.start()
        
        # self.mouseConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.mouseConnection.connect((HOST, SERVER_PORT))
        # self.mouseThread = threading.Thread(target = self.MouseControlled)
        # self.mouseThread.start()
    
    def LiveScreen(self):
        while self.screenConnection:
            #Chụp màn hình
            image = ImageGrab.grab()
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
                pag.click(x, y,button)
            #Nếu lệnh là nhấp phải
            if command == "clickRight":
                button = 'right'
                pag.click(x, y, button)
            #Nếu lệnh là di chuyển
            if command == "move":
                pag.moveTo(x,y)
            #Nếu lệnh là cuộn
            if command == "scroll":
                pag.scroll(x)

            #Dọn buffer
            buffer.clear()
                   

#main
try:
    #Khởi động ứng dụng
    App = RemoteDesktop()
except:
    print("Error")
    

