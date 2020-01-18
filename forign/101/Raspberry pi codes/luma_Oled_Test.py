import cv2
import _thread
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import Image

cap= cv2.VideoCapture('/home/pi/Downloads/videoplayback.mp4')
n_rows = 1
n_images_per_row = 2
width = 256
height = 64
dim = (width, height)
serial1 = i2c(port=4, address=0x3C)
device1 = ssd1306(serial1)
serial2 = i2c(port=3, address=0x3C)
device2 = ssd1306(serial2)

def print_Image(image,device):
    device1.display(image)
def print_Image2(image,device):
    device2.display(image)

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
            
    #Display image
    for x in range(0, n_rows):
        for y in range(0, n_images_per_row):
            cv2.imshow(str(x*n_images_per_row+y+1),images[x*n_images_per_row+y])
            cv2.moveWindow(str(x*n_images_per_row+y+1), 100+(y*roi_width), 50+(x*roi_height))
            
            image = Image.fromarray(images[0]).convert('1')
            image2 = Image.fromarray(images[1]).convert('1')
            
            time.sleep(.038)
            _thread.start_new_thread(print_Image2, (image2,device1),)
            _thread.start_new_thread(print_Image, (image,device2),)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(time.time()-start_time)
cap.release()
cv2.destroyAllWindows()

            
