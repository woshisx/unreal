import os,re,shutil,json,random,threading,socket,sys,time
from unrealtool import AssetFunctions
import unreal
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QMainWindow
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))

class MyWidget(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
    def setIcon(self):
        appIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'images/Icon128.png').replace('\\','/'))
        self.setWindowIcon(appIcon)
app = QtWidgets.QApplication.instance()
if app is None:
    # this must excu or will crash
    app = QtWidgets.QApplication(sys.argv)
window = MyWidget()
window.setStyleSheet('QMainWindow{border-image :url(C:/Users/chenxing/PycharmProjects/UnrealPython/PythonScripts/images/1534919466186.jpg);}')
window.show()
window.resize(600,400)
# AssetFunctions.createDirectory('/Game/Textures')
# texture_task = AssetFunctions.buildImportTask('C:/Users/chenxing/PycharmProjects/UnrealPython/PythonScripts/images/Icon128.png', '/Game/Textures')
# AssetFunctions.executeImportTasks([texture_task])
# AssetFunctions.saveDirectory('/Game/Textures', True, True)
sys.exit(app.exec_())

