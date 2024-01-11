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


def list_apps():
    list1 = list()
    list2 = list()
    list3 = list()

    cmd = r'powershell "gps | where {$_.mainWindowTitle} | select Description, ID, @{Name=\'CPU_Percent\'; Expression={(Get-Process -Id $_.Id).CPU}}"'
    proc = os.popen(cmd).read().split("\n")
    temp = list()
    for line in proc:
        if not line.isspace():
            temp.append(line)
    temp = temp[3:]
    for line in temp:
        try:
            arr = line.split(" ")
            if len(arr) < 3:
                continue
            if arr[0] == "" or arr[0] == " ":
                continue

            name = arr[0]
            threads = arr[-1]
            ID = 0
            # interation
            cur = len(arr) - 2
            for i in range(cur, -1, -1):
                if len(arr[i]) != 0:
                    ID = arr[i]
                    cur = i
                    break
            for i in range(1, cur, 1):
                if len(arr[i]) != 0:
                    name += " " + arr[i]
            list1.append(name)
            list2.append(ID)
            list3.append(threads)
        except:
            pass
    return list1, list2, list3


def list_processes():
    list1 = list()
    list2 = list()
    list3 = list()
    for proc in psutil.process_iter():
        try:
            name = proc.name()
            pid = proc.pid
            cpu = proc.cpu_percent(interval=None)
            list1.append(str(name))
            list2.append(str(pid))
            list3.append(str(cpu))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list1, list2, list3


def kill(pid):
    cmd = "taskkill.exe /F /PID " + str(pid)
    try:
        a = os.system(cmd)
        if a == 0:
            return 1
        else:
            return 0
    except:
        return 0


def start(name):
    subprocess.Popen(name)
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
        option = int(msg)
        
        if option == 0:
            pid = client.recv(BUFFERSIZE).decode("utf8")
            pid = int(pid)
            try:
                result = kill(pid)
            except:
                result = 0
        elif option == 1:
            try:
                status = client.recv(BUFFERSIZE).decode("utf8")
                if "PROCESS" in status:
                    list1, list2, list3 = list_apps()
                else:
                    list1, list2, list3 = list_processes()
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

            send_data(client, list1)
            send_data(client, list2)
            send_data(client, list3)
    return
