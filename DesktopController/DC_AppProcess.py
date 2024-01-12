import pickle
import struct
import tkinter as tk
from tkinter import *
from tkinter import ttk
from DC_Constant import BACKGROUND, FORMAT, BUFFERSIZE, WIDTH, HEIGHT, myButton

class AppProcess(Frame):
    def __init__(self, parent, main_connect):
        Frame.__init__(self, parent)
        self.configure(
            bg=BACKGROUND,
            height=HEIGHT,
            width=WIDTH,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        parent.geometry("900x500+200+200")
        self.grid(row=0, column=0, sticky="nsew")
        
        self.client=main_connect
        self.status = True

        self.tab = ttk.Treeview(self, height=18, selectmode="browse")
        self.scroll = tk.Scrollbar(self, orient="vertical", command=self.tab.yview)
        self.scroll.place(x=803, y=12, height=350)
        self.tab.configure(yscrollcommand=self.scroll.set)
        self.tab["columns"] = ("Name", "ID", "VM", "CPU")
        self.tab.column("#0", width=0)
        self.tab.column("Name", anchor="center", width=120, minwidth=10, stretch=True)
        self.tab.column("ID", anchor="center", width=120, minwidth=10, stretch=True)
        self.tab.column("VM", anchor="center", width=120, minwidth=10, stretch=True)
        self.tab.column("CPU", anchor="center", width=120, minwidth=10, stretch=True)
        self.tab.heading("#0", text="")
        self.tab.heading("Name", text="Name Application")
        self.tab.heading("ID", text="ID Application")
        self.tab.heading("VM", text="VM")
        self.tab.heading("CPU", text="CPU")
        self.tab.place(x=93, y=12, width=713, height=350)

        self.button_process = myButton(self)
        self.button_process.configure(text="PROCESS", command=lambda: self.switch(self.button_process, self.tab))
        self.button_process.place(x=170, y=375, width=135, height=50)

        self.button_show = myButton(self)
        self.button_show.configure(text="SHOW", command=lambda: self.list(main_connect, self.tab, self.button_process["text"]))
        self.button_show.place(x=170, y=437, width=135, height=50)

        self.button_start = myButton(self)
        self.button_start.configure(text="START", command=lambda: self.start(parent, main_connect))
        self.button_start.place(x=382, y=375, width=135, height=50)

        self.button_end = myButton(self)
        self.button_end.configure(text="END", command=lambda: self.end(parent, main_connect))
        self.button_end.place(x=382, y=437, width=135, height=50)

        self.button_clear = myButton(self)
        self.button_clear.configure(text="CLEAR", command=lambda: self.clear(self.tab))
        self.button_clear.place(x=594, y=375, width=135, height=50)

        self.button_back = myButton(self)
        self.button_back.configure(text="BACK", command=lambda: self.back())
        self.button_back.place(x=594, y=437, width=135, height=50)
        
    def recvall(self, main_connect, size):
        message = bytearray()
        while len(message) < size:
            buffer = main_connect.recv(size - len(message))
            if not buffer:
                raise EOFError("Could not receive all expected data!")
            message.extend(buffer)
        return bytes(message)

    def receive(self,main_connect):
        packed = self.recvall(main_connect, struct.calcsize("!I"))
        size = struct.unpack("!I", packed)[0]
        data = self.recvall(main_connect, size)
        return data


    def switch(self, button, tab):
        if button["text"] == "PROCESS":
            button.configure(text="APPLICATION")
            tab.heading("Name", text="Name Process")
            tab.heading("ID", text="ID Process")
            tab.heading("VM", text="VM")
            tab.heading("CPU", text="CPU")
            
        else:
            button.configure(text="PROCESS")
            tab.heading("Name", text="Name Application")
            tab.heading("ID", text="ID Application")
            tab.heading("VM", text="VM")
            tab.heading("CPU", text="CPU")
        return


    def send_end(self, main_connect):
        global pid
        main_connect.sendall(bytes("0", "utf8"))
        main_connect.sendall(bytes(str(pid.get()), "utf8"))
        message = main_connect.recv(BUFFERSIZE).decode("utf8")
        if "1" in message:
            tk.messagebox.showinfo(message="End task!")
        else:
            tk.messagebox.showerror(message="Error!")
        return


    def list(self, main_connect, tab, s):
        main_connect.sendall("1".encode(FORMAT))
        main_connect.sendall(s.encode(FORMAT))
        list1 = self.receive(main_connect)
        list1 = pickle.loads(list1)
        list2 = self.receive(main_connect)
        list2 = pickle.loads(list2)
        list3 = self.receive(main_connect)
        list3 = pickle.loads(list3)
        list4 = self.receive(main_connect)
        list4 = pickle.loads(list4)
        for i in tab.get_children():
            tab.delete(i)
        for i in range(len(list1)):
            tab.insert(
                parent="", index="end", text="", values=(list1[i], list2[i], list3[i], list4[i])
            )
        return


    def clear(self, tab):
        for i in tab.get_children():
            tab.delete(i)
        return


    def send_start(self, main_connect):
        global pname
        main_connect.sendall("3".encode(FORMAT))
        main_connect.sendall(bytes(str(pname.get()), "utf8"))
        return


    def start(self, parent, main_connect):
        global pname
        pstart = tk.Toplevel(parent)
        pstart["bg"] = BACKGROUND
        pstart.geometry("420x70+450+300")
        pname = tk.StringVar(pstart)
        tk.Entry(pstart, textvariable=pname, width=38, borderwidth=5).place(x=10, y=20)
        myButton(
            pstart,
            text="Start",
            command=lambda: self.send_start(main_connect),
        ).place(x=275, y=15)
        return


    def end(self, parent, main_connect):
        global pid
        kill = tk.Toplevel(parent)
        kill["bg"] = BACKGROUND
        kill.geometry("420x70+450+300")
        pid = tk.StringVar(kill)
        tk.Entry(kill, textvariable=pid, width=38, borderwidth=5).place(x=10, y=20)
        myButton(
            kill,
            text="End",
            command=lambda: self.send_end(main_connect),
        ).place(x=275, y=15)
        return
    
    def back(self):
        self.status=False
        self.destroy()
        self.client.sendall("STOP".encode())

    