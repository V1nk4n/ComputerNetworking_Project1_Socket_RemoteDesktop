from RD_Constant import FORMAT
from uuid import getnode as get_mac

mac = get_mac()

def mac_addr(com_con):
    com_con.sendall(hex(mac).encode(FORMAT))
    return
