import io
import tkinter as tk
import socket
from threading import Thread, Event
from tkinter import Frame
from tkinter.filedialog import asksaveasfile

from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT
from PIL import Image, ImageTk


class Control(Frame):
    def __init__(self, parent, com_con, screen_con, key_con, mouse_con):
        Frame.__init__(self, parent)
        self.configure(
            bg=BACKGROUND,
            height=HEIGHT,
            width=WIDTH,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        parent.geometry("900x500+200+200")
        self.grid(row=0, column=0, sticky="nsew")
        
        self.window = parent
        
        # initialize status to ready receiving data
        self.status = True

        # label to display frames received from server
        self.label = tk.Label(self)
        self.label.place(x=30, y=0, width=WIDTH-60, height=HEIGHT-60)

        # a button to stop receiving and return to main interface
        self.button_back = tk.Button(
            self,
            text="Back",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.click_back(),
            relief="flat",
        )
        self.button_back.place(x=167, y=HEIGHT-40, width=200, height=30)

        self.stop_event = Event()

        self.disconnect_event = Event()

        self.communicationConnection = com_con
        self.screenConnection = screen_con
        self.keyConnection = key_con
        self.mouseConnection = mouse_con
        
        self.screen_status = True
        self.key_status = True
        self.mouse_status = True

        # thread
        self.checkThread = Thread(target=self.CheckStop)
        self.screenThread = Thread(target=self.ChangeImage)
        self.keyThread = Thread(target=self.KeyControl)
        self.mouseThread = Thread(target=self.MouseControl)
        
        self.checkThread.start()
        self.screenThread.start()
        self.keyThread.start()
        self.mouseThread.start()

    def CheckStop(self):
        while not self.stop_event.is_set():
            if self.status:
                self.communicationConnection.sendall("CONTINUE".encode(FORMAT))
            else:
                self.communicationConnection.sendall("STOP".encode(FORMAT))

        # Gửi lệnh STOP và đóng kết nối
        self.communicationConnection.sendall("STOP".encode(FORMAT))
        self.disconnect_event.set()

        # Đợi cho các luồng kết thúc
        self.screenThread.join()
        self.keyThread.join()
        self.mouseThread.join()

        # Đóng GUI
        self.destroy()
        
        
    # display frames continously
    def ChangeImage(self):
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
            image = Image.open(image_byte_io).resize((WIDTH, HEIGHT))
            #Tạo đối tượng PhotoImage để đưa lên window
            photo = ImageTk.PhotoImage(image)
            
            self.label.configure(image=photo)
            self.label.image = photo
            
            if self.screen_status:
                self.screenConnection.sendall("CONTINUE".encode(FORMAT))
            else:
                self.screenConnection.sendall("STOP".encode(FORMAT))
                break

        
        # Return the main UI
    def KeyControl(self):
        #Lắng nghe bàn phím
        if self.key_status:
            self.window.bind("<Key>", self.press)
        else:
            self.window.unbind("<Key>")
            self.keyConnection.sendall("STOP".encode(FORMAT))
        
        self.key_status = False

        
    def press(self, event):
        #Truyền phím nhập
        buffer = event.char
        self.keyConnection.sendall(buffer.encode(FORMAT))
        buffer = self.keyConnection.recv(BUFFERSIZE).decode()
        buffer =""
        
    def MouseControl(self):
        #Lắng nghe chuột
        if self.mouse_status:
            self.window.bind("<Motion>", self.move)
            self.window.bind("<Button-1>", self.clickLeft)
            self.window.bind("<Button-3>", self.clickRight)
            self.window.bind("<MouseWheel>", self.scroll)
        else:
            self.window.unbind("<Motion>")
            self.window.unbind("<Button-1>")
            self.window.unbind("<Button-3>")
            self.window.unbind("<MouseWheel>")
            self.mouseConnection.sendall("STOP".encode(FORMAT))
            
        self.mouse_status = False
        
    def clickLeft(self, event):
        #Nhấn bên trái
        if(event.x>=0&event.x<=WIDTH-60&event.y>=0&event.y<=HEIGHT-60):
            buffer = f"clickLeft,{event.x*1920/(WIDTH-60)},{event.y*1080/(HEIGHT-60)}"
            self.mouseConnection.sendall(buffer.encode())
            buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
            buffer =""
    def clickRight(self, event):
        #Nhấn bên phải
        if(event.x>=0 and event.x<=WIDTH-60 and event.y>=0 and event.y<=HEIGHT-60):
            buffer = f"clickRight,{event.x*1920/(WIDTH-60)},{event.y*1080/(HEIGHT-60)}"
            self.mouseConnection.sendall(buffer.encode())
            buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
            buffer =""
    def move(self, event):
        #Di chuyển chuột
        if(event.x>=0 and event.x<=WIDTH-60 and event.y>=0 and event.y<=HEIGHT-60):
            buffer = f"move,{event.x*1920/(WIDTH-60)},{event.y*1080/(HEIGHT-60)}"
            print(buffer)
            self.mouseConnection.sendall(buffer.encode())
            buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
            buffer =""
    def scroll(self, event):
        #Cuộn chuột
        if(event.x>=0 and event.x<=WIDTH-60 and event.y>=0 and event.y<=HEIGHT-60):
            buffer = f"move,{event.x*1920/(WIDTH-60)},{event.y*1080/(HEIGHT-60)}"
            self.mouseConnection.sendall(buffer.encode())
            buffer = self.mouseConnection.recv(BUFFERSIZE).decode()
            buffer =""

    def click_back(self):
        self.status = False
        self.screen_status = False
        self.KeyControl()
        self.MouseControl()
        self.stop_event.set()