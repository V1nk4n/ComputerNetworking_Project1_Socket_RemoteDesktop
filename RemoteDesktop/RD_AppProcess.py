import os
import pickle
import struct
import subprocess
import psutil
from RD_Constant import BUFFERSIZE


def send_data(client, data):
    size = struct.pack("!I", len(data))
    data = size + data
    client.sendall(data)
    return


def list_processes():
    list1 = list()
    list2 = list()
    list3 = list()
    list4 = list()
    cmd = "PowerShell -Command \"Get-Process | Select ProcessName, ID, VM, CPU\""
    proc = os.popen(cmd).read().split("\n")
    temp = list()
    
    proc.pop(0)
    proc.pop(0)
    proc.pop(0)
    
    for i in proc:
        if i == ' ' or i == '':
            continue
        print(i)
        i = i + '0'
        list1.append(i[:i.find(' ')])
        
        i = i[i.find(' ') :].strip()
        
        list2.append(i[:i.find(' ')])
        
        i = i[i.find(' '):].strip()
        list3.append(i[:i.find(' ')])
        
        list4.append(i[i.find(' '):].strip(' '))
        

    return list1, list2, list3, list4

def list_apps():
    list1 = list()
    list2 = list()
    list3 = list()
    list4 = list()
    cmd = "PowerShell -Command \"Get-Process |  where{$_.MainWindowTitle -ne \\\"\\\"} | Select Description,Id,VM,CPU\""
    apps = os.popen(cmd).read().split("\n")
    temp = list()
    
    apps.pop(0)
    apps.pop(0)
    apps.pop(0)

    for i in apps:
        if i == ' ' or i == '':
            continue
        print(i)
        i = i + '0'
        list1.append(i[:i.find(' ')])
        
        i = i[i.find(' ') :].strip()
        
        list2.append(i[:i.find(' ')])
        
        i = i[i.find(' '):].strip()
        list3.append(i[:i.find(' ')])
        
        list4.append(i[i.find(' '):].strip(' '))
        
    return list1, list2, list3, list4


def end(pid):
    cmd = "taskkill.exe /F /PID " + str(pid)
    try:
        a = os.system(cmd)
        if a == 0:
            return 1
        else:
            return 0
    except:
        return 0


def start(pname):
    subprocess.Popen(pname)
    return

def app_process(client):
    global msg
    while True:
        msg = client.recv(BUFFERSIZE).decode("utf8")
        if "STOP" in msg and len(msg) < 20:
            return
        result = 0
        list1 = list()
        list2 = list()
        list3 = list()
        list4 = list()
        option = int(msg)
        
        if option == 0:
            pid = client.recv(BUFFERSIZE).decode("utf8")
            pid = int(pid)
            try:
                result = end(pid)
            except:
                result = 0
        elif option == 1:
            try:
                status = client.recv(BUFFERSIZE).decode("utf8")
                if "PROCESS" in status:
                    list1, list2, list3, list4 = list_apps()
                else:
                    list1, list2, list3, list4 = list_processes()

                result = 1
            except:
                result = 0
        elif option == 2:
            result = 1
        elif option == 3:
            program_name = client.recv(BUFFERSIZE).decode("utf8")
            try:
                start(program_name)
                result = 1
            except:
                result = 0
        if option != 1 and option != 3:
            client.sendall(bytes(str(result), "utf8"))
        if option == 1:
            list1 = pickle.dumps(list1)
            list2 = pickle.dumps(list2)
            list3 = pickle.dumps(list3)
            list4 = pickle.dumps(list4)

            send_data(client, list1)
            send_data(client, list2)
            send_data(client, list3)
            send_data(client, list4)
    return
