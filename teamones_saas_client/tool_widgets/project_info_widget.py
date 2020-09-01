# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :project_information_widget.py
# @Author       :LiuYang
import dayu_widgets as dy
from PySide2 import QtWidgets
from collections import OrderedDict

Theme = dy.MTheme("dark")


class ProjectInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ProjectInfoWidget, self).__init__()
        self.MainLayout = QtWidgets.QVBoxLayout(self)

        self.BasicInformationLabel = dy.MLabel(u"基础信息").h3()
        self.BasicInformationLayout = QtWidgets.QVBoxLayout()

        self.DeliveryInformationLabel = dy.MLabel(u"交付信息").h3()

        self.DeliveryInformationLayout = QtWidgets.QVBoxLayout()

        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.MainLayout.addWidget(self.BasicInformationLabel)
        self.MainLayout.addLayout(self.BasicInformationLayout)
        self.MainLayout.addWidget(self.DeliveryInformationLabel)
        self.MainLayout.addLayout(self.DeliveryInformationLayout)

    def set_project_data(self, project_data):

        basic_info = OrderedDict()
        basic_info[u"项目名称:"] = project_data.name
        basic_info[u"项目状态:"] = project_data.project_status
        basic_info[u"描述:"] = project_data.duration

        for info_name, info_value in basic_info.items():
            basic_info_label = InfoLabel(info_name, info_value)
            self.BasicInformationLayout.addWidget(basic_info_label)

        delivery_info = OrderedDict()
        delivery_info[u"交付时间"] = project_data.delivery_time
        delivery_info[u"交付平台"] = project_data.delivery_platform
        delivery_info[u"集数"] = project_data.episodes
        delivery_info[u"帧率"] = project_data.rate
        delivery_info[u"分辨率"] = project_data.resolution

        for info_name, info_value in delivery_info.items():
            delivery_info_label = InfoLabel(info_name, info_value)
            self.DeliveryInformationLayout.addWidget(delivery_info_label)

    def set_style_sheet(self):
        Theme.apply(self)


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
        self.setStyleSheet("color: #cccccc; font-weight:normal;\nfont-size: 14px '微软雅黑'")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    Alert_Example = ProjectInfoWidget()
    Alert_Example.show()
    app.exec_()
