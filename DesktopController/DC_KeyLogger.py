import tkinter as tk
from tkinter import *
from tkinter import Button, Text

from DC_Constant import BACKGROUND, BUFFERSIZE, FORMAT


def bind(client, button):
    client.sendall("BIND".encode(FORMAT))
    if button["text"] == "BIND":
        button.configure(text="UNBIND")
    else:
        button.configure(text="BIND")
    return


def show(client, textbox):
    client.sendall("SHOW".encode(FORMAT))
    data = client.recv(BUFFERSIZE).decode(FORMAT)
    
    textbox.config(state="normal")
    textbox.insert(tk.END, data)
    textbox.config(state="disable")
    return


def delete(textbox):
    textbox.config(state="normal")
    textbox.delete("1.0", "end")
    textbox.config(state="disable")
    return


def lock(client, button):
    client.sendall("LOCK".encode(FORMAT))
    if button["text"] == "LOCK":
        button.configure(text="UNLOCK")
    else:
        button.configure(text="LOCK")
    return


def back():
    return


class KeyloggerUI(Frame):
    def __init__(self, parent, client):
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

        self.box = Text(
            self,
            height=200,
            width=500,
            state="disable",
            wrap="char",
            bd=0,
            bg="white",
            highlightthickness=0,
        )
        self.box.place(x=220, y=100, width=600, height=360)

        self.button_bind = Button(
            self,
            text="BIND",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            font="Calibri 15",
            command=lambda: bind(client, self.button_bind),
            relief="raised",
        )

        self.button_bind.place(x=850, y=150, width=135, height=53.0)

        self.button_lock = Button(
            self,
            text="LOCK",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            font="Calibri 15",
            command=lambda: lock(client, self.button_lock),
            relief="raised",
        )

        self.button_lock.place(x=850, y=300, width=135, height=53)

        self.button_show = Button(
            self,
            text="SHOW",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            font="Calibri 15",
            command=lambda: show(client, self.box),
            relief="raised",
        )

        self.button_show.place(x=30, y=150, width=135, height=53)

        self.button_delete = Button(
            self,
            text="DELETE",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            font="Calibri 15",
            command=lambda: delete(self.box),
            relief="raised",
        )

        self.button_delete.place(x=30, y=300, width=135, height=53.0)

        self.button_back = Button(
            self,
            text="BACK",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            font="Calibri 15",
            command=back,
            relief="raised",
        )

        self.button_back.place(x=730, y=560, width=200, height=30)
