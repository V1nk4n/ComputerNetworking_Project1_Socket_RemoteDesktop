from tkinter import *
from PIL import Image, ImageTk

BACKGROUND = "#bbd4ce"

class HomePageUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure(
            bg=BACKGROUND,
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        parent.geometry("1000x600+200+200")
        self.grid(row=0, column=0, sticky="nsew")

        # button - live creen
        self.button_live_creen = Button(
            self,
            borderwidth=0,
            text="Live Screen",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_live_creen.place(x=80, y=80, width=200, height=60)

        # button - keylogger
        self.button_keylogger = Button(
            self,
            borderwidth=0,
            text="Key Logger",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_keylogger.place(x=80, y=180, width=200, height=60)

        # button - directory tree
        self.button_directoryTree = Button(
            self,
            borderwidth=0,
            text="Directory Tree",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_directoryTree.place(x=80, y=280, width=200, height=60)

        # button - app process
        self.button_app_process = Button(
            self,
            borderwidth=0,
            text="App Process",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_app_process.place(x=420, y=80, width=200, height=60)

        # button - registry
        self.button_registry = Button(
            self,
            borderwidth=0,
            text="Registry",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_registry.place(x=420, y=180, width=200, height=60)
        # button - mac address
        self.button_mac_address = Button(
            self,
            borderwidth=0,
            text="MAC Address",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_mac_address.place(x=420, y=280, width=200, height=60)
        # button - shut down
        self.button_shut_down = Button(
            self,
            borderwidth=0,
            text="Shut Down",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_shut_down.place(
            x=80,
            y=380,
            width=200,
            height=60,
        )

        self.button_disconnect = Button(
            self,
            borderwidth=0,
            text="Disconnect",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            highlightthickness=0,
            relief="flat",
        )
        self.button_disconnect.place(
            x=420,
            y=380,
            width=200,
            height=60,
        )
