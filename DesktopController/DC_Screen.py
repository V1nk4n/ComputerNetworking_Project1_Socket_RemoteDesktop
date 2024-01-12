import io
import tkinter as tk
from threading import Thread
from tkinter import Frame
from tkinter.filedialog import asksaveasfile
from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT, myButton
from PIL import Image, ImageTk

class Screen(Frame):
    def __init__(self, parent, screen_con):
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

        self.screenConnection = screen_con

        self.status = True

        self.on_save = False

        self.label = tk.Label(self)
        self.label.place(x=30, y=0, width=WIDTH-60, height=HEIGHT-60)
        
        self.button_save = myButton(self)
        self.button_save.configure(text="Save", command=lambda: self.click_save())
        self.button_save.place(x=167, y=HEIGHT-40, width=200, height=30)

        self.button_back = myButton(self)
        self.button_back.configure(text="Back", command=lambda: self.click_back())
        self.button_back.place(x=534, y=HEIGHT-40, width=200, height=30)

        self.start = Thread(target=self.recv_img, daemon=True)
        self.start.start()

    def recv_img(self):
        while self.status:
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
            image = Image.open(image_byte_io).resize((WIDTH-60,HEIGHT-60))
            #Tạo đối tượng PhotoImage để đưa lên window
            photo = ImageTk.PhotoImage(image)
            
            self.label.configure(image=photo)
            self.label.image = photo

            if self.on_save:
                self.frame = image_byte_array
                self.save_img()
                self.on_save = False

            if self.status:
                self.screenConnection.sendall("CONTINUE".encode(FORMAT))
            else:
                self.screenConnection.sendall("STOP".encode(FORMAT))
        self.destroy()

    def click_save(self):
        self.on_save = True

    def click_back(self):
        self.status = False

    def save_img(self):
        if self.frame == None:
            return
        types = [("Portable Network Graphics", "*.jpeg"), ("All Files", "*.*")]
        image_file = asksaveasfile(mode="wb", filetypes=types, defaultextension="*.jpeg")
        if image_file == None:
            return
        image_file.write(self.frame)


    