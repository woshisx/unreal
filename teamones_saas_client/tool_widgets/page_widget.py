# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :teamones_app_ui.py
# @Author       :LiuYang

from PySide2 import QtWidgets
from PySide2 import QtCore
import functools

from dayu_widgets import dayu_theme
from dayu_widgets.spin_box import MSpinBox
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.label import MLabel
from dayu_widgets.menu import MMenu
from dayu_widgets.tool_button import MToolButton
from dayu_widgets import utils
from dayu_widgets.qt import QWidget, Qt, QHBoxLayout


class PageWidget(QtWidgets.QFrame):
    def __init__(self):
        super(PageWidget, self).__init__()
        self.setObjectName("PageWidget")
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.page = MPage()

        self.setup_ui()
        self.set_style_sheet()

    def setup_ui(self):
        self.MainLayout.addWidget(self.page)

    def set_page(self, page_total=255):
        self.page.set_total(page_total)

    def set_style_sheet(self):
        self.setStyleSheet("border-width:0px")
        self.page.setStyleSheet("color: #FFFFFF; font: 14px '微软雅黑'")


class MPage(QWidget, MFieldMixin):
    """
    MPage
    A long list can be divided into several pages by MPage,
    and only one page will be loaded at a time.
    """
    sig_page_changed = QtCore.Signal(int, int)

    def __init__(self, parent=None):
        super(MPage, self).__init__(parent)
        self.index = 0
        self.register_field('page_size_selected', 25)

        self.register_field('page_size_list',
                            [{'label': '25 - Fastest', 'value': 25},
                             {'label': '50 - Fast', 'value': 50},
                             {'label': '75 - Medium', 'value': 75},
                             {'label': '100 - Slow', 'value': 100}])

        self.register_field('total', 0)
        self.register_field('current_page', 0)
        self.register_field('total_page',
                            lambda: utils.get_total_page(self.field('total'),
                                                         self.field('page_size_selected')))
        self.register_field('total_page_text',
                            lambda: str(self.field('total_page')))
        self.register_field('display_text',
                            lambda: utils.get_page_display_string(self.field('current_page'),
                                                                  self.field('page_size_selected'),
                                                                  self.field('total')))
        self.register_field('can_pre',
                            lambda: self.field('current_page') > 1)
        self.register_field('can_next',
                            lambda: self.field('current_page') < self.field('total_page'))
        page_setting_menu = MMenu(parent=self)

        self._display_label = MLabel()
        self._display_label.setAlignment(Qt.AlignCenter)
        self._change_page_size_button = MComboBox().small()
        self._change_page_size_button.setFixedWidth(110)
        self._change_page_size_button.set_menu(page_setting_menu)
        self._change_page_size_button.set_formatter(lambda x: u'{} per page'.format(x))
        # self._change_page_size_button.sig_value_changed.connect(self._emit_page_changed)

        self._pre_button = MToolButton().icon_only().svg('left_fill.svg').small()
        self._pre_button.clicked.connect(functools.partial(self._slot_change_current_page, -1))
        self._next_button = MToolButton().small().icon_only().svg('right_fill.svg')
        self._next_button.clicked.connect(functools.partial(self._slot_change_current_page, 1))
        self._current_page_spin_box = MSpinBox()
        self._current_page_spin_box.setMinimum(1)
        self._current_page_spin_box.set_dayu_size(dayu_theme.small)
        # self._current_page_spin_box.valueChanged.connect(self._emit_page_changed)
        self._total_page_label = MLabel()

        self.bind('page_size_list', page_setting_menu, 'data')
        self.bind('page_size_selected', page_setting_menu, 'value', signal='sig_value_changed')
        self.bind('page_size_selected', self._change_page_size_button, 'value',
                  signal='sig_value_changed')
        self.bind('current_page', self._current_page_spin_box, 'value', signal='valueChanged')
        self.bind('total_page', self._current_page_spin_box, 'maximum')
        self.bind('total_page_text', self._total_page_label, 'dayu_text')
        self.bind('display_text', self._display_label, 'dayu_text')
        self.bind('can_pre', self._pre_button, 'enabled')
        self.bind('can_next', self._next_button, 'enabled')

        main_lay = QHBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(2)
        main_lay.addStretch()
        main_lay.addWidget(self._display_label)
        main_lay.addStretch()
        main_lay.addWidget(self._pre_button)
        page_label = QtWidgets.QLabel('Page')
        page_label.setStyleSheet("font-weight:normal;\nfont-size: 12px '微软雅黑'")
        main_lay.addWidget(page_label)
        main_lay.addWidget(self._current_page_spin_box)
        main_lay.addWidget(MLabel('/'))
        main_lay.addWidget(self._total_page_label)
        main_lay.addWidget(self._next_button)
        self.setLayout(main_lay)

    def set_total(self, value):
        """Set page component total count."""
        self.set_field('total', value)

    def _slot_change_current_page(self, offset):
        self.set_field('current_page', self.field('current_page') + offset)
        self._emit_page_changed()

    def set_page_config(self, data_list):
        """Set page component per page settings."""
        self.set_field('page_size_list',
                       [{'label': str(data), 'value': data} if isinstance(data, int) else data for
                        data in data_list])

    def _emit_page_changed(self):
        self.sig_page_changed.emit(self.field('current_page'), self.field('page_size_selected'),)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    page = PageWidget()
    page.set_page()
    page.show()
    app.exec_()


