import tkinter as tk

from DC_Constant import BUFFERSIZE, FORMAT, BACKGROUND

def mac_addr(client):
    try:
        mac = client.recv(BUFFERSIZE).decode(FORMAT)
        mac = mac[2:].upper()
        mac = ':'.join(mac[i:i + 2] for i in range(0, len(mac), 2))
        tk.messagebox.showinfo(title='MAC Address', message="Server's MAC Address: "+mac)
    except:
        message = "Check the connection again"
        tk.messagebox.showerror(title='MAC Address', message=message)