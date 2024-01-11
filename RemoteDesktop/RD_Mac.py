from RD_Constant import FORMAT
from uuid import getnode as get_mac

mac = get_mac()

def mac_addr(main_connect):
    main_connect.sendall(hex(mac).encode(FORMAT))
    return
