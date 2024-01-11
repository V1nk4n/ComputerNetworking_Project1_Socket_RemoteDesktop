import tkinter as tk
from DC_Constant import BACKGROUND
from DC_Constant import FORMAT

def click_close(window, main_connect):
    main_connect.sendall("QUIT".encode(FORMAT))
    window.destroy()
    return

def shutdown(com_con):
    com_con.sendall("SHUTDOWN".encode(FORMAT))
def logout(com_con):
    com_con.sendall("LOGOUT".encode(FORMAT))

def shutout(parent, com_con):
    window = tk.Toplevel(parent)
    window.geometry("200x160")
    window.grab_set()
    window.protocol("WM_DELETE_WINDOW", lambda: click_close(window, com_con))
    shutdown_option = tk.Button(
        window, text = 'SHUTDOWN', width = 22, height = 2, fg = "black", bg = BACKGROUND, 
        command = lambda: shutdown(com_con), padx = 20, pady = 20)
    shutdown_option.grid(row = 0, column = 0)
    logout_option = tk.Button(
        window, text = 'LOGOUT', width = 22, height = 2, fg = BACKGROUND, bg = "black", 
        command = lambda: logout(com_con), padx = 20, pady = 20)
    logout_option.grid(row = 1, column = 0)
    window.mainloop()
