# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :work_widget.py
# @Author       :LiuYang
import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from functools import partial


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
    def __init__(self):
        super(FileListWidget, self).__init__()
        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.work_list = ListView([u"打开文件", u"打开目录"])

        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(dy.MDivider("Work File"))
        self.MainLayout.addWidget(self.work_list)


class ListView(dy.MListView):
    action_clicked = QtCore.Signal(str)

    def __init__(self, menu_data):
        super(ListView, self).__init__()
        self.menu = None
        self.menu_data = menu_data

    def set_menu(self):
        menu = dy.MMenu()
        for action_text in self.menu_data:
            action = menu.addAction(action_text)
            action.triggered.connect(partial(self.action_clicked.emit, action_text))

        return menu

    def mousePressEvent(self, event):
        super(ListView, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
            self.menu = self.set_menu()
            self.menu.show()
            self.menu.move(QtGui.QCursor.pos())


if __name__ == '__main__':
    # import time
    # from teamones_api import teamnoes
    #
    # tm = teamnoes.TeamOnes(base_url="http://10.168.30.17:18101", username="18107414338", password="123456")
    #
    # user = tm.get_user_info()["user"]["name"]
    # asset_user = tm.user.find_all()
    # start_time = time.time()
    #
    # tasks = tm.task.find_all(filters=[["project_id", "is", 1], ["entity_module_id", "is", 43]], page=[1, 25])
    #
    # data_list = []
    #
    # start_time = time.time()
    #
    # while True:
    #     try:
    #         task = next(tasks["entity"])
    #
    #         task_data = {"task_id": task.id,
    #                      "task_name": task.name,
    #                      "status": task.task_status,
    #                      "status_list": [u"未开始", u"已就绪", u"已取消", u"进行中", u"审核中", u"反馈", u"已完成"],
    #                      "man_hour": task.man_hour,
    #                      "executor": u"刘阳",
    #                      "plan_start_time": task.plan_start_time,
    #                      "plan_end_time": task.plan_end_time}
    #
    #         asset = tm.asset.find_one(filters=[["id", "is", task.entity_id]])
    #
    #         task_data.update({"asset_name": asset.name,
    #                           "asset_category": asset.asset_category,
    #                           "asset_grade": asset.asset_grade})
    #
    #         data_list.append(task_data)
    #     except StopIteration:
    #         break
    #
    # end_time = time.time()
    # print end_time - start_time
    # data_list = File.File(package.get("Data/TempData.yaml")).read_data_from_file()
    theme = dy.MTheme("light")
    app = QtWidgets.QApplication([])
    window = WorkWidget()
    theme.apply(window)
    window.show()
    app.exec_()
