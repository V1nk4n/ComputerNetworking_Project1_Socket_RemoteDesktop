import pyautogui as pag
import io
from RD_Constant import FORMAT, BUFFERSIZE

def send_img(screenConnection):
        while screenConnection:
            #Chụp màn hình
            image = pag.screenshot()
            #Tạo BytesIO lưu hình ảnh ở dạng byte
            image_byte_array = io.BytesIO()
            #Lưu hình ảnh vào image_byte_array dưới dạng JPEG
            image.save(image_byte_array, format='JPEG')
            #Đổi thành dạng byte
            image_byte_array = image_byte_array.getvalue()
            
            #Gửi độ dài của hình ảnh
            screenConnection.sendall(len(image_byte_array).to_bytes(4))
            #Gửi hình ảnh
            screenConnection.sendall(image_byte_array)
            
            msg = screenConnection.recv(BUFFERSIZE).decode(FORMAT)
            if "STOP" in msg:
                break