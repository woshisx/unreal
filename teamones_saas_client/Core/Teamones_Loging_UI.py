# -*- coding: utf-8 -*-
# @Time : 2020/7/10 19:58
# @Author : LiuYang
# @email : 317431629@qq.com
# @FileName: Teamones_Loging_UI.py

# _+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+
import dayu_widgets as dy
from PySide2.QtGui import QPixmap
from Libs import package


class TeamOnesLogUI(dy.qt.QWidget):
    def __init__(self):
        super(TeamOnesLogUI, self).__init__()
        self.MainLayout = dy.qt.QVBoxLayout(self)
        self.setWindowTitle("TeamOnes Logging")
        self.setGeometry(750, 300, 450, 400)
        self.setWindowFlags(dy.qt.Qt.FramelessWindowHint)

        self.titleBarLayout = dy.qt.QHBoxLayout()
        self.shrinkButton = dy.MPushButton("", dy.qt.MIcon('minus_line.svg')).tiny()

        self.closeButton = dy.MPushButton("", dy.qt.MIcon('close_line_dark.svg')).tiny()

        self.avatarLayout = dy.qt.QHBoxLayout()
        self.avatarLabel = dy.MAvatar()
        self.avatarLabel.set_dayu_size(70)
        self.avatarLabel.setAlignment(dy.qt.Qt.AlignHCenter)

        self.urlLayout = dy.qt.QHBoxLayout()
        self.urlLine = dy.MLineEdit()
        self.urlLine.setPlaceholderText("Please enter your url...")
        self.urlLine.set_prefix_widget(dy.MToolButton().svg(package.get("icon/httl.png")).icon_only())
        self.urlLine.setMinimumWidth(315)

        self.loggingNameLayout = dy.qt.QHBoxLayout()
        self.loggingNameLine = dy.MLineEdit()
        self.loggingNameLine.setPlaceholderText("Please enter your logging_name...")
        self.loggingNameLine.set_prefix_widget(dy.MToolButton().svg('user_line.svg').icon_only())
        self.loggingNameLine.setMinimumWidth(315)

        self.loggingPasswordLayout = dy.qt.QHBoxLayout()
        self.loggingPasswordLine = dy.MLineEdit()
        self.loggingPasswordLine.setPlaceholderText("Please enter your password...")
        self.loggingPasswordLine.set_prefix_widget(dy.MToolButton().svg(package.get("icon/password.png")).icon_only())
        self.loggingPasswordLine.setEchoMode(dy.MLineEdit.Password)
        self.loggingPasswordLine.setMinimumWidth(315)

        self.loggingSelectLayout = dy.qt.QHBoxLayout()

        self.autoLogging = dy.MCheckBox(u"自动登录  ")
        self.rememberCheckBox = dy.MCheckBox(u"记住密码  ")
        self.rememberCheckBox.setChecked(True)
        self.DccSelectLabel = dy.MLabel("DCC Soft: ").warning().strong()

        self.loggingLayout = dy.qt.QHBoxLayout()
        # self.rememberLoggingInfo = dy.MCheckBox("remember password:")
        self.loggingButton = dy.MPushButton(u"登录").warning()
        self.loggingButton.setMinimumWidth(315)

        self.loginLoading = dy.MLoading()
        self.loginLoading.hide()

        self.setup_ui()
        self.connect_ui()

    def setup_ui(self):
        self.MainLayout.addLayout(self.titleBarLayout)
        self.MainLayout.addLayout(self.avatarLayout)
        self.MainLayout.addLayout(self.urlLayout)
        self.MainLayout.addLayout(self.loggingNameLayout)
        self.MainLayout.addLayout(self.loggingPasswordLayout)
        self.MainLayout.addLayout(self.loggingSelectLayout)
        # self.MainLayout.addWidget(dy.MDivider())
        self.MainLayout.addLayout(self.loggingLayout)
        self.MainLayout.addWidget(self.loginLoading)
        
        self.avatarLayout.addWidget(self.avatarLabel)

        self.titleBarLayout.addStretch()
        self.titleBarLayout.addWidget(self.shrinkButton)
        self.titleBarLayout.addWidget(self.closeButton)

        self.urlLayout.addStretch()
        self.urlLayout.addWidget(self.urlLine)
        self.urlLayout.addStretch()

        self.loggingNameLayout.addStretch()
        self.loggingNameLayout.addWidget(self.loggingNameLine)
        self.loggingNameLayout.addStretch()

        self.loggingPasswordLayout.addStretch()
        self.loggingPasswordLayout.addWidget(self.loggingPasswordLine)
        self.loggingPasswordLayout.addStretch()

        self.loggingSelectLayout.addStretch()
        self.loggingSelectLayout.addWidget(self.autoLogging)
        self.loggingSelectLayout.addWidget(self.rememberCheckBox)
        self.loggingSelectLayout.addStretch()

        self.loggingLayout.addStretch()
        self.loggingLayout.addWidget(self.loggingButton)
        self.loggingLayout.addStretch()

    def connect_ui(self):
        self.closeButton.clicked.connect(self.close)
        self.shrinkButton.clicked.connect(self.showMinimized)

    def mousePressEvent(self, event):
        if event.button() == dy.qt.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            # self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if dy.qt.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()
    

if __name__ == '__main__':
    app = dy.qt.QApplication([])
    Alert_Example = TeamOnesLogUI()
    theme = dy.theme.MTheme("dark", primary_color=dy.theme.MTheme.cyan)
    theme.apply(Alert_Example)
    Alert_Example.show()
    app.exec_()
