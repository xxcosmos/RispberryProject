import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from cv2.cv2 import cvtColor, COLOR_BGR2RGB

from server.build_socket import BuildSocket
from server.get_picture import *
from server.mwin import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, connection, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.start_button.setChecked(False)
        self.start_button.clicked.connect(self.on_clicked_start_button)
        self.connection = connection
        self.last_frame = QPixmap('../assets/no_video.jpg')
        self.video_frame.setPixmap(self.last_frame)

    def on_clicked_start_button(self):
        if self.start_button.isChecked():
            # 停止播放
            self.start_button.setChecked(False)
            self.video_frame.setPixmap(QPixmap(self.last_frame))

        else:
            # 开始播放
            self.start_button.setChecked(True)
            stream_bytes = b' '
            while True:
                stream_bytes+=self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    temp_image = cvMat2QImage
                    last_frame = QPixmap(temp_image)
                    self.last_frame = last_frame
                    self.video_frame.setPixmap(last_frame)
