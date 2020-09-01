# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :information_widget.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from tool_widgets import search_widget
from tool_widgets import page_widget
from Libs import File
from Libs import package


class TaskPreviewWidget(QtWidgets.QFrame):
    executor_search = QtCore.Signal(str)
    status_search = QtCore.Signal(str)
    type_search = QtCore.Signal(str)
    search = QtCore.Signal(str)

    def __init__(self):
        super(TaskPreviewWidget, self).__init__()

        self.setObjectName("InformationWidget")

        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.model = dy.MTableModel()

        self.sortModel = dy.MSortFilterModel()
        self.sortModel.setSourceModel(self.model)

        self.searchWidget = search_widget.SearchWidget()

        self.task_table = TaskTable()

        self.task_table.horizontalHeader().setStretchLastSection(True)

        self.task_table.setModel(self.sortModel)
        self.task_table.hideColumn(0)

        self.page_widget = page_widget.PageWidget()

        self.setup_ui()
        self.connect_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(self.searchWidget)
        self.MainLayout.addWidget(self.task_table)
        self.MainLayout.addWidget(self.page_widget)

    def set_header(self, table_headers):
        self.model.set_header_list(table_headers)
        self.sortModel.set_header_list(table_headers)
        self.task_table.set_header_list(table_headers)

    def connect_ui(self):
        self.searchWidget.excuteSearch.SearchCombobox.currentTextChanged.connect(self.executor_search.emit)

        self.searchWidget.statusSearch.SearchCombobox.currentTextChanged.connect(self.status_search.emit)

        self.searchWidget.assetTypeSearch.SearchCombobox.currentTextChanged.connect(self.type_search.emit)

        self.searchWidget.otherSearch.sig_delay_text_changed.connect(self.search.emit)

    def set_model(self, data_list):
        self.model.set_data_list(data_list)


class TaskTable(dy.MTableView):
    right_clicked = QtCore.Signal()
    data_change = QtCore.Signal(dict)
    double_click = QtCore.Signal(int)

    def __init__(self):
        super(TaskTable, self).__init__(size=dy.dayu_theme.large)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.select_data = None
        self.menu = dy.MMenu()
        self.executor_menu = self.menu.addMenu("修改执行人")
        self.status_menu = self.menu.addMenu("修改任务状态")
        self.verticalHeader().setDefaultSectionSize(33)
        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.set_style_sheet()

    def set_style_sheet(self):
        self.setStyleSheet("border-width:0px; color: #cccccc; font: 14px '微软雅黑'")

    def _get_current_row(self):
        select_item = [select_index for select_index in self.selectedIndexes()]
        return select_item

    def mousePressEvent(self, event):
        super(TaskTable, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.select_data = self._get_current_row()
        if event.button() == QtCore.Qt.RightButton:
            self.menu.show()
            self.menu.move(QtGui.QCursor.pos())

    def mouseDoubleClickEvent(self, event):
        super(TaskTable, self).mouseDoubleClickEvent(event)
        task_id = self.model().index(self.selectedIndexes()[0].row(), 0).data()
        self.double_click.emit(int(task_id))

    def dataChanged(self, *args):
        select_item = args[0]
        task_id = select_item.model().index(select_item.row(), 0).data()

        modify_data = {"task_id": task_id, "executors": None, "status": None}

        if select_item.column() == self.selectedIndexes()[-1].column():
            modify_data["executors"] = select_item.data()
        if select_item.column() == self.selectedIndexes()[-2].column():
            modify_data["status"] = select_item.data()

        self.data_change.emit(modify_data)


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
    # entity_mapping = {"asset": 43, "level": 44, "episode": 45, "Sequence": 46, "Shot": 47}
    #
    # tasks = tm.task.adv_select(filters=[["task.entity_module_id", "is", 43],
    #                                              ["task.project_id", "is", 1]],
    #                                     fields=["task.id",
    #                                             "task.name",
    #                                             "task.man_hour",
    #                                             "task.plan_start_time",
    #                                             "task.plan_end_time",
    #                                             # "task.task_status"
    #                                             "entity.name",
    #                                             "entity.json",
    #                                             # "entity.asset_category"
    #                                             "user.name"
    #                                             ],
    #                                     page=[2, 50])
    #
    # data_list = []
    #
    # while True:
    #     try:
    #         task = next(tasks["entity"])
    #
    #         task_data = {"task_id": task.task["id"],
    #                      "task_name": task.task["name"],
    #                      "status": "None",
    #                      "man_hour": task.task["man_hour"],
    #                      "executor": task.user["name"],
    #                      "plan_start_time": task.task["plan_start_time"],
    #                      "plan_end_time": task.task["plan_end_time"],
    #                      "asset_name": task.entity["name"],
    #                      "asset_category": "None",
    #                      "asset_grade": "None"
    #                      }
    #
    #         data_list.append(task_data)
    #
    #     except StopIteration:
    #         break
    #
    # print time.time() - start_time
    import sys
    data_list = File.File(package.get("Data/TempData.yaml")).read_data_from_file()
    header = File.File(package.get("Data/asset_task_fields_header.yaml")).read_data_from_file()
    theme = dy.MTheme("dark")
    app = QtWidgets.QApplication(sys.argv)
    window = TaskPreviewWidget()
    window.set_header(header)
    window.set_model(data_list)
    theme.apply(window)
    window.show()
    app.exec_()
