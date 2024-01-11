import pickle
import struct
import tkinter as tk
from tkinter import *
from tkinter import ttk
from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT

class AppProcess(Frame):
    def __init__(self, parent, client):
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
        
        self.client=client
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

        self.button_process = Button(
            self,
            text="PROCESS",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.switch(self.button_process, self.tab),
        )
        self.button_process.place(x=170, y=375, width=135, height=50)

        self.button_show = Button(
            self,
            text="SHOW",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.list(client, self.tab, self.button_process["text"]),
        )
        self.button_show.place(x=170, y=437, width=135, height=50)

        self.button_start = Button(
            self,
            text="START",
            font=("Tim New Roman",15),
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.start(parent, client),
        )
        self.button_start.place(x=382, y=375, width=135, height=50)

        self.button_end = Button(
            self,
            text="END",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.end(parent, client),
        )
        self.button_end.place(x=382, y=437, width=135, height=50)

        self.button_clear = Button(
            self,
            text="CLEAR",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.clear(self.tab),
        )
        self.button_clear.place(x=594, y=375, width=135, height=50)

        self.button_back = Button(
            self,
            text="BACK",
            width=20,
            height=5,
            bg="#fdebd3",
            fg="black",
            font=("Tim New Roman",15),
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.back(),
        )
        self.button_back.place(x=594, y=437, width=135, height=50)
    def recvall(self,sock, size):
        message = bytearray()
        while len(message) < size:
            buffer = sock.recv(size - len(message))
            if not buffer:
                raise EOFError("Could not receive all expected data!")
            message.extend(buffer)
        return bytes(message)

    def receive(self,client):
        packed = self.recvall(client, struct.calcsize("!I"))
        size = struct.unpack("!I", packed)[0]
        data = self.recvall(client, size)
        return data


    def switch(self,button, tab):
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


    def send_end(self,client):
        global pid
        client.sendall(bytes("0", "utf8"))
        client.sendall(bytes(str(pid.get()), "utf8"))
        message = client.recv(BUFFERSIZE).decode("utf8")
        if "1" in message:
            tk.messagebox.showinfo(message="End task!")
        else:
            tk.messagebox.showerror(message="Error!")
        return


    def list(self,client, tab, s):
        client.sendall(bytes("1", "utf8"))
        client.sendall(bytes(s, "utf8"))
        list1 = self.receive(client)
        list1 = pickle.loads(list1)
        list2 = self.receive(client)
        list2 = pickle.loads(list2)
        list3 = self.receive(client)
        list3 = pickle.loads(list3)
        list4 = self.receive(client)
        list4 = pickle.loads(list4)
        for i in tab.get_children():
            tab.delete(i)
        for i in range(len(list1)):
            tab.insert(
                parent="", index="end", text="", values=(list1[i], list2[i], list3[i], list4[i])
            )
        return


    def clear(self,tab):
        for i in tab.get_children():
            tab.delete(i)
        return


    def send_start(self,client):
        global pname
        client.sendall(bytes("3", "utf8"))
        client.sendall(bytes(str(pname.get()), "utf8"))
        return


    def start(self, root, client):
        global pname
        pstart = tk.Toplevel(root)
        pstart["bg"] = BACKGROUND
        pstart.geometry("420x70")
        pname = tk.StringVar(pstart)
        tk.Entry(pstart, textvariable=pname, width=38, borderwidth=5).place(x=10, y=20)
        tk.Button(
            pstart,
            text="Start",
            font=("Tim New Roman",15),
            width=15,
            height=2,
            fg="black",
            bg="#fdebd3",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.send_start(client),
        ).place(x=275, y=15)
        return


    def end(self, root, client):
        global pid
        kill = tk.Toplevel(root)
        kill["bg"] = BACKGROUND
        kill.geometry("420x70")
        pid = tk.StringVar(kill)
        tk.Entry(kill, textvariable=pid, width=38, borderwidth=5).place(x=10, y=20)
        tk.Button(
            kill,
            text="End",
            font=("Tim New Roman",15),
            width=15,
            height=2,
            fg="black",
            bg="#fdebd3",
            borderwidth=3,
            highlightthickness=2,
            command=lambda: self.send_end(client),
        ).place(x=275, y=15)
        return
    def back(self):
        self.status=False
        self.destroy()
        self.client.sendall("STOP".encode())

    