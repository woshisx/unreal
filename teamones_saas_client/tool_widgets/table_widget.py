# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :table_widget.py
# @Author       :LiuYang
import os

from dayu_widgets import MLabel
from dayu_widgets import MTheme
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2.QtCore import Signal
from PySide2.QtCore import Qt
from functools import partial
from Libs import package

Theme = MTheme("dark")

class TableWidget(QtWidgets.QFrame):
    button_clicked = Signal(int)

    def __init__(self):
        super(TableWidget, self).__init__()
        # 左侧选项列表
        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName('TableWidget')
        self.setup_ui()
        self.set_style_sheet()

    def add_button(self):
        button_item = [u"项目", u"资产", u"关卡",  u"序列", u"镜头"]
        for index, button_data in enumerate(button_item):
            button = TableButton(button_data)
            button.left_clicked.connect(partial(self.button_clicked.emit, index))

            self.MainLayout.addWidget(button)
            self.MainLayout.addWidget(MLabel())

    def setup_ui(self):
        self.MainLayout.addWidget(MLabel())
        self.add_button()
        self.MainLayout.addStretch()

    def set_style_sheet(self):
        Theme.apply(self)
        self.setStyleSheet("#TableWidget{background-color: #333333;"
                           "border-color:#212121;"
                           "border-width:2px}")


class TableButton(QtWidgets.QLabel):
    icon_map = {u"项目": package.get("icon/project.png"),
                u"资产": package.get("icon/asset.png"),
                u"关卡": package.get("icon/shot.png"),
                u"序列": package.get("icon/sequence.png"),
                u"镜头": package.get("icon/shot.png")}

    left_clicked = Signal()

    def __init__(self, name):
        super(TableButton, self).__init__()
        self.setObjectName(name)
        self.pix = self.icon_map[name]
        self.hover_pix = "{}_hover.png".format(os.path.splitext(self.pix)[0])

        self.pix_map = QtGui.QPixmap(self.pix)

        self.setPixmap(self.pix_map)
        self.setToolTip(name)

    def enterEvent(self, event):
        super(TableButton, self).enterEvent(event)
        pix_map = QtGui.QPixmap(self.hover_pix)
        self.setPixmap(pix_map)

    def leaveEvent(self, event):
        super(TableButton, self).leaveEvent(event)
        pix_map = QtGui.QPixmap(self.pix)
        self.setPixmap(pix_map)

    def mousePressEvent(self, event):
        super(TableButton, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.left_clicked.emit()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = TableWidget()
    window.show()
    app.exec_()
