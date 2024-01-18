import os
import pickle
from tkinter import*
import  pickle
from RD_Constant import BUFFERSIZE


def show_tree(main_connect):
    ListDirectoryTree = []
    #Lấy các ổ đĩa của máy tính
    for c in range(65, 91):
        path = chr(c) + ":\\"
        if os.path.isdir(path):
            ListDirectoryTree.append(path)
    #Chuyển đường đi của ổ đĩa về dạng byte
    data = pickle.dumps(ListDirectoryTree)
    #Gửi size và dữ liệu của ổ đĩa qua Client
    main_connect.sendall(str(len(data)).encode())
    temp = main_connect.recv(BUFFERSIZE)
    main_connect.sendall(data)

def send_dir(main_connect):
    #Nhận đường đi
    path = main_connect.recv(BUFFERSIZE).decode()
    #Xem có tồn tại đường đi đó không
    if not os.path.isdir(path):
        return [False, path]
    try:
        listTree = []
        #Lấy tất cả các folder và file con
        ListDirectoryTree = os.listdir(path)
        #Thêm vào danh sách folde và file con để đưa cho client
        #Nếu tồn tại folder và file con đó thêm một tham số bool
        for d in ListDirectoryTree:
            listTree.append((d, os.path.isdir(path + "\\" + d)))
        # Chuyển từ dữ liệu bình thưởng sang bytes để gửi qua socket
        data = pickle.dumps(listTree)
        #Gửi size của dữ liệu đã chuyển sang byte
        main_connect.sendall(str(len(data)).encode())
        #Chờ phản hồi Client đã nhận được size
        temp = main_connect.recv(BUFFERSIZE)
        #GỬi dữ liệu
        main_connect.sendall(data)
        return [True, path]
    except:
        main_connect.sendall("error".encode())
        return [False, "error"]    

def delete_file(directoryConnection):
    file_name = directoryConnection.recv(BUFFERSIZE).decode()
    #Xem tên file có không
    if os.path.exists(file_name):
        try:
            #Xóa file
            os.remove(file_name)
            directoryConnection.sendall("ok".encode())
        except:
            directoryConnection.sendall("error".encode())
            return
    else:
        directoryConnection.sendall("error".encode())
        return

def send_file(main_connect):
    #Nhận tên file, kích cỡ của file, folder để lưu file
    received = main_connect.recv(BUFFERSIZE).decode()
    if (received == "-1"):
        main_connect.sendall("-1".encode())
        return
    filename, filesize, path = received.split(",")
    filesize = int(filesize)
    main_connect.sendall("received filename".encode())
    #Nhận dữ liệu của file
    data = b""
    while len(data) < filesize:
        packet = main_connect.recv(999999)
        data += packet
    if (data == "-1"):
        main_connect.sendall("-1".encode())
        return
    try:
        #Lưu file
        with open(path + filename, "wb") as file:
            file.write(data)
        main_connect.sendall("received content".encode())
    except:
        main_connect.sendall("-1".encode())

def copy_file(main_connect):
    #Nhận tên file
    filename = main_connect.recv(BUFFERSIZE).decode()
    if filename == "-1" or not os.path.isfile(filename):
        main_connect.sendall("-1".encode())
        return
    filesize = os.path.getsize(filename)
    #Gửi size của file
    main_connect.sendall(str(filesize).encode())
    temp = main_connect.recv(BUFFERSIZE)
    #Đọc và gửi dữ liệu của file
    with open(filename, "rb") as f:
        data = f.read()
        main_connect.sendall(data)

def directory(main_connect):
    isMod = False
    
    while True:
        if not isMod:
            mod = main_connect.recv( BUFFERSIZE).decode()

        if (mod == "SHOW"):
            show_tree(main_connect)
            while True:
                check = send_dir(main_connect)
                if not check[0]:    
                    mod = check[1]
                    if (mod != "error"):
                        isMod = True
                        break
        
        elif (mod == "SEND"):
            main_connect.sendall("OK".encode())
            send_file(main_connect)
            isMod = False

        elif (mod == "COPY"):
            main_connect.sendall("OK".encode())
            copy_file(main_connect)
            isMod = False

        elif (mod == "DEL"):
            main_connect.sendall("OK".encode())
            delete_file(main_connect)
            isMod = False

        elif (mod == "STOP"):
            return
        
        else:
            main_connect.sendall("-1".encode())