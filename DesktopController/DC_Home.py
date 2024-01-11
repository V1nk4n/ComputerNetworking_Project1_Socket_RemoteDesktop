from tkinter import *
from PIL import Image, ImageTk
from DC_Constant import BACKGROUND,WIDTH, HEIGHT, myButton

class Menu(Frame):
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
        parent.geometry("900x500+200+200")
        self.grid(row=0, column=0, sticky="nsew")

        self.button_Live_Screen = myButton(self)
        self.button_Live_Screen.configure(text="Live Screen")

        # self.button_Live_Screen = Button(
        #     self,
        #     text="Live Screen",
        #     font=("Tim New Roman",15),
        #     bg="#fdebd3",
        #     fg="black",
        #     borderwidth=3,
        #     highlightthickness=2,
        # )
        self.button_Live_Screen.place(x=167, y=52, width=200, height=60)

        self.button_App_Process = Button(
            self,
            text="App Process",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )
        self.button_App_Process.place(x=534, y=52, width=200, height=60)

        self.button_Keylogger = Button(
            self,
            text="Key Logger",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )
        self.button_Keylogger.place(x=167, y=164, width=200, height=60)

        self.button_Mac_Address = Button(
            self,
            text="MAC Address",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )
        self.button_Mac_Address.place(x=534, y=164, width=200, height=60)

        self.button_Directory_Tree = Button(
            self,
            text="Directory Tree",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )
        self.button_Directory_Tree.place(x=167, y=276, width=200, height=60)

        self.button_Shut_Down = Button(
            self,
            text="Shut Down",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )
        self.button_Shut_Down.place(x=534, y=276, width=200, height=60)

        self.button_Control_Desktop = Button(
            self,
            text="Control Desktop",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )
        self.button_Control_Desktop.place(x=167,y=388,width=200,height=60,)

        self.button_Disconnect = Button(
            self,
            text="Disconnect",
            font=("Tim New Roman",15),
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
        )
        self.button_Disconnect.place(x=534,y=388,width=200,height=60,)
