import os
import socket
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication,Qt
from PyQt5.QtWidgets import QMainWindow

from server.get_picture import *
from server.mwin import Ui_MainWindow


def send_msg(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.12.1', 8080))
    s.sendall(msg.encode('utf-8'))
    s.close()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, s, connection, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.is_played = True
        self.start_button.clicked.connect(self.on_clicked_start_button)
        self.connection = connection
        self.stream_bytes = b' '
        self.socket = s
        self.t = MyThread(self)
        self.t.start()

        self.forward_button.clicked.connect(self.on_clicked_direction_button)
        self.backward_button.clicked.connect(self.on_clicked_direction_button)
        self.right_button.clicked.connect(self.on_clicked_direction_button)
        self.left_button.clicked.connect(self.on_clicked_direction_button)
        self.stop_button.clicked.connect(self.on_clicked_direction_button)
        self.add_speed_button.clicked.connect(self.on_clicked_direction_button)
        self.sub_speed_button.clicked.connect(self.on_clicked_direction_button)
        self.exit_button.clicked.connect(QCoreApplication.quit)
        self.grabKeyboard()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Up :
            send_msg("forward")
        elif QKeyEvent.key()==Qt.Key_Down :
            send_msg("backward")
        elif QKeyEvent.key()==Qt.Key_Left :
            send_msg("left")
        elif QKeyEvent.key()==Qt.Key_Right:
            send_msg("right")
        elif QKeyEvent.key()==Qt.Key_W:
            send_msg("add")
        elif QKeyEvent.key()==Qt.Key_S:
            send_msg("sub")
        elif QKeyEvent.key()==Qt.Key_Space:
            send_msg("stop")
        else:
            pass
    def closeEvent(self, event):
        event.accept()
        os._exit(5)

    def on_clicked_direction_button(self):
        sender = str(self.sender().objectName())
        send_msg(sender.split('_')[0])

    def on_clicked_start_button(self):
        if self.is_played:
            # 停止播放
            self.is_played = False
            self.video_frame.setVisible(False)

        else:
            # 开始播放
            self.is_played = True
            self.video_frame.setVisible(True)
