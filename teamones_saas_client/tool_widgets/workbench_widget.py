# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :workbench_wedget.py
# @Author       :LiuYang
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import dayu_widgets as dy


class WorkBench(QtWidgets.QFrame):
    """
    个人工作台窗口
    """
    def __init__(self):
        super(WorkBench, self).__init__()
        # self.setFixedSize(300, 600)
        self.MainLayout = QtWidgets.QGridLayout(self)

        self.warningButton = TaskInfoWidget(u"警告任务", 3)
        self.feedbackButton = TaskInfoWidget(u"反馈任务", 2)
        self.todayTaskButton = TaskInfoWidget(u"今日任务", 1)
        self.weekTaskButton = TaskInfoWidget(u"本周任务", 0)
        self.dailyTaskButton = TaskInfoWidget(u"审核任务", 0)
        self.doneTaskButton = TaskInfoWidget(u"完成任务", 0)

        self.MainLayout.addWidget(self.warningButton, 0, 0)
        self.MainLayout.addWidget(self.feedbackButton, 0, 1)
        self.MainLayout.addWidget(self.todayTaskButton, 1, 0)
        self.MainLayout.addWidget(self.weekTaskButton, 1, 1)
        self.MainLayout.addWidget(self.dailyTaskButton, 2, 0)
        self.MainLayout.addWidget(self.doneTaskButton, 2, 1)

        theme = dy.MTheme("dark")
        theme.apply(self)

    def set_data(self, data):
        mapping = {"warning": self.warningButton,
                   "feedback": self.feedbackButton,
                   "today": self.todayTaskButton,
                   "this_week": self.weekTaskButton,
                   "daily": self.dailyTaskButton,
                   "done": self.doneTaskButton}

        for key, values in data.items():
            mapping[key].numLabel.setText(str(values))


class TaskInfoWidget(QtWidgets.QWidget):
    warning_level = {3: "danger", 2: "warning", 1: "secondary", 0: "null"}

    left_clicked = QtCore.Signal(str)

    def __init__(self, name, level):
        super(TaskInfoWidget, self).__init__()
        self.MainLayout = QtWidgets.QVBoxLayout(self)

        self.numLabel = dy.MLabel().h1()
        self.numLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel = QtWidgets.QLabel(name)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.numLabel.set_dayu_type(self.warning_level[level])
        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.MainLayout.addWidget(self.numLabel)
        self.MainLayout.addWidget(self.nameLabel)

    def set_style_sheet(self):
        self.nameLabel.setStyleSheet("color: #cccccc; \n font-size:16px '微软雅黑'")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print self.nameLabel.text()
            self.left_clicked.emit(self.nameLabel.text())


if __name__ == "__main__":
    import sys
    sys.path.append("D:/SMWH_project/teamones_sdk")
    from teamones_api import teamnoes
    tm = teamnoes.TeamOnes(base_url="http://10.168.30.17:18101", username="18210589458", password="123456")

    data = tm.task.get_personal_task_statistics()
    app = QtWidgets.QApplication([])
    log = WorkBench()
    log.set_data(data)
    log.show()
    app.exec_()
