import os
from RD_Constant import BUFFERSIZE, FORMAT

def shutout(main_connect):
    while(True):
        msg = main_connect.recv(BUFFERSIZE).decode(FORMAT)
        if "SHUTDOWN" in msg:
            #Shutdown server sau 10s
            os.system('shutdown -s -t 10')
        elif "LOGOUT" in msg:
            #Logout Server
            os.system('shutdown -l')
        else:
            return
    return
    