import socket

HOST = "127.0.0.1"
SERVER_PORT = 61000
FORMAT = "utf8"
BUFFERSIZE = 1024*1024
DELAY = 0.0001

def listen():
    with keyboard.Listener(on_press = on_key) as listener:
        listener.join()
    
def sendKey(conn):
    listen()
    while True:
        conn.sendall(buffer.encode(FORMAT))
        buffer = " "

def sendMouse(conn):
    while True:
        x, y = pag.position()
        # x = root.winfo_pointerx()
        # y = root.winfo_pointery()
        conn.sendall(f"{x},{y}".encode())
        time.sleep(1)


    # def ConnectScreen(self):
    #     return self.sk.accept()
    
    # def ConnectMouse(self):
    #     return self.sk.accept()
    
    # while self.mouseConnection:
        #     window.update_idletasks()
        #     time.sleep(2*DELAY)
        
        
# sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sk.bind((HOST, SERVER_PORT))
# sk.listen()
# print("Controller")
# MouseThread, Mouseaddr = sk.accept()
# ScreenThread, Screenaddr = sk.accept()

# MouseThread.sendall("Mouse".encode(FORMAT))
# Screen = ScreenThread.recv(BUFFERSIZE).decode(FORMAT)
# print(Screen)
# input()

    # def recvImage(self):
    #     length_bytes = self.connection.recv(4)
    #     image_length = int.from_bytes(length_bytes)
        
    #     image_byte_array = b""
    #     while len(image_byte_array) < length_bytes:
    #             buffer = self.connection.recv(BUFFERSIZE)
    #             if not buffer:
    #                 break
    #             image_byte_array += buffer


    #     if len(image_byte_array) == image_length:
    #         image_byte_io = io.BytesIO(image_byte_array)
    #         image = Image.open(image_byte_io)
    #         return image
    #     else:
    #         print("Chua nhan du du lieu")
    #         return None  
    
    # def on_key(self, key):
    #     try:
    #         key_value = key.char
    #     except:
    #         key_value = str(key)
    #     self.connection.sendall(key.encode(FORMAT))
    

    # def listen_keyboard():
    #     with keyboard.Listener(on_press = on_key) as listener:
    #         listener.join()