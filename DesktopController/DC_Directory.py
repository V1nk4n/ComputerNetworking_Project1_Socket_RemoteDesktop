import os
import tkinter as tk
import tkinter.ttk as ttk
import pickle
from tkinter import Text, filedialog, messagebox, Frame
from tkinter import *
from DC_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT, myButton

def list_dir(main_connect, path):
    #Gửi đừng đi cần nhận folder và file con
    main_connect.sendall(path.encode())
    #Nhận size của các folder và file con
    data_size = int(main_connect.recv(BUFFERSIZE))
    #Nhận size lỗi
    if (data_size == -1):
        messagebox.showerror(message = "Click SHOW button again to update and watch the new directory tree!")
        return []
    #Báo nhận size thanh cong
    main_connect.sendall("Receive size successfully".encode())
    #NHận dữ liệu các folder và file con
    data = b""
    while len(data) < data_size:
        packet = main_connect.recv(BUFFERSIZE)
        data += packet
    if (data == "error"):
        messagebox.showerror(message = "Error! Cannot open this directory.")
        return []
    #Chuyển từ bytes sang folder và file binh thường
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

        self.main_connect =  main_connect
        self.curPath = " "
        self.nodes = dict()
       
        self.frame1 = tk.Frame(self,bg = "#fdebd3")
        self.frame1.place(
            x=100,
            y=23,
            width=700,
            height=300,
        )
        self.frame = tk.Frame(self.frame1)
        self.frame.place(
            x=0,
            y=75,
            height = 300,
            width = 700,
        )
        self.tree = ttk.Treeview(self.frame)

        self.insText1 = "Selected Path"
        self.label1 = tk.Label(self.frame1, text=self.insText1,bg = "#fdebd3")
        self.label1.pack(fill = tk.X)
        self.path = Text(self.frame1, height = 1, width = 700, state = "disable")
        self.path.pack(fill = tk.X)

        ysb = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text="SERVERS'S DIRECTORY TREE", anchor='w',)
        self.tree.pack(fill = tk.BOTH)
        
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind("<<TreeviewSelect>>", self.select_node)

        self.insText2 = "Click SHOW button again to watch the new directory tree!"
        self.label2 = tk.Label(self.frame1, text=self.insText2,bg = "#fdebd3")
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
        #Thêm node vào cuối cây chỉ có text
        node = self.tree.insert(parent,'end', text=text, open=False)
        if abspath != "" and isFolder:
            #Thêm đường đi tuyệt đối của node vào danh sách self.nodes
            self.nodes[node] = abspath
            #Thêm node và danh sách tuyệt đối của node vào cây
            self.tree.insert(node, 'end')

    def open_node(self, event):
        #Node được chọn
        node = self.tree.focus()
        #Loại bỏ node đó khỏi danh sách các node của cây
        absPath = self.nodes.pop(node, None)
        #Nếu tồn tại đường đi đến node được chọn
        if absPath:
            #Xóa các node con bên trong node được chọn khỏi cây
            self.tree.delete(self.tree.get_children(node))
            try:
                #Lấy danh sách folder và file con sau đó thêm vào cây
                dirs = list_dir(self.main_connect, absPath)
                for p in dirs:
                    self.insert_node(node, p[0], os.path.join(absPath, p[0]), p[1])
            except:
                messagebox.showerror(message = "Error! Cannot open this directory.")

    def select_node(self, event):
        #Node được chọn
        selected = self.tree.selection()
        #Lấy node cha của node được chọn
        parent = self.tree.parent(selected)
        #Lấy text mà node được chọn đang giữ
        self.curPath = self.tree.item(selected,"text")
        #Ghép tên của node được chọn với tổ tiên của nó
        while parent:
            self.curPath = os.path.join(self.tree.item(parent)['text'], self.curPath)
            selected = parent
            parent = self.tree.parent(selected)
        #Cập nhật đường đi trên thanh đường đi.
        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.insert("1.0", self.curPath)
        self.path.config(state = "disable")

    def delete_tree(self):
        #Xóa hết dữ liệu của biến đường đi hiện tại
        self.curPath = " "
        #Xóa dòng hiện đường đi được chọn
        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.config(state = "disable")
        #Xóa các node của cây
        for i in self.tree.get_children():
            self.tree.delete(i)

    def show_tree(self):
        #Xóa cây để hiện cây mới
        self.delete_tree()
        self.main_connect.sendall("SHOW".encode())
        #Nhận size của cây mới (Gồm tên các ổ đĩa)
        data_size = int(self.main_connect.recv(BUFFERSIZE))
        #Nhận size thành công
        self.main_connect.sendall("Receive size successfully".encode())
        #Nhận dữ liệu
        data = b""
        while len(data) < data_size:
            packet = self.main_connect.recv(BUFFERSIZE)
            data += packet
        #Chuyển dữ liệu từ byte về folder bình thưởng
        loaded_list = pickle.loads(data)
        #Thêm các ổ đĩa vào cuối ccủa cây
        for path in loaded_list:
            try:
                #Đường đi tuyệt đối
                abspath = os.path.abspath(path)
                self.insert_node('', abspath, abspath, True)
            except:
                continue

    def send_file(self):
        self.main_connect.sendall("SEND".encode())
        isOk = self.main_connect.recv(BUFFERSIZE).decode()
        if (isOk == "OK"):
            #Chọn file cần gửi đến Server
            pathfile = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
            if pathfile == None or pathfile == "":
                self.main_connect.sendall("-1".encode())
                temp = self.main_connect.recv(BUFFERSIZE)
                return
            #Folder lưu file được nhận bên Server
            destPath = self.curPath + "\\"
            #Gửi kich cỡ của file
            filesize = os.path.getsize(pathfile)
            #Gửi tên file, kích cỡ của file, folder lưu trữ bên Server
            filename = os.path.basename(pathfile)
            self.main_connect.sendall(f"{filename},{filesize},{destPath}".encode())
            isReceived = self.main_connect.recv(BUFFERSIZE).decode()
            if (isReceived == "received filename"):
                try:
                    #Đọc và gửi dữ liệu của file
                    with open(pathfile, "rb") as f:
                        data = f.read()
                        self.main_connect.sendall(data)
                except:
                    self.main_connect.sendall("-1".encode())
                isReceivedContent = self.main_connect.recv(BUFFERSIZE).decode()
                if (isReceivedContent == "received content"):
                    messagebox.showinfo(message = "Copy file successfully!")
                    return True
        messagebox.showerror(message = "Error! Cannot copy file.")    
        return False

    def copy_file(self):
        self.main_connect.sendall("COPY".encode())
        isOk = self.main_connect.recv(BUFFERSIZE).decode()
        if (isOk == "OK"):
            try:
                #Chọn thư mục chưa file được copy
                destPath = filedialog.askdirectory()
                if destPath == None or destPath == "":
                    self.main_connect.sendall("-1".encode())
                    temp = self.main_connect.recv(BUFFERSIZE)
                    return
                #Gửi đường đi được chọn hiện tại qua Server
                self.main_connect.sendall(self.curPath.encode())
                #Lấy tên file
                filename = os.path.basename(self.curPath)
                #Nhận size của file
                filesize = int(self.main_connect.recv(100))
                if (filesize == -1):
                    messagebox.showerror(message = "Error! Cannot copy file.")  
                    return
                self.main_connect.sendall("received filesize".encode())
                #Nhận dữ liệu của file
                data = b""
                while len(data) < filesize:
                    packet = self.main_connect.recv(999999)
                    data += packet
                #Tạo ra file và ghi dữ liệu vào
                with open(destPath + "\\" + filename, "wb") as f:
                    f.write(data)
                messagebox.showinfo(message = "Copy file successfully!")
            except:
                messagebox.showerror(message = "Error! Cannot copy file.")  
        else:
            messagebox.showerror(message = "Error! Cannot copy file.") 

    def delete_file(self):
        self.main_connect.sendall("DEL".encode())
        isOk = self.main_connect.recv(BUFFERSIZE).decode()
        if (isOk == "OK"):
            #Gửi đường đi đang được chọn để xóa
            self.main_connect.sendall(self.curPath.encode())
            #Nhận thông tin xóa thành công hay không
            res = self.main_connect.recv(BUFFERSIZE).decode()
            if (res == "ok"):
                messagebox.showinfo(message = "Delete file successfully!")
            else:
                messagebox.showerror(message = "Error! Cannot delete file.") 
        else: 
            messagebox.showerror(message = "Error! Cannot delete file.")  

    def click_back(self):
        self.status = False
        self.destroy()
        self.main_connect.sendall("STOP".encode())
