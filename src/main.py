import sys

from PyQt5.QtWidgets import QApplication

from server import config
from server.ui import MyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow(config.pc_host, config.pc_port, config.car_host, config.car_port)
    window.show()
    sys.exit(app.exec_())
