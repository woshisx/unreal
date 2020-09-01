# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :task_info_widget.py
# @Author       :LiuYang


import dayu_widgets as dy

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from functools import partial
from Libs import package
import os

from dayu_widgets.mixin import stacked_animation_mixin

Theme = dy.MTheme("datk")


class TaskInfoWidget(QtWidgets.QFrame):
    def __init__(self):
        super(TaskInfoWidget, self).__init__()
        self.task_id = None

        self.setObjectName("TaskInfoWidget")
        self.setStyleSheet("background-color:#333333")

        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.LeftWidget = HideWidget()

        self.RightLayout = QtWidgets.QVBoxLayout()
        self.RightLayout.setContentsMargins(0, 10, 0, 10)
        self.EntityLabel = QtWidgets.QLabel()
        self.EntityLabel.setStyleSheet("color: #cccccc; font-weight:Bold;\n font-size:32px '微软雅黑'")
        self.TaskLabel = QtWidgets.QLabel()
        self.TaskLabel.setStyleSheet("color: #cccccc; font-size:20px '微软雅黑'")

        self.setFixedWidth(400)
        self.menu = Menu()

        self.menuStack = StackedWidget()
        self.menuStack.setStyleSheet("width:0px")
        self.infoWidget = TaskInfo()

        self.feedbackWidget = QtWidgets.QWidget()
        self.existingVersionWidget = WorkWidget()
        self.publishVersionWidget = PublishWidget()

        self.buttonLayout = QtWidgets.QHBoxLayout(self)

        self.start_task_button = dy.MPushButton(u"开始任务").primary()
        self.start_task_button.setMinimumWidth(160)

        self.publish_task_button = dy.MPushButton(u"发布版本").success()
        self.publish_task_button.setMinimumWidth(160)

        self.publish_task_button.hide()

        self.setup_ui()
        self.connect_ui()
        self.set_theme()

    def connect_ui(self):
        self.menu.menu_click.connect(self.switch_stack)

    def setup_ui(self):
        self.MainLayout.addWidget(self.LeftWidget)
        self.MainLayout.addLayout(self.RightLayout)

        self.RightLayout.addWidget(self.EntityLabel)
        self.RightLayout.addWidget(self.TaskLabel)

        self.RightLayout.addWidget(QtWidgets.QLabel())
        horizontal_line = dy.MDivider()
        horizontal_line.setMaximumHeight(2)
        self.RightLayout.addWidget(horizontal_line)
        self.RightLayout.addWidget(self.menu)
        horizontal_line = dy.MDivider()
        horizontal_line.setMaximumHeight(2)
        self.RightLayout.addWidget(horizontal_line)
        self.RightLayout.addWidget(self.menuStack)
        self.RightLayout.addLayout(self.buttonLayout)

        self.menuStack.addWidget(self.infoWidget)
        self.menuStack.addWidget(self.feedbackWidget)
        self.menuStack.addWidget(self.existingVersionWidget)
        self.menuStack.addWidget(self.publishVersionWidget)

        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.start_task_button)
        self.buttonLayout.addWidget(self.publish_task_button)
        self.buttonLayout.addStretch()

    def set_theme(self):
        theme = dy.MTheme("dark")
        theme.apply(self.start_task_button)
        theme.apply(self.publish_task_button)

    def switch_stack(self, index):
        if index == 3:
            self.start_task_button.hide()
            self.publish_task_button.show()
        else:
            self.start_task_button.show()
            self.publish_task_button.hide()

        self.menuStack.setCurrentIndex(index)

    def set_widget_data(self, index, data, path_data):
        self.task_id = index
        entity = data[u"名称"].split("_")[0]
        task = data[u"名称"].split("_")[-1]
        self.EntityLabel.setText(entity)
        self.TaskLabel.setText(task)

        self.infoWidget.set_info(data)
        self.existingVersionWidget.fileListWidget.set_data(path_data)


class HideWidget(QtWidgets.QWidget):
    def __init__(self):
        super(HideWidget, self).__init__()
        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.MainLayout.setContentsMargins(5, 0, 0, 0)
        self.hideButton = HideLabel()
        self.MainLayout.addWidget(self.hideButton)


class HideLabel(QtWidgets.QLabel):
    left_clicked = QtCore.Signal()

    def __init__(self, text=""):
        super(HideLabel, self).__init__(text)
        self.dark_pix_map = QtGui.QPixmap(package.get("icon/right_line_dark.png"))
        self.light_pix_map = QtGui.QPixmap(package.get("icon/right_line.png"))

        self.setPixmap(self.dark_pix_map)

    def mousePressEvent(self, event):
        super(HideLabel, self).mousePressEvent(event)
        self.left_clicked.emit()

    def enterEvent(self, event):
        super(HideLabel, self).enterEvent(event)
        self.setPixmap(self.light_pix_map)

    def leaveEvent(self, event):
        super(HideLabel, self).leaveEvent(event)
        self.setPixmap(self.dark_pix_map)


@stacked_animation_mixin
class StackedWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super(StackedWidget, self).__init__()


class Menu(QtWidgets.QWidget):
    MenuData = [u"任务详情", u"反馈", u"现有版本", u"发布版本"]
    menu_click = QtCore.Signal(int)

    def __init__(self):
        super(Menu, self).__init__()
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.set_menu()
        self.set_theme()

    def set_menu(self):
        for index, menu_item in enumerate(self.MenuData):
            menu = MenuItem(menu_item, index)
            self.MainLayout.addWidget(menu)
            menu.itemLabel.left_clicked.connect(partial(self.menu_clicked, index, menu))

    def menu_clicked(self, index, menu):
        self.clean_style_sheet()
        menu.itemLabel.setStyleSheet("color:#1890FF")
        menu.itemLine.setStyleSheet("color:#1890FF")
        self.menu_click.emit(index)

    def clean_style_sheet(self):
        for index in range(self.MainLayout.count()):
            menu = self.MainLayout.itemAt(index).widget()
            menu.itemLabel.setStyleSheet("color:#D9D9D9")
            menu.itemLine.setStyleSheet("color:#D9D9D9")
            menu.itemLine.hide()

    def set_theme(self):
        theme = dy.MTheme("dark")
        theme.apply(self)


class MenuItem(QtWidgets.QWidget):

    def __init__(self, name, index):
        super(MenuItem, self).__init__()
        self.index = index
        self.setMinimumWidth(100)
        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.itemLabel = LabelButton(name)
        self.itemLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.blank = QtWidgets.QLabel()
        self.blank.setMaximumHeight(1)

        self.itemLine = dy.MDivider()
        self.itemLine.hide()

        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(self.itemLabel)
        # self.MainLayout.addWidget(self.blank)
        self.MainLayout.addWidget(self.itemLine)


class LabelButton(dy.MLabel):
    left_clicked = QtCore.Signal()

    def __init__(self,  text='', parent=None, flags=0):
        super(LabelButton, self).__init__(text, parent, flags)
        self.strong()

    def mousePressEvent(self, event):
        super(LabelButton, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.left_clicked.emit()


class TaskInfoParent(QtWidgets.QWidget):
    def __init__(self):
        super(TaskInfoParent, self).__init__()

        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.ListScrollArea = QtWidgets.QScrollArea()
        self.ListScrollArea.setMinimumHeight(350)
        self.ListScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ListScrollArea.setWidgetResizable(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.MainLayout.addWidget(self.ListScrollArea)


# 任务详情面板
class TaskInfo(TaskInfoParent):
    def __init__(self):
        """
        任务详情面板
        """
        super(TaskInfo, self).__init__()
        self.infoWidget = QtWidgets.QWidget()
        self.infoLayout = QtWidgets.QVBoxLayout(self.infoWidget)

        self.ListScrollArea.setWidget(self.infoWidget)

        self.taskLayout = QtWidgets.QVBoxLayout()

        self.taskContactLayout = QtWidgets.QHBoxLayout()

        data = [package.get("icon/user.jpg"),
                package.get("icon/know.jpg"),
                package.get("icon/aaa.jpg"),
                package.get("icon/bbb.jpg"),
                package.get("icon/ccc.jpg")
                ]

        self.set_task_icon(data)

        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(dy.MDivider())
        self.MainLayout.addLayout(self.taskLayout)

        self.taskLayout.addStretch()
        self.taskLayout.addLayout(self.taskContactLayout)
        self.taskLayout.addStretch()

        self.MainLayout.addStretch()

    def set_info(self, info_data):
        """
        :param info_data: (dick)
        :return:
        """
        self.__clean_children(self.infoLayout)

        for info_name, info_value in info_data.items():
            info_label = InfoLabel(info_name, info_value)
            self.infoLayout.addWidget(info_label)

        self.infoLayout.addStretch()

    def set_task_icon(self, icon_data):
        self.taskContactLayout.addStretch()
        for icon in icon_data:
            icon_label = TaskContactLabel(icon)
            self.taskContactLayout.addWidget(QtWidgets.QLabel())
            self.taskContactLayout.addWidget(icon_label)
        self.taskContactLayout.addStretch()

    @staticmethod
    def __clean_children(layout):
        """
        清理子控件
        :param layout:  控件Layout
        :return:
        """
        for i in range(layout.count()):
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().deleteLater()
            else:
                layout.removeItem(layout.itemAt(i))


class InfoLabel(QtWidgets.QWidget):
    def __init__(self, info_name, info_value):
        super(InfoLabel, self).__init__()
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.infoNameLabel = QtWidgets.QLabel(info_name)
        self.infoValueLabel = QtWidgets.QLabel(info_value)

        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.MainLayout.addWidget(self.infoNameLabel)
        self.MainLayout.addStretch()
        self.MainLayout.addWidget(self.infoValueLabel)

    def set_style_sheet(self):
        self.setStyleSheet("color: #cccccc; font-weight:normal;\nfont-size: 12px '微软雅黑'")


class TaskContactLabel(QtWidgets.QLabel):
    left_clicked = QtCore.Signal()

    def __init__(self, icon):
        """
        任务信息
        :param icon:
        """
        super(TaskContactLabel, self).__init__()

        self.pix_map = self.__set_pix_map(icon)
        self.setPixmap(self.pix_map.scaled(50, 50))

    def __set_pix_map(self, pix):
        pix_map_a = QtGui.QPixmap(pix)
        pix_map = QtGui.QPixmap(200, 200)
        pix_map.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pix_map)
        painter.begin(self)  # 要将绘制过程用begin(self)和end()包起来
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)  # 一个是平滑，一个是缩放保持比例
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, 200, 200)  # 绘制椭圆
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, 200, 200, pix_map_a)
        painter.end()

        return pix_map

    def enterEvent(self, event):
        super(TaskContactLabel, self).enterEvent(event)
        self.setPixmap(self.pix_map.scaled(60, 60))

    def leaveEvent(self, event):
        super(TaskContactLabel, self).leaveEvent(event)
        self.setPixmap(self.pix_map.scaled(50, 50))

    def mousePressEvent(self, event):
        super(TaskContactLabel, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            # TODO: 点击发送信息
            self.left_clicked.emit()

# 任务反馈面板


# 现有版本面板
class WorkWidget(QtWidgets.QWidget):
    def __init__(self):
        super(WorkWidget, self).__init__()
        self.setObjectName("Work")
        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.fileListWidget = FileListWidget()
        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(self.fileListWidget)


class FileListWidget(QtWidgets.QWidget):
    view_heard = [{'label': 'Name', 'key': 'name', 'searchable': True},
                  {'label': 'path', 'key': 'path', 'searchable': True}]

    def __init__(self):
        super(FileListWidget, self).__init__()
        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)

        self.work_list = ListView()

        self.model = dy.MTableModel()
        self.model.set_header_list(self.view_heard)
        self.model_sort = dy.MSortFilterModel()
        self.model_sort.setSourceModel(self.model)

        self.work_list.set_header_list(self.view_heard)
        self.model_sort.set_header_list(self.view_heard)
        self.work_list.setModel(self.model_sort)

        self.setup_ui()

        theme = dy.MTheme("dark")
        theme.apply(self)

    def setup_ui(self):
        self.MainLayout.addWidget(self.work_list)

    def set_data(self, data):
        self.model.set_data_list(data)


class ListView(dy.MListView):
    action_clicked = QtCore.Signal(str)

    def __init__(self):
        super(ListView, self).__init__()
        self.menu = None
        self.menu_data = None

    def set_menu(self, menu_data):
        self.menu_data = menu_data

    def _set_action(self):
        menu = dy.MMenu()
        for action_text in self.menu_data:
            action = menu.addAction(action_text)
            action.triggered.connect(partial(self.action_clicked.emit, action_text))

        return menu

    def mousePressEvent(self, event):
        super(ListView, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
            self.menu = self._set_action()
            self.menu.show()
            self.menu.move(QtGui.QCursor.pos())


# 发布任务面板
class PublishWidget(TaskInfoParent):
    def __init__(self):
        super(PublishWidget, self).__init__()
        self.publishLayout = QtWidgets.QVBoxLayout(self.ListScrollArea)

        self.mediaButton = dy.MDragFileButton()
        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.publishLayout.addWidget(self.mediaButton)

    def set_style_sheet(self):
        Theme.apply(self.mediaButton)


if __name__ == "__main__":
    task_info = {u"编号": "52654",
                 u"名称": u"测试任务",
                 u"编码": "test_task",
                 u"优先级": u"正常",
                 u"开始时间": "",
                 u"结束时间": ""}

    app = QtWidgets.QApplication([])
    log = TaskInfoWidget()
    log.show()
    app.exec_()
