import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap
import threading


class MyThread(threading.Thread):
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window

    def run(self):
        while True:
            self.window.stream_bytes += self.window.connection.read(1024)
            first = self.window.stream_bytes.find(b'\xff\xd8')
            last = self.window.stream_bytes.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = self.window.stream_bytes[first:last + 2]
                self.window.stream_bytes = self.window.stream_bytes[last + 2:]
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                self.window.video_frame.setPixmap(QPixmap.fromImage(mat_qimage_converter(image)))


def mat_qimage_converter(mat):
    image = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    return QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
    # height,width,channel = mat.shape
    # bytesPerLine = 3*width
    # return QImage(mat.data,width,height,bytesPerLine,QImage.Format_RGB888).rgbSwapped()
