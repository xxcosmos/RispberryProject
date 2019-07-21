import socket
import threading

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

from server import ui, config

green_center = (0, 0)
red_center = (0, 0)
green_radius = 0
red_radius = 0

is_red = False
is_green = False


class MyThread(threading.Thread):
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((window.video_host, window.video_port))
        self.socket.listen(0)
        self.connection, self.client_address = self.socket.accept()
        self.connection = self.connection.makefile('rb')
        print("connection from ", self.client_address)

    def run(self):
        cnt = 20
        cnt1 = 0
        while True:
            self.window.stream_bytes += self.connection.read(1024)
            first = self.window.stream_bytes.find(b'\xff\xd8')
            last = self.window.stream_bytes.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = self.window.stream_bytes[first:last + 2]
                self.window.stream_bytes = self.window.stream_bytes[last + 2:]
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if cnt % 20 == 0:
                    global green_center, red_center, green_radius, red_radius, is_red, is_green
                    cnt1 = 0

                    hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                    low_red = np.array([5, 90, 150])
                    high_red = np.array([8, 255, 255])
                    red_th = cv2.inRange(hue_image, low_red, high_red)
                    red_dilated = cv2.dilate(red_th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
                    red_circles = cv2.HoughCircles(red_dilated, cv2.HOUGH_GRADIENT, 1, 100, param1=15, param2=7,
                                                   minRadius=10, maxRadius=100)

                    low_green = np.array([35, 150, 150])
                    high_green = np.array([77, 255, 255])
                    green_th = cv2.inRange(hue_image, low_green, high_green)
                    green_dilated = cv2.dilate(green_th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
                                               iterations=2)
                    green_circles = cv2.HoughCircles(green_dilated, cv2.HOUGH_GRADIENT, 1, 100, param1=15, param2=7,
                                                     minRadius=10, maxRadius=100)

                    if green_circles is not None:
                        is_green = True
                        x, y, green_radius = green_circles[0][0]
                        green_center = (x, y)
                        cv2.circle(image, green_center, green_radius, (0, 255, 0), 2)
                        ui.send_msg("forward", config.car_host, config.car_port)
                    else:
                        is_green = False

                    if red_circles is not None:
                        is_red = True
                        x, y, red_radius = red_circles[0][0]
                        red_center = (x, y)
                        cv2.circle(image, red_center, red_radius, (0, 0, 255), 2)
                        ui.send_msg("stop", config.car_host, config.car_port)
                    else:
                        is_red = False
                else:
                    if cnt1 < 10:
                        if is_green:
                            cv2.circle(image, green_center, green_radius, (0, 0, 255), 2)
                        if is_red:
                            cv2.circle(image, red_center, red_radius, (0, 255, 0), 2)

                self.window.video_frame.setPixmap(QPixmap.fromImage(mat_qimage_converter(image)))
                cnt = cnt + 1
                cnt1 += 1
                if not self.window.is_played:
                    print("not playing")
                    self.connection.close()
                    self.socket.close()
                    break


def mat_qimage_converter(mat):
    image = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    return QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
