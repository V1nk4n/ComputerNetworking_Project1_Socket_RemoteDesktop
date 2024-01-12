import os
import tkinter as tk
import tkinter.ttk as ttk
import pickle
from tkinter import Text, Button,filedialog, messagebox, Frame
from tkinter import *
from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT, myButton

def list_dir(main_connect, path):
    main_connect.sendall(path.encode())
    data_size = int(main_connect.recv(BUFFERSIZE))
    if (data_size == -1):
        messagebox.showerror(message = "Click SHOW button again to watch the new directory tree!")
        return []
    main_connect.sendall("received filesize".encode())
    data = b""
    while len(data) < data_size:
        packet = main_connect.recv(BUFFERSIZE)
        data += packet
    if (data == "error"):
        messagebox.showerror(message = "Cannot open this directory!")
        return []
    
    loaded_list = pickle.loads(data)
    return loaded_list

class DirectoryTree(Frame):
    def __init__(self, window, main_connect):
        Frame.__init__(self, window)

        self.configure(
            bg=BACKGROUND,
            height=HEIGHT,
            width=WIDTH,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        window.geometry("900x500+200+200")
        self.grid(row=0, column=0, sticky="nsew")
        self.status = True

        self.client =  main_connect
        self.currPath = " "
        self.nodes = dict()
       
        self.frame = tk.Frame(self, height = 400, width = 500)
        self.tree = ttk.Treeview(self.frame)
        self.frame.place(
            x=100,
            y=23,
            width=700,
            height=300,
        )
        self.insText1 = "PATH"
        self.label1 = tk.Label(self.frame, text=self.insText1)
        self.label1.pack(fill = tk.X)
        self.path = Text(self.frame, height = 1, width = 26, state = "disable")
        self.path.pack(fill = tk.X)

        ysb = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Directory Tree', anchor='w')
        self.tree.pack(fill = tk.BOTH)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind("<<TreeviewSelect>>", self.select_node)

        self.insText2 = "Ấn nút SHOW để xem cây thư mục"
        self.label2 = tk.Label(self.frame, text=self.insText2)
        self.label2.pack(fill = tk.X)
        
        self.button_show_tree = myButton(self)
        self.button_show_tree.configure(text='SHOW', command=self.show_tree, relief="flat")
        self.button_show_tree.place(x=112,y=349,width=150,height=53)
        
        # chi gui vao folder th
        self.button_send_file = myButton(self)
        self.button_send_file.configure(text='SEND', command=self.send_file, relief="flat")
        self.button_send_file.place(x=374,y=349,width=150,height=53)
        # chi copy file
        self.button_copy_file = myButton(self)
        self.button_copy_file.configure(text='COPY', command=self.copy_file, relief="flat")
        self.button_copy_file.place(x=374,y=426,width=150,height=53)
        
        self.button_delete = myButton(self)
        self.button_delete.configure(text='DELETE', command=self.delete_file, relief="flat")
        self.button_delete.place(x=112,y=426,width=150,height=53)
        
        self.button_back = myButton(self)
        self.button_back.configure(text='BACK', command=self.click_back, relief="flat")
        self.button_back.place(x=636,y=385,width=150,height=53)

    def insert_node(self, parent, text, abspath, isFolder):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if abspath != "" and isFolder:
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            try:
                dirs = list_dir(self.client, abspath)
                for p in dirs:
                    self.insert_node(node, p[0], os.path.join(abspath, p[0]), p[1])
            except:
                messagebox.showerror(message = "Cannot open this directory!")

    def select_node(self, event):
        item = self.tree.selection()[0]
        parent = self.tree.parent(item)
        self.currPath = self.tree.item(item,"text")
        while parent:
            self.currPath = os.path.join(self.tree.item(parent)['text'], self.currPath)
            item = parent
            parent = self.tree.parent(item)

        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.insert(tk.END, self.currPath)
        self.path.config(state = "disable")

    def delete_tree(self):
        self.currPath = " "
        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.config(state = "disable")
        for i in self.tree.get_children():
            self.tree.delete(i)

    def show_tree(self):
        self.delete_tree()
        self.client.sendall("SHOW".encode())

        data_size = int(self.client.recv(BUFFERSIZE))
        self.client.sendall("received filesize".encode())
        data = b""
        while len(data) < data_size:
            packet = self.client.recv(BUFFERSIZE)
            data += packet
        loaded_list = pickle.loads(data)
        
        for path in loaded_list:
            try:
                abspath = os.path.abspath(path)
                self.insert_node('', abspath, abspath, True)
            except:
                continue

    # copy file from client to server
    def send_file(self):
        self.client.sendall("SEND".encode())
        isOk = self.client.recv(BUFFERSIZE).decode()
        if (isOk == "OK"):
            filename = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
            if filename == None or filename == "":
                self.client.sendall("-1".encode())
                temp = self.client.recv(BUFFERSIZE)
                return 
            destPath = self.currPath + "\\"
            filesize = os.path.getsize(filename)
            self.client.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{destPath}".encode())
            isReceived = self.client.recv(BUFFERSIZE).decode()
            if (isReceived == "received filename"):
                try:
                    with open(filename, "rb") as f:
                        data = f.read()
                        self.client.sendall(data)
                except:
                    self.client.sendall("-1".encode())
                isReceivedContent = self.client.recv(BUFFERSIZE).decode()
                if (isReceivedContent == "received content"):
                    messagebox.showinfo(message = "Copy successfully!")
                    return True
        messagebox.showerror(message = "Cannot copy!")    
        return False

    # copy file from server to client
    def copy_file(self):
        self.client.sendall("COPY".encode())
        isOk = self.client.recv(BUFFERSIZE).decode()
        if (isOk == "OK"):
            try:
                destPath = filedialog.askdirectory()
                if destPath == None or destPath == "":
                    self.client.sendall("-1".encode())
                    temp = self.client.recv(BUFFERSIZE)
                    return 
                self.client.sendall(self.currPath.encode())
                filename = os.path.basename(self.currPath)
                filesize = int(self.client.recv(100))
                if (filesize == -1):
                    messagebox.showerror(message = "Cannot copy!")  
                    return
                self.client.sendall("received filesize".encode())
                data = b""
                while len(data) < filesize:
                    packet = self.client.recv(999999)
                    data += packet
                with open(destPath + "\\" + filename, "wb") as f:
                    f.write(data)
                messagebox.showinfo(message = "Copy successfully!")
            except:
                messagebox.showerror(message = "Cannot copy!")  
        else:
            messagebox.showerror(message = "Cannot copy!") 

    def delete_file(self):
        self.client.sendall("DEL".encode())
        isOk = self.client.recv(BUFFERSIZE).decode()
        if (isOk == "OK"):
            self.client.sendall(self.currPath.encode())
            res = self.client.recv(BUFFERSIZE).decode()
            if (res == "ok"):
                messagebox.showinfo(message = "Delete successfully!")
            else:
                messagebox.showerror(message = "Cannot delete!") 
        else: 
            messagebox.showerror(message = "Cannot delete!")  

    def click_back(self):
        self.status = False
        self.destroy()
        self.client.sendall("STOP".encode())
