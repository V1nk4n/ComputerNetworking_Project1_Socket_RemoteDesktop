import tkinter as tk
from DC_Constant import BUFFERSIZE, FORMAT
from DC_Constant import BACKGROUND,WIDTH, HEIGHT, FONT

def mac_addr(main_connect):
    try:
        #Nhận mac address từ server
        mac = main_connect.recv(BUFFERSIZE).decode(FORMAT)
        #In hoa các ký tự từ vị trí 2 trong mac
        mac = mac[2:].upper()
        #Chèn : vào mỗi 2 ký tự
        mac = ':'.join(mac[i:i + 2] for i in range(0, len(mac), 2))
        
        box = tk.Tk()
        box.configure(
            bg=BACKGROUND,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        box.title("MAC ADDRESS")
        box.geometry("420x70+450+300")

        ip_label = tk.Label(
            box,
            text="Server's MAC Address: "+mac,
            font=(FONT,13),
            bg="#fdebd3",
            fg="black",
            borderwidth=2,
            highlightthickness=2,
        )
        ip_label.place(x=40, y=20)
    except:
        message = "Check the connection again"
        tk.messagebox.showerror(title='MAC Address', message=message)