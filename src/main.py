import sys

from PyQt5.QtWidgets import QApplication

from server.ui import MyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow('192.168.1.241',8080,'192.168.1.218',8081)
    window.show()
    sys.exit(app.exec_())
