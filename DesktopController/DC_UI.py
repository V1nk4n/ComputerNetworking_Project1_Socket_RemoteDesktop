import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from DC_Home import Menu
from DC_Login import Login
import DC_ShutOut as sot
import DC_Mac as mac
from DC_Screen import Screen
from DC_Control import Control
from DC_KeyLogger import Keylogger
from DC_TaskManager import TaskManager
from DC_Directory import DirectoryTree
from DC_Constant import FORMAT, SERVER_PORT

main_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

window = Tk()
window.configure(bg="#000")
window.title("Remote Desktop Controller")
window.resizable(False, False)
login = Login(window)

def back(temp):
    temp.destroy()
    menu.tkraise()

def screen_shot():
    main_connect.sendall("SCREENSHOT".encode(FORMAT))
    screen_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_con.connect((IP,SERVER_PORT))
    temp = Screen(window, screen_con)
    if temp.status == False:
        back(temp)
    return

def mac_address():
    main_connect.sendall("MAC".encode(FORMAT))
    mac.mac_addr(main_connect)
    return

def disconnect():
    main_connect.sendall("QUIT".encode(FORMAT))
    menu.destroy()
    window.destroy()
    return

def key_logger():
    main_connect.sendall("KEYLOG".encode(FORMAT))
    temp = Keylogger(window, main_connect)
    if temp.status == False:
        back(temp)
    return

def control_desktop():
    main_connect.sendall("CONTROL".encode(FORMAT))
    screen_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_con.connect((IP,SERVER_PORT))
    key_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_con.connect((IP,SERVER_PORT))
    mouse_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_con.connect((IP,SERVER_PORT))
    temp = Control(window, main_connect, screen_con, key_con, mouse_con)
    if temp.status == False:
        back(temp)
        screen_con.close()
        key_con.close()
        mouse_con.close()
    return

def directory_tree():
    main_connect.sendall(bytes("DIRECTORY", "utf8"))
    temp = DirectoryTree(window, main_connect)
    if temp.status == False:
        back(temp)
    return

def task_manager():
    main_connect.sendall("TASK".encode(FORMAT))
    temp = TaskManager(window, main_connect)
    if temp.status == False:
        back(temp)
    return

def shutdown_logout():
    main_connect.sendall("SHUTOUT".encode(FORMAT))
    temp = sot.shutout(window, main_connect)
    return

def show_menu():
    login.destroy()
    global menu
    menu = Menu(window)
    menu.button_Screen_Shot.configure(command=screen_shot)
    menu.button_Task_Manager.configure(command=task_manager)
    menu.button_Keylogger.configure(command=key_logger)
    menu.button_Mac_Address.configure(command=mac_address)
    menu.button_Directory_Tree.configure(command=directory_tree)
    menu.button_Shut_Down.configure(command=shutdown_logout)
    menu.button_Control_Desktop.configure(command=control_desktop)
    menu.button_Disconnect.configure(command=disconnect)
    return

def connect(login):
    global main_connect
    global IP
    IP = login.ip_input.get()
    print(IP)
    try:
        main_connect.connect((IP, SERVER_PORT))
        show_menu()
    except Exception as e:
        print(e)
        messagebox.showerror(message="Error in connection!")
    return


def main():
    login.connect.configure(command=lambda: connect(login))
    window.mainloop()


if __name__ == "__main__":
    main()
