import os
from RD_Constant import BUFFERSIZE, FORMAT

def shutout(com_con):
    while(True):
        message = com_con.recv(BUFFERSIZE).decode(FORMAT)
        if "SHUTDOWN" in message:
            os.system('shutdown -s -t 15')
        elif "LOGOUT" in message:
            os.system('shutdown -l')
        else:
            return
    return
    