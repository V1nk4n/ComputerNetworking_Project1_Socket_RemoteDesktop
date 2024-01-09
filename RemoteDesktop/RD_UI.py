import socket
import tkinter as tk
import RD_Screen as screen
import RD_Controlled as ctrlled
import RD_KeyLogger as logger
import RD_ShutOut as so
import RD_Mac as ma
import RD_AppProcess as ap
import RD_Directory as dr

from RD_Constant import HOST, SERVER_PORT, FORMAT, BUFFERSIZE, DELAY

def live_screen():
    screen_con, screen_addr = s.accept()
    screen.send_img(screen_con)
    return

def control():
    screen_con, screen_addr = s.accept()
    key_con, key_addr = s.accept()
    mouse_con, mouse_addr = s.accept()
    ctrlled.controlled(com_con, screen_con, key_con, mouse_con)
    screen_con.close()
    key_con.close()
    mouse_con.close()
    return

def key_logger():
    logger.keylog(com_con)
    return

def shutout():
    so.shutout(com_con)
    return

def mac_address():
    ma.mac_addr(com_con)
    return

def app_process():
    ap.app_process(com_con)
    return  

def directory_tree():
    dr.directory(com_con)
    return
try:
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, SERVER_PORT))
    s.listen(100)
    global com_con
    com_con, com_addr = s.accept()
    while True:
        msg = com_con.recv(BUFFERSIZE).decode(FORMAT)
        if "LIVESCREEN" in msg:
            live_screen()
        elif "CONTROL" in msg:
            control()
        elif "SHUTOUT" in msg:
            shutout()
        elif "KEYLOG" in msg:
            key_logger()
        elif "PROCESS" in msg:
            app_process()
        elif "MAC" in msg:
            mac_address()
        # elif "DIRECTORY" in msg:
        #     directory_tree()
        elif "QUIT" in msg:
            com_con.close()
            s.close()
except:
    print("Error")