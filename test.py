import socket
import threading
import pyautogui as pag
from PIL import Image
import io

image = pag.screenshot()
image_byte_array = io.BytesIO()
image.save(image_byte_array, format='JPEG')
image_byte_array = image_byte_array.getvalue()

image_byte_io = io.BytesIO(image_byte_array)
image2 = Image.open(image_byte_io)
image2.show()