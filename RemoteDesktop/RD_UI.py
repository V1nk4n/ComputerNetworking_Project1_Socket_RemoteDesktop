import socket
import tkinter as tk
import RD_Screen as screen
import RD_Controlled as controlled

HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 10

def live_screen():
    global s
    screen_con, screen_addr = s.accept()
    screen.send_img(screen_con)
    return

def control():
    global s
    global com_con
    screen_con, screen_addr = s.accept()
    key_con, key_addr = s.accept()
    mouse_con, mouse_addr = s.accept()
    controlled.controlled(com_con, screen_con, key_con, mouse_con)
    return    

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, SERVER_PORT))
    s.listen(100)
    com_con, com_addr = s.accept()
    while True:
        msg = com_con.recv(BUFFERSIZE).decode(FORMAT)
        if "LIVESCREEN" in msg:
            live_screen()
        elif "CONTROL" in msg:
            control()
        # elif "SD_LO" in msg:
        #     shutdown_logout()
        # elif "KEYLOG" in msg:
        #     keylogger()
        # elif "APP_PRO" in msg:
        #     app_process()
        # elif "MAC" in msg:
        #     mac_address()
        # elif "DIRECTORY" in msg:
        #     directory_tree()
        # elif "REGISTRY" in msg:
        #     registry()
        # elif "QUIT" in msg:
        #     client.close()
        #     s.close()
except:
    print("Error")