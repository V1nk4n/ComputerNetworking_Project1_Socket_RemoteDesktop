from RD_Constant import FORMAT
from uuid import getnode as get_mac

#Lấy địa chỉ mac
mac = get_mac()
#Gửi địa chỉ mac
def mac_addr(main_connect):
    main_connect.sendall(hex(mac).encode(FORMAT))
    return
