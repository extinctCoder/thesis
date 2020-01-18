import logging
import pyautogui
from time import sleep
import numpy as np
import cv2 as opencv_four
from mss import mss
import paho.mqtt.client as mqtt
from param import i2c_panel_width, i2c_panel_height, number_of_display_row_col, n_rows, n_images_per_row
from param import broker_address, motor_lift_chanel_prefix

screenshot_tool = mss()
client = mqtt.Client(str(__name__))
client.connect(broker_address)
logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def find_motor_lift(screenshot_converted):
    screenshot_height, screenshot_width = screenshot_converted.shape
    segment_height = int(screenshot_height / number_of_display_row_col)
    segment_width = int(screenshot_width / number_of_display_row_col)
    for row in range(0, number_of_display_row_col):
        for column in range(0, number_of_display_row_col):
            temp_segment = screenshot_converted[row*segment_height:(
                row+1)*segment_height, column*segment_width:(column+1)*segment_width]
            yield row, column, int(np.mean(temp_segment))
    pass


def screenshot_convert(screenshot):
    screenshot = np.array(screenshot)
    screenshot_gray = opencv_four.cvtColor(
        screenshot, opencv_four.COLOR_BGR2GRAY)
    screenshot = np.array(np.ones((11, 11), np.float32))/121
    screenshot = np.array(([1, 0, -1], [0, 0, 0], [-1, 0, 1]), np.float32)
    return opencv_four.filter2D(screenshot_gray, -1, screenshot)


def screenshot_convert_updated(screenshot, threshold_vale=0):
    screenshot = np.array(screenshot)
    screenshot_gray = opencv_four.cvtColor(
        screenshot, opencv_four.COLOR_BGR2GRAY)
    _, screenshot_converted = opencv_four.threshold(
        screenshot_gray, threshold_vale, 255, opencv_four.THRESH_TOZERO_INV + opencv_four.THRESH_OTSU)
    return screenshot_converted


def run_main():
    while True:
        mouse_possition = pyautogui.position()
        mouse_x = int(mouse_possition[0])
        mouse_y = int(mouse_possition[1])

        binding_box_top = mouse_y-number_of_display_row_col*i2c_panel_height/2
        binding_box_left = mouse_x-number_of_display_row_col*i2c_panel_height/2
        binding_box_width = number_of_display_row_col*i2c_panel_width
        binding_box_height = number_of_display_row_col*i2c_panel_height

        binding_box = {'top': binding_box_top, 'left': binding_box_left,
                       'width': binding_box_width, 'height': binding_box_height}

        screenshot = screenshot_tool.grab(binding_box)

        # preview the live image
        opencv_four.imshow('LIVE VIEW (press c to capture)',
                           np.array(screenshot))
        if (opencv_four.waitKey(1) & 0xFF) == ord('c'):
            screenshot_converted = screenshot_convert_updated(screenshot)
            motor_lift = find_motor_lift(screenshot_converted)
            for row, column, value in motor_lift:
                client.publish(
                    ''.join((motor_lift_chanel_prefix, str(row), str(column))), value)
            opencv_four.imshow('CONVERTED SCREENSHOT', screenshot_converted)
            pass
        if (opencv_four.waitKey(1) & 0xFF) == ord('q'):
            opencv_four.destroyAllWindows()
            break
    pass


if __name__ == '__main__':
    run_main()
