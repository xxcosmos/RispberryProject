# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mwin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(664, 568)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.forward_button = QtWidgets.QPushButton(self.centralwidget)
        self.forward_button.setObjectName("forward_button")
        self.gridLayout.addWidget(self.forward_button, 1, 1, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 2, 1, 1, 1)
        self.backward_button = QtWidgets.QPushButton(self.centralwidget)
        self.backward_button.setObjectName("backward_button")
        self.gridLayout.addWidget(self.backward_button, 3, 1, 1, 1)
        self.left_button = QtWidgets.QPushButton(self.centralwidget)
        self.left_button.setObjectName("left_button")
        self.gridLayout.addWidget(self.left_button, 2, 0, 1, 1)
        self.right_button = QtWidgets.QPushButton(self.centralwidget)
        self.right_button.setObjectName("right_button")
        self.gridLayout.addWidget(self.right_button, 2, 2, 1, 1)
        self.video_frame = QtWidgets.QLabel(self.centralwidget)
        self.video_frame.setObjectName("video_frame")
        self.gridLayout.addWidget(self.video_frame, 0, 0, 1, 2)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 3, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 664, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RaspberryPi"))
        self.forward_button.setText(_translate("MainWindow", "前进"))
        self.start_button.setText(_translate("MainWindow", "播放 / 暂停"))
        self.backward_button.setText(_translate("MainWindow", "后退"))
        self.left_button.setText(_translate("MainWindow", "左转"))
        self.right_button.setText(_translate("MainWindow", "右转"))
        self.video_frame.setText(_translate("MainWindow", "Hello"))
        self.stop_button.setText(_translate("MainWindow", "停止"))
