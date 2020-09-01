# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :teamones_app_ui.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from tool_widgets import table_widget
from tool_widgets import project_preview_widget
from tool_widgets import task_preview_widget
from tool_widgets import task_info_widget
from tool_widgets import project_info_widget
from Libs import package

Theme = dy.MTheme("dark")


class TeamonesUI(QtWidgets.QWidget):
    def __init__(self):
        super(TeamonesUI, self).__init__()
        self.setObjectName('Teamones_Tool')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        self.setGeometry(150, 50, 1570, 800)

        self.MainLayout = QtWidgets.QVBoxLayout(self, spacing=6)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)

        # menu 模块
        self.menuWidget = ToolMenu()

        self.informationLayout = QtWidgets.QHBoxLayout()

        self.tableWidget = table_widget.TableWidget()

        self.mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.stackedWidget = QtWidgets.QStackedWidget()

        # 项目面板
        self.projectWidget = project_preview_widget.ProjectPreviewWidget()

        # 任务信息面板
        self.informationWidget = task_preview_widget.TaskPreviewWidget()

        # 工作侧边栏
        self.taskSideWidget = task_info_widget.TaskInfoWidget()
        self.taskSideWidget.hide()

        # 项目侧边栏
        self.projectSideWidget = project_info_widget.ProjectInfoWidget()
        self.projectSideWidget.hide()

        self.menu = dy.MMenu()
        self.executor_menu = self.menu.addMenu("修改执行人")
        self.status_menu = self.menu.addMenu("修改任务状态")

        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.MainLayout.addWidget(self.menuWidget)

        self.MainLayout.addLayout(self.informationLayout)

        self.informationLayout.addWidget(self.tableWidget)

        self.informationLayout.addWidget(self.mainSplitter)

        self.informationLayout.addWidget(self.taskSideWidget)
        self.informationLayout.addWidget(self.projectSideWidget)

        self.mainSplitter.addWidget(self.stackedWidget)

        self.stackedWidget.addWidget(self.projectWidget)
        self.stackedWidget.addWidget(self.informationWidget)

    # 实现拖拽移动窗口
    def mousePressEvent(self, event):
        super(TeamonesUI, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def set_style_sheet(self):
        self.setStyleSheet("#Teamones_Tool{background-color: #3A3A3A}")

        Theme.apply(self.mainSplitter)
        Theme.apply(self.stackedWidget)


class ToolMenu(QtWidgets.QFrame):
    def __init__(self):
        super(ToolMenu, self).__init__()
        self.setObjectName("Menu")

        self.menuLayout = QtWidgets.QHBoxLayout(self)

        self.userAvatar = UserAvatar().huge()
        user_pix = self.__set_pix_map(QtGui.QPixmap(package.get("icon/user.jpg")))
        self.userAvatar.set_dayu_image(user_pix)
        self.userLabel = dy.MLabel("").h4()
        self.userLabel.setAlignment(QtCore.Qt.AlignTop)

        self.projectLabel = QtWidgets.QLabel()
        self.projectLabel.setStyleSheet("color: #cccccc; font-weight:Bold;\n font-size:30px '微软雅黑'")
        
        self.hideButton = dy.MPushButton("", dy.qt.MIcon('minus_line.svg', '#ddd')).small()
        self.hideButton.setFlat(True)

        self.closeButton = dy.MPushButton("", dy.qt.MIcon('close_line.svg', '#ddd')).small().warning()
        self.closeButton.setFlat(True)

        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.menuLayout.addWidget(self.userAvatar)
        self.menuLayout.addWidget(self.userLabel)

        self.menuLayout.addStretch()
        self.menuLayout.addWidget(self.projectLabel)
        self.menuLayout.addStretch()

        self.menuLayout.addWidget(dy.MLabel())
        self.menuLayout.addWidget(self.hideButton)
        self.menuLayout.addWidget(dy.MLabel(" "))
        self.menuLayout.addWidget(self.closeButton)

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

    def set_style_sheet(self):
        self.setStyleSheet("#Menu{background-color:#323232}")
        self.userAvatar.setStyleSheet("border-radius:5px; border-width:10px")
        Theme.apply(self.userAvatar)
        Theme.apply(self.userLabel)
        Theme.apply(self.hideButton)
        Theme.apply(self.closeButton)


class UserAvatar(dy.MAvatar):
    def __init__(self):
        super(UserAvatar, self).__init__()
        self.menu = dy.MMenu()

        self.logout_menu = self.menu.addAction(u"登出")
        self.info_menu = self.menu.addAction(u"个人详细信息")

        self.menu.setStyleSheet("MMenu{\n font-size:13px '微软雅黑'}")

    def mousePressEvent(self, event):
        super(UserAvatar, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.menu.show()
            self.menu.move(QtGui.QCursor.pos())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # log = ToolMenu()
    log = TeamonesUI()
    log.show()
    app.exec_()
