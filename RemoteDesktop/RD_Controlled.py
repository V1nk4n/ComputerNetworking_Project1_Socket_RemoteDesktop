from threading import Thread
from Constant import FORMAT, BUFFERSIZE
import pyautogui as pag
import io
import socket

def controlled(com_con, screen_con, key_con, mouse_con):
    global status
    status = True
    
    checkThread = Thread(target = CheckStop, args=(com_con,))
    checkThread.start()
    
    screenThread = Thread(target = send_img, args=(screen_con,))
    screenThread.start()
        
    #Tương tự dành cho bàn phím
    keyThread = Thread(target = KeyControlled, args=(key_con,))
    keyThread.start()
        
    #Hàm chuột đang lỗi
    mouseThread = Thread(target = MouseControlled, args=(mouse_con,))
    mouseThread.start()

def CheckStop(com_con):
    global status
    while com_con:
        flag = com_con.recv(BUFFERSIZE).decode(FORMAT)
        if "STOP" in flag:
            status = False

def send_img(screen_con):
    global status
    while status:
        #Chụp màn hình
        image = pag.screenshot()
        #Tạo BytesIO lưu hình ảnh ở dạng byte
        image_byte_array = io.BytesIO()
        #Lưu hình ảnh vào image_byte_array dưới dạng JPEG
        image.save(image_byte_array, format='JPEG')
        #Đổi thành dạng byte
        image_byte_array = image_byte_array.getvalue()
            
        #Gửi độ dài của hình ảnh
        screen_con.sendall(len(image_byte_array).to_bytes(4))
        #Gửi hình ảnh
        screen_con.sendall(image_byte_array)
            

def KeyControlled(key_con):
    while status:
        #Nhận dữ liệu bàn phím
        buffer = key_con.recv(BUFFERSIZE).decode()
        
        if not buffer:
            break
        
        print(buffer)
        
        key_con.sendall(buffer.encode(FORMAT))
        buffer=""

def MouseControlled(mouse_con):
    while status:
        #Nhận dữ liệu chuột
        buffer = mouse_con.recv(BUFFERSIZE).decode()
        
        if not buffer:
            break
        
        #Lệnh có dạng: move,123,456 (di chuyển chuột đến tọa độ (123,456))
        #Tách lệnh trên ra thành 3 thành phần command, x, y
        command, x, y = buffer.split(",")
        
        #Nếu lệnh là nhấp trái
        if command == "clickLeft":
            button = 'left'
            print("ClickLeft ",x,y)
            # pag.click(x, y,button)
        #Nếu lệnh là nhấp phải
        if command == "clickRight":
            button = 'right'
            print("ClickRight ",x,y)
            # pag.click(x, y, button)
        #Nếu lệnh là di chuyển
        if command == "move":
            print(x,y)
            # pag.moveTo(x,y)
        #Nếu lệnh là cuộn
        if command == "scroll":
            print("Scroll ",x,y)
            # pag.scroll(x)
        mouse_con.sendall(buffer.encode())
        #Dọn buffer
        buffer=""