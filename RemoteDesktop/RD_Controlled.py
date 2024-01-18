from threading import Thread, Event
import pyautogui as pag
import io
from RD_Constant import FORMAT, BUFFERSIZE

def controlled(com_con, screen_con, key_con, mouse_con):

    global stop_event
    stop_event = Event()
    
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
    
    screenThread.join()
    keyThread.join()
    mouseThread.join()
    
    stop_event.clear()
    

def CheckStop(com_con):
    while not stop_event.is_set():
        flag = com_con.recv(BUFFERSIZE).decode(FORMAT)
        if "STOP" in flag:
            stop_event.set()

def send_img(screen_con):
    while not stop_event.is_set():
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
         
        status = screen_con.recv(BUFFERSIZE).decode(FORMAT)
        if "STOP" in status:
            break   

def KeyControlled(key_con):
    while not stop_event.is_set():
        #Nhận dữ liệu bàn phím
        buffer = key_con.recv(BUFFERSIZE).decode()
        
        if "STOP" in buffer:
            break   
        
        if not buffer:
            break
        
        pag.press(buffer)
        
        key_con.sendall(buffer.encode(FORMAT))
        buffer=""

def MouseControlled(mouse_con):
    while not stop_event.is_set():
        #Nhận dữ liệu chuột
        buffer = mouse_con.recv(BUFFERSIZE).decode()
        
        if "STOP" in buffer:
            break   
        
        if not buffer:
            break
        
        #Lệnh có dạng: move,123,456 (di chuyển chuột đến tọa độ (123,456))
        #Tách lệnh trên ra thành 3 thành phần command, x, y
        command, x, y = buffer.split(",")
        
        #Nếu lệnh là nhấp trái
        if command == "clickLeft":
            try:
                x, y = int(x), int(y)
                pag.click(x, y, button='left')
            except ValueError:
                print("Invalid clickLeft command:", buffer)

        #Nếu lệnh là nhấp phải
        if command == "clickRight":
            try:
                x, y = int(x), int(y)
                pag.click(x, y, button='right')
            except ValueError:
                print("Invalid clickRight command:", buffer)
        #Nếu lệnh là di chuyển
        if command == "move":
            try:
                x, y = int(x), int(y)
                pag.moveTo(x, y)
            except ValueError:
                print("Invalid move command:", buffer)
        #Nếu lệnh là cuộn
        if command == "scroll":
            x, y = int(x), int(y)
            pag.scroll(x)
        mouse_con.sendall(buffer.encode())
        #Dọn buffer
        buffer=""