import tkinter as tk
from tkinter import *
from tkinter import ttk

HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 1
BACKGROUND = "pink"
WIDTH = 900
HEIGHT = 500
FONT = "Consolas"
FONTSIZE = 15
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 5
BUTTON_BG = "#fdebd3"
BUTTON_FG = "black"
BUTTON_BORDER = 3
BUTTON_HIGHLIGHT = 2


class myButton(Button):
    def __init__(self, master=None, **kwargs):
        Button.__init__(self, master, **kwargs)
        self.configure(
            font=(FONT, FONTSIZE),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            borderwidth=BUTTON_BORDER,
            highlightthickness=BUTTON_HIGHLIGHT,
        )
        
    