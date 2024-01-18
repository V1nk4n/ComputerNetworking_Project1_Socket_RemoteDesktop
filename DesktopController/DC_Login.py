from tkinter import *
from DC_Constant import BACKGROUND,WIDTH, HEIGHT, myButton, FONT

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
            text="Server IP Address",
            font=(FONT,20),
            bg="#fdebd3",
            fg="black",
            borderwidth=2,
            highlightthickness=2,
        )
        self.ip_label.place(x=320, y=100)

        self.ip_input = Entry(
            self,
            font=(FONT,15),
            bg="white",
            fg="black",
            highlightthickness=2,
            relief="flat",
        )
        self.ip_input.place(x=300,y=133,width=300,height=50)

        self.connect = myButton(self)
        self.connect.configure(text="Connect")
        self.connect.place(x=300,y=316,height=50,width=300)


