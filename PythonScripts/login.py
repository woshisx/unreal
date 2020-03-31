# -*- coding: utf-8 -*-
import os,re,shutil,json,random,threading,socket,sys,time
import unreal
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor, QColor
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.login_pushButton = QtWidgets.QPushButton(Form)
        self.login_pushButton.setGeometry(QtCore.QRect(173, 177, 100, 40))
        self.login_pushButton.setText("")
        self.login_pushButton.setObjectName("login_pushButton")
        self.login_checkBox = QtWidgets.QCheckBox(Form)
        self.login_checkBox.setGeometry(QtCore.QRect(61, 188, 71, 16))
        self.login_checkBox.setObjectName("login_checkBox")
        self.usename_label = QtWidgets.QLabel(Form)
        self.usename_label.setGeometry(QtCore.QRect(55, 74, 61, 31))
        self.usename_label.setObjectName("usename_label")
        self.password_label = QtWidgets.QLabel(Form)
        self.password_label.setGeometry(QtCore.QRect(55, 129, 61, 21))
        self.password_label.setObjectName("password_label")
        self.usename_lineEdit = QtWidgets.QLineEdit(Form)
        self.usename_lineEdit.setGeometry(QtCore.QRect(122, 75, 211, 31))
        self.usename_lineEdit.setObjectName("usename_lineEdit")
        self.password_lineEdit = QtWidgets.QLineEdit(Form)
        self.password_lineEdit.setGeometry(QtCore.QRect(122, 125, 211, 31))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.login_close_button = QtWidgets.QPushButton(Form)
        self.login_close_button.setGeometry(QtCore.QRect(372, -1, 27, 27))
        self.login_close_button.setText("")
        self.login_close_button.setObjectName("login_close_button")
        self.login_min_button = QtWidgets.QPushButton(Form)
        self.login_min_button.setGeometry(QtCore.QRect(343, -1, 27, 27))
        self.login_min_button.setText("")
        self.login_min_button.setObjectName("login_min_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.login_checkBox.setText(QtWidgets.QApplication.translate("Form", "记住", None, -1))
        self.usename_label.setText(QtWidgets.QApplication.translate("Form", "用户名 :", None, -1))
        self.password_label.setText(QtWidgets.QApplication.translate("Form", "密码 :", None, -1))

class MyLogin(QMainWindow,Ui_Form):
    def __init__(self):
        self.local_path = os.path.dirname(__file__).replace('\\','/')
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.login_close_button.clicked.connect(self.close)
        self.login_min_button.clicked.connect(self.showMinimized)
    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                    background-image:url('%s/images/04.jpg');
                }
                #login_pushButton:Pressed{
                background-image:url('%s/images/05.jpg');
                }
                ''' % (self.local_path, self.local_path)
        self.login_pushButton.setStyleSheet(style)
        self.login_close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/09.jpg' % self.local_path)))
        self.login_min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/08.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/07.jpg);}' % self.local_path)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def showColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QInputDialog.getText(self, '对话框',
                                        '请输入你的名字:')

        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        # this must excu or will crash
        app = QtWidgets.QApplication(sys.argv)
    window = MyLogin()
    window.show()
    window.setFixedSize(400, 300)
    sys.exit(app.exec_())
