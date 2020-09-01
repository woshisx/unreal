# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from functools import partial


class Menu(QWidget):
    item_clicked = Signal(str)

    def __init__(self, parent):
        """
        构建menu
        :param parent: 父对象
        """
        super(Menu, self).__init__()
        self.parent = parent
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)

        self.set_style_sheet()

    def add_menu(self, menu_data):
        """
        添加menu 菜单
        :param menu_data: (dict) {name_a: icon_a, name_b: icon_b}
        :return:
        """
        for menu_name, menu_icon in menu_data.items():
            menu_item = dy.MPushButton(menu_name, icon=dy.qt.MIcon(menu_icon)).tiny()
            menu_item.clicked.connect(partial(self.clicked_signal, menu_name))
            self.MainLayout.addWidget(menu_item)

    def clicked_signal(self, item_name):
        """
        发送点击信号
        :param item_name:
        :return:
        """
        self.item_clicked.emit(item_name)

    def set_style_sheet(self, theme="dark"):
        """
        设置 styleSheet
        :param theme:  (str) theme of dy widget
        :return:
        """

        widget_theme = dy.MTheme(theme=theme)
        widget_theme.apply(self)


if __name__ == '__main__':
    from PySide2 import QtWidgets
    menu = Menu("a")
    data = {"导入maya": "", "导入sp": "", "打开ZB": ""}
    app = QtWidgets.QApplication([])
    menu.add_menu(data)
    menu.show()
    app.exec_()
