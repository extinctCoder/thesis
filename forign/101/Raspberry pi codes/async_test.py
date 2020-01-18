import cv2
import _thread
import time
import asyncio
import multiprocessing as mp
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import Image

cap= cv2.VideoCapture('/home/pi/Downloads/videoplayback.mp4')
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

async def print_Image(image,device):
    device.display(image)
    ##print("called")
    await asyncio.sleep(.0001)
async def print_Image2(image,device):
    device.display(image)
    await asyncio.sleep(.0001)
    #print("print image2")
async def print_Image3(image,device):
    device.display(image)
    await asyncio.sleep(.0001)
    #print("print image3")
async def print_Image4(image,device):
    device.display(image)
    await asyncio.sleep(.0001)
    #print("print image4")
async def print_Image5(image,device):
    device.display(image)
    await asyncio.sleep(.0001)
async def print_Image6(image,device):
    device.display(image)
    await asyncio.sleep(.0001)
async def print_Image7(image,device):
    device.display(image)
    await asyncio.sleep(.0001)
async def print_Image8(image,device):
    device.display(image)
    await asyncio.sleep(.0001)
async def print_Image9(image,device):
    device.display(image)
    await asyncio.sleep(.0001)

while(True):
    start_time = time.time()
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    height, width = frame.shape
    roi_height = int(height / n_rows)
    roi_width = int(width / n_images_per_row)
    
    images = []
    
    for x in range(0, n_rows):
        for y in range(0, n_images_per_row):
            tmp_image=frame[x*roi_height:(x+1)*roi_height, y*roi_width:(y+1)*roi_width]
            images.append(tmp_image)
            
    image = Image.fromarray(images[0]).convert('1')
    image2 = Image.fromarray(images[1]).convert('1')
    image3 = Image.fromarray(images[2]).convert('1')
    image4 = Image.fromarray(images[3]).convert('1')
    image5 = Image.fromarray(images[4]).convert('1')
    image6 = Image.fromarray(images[5]).convert('1')
    image7 = Image.fromarray(images[6]).convert('1')
    image8 = Image.fromarray(images[7]).convert('1')
    image9 = Image.fromarray(images[8]).convert('1')
    async def call():
        await asyncio.gather(print_Image(image,device9),print_Image2(image2,device8),print_Image3(image3,device7),
                             print_Image4(image4,device6),print_Image5(image5,device5),print_Image6(image6,device4),
                             print_Image7(image7,device3),print_Image8(image8,device2),print_Image9(image9,device1))
    asyncio.run(call())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(time.time()-start_time)
cap.release()
cv2.destroyAllWindows()
