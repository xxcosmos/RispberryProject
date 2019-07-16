import socket

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
import threading

from server.build_socket import BuildSocket
from server.get_picture import *
from server.mwin import Ui_MainWindow

def send_msg(msg):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('192.168.12.1',8080))
    s.sendall(msg.encode('utf-8'))
    s.close()
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, s, connection, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.is_played = True
        self.start_button.clicked.connect(self.on_clicked_start_button)
        self.connection = connection
        # self.last_frame = QPixmap('../assets/no_video.jpg')
        # self.video_frame.setPixmap(self.last_frame)
        self.stream_bytes = b' '
        self.socket = s
        self.t = MyThread(self)
        self.t.start()

        self.forward_button.clicked.connect(self.on_clicked_direction_button)
        self.backward_button.clicked.connect(self.on_clicked_direction_button)
        self.right_button.clicked.connect(self.on_clicked_direction_button)
        self.left_button.clicked.connect(self.on_clicked_direction_button)
        self.stop_button.clicked.connect(self.on_clicked_direction_button)

    def on_clicked_direction_button(self, event):
        sender = str(self.sender().objectName())
        if sender == "forward_button":
            send_msg("Forward")

        elif sender == "backward_button":
            send_msg("Backward")


        elif sender == "right_button":
            send_msg("Right")


        elif sender == "left_button":
            send_msg("Left")

        elif sender == "stop_button":
            send_msg("Stop")

    def on_clicked_start_button(self):
        if self.is_played:
            # 停止播放
            self.is_played = False
            self.video_frame.setVisible(False)

        else:
            # 开始播放
            self.is_played = True
            self.video_frame.setVisible(True)
            # while True:
            #     self.stream_bytes += self.connection.read(1024)
            #     first = self.stream_bytes.find(b'\xff\xd8')
            #     last = self.stream_bytes.find(b'\xff\xd9')
            #     if first != -1 and last != -1:
            #         jpg = self.stream_bytes[first:last + 2]
            #         self.stream_bytes = self.stream_bytes[last + 2:]
            #         image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            #         temp_image = mat_qimage_converter(image)
            #         last_frame = QPixmap.fromImage(temp_image)
            #         self.last_frame = last_frame
            #         self.video_frame.setPixmap(last_frame)
            #         print("here")
