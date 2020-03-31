# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMenu,\
    QAction

class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.labelInfo = QLabel(self)
        self.button = QPushButton(u'带按钮的菜单', self)
        layout.addWidget(self.labelInfo)
        layout.addWidget(self.button)

        # 添加菜单
        self._initMenu()

    def _initMenu(self):
        # 创建菜单
        self._menu = QMenu(self.button)
        # 替换menu的鼠标释放事件达到选择性不关闭菜单
        self._menu.mouseReleaseEvent = self._menu_mouseReleaseEvent
        self._menu.addAction(u'菜单1', self._checkAction)
        self._menu.addAction(u'菜单2', self._checkAction)
        self._menu.addAction(
            QAction(u'菜单3', self._menu, triggered=self._checkAction))
        action = QAction(u'菜单4', self._menu, triggered=self._checkAction)
        # 添加自定义的属性,判断该属性可以关闭菜单
        action.setProperty('canHide', True)
        self._menu.addAction(action)
        for action in self._menu.actions():
            # 循环设置可勾选
            action.setCheckable(True)
        self.button.setMenu(self._menu)

    def _menu_mouseReleaseEvent(self, event):
        action = self._menu.actionAt(event.pos())
        if not action:
            # 没有找到action就交给QMenu自己处理
            return QMenu.mouseReleaseEvent(self._menu, event)
        if action.property('canHide'):  # 如果有该属性则给菜单自己处理
            return QMenu.mouseReleaseEvent(self._menu, event)
        # 找到了QAction则只触发Action
        action.activate(action.Trigger)

    def _checkAction(self):
        # 三个action都响应该函数
        self.labelInfo.setText('\n'.join([u'{}\t选中：{}'.format(
            action.text(), action.isChecked()) for action in self._menu.actions()]))


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, 'text')
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.resize(400, 400)
    w.show()
    sys.exit(app.exec_())