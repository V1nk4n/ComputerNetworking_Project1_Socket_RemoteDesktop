import os
import pickle
from tkinter import*
import  pickle
from RD_Constant import BUFFERSIZE


def show_tree(main_connect):
    ListDirectoryTree = []
    for c in range(ord('A'), ord('Z') + 1):
        path = chr(c) + ":\\"
        if os.path.isdir(path):
            ListDirectoryTree.append(path)
    data = pickle.dumps(ListDirectoryTree)
    main_connect.sendall(str(len(data)).encode())
    temp = main_connect.recv(BUFFERSIZE)
    main_connect.sendall(data)

def send_dir(main_connect):
    path = main_connect.recv(BUFFERSIZE).decode()
    if not os.path.isdir(path):
        return [False, path]

    try:
        listTree = []
        ListDirectoryTree = os.listdir(path)
        for d in ListDirectoryTree:
            listTree.append((d, os.path.isdir(path + "\\" + d)))
        
        data = pickle.dumps(listTree)
        main_connect.sendall(str(len(data)).encode())
        temp = main_connect.recv(BUFFERSIZE)
        main_connect.sendall(data)
        return [True, path]
    except:
        main_connect.sendall("error".encode())
        return [False, "error"]    

def delete_file(directoryConnection):
    file_name = directoryConnection.recv(BUFFERSIZE).decode()
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            directoryConnection.sendall("ok".encode())
        except:
            directoryConnection.sendall("error".encode())
            return
    else:
        directoryConnection.sendall("error".encode())
        return

# copy file from client to server
def send_file(main_connect):
    received = main_connect.recv(BUFFERSIZE).decode()
    if (received == "-1"):
        main_connect.sendall("-1".encode())
        return
    filename, filesize, path = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    main_connect.sendall("received filename".encode())
    data = b""
    while len(data) < filesize:
        packet = main_connect.recv(999999)
        data += packet
    if (data == "-1"):
        main_connect.sendall("-1".encode())
        return
    try:
        with open(path + filename, "wb") as file:
            file.write(data)
        main_connect.sendall("received content".encode())
    except:
        main_connect.sendall("-1".encode())

def copy_file(main_connect):
    filename = main_connect.recv(BUFFERSIZE).decode()
    if filename == "-1" or not os.path.isfile(filename):
        main_connect.sendall("-1".encode())
        return
    filesize = os.path.getsize(filename)
    main_connect.sendall(str(filesize).encode())
    temp = main_connect.recv(BUFFERSIZE)
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
        
        # copy file from client to server
        elif (mod == "COPYTO"):
            main_connect.sendall("OK".encode())
            send_file(main_connect)
            isMod = False

        # copy file from server to client
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