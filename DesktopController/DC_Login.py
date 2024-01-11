from tkinter import *
from PIL import Image, ImageTk
from DC_Constant import BACKGROUND,WIDTH, HEIGHT, myButton

class Login(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure(
            bg=BACKGROUND,
            height=HEIGHT,
            width=WIDTH,
            bd=0,# Do day duong vien
            highlightthickness=0,#in dam duong vien
            relief="ridge",
        )
        self.grid(row=0, column=0, sticky="nsew")

        self.ip_label = Label(
            self,
            text="Server IP Addresss",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=2,
            highlightthickness=2,
        )
        self.ip_label.place(x=362, y=103)

        self.ip_input = Entry(
            self,
            font=("Tim New Roman",15),
            bg="white",
            fg="black",
            highlightthickness=2,
            relief="flat",
        )
        self.ip_input.place(x=300,y=133,width=300,height=50,)

        self.connect = Button(
            self,
            text="Connect",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )

        self.connect.place(x=300,y=316,height=50,width=300,)


