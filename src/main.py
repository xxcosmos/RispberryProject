import socket
import sys
import threading
from PyQt5.QtWidgets import QApplication

from server.build_socket import BuildSocket
from server.ui import MyWindow

if __name__ == '__main__':
    host, port = '192.168.1.241', 8888
    s = BuildSocket(host, port,is_video=True)
    app = QApplication(sys.argv)

    window = MyWindow(s, s.get_connection())
    window.show()
    sys.exit(app.exec_())
