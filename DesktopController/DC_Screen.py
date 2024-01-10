import io
import tkinter as tk
from threading import Thread
from tkinter import Frame
from tkinter.filedialog import asksaveasfile
from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT
from PIL import Image, ImageTk

class DesktopUI(Frame):
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

        # copy socket connection to own attribute
        self.screenConnection = screen_con

        # initialize status to ready receiving data
        self.status = True

        # initialize the sentinel of saving image command
        self.on_save = False

        # label to display frames received from server
        self.label = tk.Label(self)
        self.label.place(x=30, y=0, width=WIDTH-60, height=HEIGHT-60)
        
        # a button to save captured screen
        self.button_save = tk.Button(
            self,
            text="Save",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            command=lambda: self.click_save(),
            relief="flat",
        )
        self.button_save.place(x=167, y=HEIGHT-40, width=200, height=30)

        # a button to stop receiving and return to main interface
        self.button_back = tk.Button(
            self,
            text="Back",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            command=lambda: self.click_back(),
            relief="flat",
        )
        self.button_back.place(x=534, y=HEIGHT-40, width=200, height=30)

        # thread
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.start.start()

    # display frames continously
    def ChangeImage(self):
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

            # check save image command
            # while saving image, server will delay capturing and wait for the next command from client
            if self.on_save:
                self.frame = image_byte_array
                self.save_img()
                self.on_save = False

            # check stop command
            if self.status:
                self.screenConnection.sendall("CONTINUE".encode(FORMAT))
            else:
                self.screenConnection.sendall("STOP".encode(FORMAT))
        # Return the main UI
        self.destroy()

    def click_back(self):
        self.status = False

    def click_save(self):
        self.on_save = True

    def save_img(self):
        if self.frame == None:
            return

        types = [("Portable Network Graphics", "*.png"), ("All Files", "*.*")]
        image_file = asksaveasfile(mode="wb", filetypes=types, defaultextension="*.png")
        if image_file == None:
            return
        image_file.write(self.frame)


    