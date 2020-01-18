import cv2
#import _thread
import multiprocessing
import time
#from luma.core.interface.serial import i2c
#from luma.core.render import canvas
#from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import Image

cap= cv2.VideoCapture("videoplayback.mp4")
print("Done")
n_rows = 2
n_images_per_row = 2
width = 256
height = 128
dim = (width, height)
#serial4 = i2c(port=6, address=0x3C)
#device4 = ssd1306(serial4)
#serial3 = i2c(port=5, address=0x3C)
#device3 = ssd1306(serial3)
#serial2 = i2c(port=4, address=0x3C)
#device2 = ssd1306(serial2)
#serial1 = i2c(port=3, address=0x3C)
#device1 = ssd1306(serial1)

def print_Image(image):
    #device.display(image)
    print('called')
def print_Image2(image):
    #device.display(image)
    print('called2')
def print_Image3(image):
    #device.display(image)
    print('called3')
def print_Image4(image):
    #device.display(image)
    print('called4')


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
            image3 = Image.fromarray(images[2]).convert('1')
            image4 = Image.fromarray(images[3]).convert('1')
            
            a=multiprocessing.Process(target=print_Image, args=(image,))
            b=multiprocessing.Process(target=print_Image2, args=(image2,))
            c=multiprocessing.Process(target=print_Image3, args=(image3,))
            d=multiprocessing.Process(target=print_Image4, args=(image4,))
            a.start()
            b.start()
            c.start()
            d.start()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(time.time()-start_time)
cap.release()
cv2.destroyAllWindows()

            
