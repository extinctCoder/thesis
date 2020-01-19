import base64
import socket
import time
from fileinput import close
from lib2to3.pytree import convert
from time import sleep

import cv2 as opencv_four
import numpy
from PIL import Image

import _thread
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

server_port = 5050
server_address = '127.0.0.1'


image_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
image_server.bind((server_address, server_port))
image_server.listen(True)


i2c_panel_width = 128
i2c_panel_height = 64
number_of_display_row_col = 3

i2c_address = 0x3C
i2c_port = [3, 4, 5, 6, 7, 8, 9, 10, 11]

serial_array = [[None for row in range(number_of_display_row_col)]
                for column in range(number_of_display_row_col)]

display_array = [[None for row in range(number_of_display_row_col)]
                 for column in range(number_of_display_row_col)]

port_index = 0
for row in range(3):
    for column in range(3):
        serial_array[row][column] = i2c(int(i2c_port[port_index]), i2c_address)
        display_array[row][column] = ssd1306(serial_array[row][column])
        port_index = port_index+1
        pass
    pass
port_index = 0


def convert_image_segment(screenshot):
    logging.info('converting image into {}x{} segments'.format(
        number_of_display_row_col, number_of_display_row_col))
    screenshot_height, screenshot_width = screenshot.shape
    logging.debug('the image is {}px wide & {}px tall'.format(
        screenshot_width, screenshot_height))
    segment_height = int(screenshot_height / number_of_display_row_col)
    segment_width = int(screenshot_width / number_of_display_row_col)
    logging.info('size of the segment matrix will be : {}x{}'.format(
        number_of_display_row_col, number_of_display_row_col))
    logging.debug('each segment will be {}px wide & {}px tall'.format(
        segment_width, segment_height))
    for row in range(0, number_of_display_row_col):
        for column in range(0, number_of_display_row_col):
            temp_segment = screenshot[row*segment_height:(
                row+1)*segment_height, column*segment_width:(column+1)*segment_width]
            logging.debug('position of segment number {}x{} is : {},{}'.format(
                row+1, column+1, (row+1)*segment_height, (column+1)*segment_width))
            yield row, column, temp_segment
    pass


def print_segment_image(display_device, segment_image):
    display_device.display(segment_image)
    pass


def convert_string_image(screenshot_string):
    screenshot_decoded = base64.b64decode(screenshot)
    screenshot_array = numpy.frombuffer(screenshot_decoded, dtype='uint8')
    return opencv_four.imdecode(screenshot_array, 0)


def receive_image_string(image_sender, sender_address):
    screenshot_string = b''
    try:
        while True:
            temp_string = image_sender.recv(4096)
            # print(stringData)
            # time.sleep(1)
            if len(temp_string) <= 0:
                break
            screenshot_string += temp_string
            pass
        image_sender.close()
    except Exception as client_error:
        print(client_error)
        pass
    return screenshot_string


def run_main():
    try:
        while True:
            image_sender, sender_address = image_server.accept()
            screenshot_string = receive_image_string(
                image_sender, sender_address)
            screenshot = convert_string_image(screenshot)
            image_segments = convert_image_segment(screenshot)
            for row, column, segment in image_segments:
                _thread.start_new_thread(
                    print_segment_image, (segment, display_array[row][column]))
    except Exception as server_error:
        print(server_error)
        pass
    pass


if __name__ == '__main__':
    run_main()
