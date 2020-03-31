# -*- coding: utf-8 -*-
import os,re,shutil,json,random,threading,socket,sys,time,datetime
try:
    import requests
except:
    pass
# import unreal
try:
    import pyfbsdk as fb
except:
    pass
try:
    import maya.cmds as mc
    import maya.mel as mel
except:
    pass
# from Qt import QtGui, QtCore,QtWidgets
from strack_api.strack import Strack
from PySide2 import QtCore, QtGui, QtWidgets
class Mobu:
    def __init__(self):
        pass
    def openFile(self,filePath):
        options = fb.FBFbxOptions(True, filePath)
        actionDiscard = fb.FBElementAction.kFBElementActionDiscard
        options.BaseCameras = False
        options.CameraSwitcherSettings = False
        options.GlobalLightingSettings = False
        options.CurrentCameraSettings = False
        options.TransportSettings = False
        options.ShowOptionsDialog = False
        fb.FBApplication().FileOpen(filePath, True, options)
        fb.FBPlayerControl().SnapMode = fb.FBTransportSnapMode.kFBTransportSnapModeSnapOnFrames
        del (fb.FBApplication, fb.FBPlayerControl, options, filePath)

    def mergeFile(self, filePath):
        options = fb.FBFbxOptions(True, filePath)
        options.NamespaceList = filePath.split('/')[-1].split('.')[0]
        actionDiscard = fb.FBElementAction.kFBElementActionDiscard
        options.BaseCameras = False
        options.CameraSwitcherSettings = False
        options.GlobalLightingSettings = False
        options.CurrentCameraSettings = False
        options.TransportSettings = False
        options.ShowOptionsDialog = False
        fb.FBApplication().FileAppend(filePath, True, options)
        fb.FBPlayerControl().SnapMode = fb.FBTransportSnapMode.kFBTransportSnapModeSnapOnFrames
        del (options, filePath)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 320)
        self.login_pushButton = QtWidgets.QPushButton(Form)
        self.login_pushButton.setGeometry(QtCore.QRect(100, 264, 200, 35))
        self.login_pushButton.setText("")
        self.login_pushButton.setIconSize(QtCore.QSize(195, 34))
        self.login_pushButton.setObjectName("login_pushButton")
        self.login_checkBox = QtWidgets.QCheckBox(Form)
        self.login_checkBox.setGeometry(QtCore.QRect(44, 277, 71, 16))
        self.login_checkBox.setObjectName("login_checkBox")
        self.usename_lineEdit = QtWidgets.QLineEdit(Form)
        self.usename_lineEdit.setGeometry(QtCore.QRect(101, 117, 200, 28))
        self.usename_lineEdit.setPlaceholderText("")
        self.usename_lineEdit.setObjectName("usename_lineEdit")
        self.password_lineEdit = QtWidgets.QLineEdit(Form)
        self.password_lineEdit.setGeometry(QtCore.QRect(101, 167, 200, 28))
        self.password_lineEdit.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setPlaceholderText("")
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.login_min_button = QtWidgets.QPushButton(Form)
        self.login_min_button.setGeometry(QtCore.QRect(340, 0, 27, 27))
        self.login_min_button.setText("")
        self.login_min_button.setIconSize(QtCore.QSize(23, 23))
        self.login_min_button.setObjectName("login_min_button")
        self.software_selector = QtWidgets.QComboBox(Form)
        self.software_selector.setGeometry(QtCore.QRect(101, 214, 200, 28))
        self.software_selector.setObjectName("software_selector")
        self.software_selector.addItem("")
        self.software_selector.addItem("")
        self.software_selector.addItem("")
        self.login_close_button = QtWidgets.QPushButton(Form)
        self.login_close_button.setGeometry(QtCore.QRect(370, 0, 27, 27))
        self.login_close_button.setText("")
        self.login_close_button.setIconSize(QtCore.QSize(23, 23))
        self.login_close_button.setObjectName("login_close_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.login_checkBox.setText(QtWidgets.QApplication.translate("Form", "记住", None, -1))
        self.software_selector.setItemText(0, QtWidgets.QApplication.translate("Form", "Unreal", None, -1))
        self.software_selector.setItemText(1, QtWidgets.QApplication.translate("Form", "Maya", None, -1))
        self.software_selector.setItemText(2, QtWidgets.QApplication.translate("Form", "Motionbuilder", None, -1))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(916, 594)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.module_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.module_tab.setGeometry(QtCore.QRect(0, 40, 636, 560))
        self.module_tab.setObjectName("module_tab")
        self.Asset_tab = QtWidgets.QWidget()
        self.Asset_tab.setObjectName("Asset_tab")
        self.AssetSearchText = QtWidgets.QLineEdit(self.Asset_tab)
        self.AssetSearchText.setGeometry(QtCore.QRect(219, 0, 411, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.AssetSearchText.setFont(font)
        self.AssetSearchText.setObjectName("AssetSearchText")
        self.asset_proj_selector = QtWidgets.QComboBox(self.Asset_tab)
        self.asset_proj_selector.setGeometry(QtCore.QRect(0, 0, 72, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.asset_proj_selector.setFont(font)
        self.asset_proj_selector.setObjectName("asset_proj_selector")
        self.asset_proj_selector.addItem("")
        self.asset_proj_selector.setItemText(0, "")
        self.asset_treeWidget = QtWidgets.QTreeWidget(self.Asset_tab)
        self.asset_treeWidget.setGeometry(QtCore.QRect(0, 29, 630, 501))
        self.asset_treeWidget.setObjectName("asset_treeWidget")
        self.asset_type_selector = QtWidgets.QComboBox(self.Asset_tab)
        self.asset_type_selector.setGeometry(QtCore.QRect(73, 0, 72, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.asset_type_selector.setFont(font)
        self.asset_type_selector.setObjectName("asset_type_selector")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.setItemText(0, "")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.addItem("")
        self.asset_step_selector = QtWidgets.QComboBox(self.Asset_tab)
        self.asset_step_selector.setGeometry(QtCore.QRect(146, 0, 72, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.asset_step_selector.setFont(font)
        self.asset_step_selector.setObjectName("asset_step_selector")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.setItemText(0, "")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.module_tab.addTab(self.Asset_tab, "")
        self.Shot_tab = QtWidgets.QWidget()
        self.Shot_tab.setObjectName("Shot_tab")
        self.shot_proj_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_proj_selector.setGeometry(QtCore.QRect(0, 0, 72, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_proj_selector.setFont(font)
        self.shot_proj_selector.setObjectName("shot_proj_selector")
        self.shot_proj_selector.addItem("")
        self.shot_proj_selector.setItemText(0, "")
        self.shot_treeWidget = QtWidgets.QTreeWidget(self.Shot_tab)
        self.shot_treeWidget.setGeometry(QtCore.QRect(0, 29, 630, 500))
        self.shot_treeWidget.setObjectName("shot_treeWidget")
        self.ShotSearchText = QtWidgets.QLineEdit(self.Shot_tab)
        self.ShotSearchText.setGeometry(QtCore.QRect(300, 0, 330, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ShotSearchText.setFont(font)
        self.ShotSearchText.setObjectName("ShotSearchText")
        self.shot_episode_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_episode_selector.setGeometry(QtCore.QRect(73, 0, 72, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_episode_selector.setFont(font)
        self.shot_episode_selector.setObjectName("shot_episode_selector")
        self.shot_episode_selector.addItem("")
        self.shot_episode_selector.setItemText(0, "")
        self.shot_step_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_step_selector.setGeometry(QtCore.QRect(219, 0, 81, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_step_selector.setFont(font)
        self.shot_step_selector.setObjectName("shot_step_selector")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.setItemText(0, "")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_session_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_session_selector.setGeometry(QtCore.QRect(146, 0, 72, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_session_selector.setFont(font)
        self.shot_session_selector.setObjectName("shot_session_selector")
        self.shot_session_selector.addItem("")
        self.shot_session_selector.setItemText(0, "")
        self.module_tab.addTab(self.Shot_tab, "")
        self.Level_tab = QtWidgets.QWidget()
        self.Level_tab.setObjectName("Level_tab")
        self.level_treeWidget = QtWidgets.QTreeWidget(self.Level_tab)
        self.level_treeWidget.setGeometry(QtCore.QRect(0, 29, 630, 500))
        self.level_treeWidget.setObjectName("level_treeWidget")
        self.level_step_selector = QtWidgets.QComboBox(self.Level_tab)
        self.level_step_selector.setGeometry(QtCore.QRect(70, 0, 95, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.level_step_selector.setFont(font)
        self.level_step_selector.setObjectName("level_step_selector")
        self.level_step_selector.addItem("")
        self.level_step_selector.setItemText(0, "")
        self.level_step_selector.addItem("")
        self.level_step_selector.addItem("")
        self.level_step_selector.addItem("")
        self.level_step_selector.addItem("")
        self.level_proj_selector = QtWidgets.QComboBox(self.Level_tab)
        self.level_proj_selector.setGeometry(QtCore.QRect(0, 0, 69, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.level_proj_selector.setFont(font)
        self.level_proj_selector.setObjectName("level_proj_selector")
        self.level_proj_selector.addItem("")
        self.level_proj_selector.setItemText(0, "")
        self.LevelSearchText = QtWidgets.QLineEdit(self.Level_tab)
        self.LevelSearchText.setGeometry(QtCore.QRect(166, 0, 464, 25))
        self.LevelSearchText.setObjectName("LevelSearchText")
        self.module_tab.addTab(self.Level_tab, "")
        self.min_button = QtWidgets.QPushButton(self.centralwidget)
        self.min_button.setGeometry(QtCore.QRect(860, 1, 25, 25))
        self.min_button.setText("")
        self.min_button.setIconSize(QtCore.QSize(21, 21))
        self.min_button.setObjectName("min_button")
        self.close_button = QtWidgets.QPushButton(self.centralwidget)
        self.close_button.setGeometry(QtCore.QRect(891, 1, 25, 25))
        self.close_button.setMouseTracking(False)
        self.close_button.setText("")
        self.close_button.setIconSize(QtCore.QSize(21, 21))
        self.close_button.setObjectName("close_button")
        self.dealWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.dealWidget.setGeometry(QtCore.QRect(635, 59, 281, 541))
        self.dealWidget.setObjectName("dealWidget")
        self.filter_tab = QtWidgets.QWidget()
        self.filter_tab.setObjectName("filter_tab")
        self.graphicsView = QtWidgets.QGraphicsView(self.filter_tab)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 256, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.todayTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.todayTaskBtn.setGeometry(QtCore.QRect(30, 242, 118, 31))
        self.todayTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.todayTaskBtn.setObjectName("todayTaskBtn")
        self.weekTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.weekTaskBtn.setGeometry(QtCore.QRect(30, 282, 118, 31))
        self.weekTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.weekTaskBtn.setObjectName("weekTaskBtn")
        self.monthTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.monthTaskBtn.setGeometry(QtCore.QRect(30, 322, 118, 31))
        self.monthTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.monthTaskBtn.setObjectName("monthTaskBtn")
        self.label = QtWidgets.QLabel(self.filter_tab)
        self.label.setGeometry(QtCore.QRect(10, 219, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.assignedTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.assignedTaskBtn.setGeometry(QtCore.QRect(34, 426, 118, 31))
        self.assignedTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.assignedTaskBtn.setObjectName("assignedTaskBtn")
        self.myTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.myTaskBtn.setGeometry(QtCore.QRect(34, 387, 118, 31))
        self.myTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.myTaskBtn.setObjectName("myTaskBtn")
        self.label_2 = QtWidgets.QLabel(self.filter_tab)
        self.label_2.setGeometry(QtCore.QRect(10, 360, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.allTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.allTaskBtn.setGeometry(QtCore.QRect(34, 468, 118, 31))
        self.allTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.allTaskBtn.setObjectName("allTaskBtn")
        self.dealWidget.addTab(self.filter_tab, "")
        self.work_tab = QtWidgets.QWidget()
        self.work_tab.setObjectName("work_tab")
        self.workListWidget = QtWidgets.QListWidget(self.work_tab)
        self.workListWidget.setGeometry(QtCore.QRect(10, 10, 256, 420))
        self.workListWidget.setObjectName("workListWidget")
        self.dealWidget.addTab(self.work_tab, "")
        self.pubilsh_tab = QtWidgets.QWidget()
        self.pubilsh_tab.setObjectName("pubilsh_tab")
        self.pubilshListWidget = QtWidgets.QListWidget(self.pubilsh_tab)
        self.pubilshListWidget.setGeometry(QtCore.QRect(10, 10, 256, 420))
        self.pubilshListWidget.setObjectName("pubilshListWidget")
        self.dealWidget.addTab(self.pubilsh_tab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.dealWidget.addTab(self.tab, "")
        self.refesh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refesh_button.setGeometry(QtCore.QRect(828, 1, 25, 25))
        self.refesh_button.setText("")
        self.refesh_button.setIconSize(QtCore.QSize(21, 21))
        self.refesh_button.setObjectName("refesh_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actiontemp = QtWidgets.QAction(MainWindow)
        self.actiontemp.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.actiontemp.setObjectName("actiontemp")
        self.actiontemp_2 = QtWidgets.QAction(MainWindow)
        self.actiontemp_2.setObjectName("actiontemp_2")
        self.actiontest = QtWidgets.QAction(MainWindow)
        self.actiontest.setObjectName("actiontest")
        self.actiontest_2 = QtWidgets.QAction(MainWindow)
        self.actiontest_2.setObjectName("actiontest_2")

        self.retranslateUi(MainWindow)
        self.module_tab.setCurrentIndex(1)
        self.dealWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.asset_treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "id", None, -1))
        self.asset_treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow", "项目", None, -1))
        self.asset_treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("MainWindow", "资产名", None, -1))
        self.asset_treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("MainWindow", "中文名", None, -1))
        self.asset_treeWidget.headerItem().setText(4, QtWidgets.QApplication.translate("MainWindow", "任务", None, -1))
        self.asset_treeWidget.headerItem().setText(5, QtWidgets.QApplication.translate("MainWindow", "资产类型", None, -1))
        self.asset_treeWidget.headerItem().setText(6, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.asset_type_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Character", None, -1))
        self.asset_type_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "Prop", None, -1))
        self.asset_type_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "Scene", None, -1))
        self.asset_type_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "Level", None, -1))
        self.asset_step_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "design", None, -1))
        self.asset_step_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "model", None, -1))
        self.asset_step_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "texture", None, -1))
        self.asset_step_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "hair", None, -1))
        self.asset_step_selector.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "rig", None, -1))
        self.asset_step_selector.setItemText(6, QtWidgets.QApplication.translate("MainWindow", "engineset", None, -1))
        self.module_tab.setTabText(self.module_tab.indexOf(self.Asset_tab), QtWidgets.QApplication.translate("MainWindow", "Asset", None, -1))
        self.shot_treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "id", None, -1))
        self.shot_treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow", "项目", None, -1))
        self.shot_treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("MainWindow", "集数", None, -1))
        self.shot_treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("MainWindow", "场次", None, -1))
        self.shot_treeWidget.headerItem().setText(4, QtWidgets.QApplication.translate("MainWindow", "序列", None, -1))
        self.shot_treeWidget.headerItem().setText(5, QtWidgets.QApplication.translate("MainWindow", "任务", None, -1))
        self.shot_treeWidget.headerItem().setText(6, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.shot_step_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "StoryBoard", None, -1))
        self.shot_step_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "mocap", None, -1))
        self.shot_step_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "layout", None, -1))
        self.shot_step_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "anim", None, -1))
        self.shot_step_selector.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "excloth", None, -1))
        self.shot_step_selector.setItemText(6, QtWidgets.QApplication.translate("MainWindow", "lighting", None, -1))
        self.shot_step_selector.setItemText(7, QtWidgets.QApplication.translate("MainWindow", "efx", None, -1))
        self.module_tab.setTabText(self.module_tab.indexOf(self.Shot_tab), QtWidgets.QApplication.translate("MainWindow", "Shot", None, -1))
        self.level_treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "id", None, -1))
        self.level_treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow", "项目", None, -1))
        self.level_treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("MainWindow", "资产名", None, -1))
        self.level_treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("MainWindow", "中文名", None, -1))
        self.level_treeWidget.headerItem().setText(4, QtWidgets.QApplication.translate("MainWindow", "任务", None, -1))
        self.level_treeWidget.headerItem().setText(5, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.level_step_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "leveldesign", None, -1))
        self.level_step_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "levelart", None, -1))
        self.level_step_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "levellight", None, -1))
        self.level_step_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "levelefx", None, -1))
        self.module_tab.setTabText(self.module_tab.indexOf(self.Level_tab), QtWidgets.QApplication.translate("MainWindow", "Level", None, -1))
        self.todayTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "当天任务", None, -1))
        self.weekTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "本周任务", None, -1))
        self.monthTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "本月任务", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "任务周期", None, -1))
        self.assignedTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "我发布的", None, -1))
        self.myTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "指派给我的", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "我的任务", None, -1))
        self.allTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "所有任务", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.filter_tab), QtWidgets.QApplication.translate("MainWindow", "我的任务", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.work_tab), QtWidgets.QApplication.translate("MainWindow", "work", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.pubilsh_tab), QtWidgets.QApplication.translate("MainWindow", "pubilsh", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "页", None, -1))
        self.actionopen.setText(QtWidgets.QApplication.translate("MainWindow", "temp", None, -1))
        self.actiontemp.setText(QtWidgets.QApplication.translate("MainWindow", "打开", None, -1))
        self.actiontemp_2.setText(QtWidgets.QApplication.translate("MainWindow", "更新", None, -1))
        self.actiontest.setText(QtWidgets.QApplication.translate("MainWindow", "test", None, -1))
        self.actiontest_2.setText(QtWidgets.QApplication.translate("MainWindow", "test", None, -1))

class strack():
    def __init__(self,url,user,password):
        self.st = Strack(base_url=url, login_name=user, password=password)
        self.statusTable = self.st.select('status').get('rows')
        self.projectTable = self.st.select('project', fields=['id', 'code', 'name']).get('rows')
        self.episodeTable = self.st.select('episode').get('rows')
        self.sessionTable = self.st.select('session').get('rows')
    def asset_task(self):
        list = self.st.select('asset',fields=['id']).get('rows')
        id_list = [asset.get('id') for asset in list]
        if id_list:
            task = self.st.select('base', [['entity_id', 'in', id_list]])
            return task.get('rows')
        else:
            return []

    def shot_task(self):
        list = self.st.select('sequence',fields=['id']).get('rows')
        id_list = [shot.get('id') for shot in list]
        if id_list:
            task = self.st.select('base', [['entity_id', 'in', id_list]])
            return task.get('rows')
        else:
            return []

    def level_task(self):
        list = self.st.select('level',fields=['id']).get('rows')
        id_list = [shot.get('id') for shot in list]
        if id_list:
            task = self.st.select('base', [['entity_id', 'in', id_list]])
            return task.get('rows')
        else:
            return []


class mayaWidget(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,myStrack,local_path):
        self.strack = myStrack
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable
        self.status_data = self.strack.statusTable
        self.episode_data = self.strack.episodeTable
        self.session_data = self.strack.sessionTable
        self.local_path = local_path
        self.now = datetime.datetime.now()
        self.deadline = self.now + datetime.timedelta(days=300)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.close_button.clicked.connect(self.close)
        self.min_button.clicked.connect(self.showMinimized)
        self.asset_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_treeWidget.customContextMenuRequested.connect(self.assetOpenMenu)
        self.shot_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shot_treeWidget.customContextMenuRequested.connect(self.shotOpenMenu)
        self.level_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.level_treeWidget.customContextMenuRequested.connect(self.levelOpenMenu)
        self.workListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workListWidget.customContextMenuRequested.connect(self.workOpenMenu)
        self.pubilshListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pubilshListWidget.customContextMenuRequested.connect(self.pubilshOpenMenu)
        self.AssetSearchText.textChanged.connect(self.refeshAssetTree)
        self.ShotSearchText.textChanged.connect(self.refeshShotTree)
        self.LevelSearchText.textChanged.connect(self.refeshLevelTree)
        self.asset_proj_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_type_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_step_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_step_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.level_step_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_proj_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.asset_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.shot_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.asset_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.shot_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.todayTaskBtn.clicked.connect(self.todayFilter)
        self.weekTaskBtn.clicked.connect(self.weekFilter)
        self.monthTaskBtn.clicked.connect(self.monthFilter)
        self.refesh_button.clicked.connect(self.refeshData)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
        self.additem_init()

    def refeshData(self):
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable
        self.status_data = self.strack.statusTable
        self.episode_data = self.strack.episodeTable
        self.session_data = self.strack.sessionTable
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def findEpisode(self,code,projId):
        for item in self.episode_data:
            if item.get('code') == code and item.get('project_id')==projId:
                return item

    def findSession(self,code,projId,parent_id):
        for item in self.session_data:
            if item.get('code') == code and item.get('project_id')==projId and item.get('parent_id')==parent_id:
                return item

    def projCodeToItem(self,code):
        for item in self.project_data:
            if item.get('code') == code:
                return item

    def refeshWorkList(self):
            self.workListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)

    def refeshPubilshList(self):
            self.pubilshListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)

    def additem_init(self):
        for item in self.project_data:
            self.asset_proj_selector.addItem(item.get('name'))
            self.shot_proj_selector.addItem(item.get('name'))
            self.level_proj_selector.addItem(item.get('name'))
        for item in self.episode_data:
            self.shot_episode_selector.addItem(item.get('code'))
        for item in self.session_data:
            self.shot_session_selector.addItem(item.get('code'))


    def list_file(self, path):
        temp_list = []
        fs = os.listdir(path.decode('utf-8'))
        if fs:
            for obj in fs:
                tmp_path = os.path.join(path, obj)
                if not os.path.isdir(tmp_path):
                    temp_list.append(obj)
        return temp_list

    def todayFilter(self):
        temp = str(datetime.datetime.now()).split(' ')[0] + ' 23:59:00'
        self.deadline = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def weekFilter(self):
        self.deadline =self.now + datetime.timedelta(days=7)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def monthFilter(self):
        self.deadline =self.now + datetime.timedelta(days=30)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def dataIdSelect(self,data,id):
        temp = {}
        for item in data:
            if item.get('id') ==int(id):
                temp = item
                break
        return temp

    def refeshAssetTree(self):
        word = self.AssetSearchText.text()
        self.asset_treeWidget.clear()
        self.asset_treeWidget.hideColumn(0)
        assetType = self.asset_type_selector.currentText()
        step = self.asset_step_selector.currentText()
        for item in self.asset_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('asset_code')) or re.search(word,item.get('json').get('asset_name')))\
                    and re.search(assetType, item.get('json').get('asset_type_code')) \
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.asset_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('asset_code'))
                child.setText(3, item.get('json').get('asset_name'))
                child.setText(4, item.get('json').get('task_name'))
                child.setText(5, item.get('json').get('asset_type_name'))
                child.setText(6, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(6, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def refeshShotTree(self):
        word = self.ShotSearchText.text()
        self.shot_treeWidget.clear()
        self.shot_treeWidget.hideColumn(0)
        step = self.shot_step_selector.currentText()
        for item in self.shot_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('sequence_name')) or re.search(word,item.get('json').get('sequence_code'))) \
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.shot_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('episode_name'))
                child.setText(3, item.get('json').get('session_name'))
                child.setText(4, item.get('json').get('sequence_name'))
                child.setText(5, item.get('json').get('task_name'))
                child.setText(6, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(6, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def refeshLevelTree(self):
        word = self.LevelSearchText.text()
        self.level_treeWidget.clear()
        self.level_treeWidget.hideColumn(0)
        step = self.level_step_selector.currentText()
        for item in self.level_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('level_code')) or re.search(word,item.get('json').get('level_name')))\
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.level_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('level_code'))
                child.setText(3, item.get('json').get('level_name'))
                child.setText(4, item.get('json').get('task_name'))
                child.setText(5, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(5, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def assetOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.asset_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.asset_treeWidget.selectedItems():
                print(self.asset_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.asset_data, id))

    def shotOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.shot_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.shot_treeWidget.selectedItems():
                print(self.shot_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.shot_data, id))


    def levelOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.level_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.level_treeWidget.selectedItems():
                print(self.level_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.level_data, id))

    def workOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        openAction = menu.addAction("打开文件")
        importAction = menu.addAction("导入文件")
        exportAction = menu.addAction("导出文件")
        refAction = menu.addAction("引用文件")
        menu.addSeparator()
        commitAnimExport = menu.addAction("提交动画导出")
        localAnimExport = menu.addAction("本机自动导出")
        bqAnimImport = menu.addAction("表情导入")
        action = menu.exec_(self.workListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                file_name = '%s_%s_V##.mb'%(code,step)
                check_name = '%s_%s_V\d\d.mb'%(code,step)
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本序号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s'%(item.get('json').get('Work_path'),str(my_str))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshWorkList()

            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                proj = item.get('json').get('project_code')
                episode = item.get('json').get('episode_code')
                session = item.get('json').get('session_code')
                sequence = item.get('json').get('sequence_code')
                newpath = '%s/%s_%s_%s_%s.mb'%(item.get('json').get('Work_path'),proj,episode,session,sequence)
                mc.file(rename='C:/Users/Public/Documents/temp.mb')
                mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                self.refeshWorkList()
        if action == openAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, open=1, f=1)
        if action == importAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path,i=1, ignoreVersion=1)
        if action == exportAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                if step == 'rig':
                    file_name = '%s_%s_##.fbx' % (code, step)
                    check_name = '%s_%s_*.fbx' % (code, step)
                else:
                    file_name = '%s_%s_V##.fbx' % (code, step)
                    check_name = '%s_%s_V\d\d.fbx' % (code, step)
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s' % (item.get('json').get('Work_path'), str(my_str))
                    mc.file(newpath, f=1, type='FBX export', pr=1, es=1)
                    self.refeshWorkList()
        if action == refAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, reference=1, namespace=path.split('.')[0].split('/')[-1])
        if action == commitAnimExport:
            if self.shot_treeWidget.selectedItems() and self.workListWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                step = item.get('json').get('step_code')
                if step == 'anim':
                    path = item.get('json').get('Work_path')+ '/'+ str(self.workListWidget.selectedItems()[0].text())
                    dic = {'taskStatus': 'wait', 'TaskType': 'AnimateTask', 'input_file': path,
                           'publish_dir': item.get('json').get('Publish_path'),
                           'TaskId': item.get('uuid'), 'db': item.get('json').get('project_code'),
                           'eps_cnname': item.get('json').get('episode_code'), 'asset_shot': item.get('json').get('sequence_code'),
                           'abc': 0}
                    r_json = requests.post('http://192.168.1.32:5000/maya/con?action=post', json.dumps(dic))
                    msg_box = QtWidgets.QMessageBox
                    msg_box.question(self, '提示', r_json.content, msg_box.Ok)
        if action == localAnimExport:
            import sys
            sys.path.append("//192.168.1.9/dlq/maya_script")
            # from maya_excute import *
            # main()
    def pubilshOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        openAction = menu.addAction("打开文件")
        importAction = menu.addAction("导入文件")
        exportAction = menu.addAction("导出文件")
        refAction = menu.addAction("引用文件")
        action = menu.exec_(self.pubilshListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                if step == 'rig':
                    file_name = '%s_%s_V##.mb'%(code,step)
                    check_name = '%s_%s_V\d\d.mb'%(code,step)
                    my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号',QtWidgets.QLineEdit.Normal, file_name)
                    if re.search(check_name, str(my_str)) and ok:
                        newpath = '%s/%s' % (item.get('json').get('Publish_path'), str(my_str))
                        mc.file(rename='C:/Users/Public/Documents/temp.mb')
                        mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                        shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                        self.refeshPubilshList()
                else:
                    file_name = '%s_%s_V01.mb' % (code, step)
                    newpath = '%s/%s'%(item.get('json').get('Publish_path'),str(file_name))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshPubilshList()
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                if step == 'anim':
                    pass
                else:
                    file_name = '%s_%s_V01.mb' % (code, step)
                    newpath = '%s/%s'%(item.get('json').get('Publish_path'),str(file_name))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshPubilshList()
        if action == openAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, open=1, f=1)
        if action == exportAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                task_code = item.get('json').get('task_code')
                if step == 'rig':
                    file_name = '%s_%s_##.fbx' % (code, step)
                    check_name = '%s_%s_.+.\.fbx' % (code, step)
                    my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号',QtWidgets.QLineEdit.Normal, file_name)
                    if re.search(check_name, str(my_str)) and ok:
                        newpath = '%s/%s' % (item.get('json').get('Publish_path'), str(my_str))
                        mc.file(newpath, f=1, type='FBX export', pr=1, es=1)
                if step == 'model':
                    if re.search('LowModel',task_code):
                        file_name = '%s/%s_%s_LowModel.fbx' % (item.get('json').get('Publish_path'),code, step)
                        mc.file(file_name, f=1, type='FBX export', pr=1, es=1)
                    if re.search('HighModel',task_code):
                        file_name = '%s/%s_%s_HighModel.fbx' % (item.get('json').get('Publish_path'),code, step)
                        mc.file(file_name, f=1, type='FBX export', pr=1, es=1)
                    if re.search('EngineModel',task_code):
                        file_name = '%s/%s_%s_EngineModel.fbx' % (item.get('json').get('Publish_path'),code, step)
                        mc.file(file_name, f=1, type='FBX export', pr=1, es=1)
                else:
                    file_name = '%s/%s_%s_V01.fbx' % (item.get('json').get('Publish_path'), code, step)
                    mc.file(file_name, f=1, type='FBX export', pr=1, es=1)
                self.refeshPubilshList()
        if action == refAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, reference=1, namespace=path.split('.')[0].split('/')[-1])
        if action == importAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, i=1, ignoreVersion=1)

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

        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/12.jpg'%self.local_path)))
        self.min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/13.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/11.jpg);}' % self.local_path)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def showColor(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '对话框','请输入序列名:')
        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

class mobuWidget(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,myStrack,local_path):
        self.mobu = Mobu()
        self.strack = myStrack
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable
        self.status_data = self.strack.statusTable
        self.episode_data = self.strack.episodeTable
        self.session_data = self.strack.sessionTable
        self.local_path = local_path
        self.now = datetime.datetime.now()
        self.deadline = self.now + datetime.timedelta(days=300)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.close_button.clicked.connect(self.close)
        self.min_button.clicked.connect(self.showMinimized)
        self.asset_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_treeWidget.customContextMenuRequested.connect(self.assetOpenMenu)
        self.shot_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shot_treeWidget.customContextMenuRequested.connect(self.shotOpenMenu)
        self.level_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.level_treeWidget.customContextMenuRequested.connect(self.levelOpenMenu)
        self.AssetSearchText.textChanged.connect(self.refeshAssetTree)
        self.ShotSearchText.textChanged.connect(self.refeshShotTree)
        self.LevelSearchText.textChanged.connect(self.refeshLevelTree)
        self.asset_proj_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_type_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_step_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_step_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.level_step_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_proj_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.asset_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.shot_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.asset_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.shot_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.todayTaskBtn.clicked.connect(self.todayFilter)
        self.weekTaskBtn.clicked.connect(self.weekFilter)
        self.monthTaskBtn.clicked.connect(self.monthFilter)
        self.refesh_button.clicked.connect(self.refeshData)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
        self.additem_init()

    def refeshData(self):
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable
        self.status_data = self.strack.statusTable
        self.episode_data = self.strack.episodeTable
        self.session_data = self.strack.sessionTable
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def findEpisode(self,code,projId):
        for item in self.episode_data:
            if item.get('code') == code and item.get('project_id')==projId:
                return item

    def findSession(self,code,projId,parent_id):
        for item in self.session_data:
            if item.get('code') == code and item.get('project_id')==projId and item.get('parent_id')==parent_id:
                return item

    def projCodeToItem(self,code):
        for item in self.project_data:
            if item.get('code') == code:
                return item
    def refeshWorkList(self):
            self.workListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)

    def refeshPubilshList(self):
            self.pubilshListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)

    def additem_init(self):
        for item in self.project_data:
            self.asset_proj_selector.addItem(item.get('name'))
            self.shot_proj_selector.addItem(item.get('name'))
            self.level_proj_selector.addItem(item.get('name'))

    def list_file(self, path):
        temp_list = []
        fs = os.listdir(path.decode('utf-8'))
        if fs:
            for obj in fs:
                tmp_path = os.path.join(path, obj)
                if not os.path.isdir(tmp_path):
                    temp_list.append(obj)
        return temp_list

    def todayFilter(self):
        temp = str(datetime.datetime.now()).split(' ')[0] + ' 23:59:00'
        self.deadline = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def weekFilter(self):
        self.deadline =self.now + datetime.timedelta(days=7)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def monthFilter(self):
        self.deadline =self.now + datetime.timedelta(days=30)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def dataIdSelect(self,data,id):
        temp = {}
        for item in data:
            if item.get('id') ==int(id):
                temp = item
                break
        return temp

    def refeshAssetTree(self):
        word = self.AssetSearchText.text()
        self.asset_treeWidget.clear()
        self.asset_treeWidget.hideColumn(0)
        assetType = self.asset_type_selector.currentText()
        step = self.asset_step_selector.currentText()
        for item in self.asset_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('asset_code')) or re.search(word,item.get('json').get('asset_name')))\
                    and re.search(assetType, item.get('json').get('asset_type_code')) \
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.asset_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('asset_code'))
                child.setText(3, item.get('json').get('asset_name'))
                child.setText(4, item.get('json').get('task_name'))
                child.setText(5, item.get('json').get('asset_type_name'))
                child.setText(6, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(6, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def refeshShotTree(self):
        word = self.ShotSearchText.text()
        self.shot_treeWidget.clear()
        self.shot_treeWidget.hideColumn(0)
        step = self.shot_step_selector.currentText()
        for item in self.shot_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('sequence_name')) or re.search(word,item.get('json').get('sequence_code'))) \
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.shot_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('episode_name'))
                child.setText(3, item.get('json').get('session_name'))
                child.setText(4, item.get('json').get('sequence_name'))
                child.setText(5, item.get('json').get('task_name'))
                child.setText(6, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(6, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def refeshLevelTree(self):
        word = self.LevelSearchText.text()
        self.level_treeWidget.clear()
        self.level_treeWidget.hideColumn(0)
        step = self.level_step_selector.currentText()
        for item in self.level_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('level_code')) or re.search(word,item.get('json').get('level_name')))\
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.level_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('level_code'))
                child.setText(3, item.get('json').get('level_name'))
                child.setText(4, item.get('json').get('task_name'))
                child.setText(5, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(5, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def assetOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.asset_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.asset_treeWidget.selectedItems():
                print(self.asset_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.asset_data, id))

    def shotOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.shot_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.shot_treeWidget.selectedItems():

                # print(self.shot_treeWidget.selectedItems()[0].text(1))
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                if item.get('json').get('step_code') == 'layout':
                    path = item.get('json').get('Publish_path').replace('layout','mocap')
                    self.mobu.mergeFile('P:/TestProject/shot_work/ep001/sc01/seq01/mocap/Publish/iphone_face.fbx')
                    # for each in self.list_file(path):
                    #     if re.search('.fbx',each):
                    #         print('%s/%s'%(path,each))
                    #         self.mobu.mergeFile('%s/%s'%(path,each))

        if action == updateAction:
            if self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.shot_data, id))

    def levelOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.level_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.level_treeWidget.selectedItems():
                print(self.level_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.level_data, id))


    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                    background-image:url('%s/images/04.jpg');
                }
                #login_pushButton:Pressed{
                background-image:url('%s/images/05.jpg');
                }
                #close_button{
                background-image:url('%s/images/09.jpg');
                }
                #min_button{
                background-image:url('%s/images/08.jpg');
                }
                ''' % (self.local_path, self.local_path, self.local_path, self.local_path)

        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/12.jpg'%self.local_path)))
        self.min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/13.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/11.jpg);}' % self.local_path)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def showColor(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '对话框',
                                        '请输入你的名字:')

        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

class unrealWidget(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,myStrack,local_path):
        self.strack = myStrack
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable
        self.status_data = self.strack.statusTable
        self.episode_data = self.strack.episodeTable
        self.session_data = self.strack.sessionTable
        self.local_path = local_path
        self.now = datetime.datetime.now()
        self.deadline = self.now + datetime.timedelta(days=300)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.close_button.clicked.connect(self.close)
        self.min_button.clicked.connect(self.showMinimized)
        self.asset_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_treeWidget.customContextMenuRequested.connect(self.assetOpenMenu)
        self.shot_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shot_treeWidget.customContextMenuRequested.connect(self.shotOpenMenu)
        self.level_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.level_treeWidget.customContextMenuRequested.connect(self.levelOpenMenu)
        self.workListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workListWidget.customContextMenuRequested.connect(self.workOpenMenu)
        self.pubilshListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pubilshListWidget.customContextMenuRequested.connect(self.pubilshOpenMenu)
        self.AssetSearchText.textChanged.connect(self.refeshAssetTree)
        self.ShotSearchText.textChanged.connect(self.refeshShotTree)
        self.LevelSearchText.textChanged.connect(self.refeshLevelTree)
        self.asset_proj_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_type_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_step_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_step_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.level_step_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_proj_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.asset_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.shot_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.asset_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.shot_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.todayTaskBtn.clicked.connect(self.todayFilter)
        self.weekTaskBtn.clicked.connect(self.weekFilter)
        self.monthTaskBtn.clicked.connect(self.monthFilter)
        self.refesh_button.clicked.connect(self.refeshData)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
        self.additem_init()

    def refeshData(self):
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable
        self.status_data = self.strack.statusTable
        self.episode_data = self.strack.episodeTable
        self.session_data = self.strack.sessionTable
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()

    def findEpisode(self,code,projId):
        for item in self.episode_data:
            if item.get('code') == code and item.get('project_id')==projId:
                return item

    def findSession(self,code,projId,parent_id):
        for item in self.session_data:
            if item.get('code') == code and item.get('project_id')==projId and item.get('parent_id')==parent_id:
                return item

    def projCodeToItem(self,code):
        for item in self.project_data:
            if item.get('code') == code:
                return item

    def refeshWorkList(self):
            self.workListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)

    def refeshPubilshList(self):
            self.pubilshListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)

    def additem_init(self):
        for item in self.project_data:
            self.asset_proj_selector.addItem(item.get('code'))
            self.shot_proj_selector.addItem(item.get('code'))
            self.level_proj_selector.addItem(item.get('code'))
        for item in self.episode_data:
            self.shot_episode_selector.addItem(item.get('code'))
        for item in self.session_data:
            self.shot_session_selector.addItem(item.get('code'))
    def list_file(self, path):
        temp_list = []
        fs = os.listdir(path.decode('utf-8'))
        if fs:
            for obj in fs:
                tmp_path = os.path.join(path, obj)
                if not os.path.isdir(tmp_path):
                    temp_list.append(obj)
        return temp_list

    def todayFilter(self):
        temp = str(datetime.datetime.now()).split(' ')[0] + ' 23:59:00'
        self.deadline = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def weekFilter(self):
        self.deadline =self.now + datetime.timedelta(days=7)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def monthFilter(self):
        self.deadline =self.now + datetime.timedelta(days=30)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def dataIdSelect(self,data,id):
        temp = {}
        for item in data:
            if item.get('id') ==int(id):
                temp = item
                break
        return temp

    def refeshAssetTree(self):
        word = self.AssetSearchText.text()
        self.asset_treeWidget.clear()
        self.asset_treeWidget.hideColumn(0)
        assetType = self.asset_type_selector.currentText()
        step = self.asset_step_selector.currentText()
        for item in self.asset_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('asset_code')) or re.search(word,item.get('json').get('asset_name')))\
                    and re.search(assetType, item.get('json').get('asset_type_code')) \
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.asset_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('asset_code'))
                child.setText(3, item.get('json').get('asset_name'))
                child.setText(4, item.get('json').get('task_name'))
                child.setText(5, item.get('json').get('asset_type_name'))
                child.setText(6, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(6, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def refeshShotTree(self):
        word = self.ShotSearchText.text()
        self.shot_treeWidget.clear()
        self.shot_treeWidget.hideColumn(0)
        step = self.shot_step_selector.currentText()
        for item in self.shot_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('sequence_name')) or re.search(word,item.get('json').get('sequence_code'))) \
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.shot_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('episode_name'))
                child.setText(3, item.get('json').get('session_name'))
                child.setText(4, item.get('json').get('sequence_name'))
                child.setText(5, item.get('json').get('task_name'))
                child.setText(6, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(6, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def refeshLevelTree(self):
        word = self.LevelSearchText.text()
        self.level_treeWidget.clear()
        self.level_treeWidget.hideColumn(0)
        step = self.level_step_selector.currentText()
        for item in self.level_data:
            if item.get('end_time'):
                self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
            else:
                self.endTime = self.now + datetime.timedelta(days=6)
            if (re.search(word,item.get('json').get('level_code')) or re.search(word,item.get('json').get('level_name')))\
                    and re.search(step, item.get('json').get('step_code')) \
                    and self.endTime < self.deadline:
                child = QtWidgets.QTreeWidgetItem(self.level_treeWidget)
                child.setText(0, str(item.get('id')))
                child.setText(1, item.get('json').get('project_name'))
                child.setText(2, item.get('json').get('level_code'))
                child.setText(3, item.get('json').get('level_name'))
                child.setText(4, item.get('json').get('task_name'))
                child.setText(5, self.dataIdSelect(self.status_data,item.get('status_id')).get('name'))
                child.setIcon(5, QtGui.QIcon('%s/images/13.jpg' % self.local_path))

    def assetOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.asset_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.asset_treeWidget.selectedItems():
                print(self.asset_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.asset_data, id))

    def shotOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        createSequence = menu.addAction("创建动画序列")
        action = menu.exec_(self.shot_treeWidget.mapToGlobal(position))
        if self.shot_treeWidget.selectedItems():
            if action == importAction:
                print(self.shot_treeWidget.selectedItems()[0].text(1))
            if action == updateAction:
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.shot_data, id))
        if action == createSequence:
            if self.shot_proj_selector.currentText() and self.shot_episode_selector.currentText() and self.shot_session_selector.currentText():
                sequence, ok = QtWidgets.QInputDialog.getText(self, '对话框', '请输入序列名:')
                if ok:
                    print('P:/%s/shot_work/%s/%s/%s/mocap/Publish'%(str(self.shot_proj_selector.currentText()),
                                                                    str(self.shot_episode_selector.currentText()),
                                                                    str(self.shot_session_selector.currentText()),
                                                                    str(sequence)))
                    projId = self.projCodeToItem(str(self.shot_proj_selector.currentText())).get('id')
                    episode = self.findEpisode(str(self.shot_episode_selector.currentText()),projId)
                    session = self.findSession(str(self.shot_session_selector.currentText()),projId,episode.get('id'))
                    data = {
                        'project_id': projId,
                        'code': str(sequence),
                        'name': str(sequence),
                        'parent_id': session.get('id'),
                        'module_id': 58
                    }
                    self.strack.st.create('sequence',data)

    def levelOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.level_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.level_treeWidget.selectedItems():
                print(self.level_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.level_data, id))

    def workOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        openAction = menu.addAction("打开文件")
        importAction = menu.addAction("导入文件")
        exportAction = menu.addAction("导出文件")
        refAction = menu.addAction("引用文件")
        action = menu.exec_(self.workListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                file_name = '%s_%s_V##.mb'%(code,step)
                check_name = '%s_%s_V\d\d.mb'%(code,step)
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本序号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s'%(item.get('json').get('Work_path'),str(my_str))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshWorkList()

            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                proj = item.get('json').get('project_code')
                episode = item.get('json').get('episode_code')
                session = item.get('json').get('session_code')
                sequence = item.get('json').get('sequence_code')
                newpath = '%s/%s_%s_%s_%s.mb'%(item.get('json').get('Work_path'),proj,episode,session,sequence)
                mc.file(rename='C:/Users/Public/Documents/temp.mb')
                mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                self.refeshWorkList()
        if action == openAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, open=1, f=1)
        if action == importAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path,i=1, ignoreVersion=1)
        if action == exportAction:
            id = self.asset_treeWidget.selectedItems()[0].text(0)
            item = self.dataIdSelect(self.asset_data, id)
            code = item.get('json').get('asset_code')
            step = item.get('json').get('step_code')
            if step == 'rig':
                file_name = '%s_%s_##.fbx' % (code, step)
                check_name = '%s_%s_*.fbx' % (code, step)
            else:
                file_name = '%s_%s_V##.fbx' % (code, step)
                check_name = '%s_%s_V\d\d.fbx' % (code, step)
            my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号', QtWidgets.QLineEdit.Normal,file_name)
            if re.search(check_name, str(my_str)) and ok:
                newpath = '%s/%s' % (item.get('json').get('Work_path'), str(my_str))
                mc.file(newpath, f=1, type='FBX export', pr=1, es=1)
                self.refeshWorkList()
        if action == refAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, reference=1, namespace=path.split('.')[0].split('/')[-1])

    def pubilshOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        openAction = menu.addAction("打开文件")
        importAction = menu.addAction("导入文件")
        exportAction = menu.addAction("导出文件")
        refAction = menu.addAction("引用文件")
        action = menu.exec_(self.workListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                if step == 'rig':
                    file_name = '%s_%s_##.mb'%(code,step)
                    check_name = '%s_%s_*.mb'%(code,step)
                else:
                    file_name = '%s_%s_V##.mb' % (code, step)
                    check_name = '%s_%s_V\d\d.mb' % (code, step)
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s'%(item.get('json').get('Work_path'),str(my_str))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshWorkList()
    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                    background-image:url('%s/images/04.jpg');
                }
                #login_pushButton:Pressed{
                background-image:url('%s/images/05.jpg');
                }
                #close_button{
                background-image:url('%s/images/09.jpg');
                }
                #min_button{
                background-image:url('%s/images/08.jpg');
                }
                ''' % (self.local_path, self.local_path, self.local_path, self.local_path)
        self.refesh_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/03.jpg'%self.local_path)))
        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/12.jpg'%self.local_path)))
        self.min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/13.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/11.jpg);}' % self.local_path)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def showColor(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '对话框','请输入你的名字:')
        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

class MyLogin(QtWidgets.QMainWindow,Ui_Form):
    def __init__(self):
        self.local_path = os.path.dirname(__file__).replace('\\','/')
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.remember()
        self.login_close_button.clicked.connect(self.close)
        self.login_min_button.clicked.connect(self.showMinimized)
        self.login_pushButton.clicked.connect(self.login)


    def remember(self):
        if os.path.exists('C:/Users/Public/Documents/user.txt'):
            self.usename_lineEdit.setText(open('C:/Users/Public/Documents/user.txt').read().split(' ')[0])
            self.password_lineEdit.setText(open('C:/Users/Public/Documents/user.txt').read().split(' ')[1])

    def login(self):
        user = self.usename_lineEdit.text()
        password = self.password_lineEdit.text()
        if self.login_checkBox.isChecked():
            with open('C:/Users/Public/Documents/user.txt', 'w') as fileobject:
                fileobject.write(str(user) + ' ' + str(password))
                fileobject.close()
        myStrack = None
        software = self.software_selector.currentText()
        try:
            myStrack = strack("https://strack.teamones.com/", user, password)
        except:
            QtWidgets.QMessageBox.warning(self,u"提示", u"用户名或密码错误")
        if myStrack:
            self.hide()
            app = QtWidgets.QApplication.instance()
            if app is None:
                # this must excu or will crash
                app = QtWidgets.QApplication(sys.argv)
            if software == 'Unreal':
                self.window = unrealWidget(myStrack, self.local_path)
                self.window.show()
                self.window.setFixedSize(920, 600)
            if software == 'Maya':
                self.window = mayaWidget(myStrack,self.local_path)
                self.window.show()
                self.window.setFixedSize(920, 600)
            if software == 'Motionbuilder':
                self.window = mobuWidget(myStrack, self.local_path)
                self.window.show()
                self.window.setFixedSize(920, 600)
    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                }
                '''
        # self.login_pushButton.setStyleSheet(style)
        self.login_pushButton.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/04.jpg' % self.local_path)))
        self.login_close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/09.jpg' % self.local_path)))
        self.login_min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/08.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/zhhy02.png);}' % self.local_path)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        # this must excu or will crash
        app = QtWidgets.QApplication(sys.argv)
    log = MyLogin()
    log.show()
    log.setFixedSize(400, 320)
    sys.exit(app.exec_())
