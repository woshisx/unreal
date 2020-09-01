# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :project_widget.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtWidgets


class ProjectPreviewWidget(QtWidgets.QFrame):
    def __init__(self):
        """
        项目浏览窗口吧
        :return:
        """
        super(ProjectPreviewWidget, self).__init__()
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.ListScrollArea = QtWidgets.QScrollArea()
        self.ListScrollArea.setWidgetResizable(True)
        self.ListScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.setObjectName('ProjectCardWidget')

        self.ProjectCardWidget = QtWidgets.QWidget()

        self.ProjectCardLayout = dy.MFlowLayout(self.ProjectCardWidget)
        self.ProjectCardLayout.setSpacing(3)
        self.ProjectCardLayout.setContentsMargins(0, 0, 0, 0)

        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(self.ListScrollArea)
        self.ListScrollArea.setWidget(self.ProjectCardWidget)

    def set_style_sheet(self):
        self.setStyleSheet("#ProjectCardWidget{background-color: #1A1A1A}")


if __name__ == '__main__':
    import sys
    sys.path.append("D:/SMWH_project/teamones_sdk")
    from teamones_api.teamnoes import TeamOnes
    # tm = TeamOnes(base_url="http://10.168.30.17:18101", username="18107414338", password="123456")
    # project = tm.project.find_all(filters=[["is_demo", "is", "no"]], fields=["id", "code", "name", "description"])

    app = QtWidgets.QApplication([])
    window = ProjectPreviewWidget()

    window.show()
    app.exec_()
