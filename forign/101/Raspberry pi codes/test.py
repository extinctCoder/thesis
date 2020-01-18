from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep

serial0 = i2c(port=3, address=0x3C)
device0 = ssd1306(serial0, rotate=0)
serial1 = i2c(port=1, address=0x3C)
device1 = ssd1306(serial1, rotate=0)
# Box and text rendered in portrait mode
with canvas(device0) as draw:
    draw.rectangle(device0.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "Hello World", fill="red")
with canvas(device1) as draw:
    draw.rectangle(device1.bounding_box, outline="white", fill="black")
    draw.text((10, 40), "thank you", fill="white")    
sleep(10)
