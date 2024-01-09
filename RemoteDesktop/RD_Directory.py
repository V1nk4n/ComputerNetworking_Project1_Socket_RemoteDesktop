import os
import pickle
from tkinter import*
import  pickle
from RD_Constant import BACKGROUND, BUFFERSIZE, WIDTH, HEIGHT, FORMAT


def showTree(directoryConnection):
    ListDirectoryTree = []
    for c in range(ord('A'), ord('Z') + 1):
        path = chr(c) + ":\\"
        if os.path.isdir(path):
            ListDirectoryTree.append(path)
    data = pickle.dumps(ListDirectoryTree)
    directoryConnection.sendall(str(len(data)).encode())
    temp = directoryConnection.recv(BUFFERSIZE)
    directoryConnection.sendall(data)

def sendListDirs(directoryConnection):
    path = directoryConnection.recv(BUFFERSIZE).decode()
    if not os.path.isdir(path):
        return [False, path]

    try:
        listTree = []
        ListDirectoryTree = os.listdir(path)
        for d in ListDirectoryTree:
            listTree.append((d, os.path.isdir(path + "\\" + d)))
        
        data = pickle.dumps(listTree)
        directoryConnection.sendall(str(len(data)).encode())
        temp = directoryConnection.recv(9999999)
        directoryConnection.sendall(data)
        return [True, path]
    except:
        directoryConnection.sendall("error".encode())
        return [False, "error"]    

def deleteFile(directoryConnection):
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
def copyFileToServer(directoryConnection):
    received = directoryConnection.recv(BUFFERSIZE).decode()
    if (received == "-1"):
        directoryConnection.sendall("-1".encode())
        return
    filename, filesize, path = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    directoryConnection.sendall("received filename".encode())
    data = b""
    while len(data) < filesize:
        packet = directoryConnection.recv(999999)
        data += packet
    if (data == "-1"):
        directoryConnection.sendall("-1".encode())
        return
    try:
        with open(path + filename, "wb") as file:
            file.write(data)
        directoryConnection.sendall("received content".encode())
    except:
        directoryConnection.sendall("-1".encode())

# copy file from server to client
def copyFileToClient(directoryConnection):
    filename = directoryConnection.recv(BUFFERSIZE).decode()
    if filename == "-1" or not os.path.isfile(filename):
        directoryConnection.sendall("-1".encode())
        return
    filesize = os.path.getsize(filename)
    directoryConnection.sendall(str(filesize).encode())
    temp = directoryConnection.recv(BUFFERSIZE)
    with open(filename, "rb") as f:
        data = f.read()
        directoryConnection.sendall(data)

def directory(directoryConnection):
    isMod = False
    
    while True:
        if not isMod:
            mod = directoryConnection.recv( BUFFERSIZE).decode()

        if (mod == "SHOW"):
            showTree(directoryConnection)
            while True:
                check = sendListDirs(directoryConnection)
                if not check[0]:    
                    mod = check[1]
                    if (mod != "error"):
                        isMod = True
                        break
        
        # copy file from client to server
        elif (mod == "COPYTO"):
            directoryConnection.sendall("OK".encode())
            copyFileToServer(directoryConnection)
            isMod = False

        # copy file from server to client
        elif (mod == "COPY"):
            directoryConnection.sendall("OK".encode())
            copyFileToClient(directoryConnection)
            isMod = False

        elif (mod == "DEL"):
            directoryConnection.sendall("OK".encode())
            deleteFile(directoryConnection)
            isMod = False

        elif (mod == "QUIT"):
            return
        
        else:
            directoryConnection.sendall("-1".encode())