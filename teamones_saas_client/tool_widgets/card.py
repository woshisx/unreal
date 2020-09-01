# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :card.py
# @Author       :LiuYang

from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from Libs import package


class Card(QtWidgets.QFrame):
    double_click = QtCore.Signal(int)
    left_clicked = QtCore.Signal(dict)

    def __init__(self, project_data):
        super(Card, self).__init__()
        self.setObjectName("Card")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(300, 200)
        self.project_object = project_data
        cover, title = self.__format_project_data(self.project_object)
        # image = package.get('icon/know.jpg')
        self._preview_image = QtGui.QPixmap(cover).scaled(300, 150)
        # self._preview_image = QtGui.QPixmap(image).scaled(300, 150)

        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setPixmap(self._preview_image)

        self.informationLayout = QtWidgets.QHBoxLayout()
        self.informationLayout.setContentsMargins(0, 0, 0, 0)
        # title = u"测试任务"
        self.nameLabel = QtWidgets.QLabel(title)

        self.setup_ui()
        self.set_style_sheet()

    @staticmethod
    def __format_project_data(project_data):
        title = project_data.name
        if len(title) > 8:
            title = "{}...".format(title[:5].encode("utf-8"))

        return QtGui.QPixmap(package.get('icon/know.jpg')).scaled(350, 200), title

    def setup_ui(self):
        self.MainLayout.addWidget(self.imageLabel)
        self.MainLayout.addLayout(self.informationLayout)
        self.informationLayout.addWidget(self.nameLabel)

    def set_style_sheet(self):
        self.setStyleSheet("background-color: #323232")
        self.nameLabel.setStyleSheet("font: 14pt '微软雅黑';color:#cccccc")

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: #323232")

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #2db7f5")

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.left_clicked.emit({"name": self.project_object.name, "id":self.project_object.id})

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.double_click.emit(self.project_object.id)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    Alert_Example = Card("1")
    Alert_Example.show()
    app.exec_()
