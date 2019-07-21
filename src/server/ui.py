import os

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QMainWindow

from server.get_picture import *
from server.mwin import Ui_MainWindow


def send_msg(msg, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(msg.encode('utf-8'))
    s.close()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, video_host, video_port, car_host, car_port, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.car_host = car_host
        self.car_port = car_port
        self.video_host = video_host
        self.video_port = video_port

        self.start_button.clicked.connect(self.on_clicked_start_button)

        self.photo_button.clicked.connect(self.on_clicked_direction_button)
        self.video_button.clicked.connect(self.on_clicked_direction_button)
        self.is_played = False
        self.stream_bytes = b' '

        self.forward_button.clicked.connect(self.on_clicked_direction_button)
        self.backward_button.clicked.connect(self.on_clicked_direction_button)
        self.right_button.clicked.connect(self.on_clicked_direction_button)
        self.left_button.clicked.connect(self.on_clicked_direction_button)
        self.stop_button.clicked.connect(self.on_clicked_direction_button)
        self.add_speed_button.clicked.connect(self.on_clicked_direction_button)
        self.sub_speed_button.clicked.connect(self.on_clicked_direction_button)
        self.grabKeyboard()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            send_msg("FORWARD", self.car_host, self.car_port)
        elif event.key() == Qt.Key_Down:
            send_msg("BACKWARD", self.car_host, self.car_port)
        elif event.key() == Qt.Key_Left:
            send_msg("LEFT", self.car_host, self.car_port)
        elif event.key() == Qt.Key_Right:
            send_msg("RIGHT", self.car_host, self.car_port)
        elif event.key() == Qt.Key_W:
            send_msg("ADD_SPEED", self.car_host, self.car_port)
        elif event.key() == Qt.Key_S:
            send_msg("SUB_SPEED", self.car_host, self.car_port)
        elif event.key() == Qt.Key_Space:
            send_msg("STOP", self.car_host, self.car_port)
        else:
            pass

    def closeEvent(self, event):
        event.accept()
        os._exit(5)

    def on_clicked_direction_button(self):
        sender = str(self.sender().objectName())
        send_msg(sender.split('_')[0], self.car_host, self.car_port)

    def on_clicked_start_button(self):
        sender = str(self.sender().objectName())
        send_msg(sender.split('_')[0], self.car_host, self.car_port)
        if not self.is_played:
            self.stream_bytes = b' '
            MyThread(self).start()
        self.is_played = not self.is_played
        print(self.is_played)
