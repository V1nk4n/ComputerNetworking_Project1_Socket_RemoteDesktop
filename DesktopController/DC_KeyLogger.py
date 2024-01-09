import tkinter as tk
from tkinter import *
from tkinter import Button, Text

from DC_Constant import BACKGROUND, BUFFERSIZE


def hook(client, button):
    client.sendall(bytes("HOOK", "utf8"))
    if button["text"] == "HOOK":
        button.configure(text="UNHOOK")
    else:
        button.configure(text="HOOK")
    return


def _print(client, textbox):
    client.sendall(bytes("PRINT", "utf8"))
    data = client.recv(BUFFERSIZE).decode("utf8")
    data = data[1:]
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
    client.sendall(bytes("LOCK", "utf8"))
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

        self.text_1 = Text(
            self,
            height=200,
            width=500,
            state="disable",
            wrap="char",
            bd=0,
            bg="white",
            highlightthickness=0,
        )
        self.text_1.place(x=220, y=100, width=600, height=360)

        self.button_hook = Button(
            self,
            text="HOOK",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            font="Calibri 15",
            command=lambda: hook(client, self.button_hook),
            relief="raised",
        )

        self.button_hook.place(x=850, y=150, width=135, height=53.0)

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

        self.button_print = Button(
            self,
            text="PRINT",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            font="Calibri 15",
            command=lambda: _print(client, self.text_1),
            relief="raised",
        )

        self.button_print.place(x=30, y=150, width=135, height=53)

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
            command=lambda: delete(self.text_1),
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
