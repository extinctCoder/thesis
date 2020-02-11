import pyautogui
from time import sleep
import numpy as np
import cv2
from mss import mss
from PIL import Image , ImageGrab 
import wx
import serial
app = wx.App(False)
width, height = wx.GetDisplaySize()
#arduino_Data = serial.Serial('com5',9600) 

n_rows = 3
n_images_per_row = 3

a=0
b=0
#a=(GetSystemMetrics(0))
#b=(GetSystemMetrics(1))
sct = mss()
#events=
#arduino_1=1
#print(arduino_Data.isOpen())
#arduino_Data.write(arduino_1)

while True:
    images = []
    arduino_1=[]
    arduino_2=[]
    pos = pyautogui.position()
    a=(f'{pos[0]}')
    b=(f'{pos[1]}')
    #print(type(x))
    #print(type(y))
    a=int(a)
    b=int(b)
    #file.write(f'{pos[0]}, {pos[1]}\n')
    #sleep(.16)
    #print("X:",x,"Y:",y)
    bounding_box = {'top': (b-100), 'left': (a-100), 'width': 384, 'height': 192}
    sleep(.1)

    sct_img = sct.grab(bounding_box)
    cv2.namedWindow('press c to capture')
    cv2.moveWindow('press c to capture', width-384,30)
    cv2.imshow('press c to capture', np.array(sct_img))
    
    if (cv2.waitKey(1) & 0xFF) == ord('c'):
        #img =ImageGrab.grab(bbox=bounding_box)
        

        k=np.array(sct_img)
        gray = cv2.cvtColor(k, cv2.COLOR_BGR2GRAY)
        th = 0
        max_val = 255
        ret, o4 = cv2.threshold(gray, th, max_val, cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU )
        
        k = np.array(np.ones((11, 11), np.float32))/121
    
        k = np.array(([1, 0, -1], [0, 0, 0], [-1, 0, 1]), np.float32)
        output = cv2.filter2D(gray, -1, k)
        cv2.namedWindow('cap')
        cv2.moveWindow('cap', width-384,252)
        cv2.imshow("cap",o4)
        height, width = o4.shape
        roi_height = int(height / n_rows)
        roi_width = int(width / n_images_per_row)
        for x in range(0, n_rows):
            for y in range(0, n_images_per_row):
                tmp_image=o4[x*roi_height:(x+1)*roi_height, y*roi_width:(y+1)*roi_width]
                images.append(tmp_image)
                #print(len(images))
        for x in range(0, n_rows):
            for y in range(0, n_images_per_row):
                cv2.imshow(str(x*n_images_per_row+y+1),images[x*n_images_per_row+y])
                cv2.moveWindow(str(x*n_images_per_row+y+1), 100+(y*roi_width), 50+(x*roi_height))
                
        frame_1=int(np.mean(images[0]))
        frame_2=int(np.mean(images[1]))
        frame_3=int(np.mean(images[2]))
        frame_4=int(np.mean(images[3]))
        frame_5=np.mean(images[4])
        frame_6=np.mean(images[5])
        frame_7=np.mean(images[6])
        frame_8=np.mean(images[7])
        frame_9=np.mean(images[8])
        print(frame_1)
        print(frame_2)
        print(frame_3)
        print(frame_4)
        print(frame_5)
        print(frame_6)
        print(frame_7)
        print(frame_8)
        print(frame_9)
        arduino_1= str (frame_1)+ "," +str(frame_2) 
        print('\n')
        print(arduino_1)
        #print(arduino_Data.isOpen())
        print(type(arduino_1))
        
        #arduino_Data.write(arduino_1.encode())
        sleep(3)
        print("open")
        #print(type(arduino_1))
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break