import cv2
import _thread
import time
import socket
import base64
import numpy
import multiprocessing as mp
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import Image
full_Data = b''

TCP_IP = '192.168.0.101'
TCP_PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()

while True:    
    stringData = conn.recv(4096)
    #print(stringData)
    #time.sleep(1)
    if len(stringData) <= 0:
        break
    full_Data += stringData
# print(full_Data)

data= base64.b64decode(full_Data)
print(data)
s.close()
nparr = numpy.frombuffer(data,dtype='uint8')
decimg=cv2.imdecode(nparr,0)

n_rows = 3
n_images_per_row = 3
width = 384
height = 192
dim = (width, height)
serial9 = i2c(port=11, address=0x3C)
device9 = ssd1306(serial9)
serial8 = i2c(port=10, address=0x3C)
device8 = ssd1306(serial8)
serial7 = i2c(port=9, address=0x3C)
device7 = ssd1306(serial7)
serial6 = i2c(port=8, address=0x3C)
device6 = ssd1306(serial6)
serial5 = i2c(port=7, address=0x3C)
device5 = ssd1306(serial5)
serial4 = i2c(port=6, address=0x3C)
device4 = ssd1306(serial4)
serial3 = i2c(port=5, address=0x3C)
device3 = ssd1306(serial3)
serial2 = i2c(port=4, address=0x3C)
device2 = ssd1306(serial2)
serial1 = i2c(port=3, address=0x3C)
device1 = ssd1306(serial1)

def print_Image(image,device):
    device.display(image)
    #print("print image1")
def print_Image2(image,device):
    device.display(image)
    #print("print image2")
def print_Image3(image,device):
    device.display(image)
    #print("print image3")
def print_Image4(image,device):
    device.display(image)
    #print("print image4")
def print_Image5(image,device):
    device.display(image)
def print_Image6(image,device):
    device.display(image)
def print_Image7(image,device):
    device.display(image)
def print_Image8(image,device):
    device.display(image)
def print_Image9(image,device):
    device.display(image)

'''def process_1(image,device4,image2,device3):
   
    print("Process1_called")
    #device4.display(image)
    #device3.display(image2)
    _thread.start_new_thread(print_Image, (image,device4),)
    _thread.start_new_thread(print_Image2, (image2,device3),)
def process_2(image3,device2,image4,device1):
   
    print("Process2_called")
    #device2.display(image3)
    #device1.display(image4)
    _thread.start_new_thread(print_Image3, (image3,device2),)
    _thread.start_new_thread(print_Image4, (image4,device1),)
'''
while(True):
    start_time = time.time()
    #ret, frame = cap.read()
    #cap = cv2.cvtColor(cap, cv2.COLOR_RGB2GRAY)
    cap = cv2.resize(decimg, dim, interpolation = cv2.INTER_AREA)
    height, width = cap.shape
    roi_height = int(height / n_rows)
    roi_width = int(width / n_images_per_row)
    
    images = []
    
    for x in range(0, n_rows):
        for y in range(0, n_images_per_row):
            tmp_image=cap[x*roi_height:(x+1)*roi_height, y*roi_width:(y+1)*roi_width]
            images.append(tmp_image)
            
    #Display image
    for x in range(0, n_rows):
       for y in range(0, n_images_per_row):
            cv2.imshow(str(x*n_images_per_row+y+1),images[x*n_images_per_row+y])
            cv2.moveWindow(str(x*n_images_per_row+y+1), 100+(y*roi_width), 50+(x*roi_height))
            
            #image = Image.fromarray(images[0]).convert('1')
            #image2 = Image.fromarray(images[1]).convert('1')
            #image3 = Image.fromarray(images[2]).convert('1')
            #image4 = Image.fromarray(images[3]).convert('1')
            #time.sleep(.01)
            #a=mp.Process(target=process_1, args=(image,image2,device4,device3,))
            #b=mp.Process(target=process_2, args=(image3,image4,device2,device1,))
            #time.sleep(.052)
            #_thread.start_new_thread(print_Image, (image,device4),)
            #_thread.start_new_thread(print_Image2, (image2,device3),)
            #_thread.start_new_thread(print_Image3, (image3,device2),)
            #_thread.start_new_thread(print_Image4, (image4,device1),)
            #a.start()
            #a.join()
            #b.start()
            #b.join()
    image = Image.fromarray(images[0]).convert('1')
    image2 = Image.fromarray(images[1]).convert('1')
    image3 = Image.fromarray(images[2]).convert('1')
    image4 = Image.fromarray(images[3]).convert('1')
    image5 = Image.fromarray(images[4]).convert('1')
    image6 = Image.fromarray(images[5]).convert('1')
    image7 = Image.fromarray(images[6]).convert('1')
    image8 = Image.fromarray(images[7]).convert('1')
    image9 = Image.fromarray(images[8]).convert('1')
    time.sleep(.5)
    _thread.start_new_thread(print_Image, (image,device9),)
    _thread.start_new_thread(print_Image2, (image2,device8),)
    _thread.start_new_thread(print_Image3, (image3,device7),)
    _thread.start_new_thread(print_Image4, (image4,device6),)
    _thread.start_new_thread(print_Image5, (image5,device5),)
    _thread.start_new_thread(print_Image6, (image6,device4),)
    _thread.start_new_thread(print_Image7, (image7,device3),)
    _thread.start_new_thread(print_Image8, (image8,device2),)
    _thread.start_new_thread(print_Image9, (image9,device1),)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(time.time()-start_time)
cap.release()
cv2.destroyAllWindows()

            


