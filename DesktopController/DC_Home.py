from tkinter import *
from PIL import Image, ImageTk
from DC_Constant import BACKGROUND,WIDTH, HEIGHT

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

        # button - live creen
        self.button_live_creen = Button(
            self,
            borderwidth=0,
            text="Live Screen",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_live_creen.place(x=167, y=52, width=200, height=60)

        # button - keylogger
        self.button_keylogger = Button(
            self,
            borderwidth=0,
            text="Key Logger",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_keylogger.place(x=167, y=164, width=200, height=60)

        # button - directory tree
        self.button_directoryTree = Button(
            self,
            borderwidth=0,
            text="Directory Tree",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_directoryTree.place(x=167, y=276, width=200, height=60)

        # button - control
        self.button_control = Button(
            self,
            borderwidth=0,
            text="Control",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_control.place(x=167,y=388,width=200,height=60,)

        # button - app process
        self.button_app_process = Button(
            self,
            borderwidth=0,
            text="App Process",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_app_process.place(x=534, y=52, width=200, height=60)
        # button - mac address
        self.button_mac_address = Button(
            self,
            borderwidth=0,
            text="MAC Address",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_mac_address.place(x=534, y=164, width=200, height=60)
        # button - shut down
        self.button_shut_down = Button(
            self,
            borderwidth=0,
            text="Shut Down",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_shut_down.place(x=534, y=276, width=200, height=60)

        self.button_disconnect = Button(
            self,
            borderwidth=0,
            text="Disconnect",
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            highlightthickness=0,
            relief="flat",
        )
        self.button_disconnect.place(x=534,y=388,width=200,height=60,)
