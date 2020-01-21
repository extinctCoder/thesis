import base64
import logging
import os
import socket
from time import sleep
import wx

import cv2 as opencv_four
import numpy as np
import pyautogui
from mss import mss

import paho.mqtt.client as data_transponder_tool

# program parameters
i2c_panel_width = 128
i2c_panel_height = 64
number_of_display_row_col = 3

remote_port = 5050
remote_address = '192.168.0.101'
motor_lift_chanel_prefix = 'thesis/motor/'

# program classes
file_name = os.path.basename(__file__)
screenshot_tool = mss()
data_transponder = data_transponder_tool.Client(file_name)
data_transponder.connect(remote_address)
image_transponder = socket.socket()

# logging.basicConfig(format='%(asctime)s, %(levelname)s\t: %(message)s', filename=file_name+'.log', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s, %(levelname)s\t: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def find_motor_lift(screenshot_converted):
    logging.info('finding the individual segments z-axis value')
    screenshot_height, screenshot_width = screenshot_converted.shape
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
            temp_segment = screenshot_converted[row*segment_height:(
                row+1)*segment_height, column*segment_width:(column+1)*segment_width]
            logging.debug('position of segment number {}x{} is : {},{}'.format(
                row+1, column+1, (row+1)*segment_height, (column+1)*segment_width))
            yield row, column, int(np.mean(temp_segment))
    pass


def screenshot_convert(screenshot):
    logging.info('converting image from 2d to 3d in gray scale')
    logging.debug('converting image from into numpy array')
    screenshot = np.array(screenshot)
    logging.debug('applying algorithm to convert the image into gray scale')
    screenshot_gray = opencv_four.cvtColor(
        screenshot, opencv_four.COLOR_BGR2GRAY)
    logging.debug('applying algorithm to find the edges of the image')
    screenshot = np.array(np.ones((11, 11), np.float32))/121
    screenshot = np.array(([1, 0, -1], [0, 0, 0], [-1, 0, 1]), np.float32)
    return opencv_four.filter2D(screenshot_gray, -1, screenshot)


def screenshot_convert_updated(screenshot, threshold_vale=0):
    logging.info('converting image from 2d to 3d in gray scale')
    logging.debug('converting image from into numpy array')
    screenshot = np.array(screenshot)
    logging.debug('applying algorithm to convert the image into gray scale')
    screenshot_gray = opencv_four.cvtColor(
        screenshot, opencv_four.COLOR_BGR2GRAY)
    logging.debug('applying algorithm to find the depth of the image')
    _, screenshot_converted = opencv_four.threshold(
        screenshot_gray, threshold_vale, 255, opencv_four.THRESH_TOZERO_INV + opencv_four.THRESH_OTSU)
    return screenshot_converted


def run_main():
    logging.debug('entering to image capture mode')
    while True:
        mouse_possition = pyautogui.position()
        mouse_x = int(mouse_possition[0])
        mouse_y = int(mouse_possition[1])
        # logging.info('mouse possition is at x : {}, y : {}'.format(mouse_x, mouse_y))

        binding_box_top = mouse_y-number_of_display_row_col*i2c_panel_height/2
        binding_box_left = mouse_x-number_of_display_row_col*i2c_panel_height/2
        binding_box_width = number_of_display_row_col*i2c_panel_width
        binding_box_height = number_of_display_row_col*i2c_panel_height

        binding_box = {'top': binding_box_top, 'left': binding_box_left,
                       'width': binding_box_width, 'height': binding_box_height}

        screenshot = screenshot_tool.grab(binding_box)
        # logging.debug('display captured at : {}'.format(binding_box))
        screenshot = np.array(screenshot)

        # preview the live image
        opencv_four.imshow('LIVE VIEW (press f to freeze)', screenshot)
        if (opencv_four.waitKey(1) & 0xFF) == ord('f'):
            logging.debug('display freezed at : {}'.format(binding_box))

            logging.info('sending image to display server')
            try:
                logging.debug('converting image from numpy array to jpg')
                _, screenshot_jpg = opencv_four.imencode('.jpg', screenshot)
                logging.debug('trying to connect with display image server')
                image_transponder.connect((remote_address, remote_port))
                logging.debug(
                    'sending the jpg image to the display image server')
                image_transponder.send(base64.b64encode(screenshot_jpg))
                image_transponder.close()
                logging.info('image send to image display server')
            except Exception as sending_error:
                logging.error(
                    'image sending failed : {}'.format(sending_error))

            screenshot_converted = screenshot_convert_updated(screenshot)
            logging.info('image convertion successful')
            motor_lift = find_motor_lift(screenshot_converted)
            for row, column, value in motor_lift:
                logging.debug(
                    'z-axis value of segment number {}x{} is : {}'.format(row+1, column+1, value))
                logging.info(
                    'publissing z-axis data into the transport server')
                data_transponder.publish(
                    ''.join((motor_lift_chanel_prefix, str(row), str(column))), value)
                logging.debug('data published for segment number {}x{} in chanel : {}'.format(
                    row+1, column+1, ''.join((motor_lift_chanel_prefix, str(row), str(column)))))
            opencv_four.imshow('CONVERTED SCREENSHOT', screenshot_converted)
            logging.info('process done')
            break
        if (opencv_four.waitKey(1) & 0xFF) == ord('q'):
            opencv_four.destroyAllWindows()
            break
    pass


if __name__ == '__main__':
    logging.info('welcome to thesis {} script'.format(file_name))
    run_main()
    logging.info('leaving from thesis {} script'.format(file_name))
