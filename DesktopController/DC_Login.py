from tkinter import *
from PIL import Image, ImageTk
from DC_Constant import BACKGROUND,WIDTH, HEIGHT




class Login(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure(
            bg=BACKGROUND,
            height=HEIGHT,
            width=WIDTH,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.grid(row=0, column=0, sticky="nsew")

        self.ip_label = Label(
            self,
            text="Server IP Addresss",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
        )
        self.ip_label.place(x=362, y=103)

        self.ip_input = Entry(
            self,
            bg="white",
            highlightthickness=1,
            fg="black",
            relief="flat",
            font=("Tim New Roman",15),
        )
        self.ip_input.place(
            x=300,
            y=133,
            width=300,
            height=50,
        )
        self.ip_input.insert(END, "192.168.1.8")

        self.connect = Button(
            self,
            text="Connect",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            borderwidth=0,
            highlightthickness=0,
        )

        self.connect.place(
            x=300,
            y=316,
            height=50,
            width=300,
        )

# self.password_label = Label(
        #     self,
        #     text="Password",
        #     font="Calibri 15 bold",
        #     bg=BACKGROUND,
        #     fg="#264e70",
        # ).place(x=60, y=200)
        # self.password_input = Entry(
        #     self,
        #     bg="white",
        #     highlightthickness=1,
        #     fg="black",
        #     relief="flat",
        #     font="Calibri 15",
        # ).place(
        #     x=60,
        #     y=230,
        #     width=300,
        #     height=50,
        # )

