# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'root.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import image.root

class Ui_root(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(736, 652)
        Form.setStyleSheet("background-image: url(:/background/7.jpg);")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 390, 271, 41))
        self.pushButton.setStyleSheet("font: 16pt \"Arial\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 210, 271, 41))
        self.pushButton_2.setStyleSheet("font: 16pt \"Arial\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 60, 271, 41))
        self.pushButton_3.setStyleSheet("font: 16pt \"Arial\";")
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "普通管理员"))
        self.pushButton.setText(_translate("Form", "查看员工信息"))
        self.pushButton_2.setText(_translate("Form", "查看住户信息"))
        self.pushButton_3.setText(_translate("Form", "查看小区信息"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_root()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())