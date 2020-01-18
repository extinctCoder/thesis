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

w=128
h=64
dim=(w,h)
disp1 = Adafruit_SSD1306.SSD1306_128_64(rst=RST,i2c_bus=1)
disp1.begin()

# Clear display.
disp1.clear()
disp1.display()

resized = cv2.resize(image, dim, interpolation =cv2.INTER_AREA)

if disp1.height == 64:
    image = Image.fromarray(resized).convert('1')
else:
    image = Image.fromarray(resized).convert('1')
disp1.image(image)
disp1.display()
cv2.waitKey(0)