import pyautogui
from time import sleep
import numpy as np
import cv2
from mss import mss
from PIL import Image , ImageGrab 
import wx
 
app = wx.App(False)
width, height = wx.GetDisplaySize()

n_rows = 3
n_images_per_row = 3

a=0
b=0
#a=(GetSystemMetrics(0))
#b=(GetSystemMetrics(1))
sct = mss()
#events=


while True:
    images = []
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
        k = np.array(np.ones((11, 11), np.float32))/121
    
        k = np.array(([1, 0, -1], [0, 0, 0], [-1, 0, 1]), np.float32)
        output = cv2.filter2D(gray, -1, k)
        cv2.namedWindow('cap')
        cv2.moveWindow('cap', width-384,252)
        cv2.imshow("cap",output)
        """height, width = gray.shape
        roi_height = int(height / n_rows)
        roi_width = int(width / n_images_per_row)
        for x in range(0, n_rows):
            for y in range(0, n_images_per_row):
                tmp_image=gray[x*roi_height:(x+1)*roi_height, y*roi_width:(y+1)*roi_width]
                images.append(tmp_image)
                #print(len(images))
        for x in range(0, n_rows):
            for y in range(0, n_images_per_row):
                cv2.imshow(str(x*n_images_per_row+y+1),images[x*n_images_per_row+y])
                cv2.moveWindow(str(x*n_images_per_row+y+1), 100+(y*roi_width), 50+(x*roi_height))
                
        frame_1=np.mean(images[0])
        frame_2=np.mean(images[1])
        frame_3=np.mean(images[2])
        frame_4=np.mean(images[3])
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
        print('\n')"""     
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break