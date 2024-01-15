from tkinter import *
from DC_Constant import BACKGROUND, WIDTH, HEIGHT, myButton

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
        self.button_Live_Screen.place(x=534, y=276, width=200, height=60)

        self.button_App_Process = myButton(self)
        self.button_App_Process.configure(text="App Process")
        self.button_App_Process.place(x=534, y=52, width=200, height=60)

        self.button_Keylogger = myButton(self)
        self.button_Keylogger.configure(text="Key Logger")
        self.button_Keylogger.place(x=167, y=164, width=200, height=60)

        self.button_Mac_Address = myButton(self)
        self.button_Mac_Address.configure(text="MAC Address")
        self.button_Mac_Address.place(x=534, y=164, width=200, height=60)

        self.button_Directory_Tree = myButton(self)
        self.button_Directory_Tree.configure(text="Directory Tree")
        self.button_Directory_Tree.place(x=167, y=276, width=200, height=60)

        self.button_Control_Desktop = myButton(self)
        self.button_Control_Desktop.configure(text="Control Desktop")
        self.button_Control_Desktop.place(x=167, y=52, width=200, height=60)

        self.button_Shut_Down = myButton(self)
        self.button_Shut_Down.configure(text="Shut Down")
        self.button_Shut_Down.place(x=167, y=388, width=200, height=60)

        self.button_Disconnect = myButton(self)
        self.button_Disconnect.configure(text="Disconnect")
        self.button_Disconnect.place(x=534,y=388,width=200,height=60)
