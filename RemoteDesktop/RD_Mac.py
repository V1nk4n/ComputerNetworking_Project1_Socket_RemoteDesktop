import uuid
from RD_Constant import FORMAT

def mac_addr(com_con):
    com_con.sendall(hex(uuid.getnode()).encode(FORMAT))
    return
