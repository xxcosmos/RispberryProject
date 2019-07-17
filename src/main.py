import sys

from PyQt5.QtWidgets import QApplication

from server.build_socket import BuildSocket
from server.ui import MyWindow

if __name__ == '__main__':
    s = BuildSocket('192.168.12.128', 8888,is_video=True)

    app = QApplication(sys.argv)
    window = MyWindow(s, s.get_connection())
    window.show()
    sys.exit(app.exec_())
