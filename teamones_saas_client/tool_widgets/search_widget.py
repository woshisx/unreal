# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :search_widget.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2 import QtCore
from functools import partial
Theme = dy.MTheme("dark")


class SearchWidget(QtWidgets.QFrame):
    def __init__(self):
        super(SearchWidget, self).__init__()
        self.setObjectName("SearchWidget")

        self.setGeometry(150, 50, 1350, 100)
        self.MainLayout = QtWidgets.QHBoxLayout(self)

        self.excuteSearch = SearchGroup(label_name=u"执行人", combobox_data=[])

        self.statusSearch = SearchGroup(label_name=u"任务状态", combobox_data=[])

        self.assetTypeSearch = SearchGroup(label_name=u"资产类型", combobox_data=[u"角色", u"道具", u"场景"])

        self.episodesSearch = SearchGroup(label_name=u"集数", combobox_data=[])
        self.episodesSearch.hide()

        self.sequenceSearch = SearchGroup(label_name=u"序列", combobox_data=[])
        self.sequenceSearch.hide()

        self.stepCategorySearch = SearchGroup(label_name=u"工序分类", combobox_data=[])

        self.otherSearch = SearchLine()
        self.otherSearch.setMinimumWidth(360)
        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(self.episodesSearch)
        self.MainLayout.addWidget(self.sequenceSearch)
        self.MainLayout.addWidget(self.assetTypeSearch)
        self.MainLayout.addWidget(self.stepCategorySearch)

        self.MainLayout.addWidget(self.excuteSearch)
        self.MainLayout.addWidget(self.statusSearch)

        self.MainLayout.addWidget(self.otherSearch)

    def change_search(self, cur_moudle):
        if cur_moudle == "sequence":
            self.episodesSearch.show()
            self.sequenceSearch.show()
            self.assetTypeSearch.hide()

        else:
            self.assetTypeSearch.show()
            self.episodesSearch.hide()
            self.sequenceSearch.hide()


class SearchGroup(QtWidgets.QWidget):
    def __init__(self, label_name, combobox_data, exclusive=False):
        super(SearchGroup, self).__init__()
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.SearchLabel = dy.MLabel(label_name)

        self.SearchCombobox = dy.MComboBox()
        self.menu = dy.MMenu(exclusive=exclusive)
        self.set_combobox(combobox_data)

        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.MainLayout.addWidget(self.SearchLabel)
        self.MainLayout.addWidget(self.SearchCombobox)

    def set_combobox(self, data):
        self.menu.set_data(data)
        self.SearchCombobox.set_menu(self.menu)

    def set_style_sheet(self):
        self.SearchLabel.setStyleSheet("color: #cccccc; font: 14px '微软雅黑'")


class SearchLine(QtWidgets.QWidget):
    sig_delay_text_changed = QtCore.Signal(str)

    def __init__(self):
        super(SearchLine, self).__init__()
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)

        self.SearchLine = dy.MLineEdit().search()
        self.SearchLine.setPlaceholderText(self.tr('Press Enter to search...'))
        self.SearchLine.returnPressed.connect(partial(self.emit_signal, self.SearchLine.text))
        self.SearchLine.textChanged.connect(self.clean_emit_signal)

        self.SearchCombobox = dy.MComboBox()
        self.SearchCombobox.set_value('name')
        self.SearchCombobox.setFixedWidth(90)
        self.option_menu = dy.MMenu()
        self.option_menu.set_separator('|')

        # todo: 可以修改menu的元素
        self.option_menu.set_data([u"name", u"code"])
        self.SearchCombobox.set_menu(self.option_menu)
        self.SearchLine.set_prefix_widget(self.SearchCombobox)
        self.SearchLine.setMinimumWidth(250)

        self.MainLayout.addWidget(self.SearchLine)

    def clean_emit_signal(self, data):
        if not data:
            self.sig_delay_text_changed.emit(data)

    def emit_signal(self, data):
        self.sig_delay_text_changed.emit(data())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    log = SearchWidget()
    Theme.apply(log)

    log.show()
    app.exec_()
