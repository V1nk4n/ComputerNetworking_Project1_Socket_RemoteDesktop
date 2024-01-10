import tkinter as tk
from DC_Constant import BACKGROUND
from DC_Constant import FORMAT

def close_event(main, com_con):
    com_con.sendall("QUIT".encode(FORMAT))
    main.destroy()
    return

def shutdown(com_con):
    com_con.sendall("SHUTDOWN".encode(FORMAT))
def logout(com_con):
    com_con.sendall("LOGOUT".encode(FORMAT))

def shutdown_logout(parent, com_con):
    window = tk.Toplevel(parent)
    window.geometry("190x160")
    window.grab_set()
    window.protocol("WM_DELETE_WINDOW", lambda: close_event(window, com_con))
    shutdown_button = tk.Button(
        window, text = 'SHUTDOWN', width = 20, height = 2, fg = "black", bg = BACKGROUND, 
        command = lambda: shutdown(com_con), padx = 20, pady = 20)
    shutdown_button.grid(row = 0, column = 0)
    logout_button = tk.Button(
        window, text = 'LOGOUT', width = 20, height = 2, fg = BACKGROUND, bg = "black", 
        command = lambda: logout(com_con), padx = 20, pady = 20)
    logout_button.grid(row = 1, column = 0)
    window.mainloop()
