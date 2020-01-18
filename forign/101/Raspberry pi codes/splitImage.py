import cv2
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import Image

RST = 24

image = cv2.imread("download.jpeg")
w=256
h=64
dim=(w,h)
resized = cv2.resize(image, dim, interpolation =cv2.INTER_AREA)
M = resized.shape[0]//1
N = resized.shape[1]//2
tiles = [resized[x:x+M,y:y+N] for x in range(0,resized.shape[0],M) for y in range(0,resized.shape[1],N)]

disp1 = Adafruit_SSD1306.SSD1306_128_64(rst=RST,i2c_bus=1)
disp2 = Adafruit_SSD1306.SSD1306_128_64(rst=RST,i2c_bus=3)
disp1.begin()
disp1.clear()
disp1.display()

disp2.begin()
disp2.clear()
disp2.display()

if disp1.height == 64:
    image = Image.fromarray(tiles[0]).convert('1')
else:
    image = Image.fromarray(tirles[0]).convert('1')

if disp2.height == 64:
    image2 = Image.fromarray(tiles[1]).convert('1')
else:
    image2 = Image.fromarray(tirles[1]).convert('1')

disp1.image(image)
disp1.display()
disp2.image(image2)
disp2.display()
cv2.waitKey(0)