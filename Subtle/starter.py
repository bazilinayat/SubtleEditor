# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'starter.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(465, 331)
        MainWindow.setAccessibleDescription("")
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, -200, 841, 731))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("start.png"))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    wind = Ui_MainWindow()
    wind.setupUi(MainWindow)
    wind.retranslateUi(MainWindow)
    MainWindow.show()
    QtCore.QTimer.singleShot(3000, MainWindow.close)
    app.exec()
