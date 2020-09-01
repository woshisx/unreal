# -*- coding: utf-8 -*-
import os
from Qt.QtGui import *
import package
import stylesheet
import liberConfig


def icon_file(icon_name):
    resource_dir = package.get("liberIcon")
    _file = "%s/%s" % (resource_dir, icon_name)
    if os.path.isfile(_file):
        return _file
    return ""


def icon(icon_name):
    return QIcon(icon_file(icon_name))


def pixmap(icon_name):
    icon_path = icon_file(icon_name)
    return QPixmap(icon_path)


def qss(file_name="style.css"):
    resource_dir = package.get("liberResource")
    qss_file = "%s/qss/%s" % (resource_dir, file_name)
    return qss_file


def img_dir():
    resource_dir = package.get("liberResource")
    _dir = "%s/%s" % (resource_dir, "img")
    return _dir


def style(file_name="style.css"):
    qss_file = qss(file_name)
    options = dict(FONT_NAME=liberConfig.FONT_NAME,
                   BACKGROUND_COLOR=liberConfig.BACKGROUND_COLOR,
                   ACCENT_COLOR=liberConfig.ACCENT_COLOR,
                   IMG_DIR=img_dir())
    style_sheet = stylesheet.StyleSheet.fromPath(qss_file, options=options)
    return style_sheet.data()


if __name__ == "__main__":
    print style()