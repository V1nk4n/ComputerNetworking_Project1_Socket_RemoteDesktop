import tkinter as tk
from tkinter import *
from tkinter import Button, Text
from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT, myButton

class Keylogger(Frame):
    def __init__(self, window, client):
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

        self.client=client
        self.status=True
        
        self.box = Text(
            self,
            height=200,
            width=500,
            state="disable",
            wrap="char",
            font=("Tim New Roman",15),
            bg="white",
            bd=0,
            highlightthickness=0,
        )
        self.box.place(x=200, y=29, width=500, height=360)

        self.button_bind = Button(
            self,
            text="BIND",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.bind(client, self.button_bind),
        )

        self.button_bind.place(x=733, y=113, width=135, height=53.0)

        self.button_lock = Button(
            self,
            text="LOCK",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.lock(client, self.button_lock),
        )

        self.button_lock.place(x=733, y=250, width=135, height=53)

        self.button_show = Button(
            self,
            text="SHOW",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.show(client, self.box),
        )

        self.button_show.place(x=32, y=113, width=135, height=53)

        self.button_delete = Button(
            self,
            text="DELETE",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.delete(self.box),
        )

        self.button_delete.place(x=32, y=250, width=135, height=53)

        self.button_back = Button(
            self,
            text="BACK",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda:self.back(),
        )
        
        self.button_back.place(x=382, y=418, width=135, height=53)

    def bind(self, main_connect, button):
        main_connect.sendall("BIND".encode(FORMAT))
        if button["text"] == "BIND":
            button.configure(text="UNBIND")
        else:
            button.configure(text="BIND")
        return


    def show(self, main_connect, textbox):
        main_connect.sendall("SHOW".encode(FORMAT))
        data = main_connect.recv(BUFFERSIZE).decode(FORMAT)
    
        textbox.config(state="normal")
        textbox.insert(tk.END, data)
        textbox.config(state="disable")
        return


    def delete(self, textbox):
        textbox.config(state="normal")
        textbox.delete("1.0", "end")
        textbox.config(state="disable")
        return


    def lock(self, main_connect, button):
        main_connect.sendall("LOCK".encode(FORMAT))
        if button["text"] == "LOCK":
            button.configure(text="UNLOCK")
        else:
            button.configure(text="LOCK")
        return


    def back(self):
        self.status = False
        self.destroy()
        self.client.sendall("STOP".encode())
        return
