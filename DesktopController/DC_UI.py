import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from DC_Home import HomePageUI
from DC_Login import LoginPageUI
from DC_Screen import DesktopUI


HOST = "127.0.0.1"
SERVER_PORT = 61000

# global variables
CommunicationConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

window = Tk()
window.configure(bg="#000")
window.title("Remote Desktop Controller")
# window.resizable(False, False)
frame_login = LoginPageUI(window)


def back(temp):
    temp.destroy()
    frame_hp.tkraise()
    CommunicationConnection.sendall(bytes("QUIT", "utf8"))


def live_screen():
    CommunicationConnection.sendall(bytes("LIVESCREEN", "utf8"))
    screen_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_con.connect((HOST,SERVER_PORT))
    temp = DesktopUI(window, screen_con)
    if temp.status == False:
        back(temp)
    return


def mac_address():
    CommunicationConnection.sendall(bytes("MAC", "utf8"))
    # mac.mac_address(client)
    return


def disconnect():
    CommunicationConnection.sendall(bytes("QUIT", "utf8"))
    frame_hp.destroy()
    window.destroy()
    return


def keylogger():
    CommunicationConnection.sendall(bytes("KEYLOG", "utf8"))
    # temp = kl.KeyloggerUI(window, client)
    # temp.button_back.configure(command=lambda: back(temp))
    return


def app_process():
    CommunicationConnection.sendall(bytes("APP_PRO", "utf8"))
    # temp = ap.AppProcessUI(window, client)
    # temp.button_back.configure(command=lambda: back(temp))
    return


def back_reg(temp):
    temp.client.sendall(bytes("STOP_EDIT_REGISTRY", "utf8"))
    temp.destroy()
    frame_hp.tkraise()


def directory_tree():
    CommunicationConnection.sendall(bytes("DIRECTORY", "utf8"))
    # temp = dt.DirectoryTreeUI(window, client)
    # temp.button_6.configure(command=lambda: back(temp))
    return


def registry():
    CommunicationConnection.sendall(bytes("REGISTRY", "utf8"))
    # temp = rc.RegistryUI(window, client)
    # temp.btn_back.configure(command=lambda: back_reg(temp))
    return


def shutdown_logout():
    CommunicationConnection.sendall(bytes("SD_LO", "utf8"))
    # temp = sl.shutdown_logout(client, window)
    return


def show_main_ui():
    frame_login.destroy()
    global frame_hp
    frame_hp = HomePageUI(window)
    frame_hp.button_live_creen.configure(command=live_screen)
    frame_hp.button_mac_address.configure(command=mac_address)
    frame_hp.button_disconnect.configure(command=disconnect)
    frame_hp.button_keylogger.configure(command=keylogger)
    frame_hp.button_app_process.configure(command=app_process)
    frame_hp.button_directoryTree.configure(command=directory_tree)
    frame_hp.button_registry.configure(command=registry)
    frame_hp.button_shut_down.configure(command=shutdown_logout)
    return


def connect(frame):
    global CommunicationConnection
    # ip = frame.ip_input.get()
    try:
        # client.connect((HOST, SERVER_PORT))
        show_main_ui()
    except Exception as e:
        print(e)
        messagebox.showerror(message="Cannot connect!")
    return


def main():
    CommunicationConnection.connect((HOST, SERVER_PORT))
    frame_login.connect.configure(command=lambda: connect(frame_login))
    window.mainloop()


if __name__ == "__main__":
    main()
