import os
from RD_Constant import BUFFERSIZE, FORMAT

def shutout(main_connect):
    while(True):
        msg = main_connect.recv(BUFFERSIZE).decode(FORMAT)
        if "SHUTDOWN" in msg:
            os.system('shutdown -s -t 15')
        elif "LOGOUT" in msg:
            os.system('shutdown -l')
        else:
            return
    return
    