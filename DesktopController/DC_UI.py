import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from DC_Home import Menu
from DC_Login import Login

import DC_ShutOut as so
import DC_Mac as ma
from DC_Screen import DesktopUI
from DC_Control import Control
from DC_KeyLogger import KeyloggerUI
from DC_AppProcess import AppProcessUI
from DC_Directory import DirectoryTreeUI
from DC_Constant import FORMAT, HOST, SERVER_PORT

# global variables
com_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

window = Tk()
window.configure(bg="#000")
window.title("Remote Desktop Controller")
window.resizable(False, False)
frame_login = Login(window)


def back(temp):
    temp.destroy()
    frame_hp.tkraise()
    # com_con.sendall(bytes("QUIT", "utf8"))


def live_screen():
    com_con.sendall("LIVESCREEN".encode(FORMAT))
    screen_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_con.connect((HOST,SERVER_PORT))
    temp = DesktopUI(window, screen_con)
    if temp.status == False:
        back(temp)
    return


def mac_address():
    com_con.sendall("MAC".encode(FORMAT))
    ma.mac_addr(com_con)
    return


def disconnect():
    com_con.sendall("QUIT".encode(FORMAT))
    frame_hp.destroy()
    window.destroy()
    return


def keylogger():
    com_con.sendall("KEYLOG".encode(FORMAT))
    temp = KeyloggerUI(window, com_con)
    temp.button_back.configure(command=lambda: back(temp))
    return


def control():
    com_con.sendall("CONTROL".encode(FORMAT))
    screen_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_con.connect((HOST,SERVER_PORT))
    key_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_con.connect((HOST,SERVER_PORT))
    mouse_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_con.connect((HOST,SERVER_PORT))
    temp = Control(window, com_con, screen_con, key_con, mouse_con)
    if temp.status == False:
        back(temp)
        screen_con.close()
        key_con.close()
        mouse_con.close()
    return

def directory_tree():
    com_con.sendall(bytes("DIRECTORY", "utf8"))
    temp = DirectoryTreeUI(window, com_con)
    temp.button_6.configure(command=lambda: back(temp))
    return

def app_process():
    com_con.sendall("PROCESS".encode(FORMAT))
    temp = AppProcessUI(window, com_con)
    temp.button_back.configure(command=lambda: back(temp))
    return

def shutdown_logout():
    com_con.sendall("SHUTOUT".encode(FORMAT))
    temp = so.shutdown_logout(window, com_con)
    return


def show_main_ui():
    frame_login.destroy()
    global frame_hp
    frame_hp = Menu(window)
    frame_hp.button_live_creen.configure(command=live_screen)
    frame_hp.button_mac_address.configure(command=mac_address)
    frame_hp.button_disconnect.configure(command=disconnect)
    frame_hp.button_keylogger.configure(command=keylogger)
    frame_hp.button_control.configure(command=control)
    frame_hp.button_directoryTree.configure(command=directory_tree)
    frame_hp.button_app_process.configure(command=app_process)
    frame_hp.button_shut_down.configure(command=shutdown_logout)
    return


def connect(frame):
    global com_con
    # ip = frame.ip_input.get()
    try:
        # client.connect((HOST, SERVER_PORT))
        show_main_ui()
    except Exception as e:
        print(e)
        messagebox.showerror(message="Cannot connect!")
    return


def main():
    com_con.connect((HOST, SERVER_PORT))
    frame_login.connect.configure(command=lambda: connect(frame_login))
    window.mainloop()


if __name__ == "__main__":
    main()
