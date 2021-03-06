import base64
import socket
import time
from fileinput import close
from lib2to3.pytree import convert
from time import sleep

import cv2 as opencv_four
import numpy
from PIL import Image
import os
import logging
import _thread
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306


file_name = os.path.basename(__file__)
server_port = 5050
server_address = '192.168.0.101'


image_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
image_server.bind((server_address, server_port))
image_server.listen(True)


i2c_panel_width = 128
i2c_panel_height = 64
number_of_display_row_col = 3

i2c_port = [3, 4, 5, 6, 7, 8, 9, 10, 11]
serial_array = [[None for row in range(number_of_display_row_col)]
                for column in range(number_of_display_row_col)]

display_array = [[None for row in range(number_of_display_row_col)]
                 for column in range(number_of_display_row_col)]

logging.basicConfig(format='%(asctime)s, %(levelname)s\t: %(message)s', filename=file_name+'.log', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
#logging.basicConfig(format='%(asctime)s, %(levelname)s\t: %(message)s',
                    #datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def init_display():
    logging.info('initializing displays for the script')
    port_index = 0
    global serial_array
    global display_array
    try:
        for row in range(3):
            for column in range(3):
                logging.info(
                    'initializing display no : {}x{}'.format(row+1, column+1))
                serial_array[row][column] = i2c(
                    port=i2c_port[port_index], address=0x3C)
                logging.debug(
                    '{}x{} no port is initialized'.format(row+1, column+1))
                display_array[row][column] = ssd1306(serial_array[row][column])
                logging.debug(
                    '{}x{} no display is initialized'.format(row+1, column+1))
                port_index = port_index+1
                pass
            pass
    except Exception as client_error:
        logging.error('display initializing failed : {}'.format(client_error))
        pass

    port_index = 0
    pass


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
            temp_segment = Image.fromarray(temp_segment).convert('1')
            yield row, column, temp_segment
    pass


def convert_string_image(screenshot_string):
    logging.info('converting image string into image')
    logging.debug('decodeing image bytes from image string')
    screenshot_decoded = base64.b64decode(screenshot_string)
    logging.debug('converting bytecode image into numpy array')
    screenshot_array = numpy.frombuffer(screenshot_decoded, dtype='uint8')
    logging.debug('converting numpy array into image')
    return opencv_four.imdecode(screenshot_array, 0)


def receive_image_string(image_sender, sender_address):
    screenshot_string = b''
    global display_array
    try:
        logging.info(
            'starting to receive the image data from the image client')
        logging.debug('image client address is : {}'.format(sender_address))
        logging.debug('reading image string from image sender')
        while True:
            temp_string = image_sender.recv(4096)
            if len(temp_string) <= 0:
                logging.info('image string reading complete')
                break
            screenshot_string += temp_string
            pass
        screenshot = convert_string_image(screenshot_string)
        image_segments = convert_image_segment(screenshot)
        for row, column, segment in image_segments:
            try:
                logging.info(
                    'printing image in segment number : {}x{}'.format(row+1, column+1))
                display_array[row][column].clear()
                display_array[row][column].display(segment)

                logging.debug(
                    'image printing successfull in segment number : {}x{}'.format(row+1, column+1))
            except Exception as client_error:
                logging.error('image printing error : {}'.format(client_error))
            pass
        logging.debug('clossing connection with image sender')
        image_sender.close()
        logging.info('connection closed with image sender')
    except Exception as client_error:
        logging.error('image string receiving error : {}'.format(client_error))
        pass


def run_main():
    init_display()
    try:
        logging.debug('image server successfully created')
        while True:
            logging.info('waiting for new image sender request')
            image_sender, sender_address = image_server.accept()
            # receive_image_string(image_sender, sender_address)
            _thread.start_new_thread(
                receive_image_string, (image_sender, sender_address),)
    except Exception as server_error:
        logging.error('image server error : {}'.format(server_error))
        pass
    pass


if __name__ == '__main__':
    logging.info('welcome to thesis {} script'.format(file_name))
    run_main()
    logging.info('leaving from thesis {} script'.format(file_name))