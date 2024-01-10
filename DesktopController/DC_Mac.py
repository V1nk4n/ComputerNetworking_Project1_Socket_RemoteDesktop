import tkinter as tk

from DC_Constant import BUFFERSIZE, FORMAT, BACKGROUND

def mac_addr(client):
    try:
        result = client.recv(BUFFERSIZE).decode(FORMAT)
        result = result[2:].upper()
        result = ':'.join(result[i:i + 2] for i in range(0, len(result), 2))
        tk.messagebox.showinfo(title='MAC Address', message="Server's MAC Address: "+result)
    except:
        message = "Check the connection again"
        tk.messagebox.showerror(title='MAC Address', message=message)