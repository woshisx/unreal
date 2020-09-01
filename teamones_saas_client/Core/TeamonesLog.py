# -*- coding: utf-8 -*-
# @Time : 2020/7/10 20:50
# @Author : LiuYang
# @email : 317431629@qq.com
# @FileName: TeamonesLog.py

# _+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+
import dayu_widgets as dy
import os
import json
import collections
import sys
sys.path.append("D:/SMWH_project/teamones_sdk")

from teamones_api.teamnoes import TeamOnes
from PySide2 import QtWidgets
from Core.Teamones_Loging_UI import TeamOnesLogUI
from Core.Teamones import TeamonesFoo


class TeamOnesLog(TeamOnesLogUI):
    
    def __init__(self):
        super(TeamOnesLog, self).__init__()
        self._teamOnes_dir = os.path.join(os.environ["TMP"], "TeamOnes")
        self._user_config = "userConfig.json"
        self._user_pix = os.path.join(self._teamOnes_dir, "user_pic.jpg")
        self._auto_login, self._user_name, self._user_password, self._url = self._init_user()
        self._create_dir()

        self.TeamOnesWindow = None
        self.theme = dy.theme.MTheme("dark", primary_color=dy.theme.MTheme.cyan)

        self.login_status = False

        if self._auto_login:
            self.login_status = self.logging()

        self._theme_apply()

    def connect_ui(self):
        """
        connect_ui
        :return:
        """
        self.loggingButton.clicked.connect(self.logging)
        super(TeamOnesLog, self).connect_ui()

    def _init_user(self):
        user_dict = collections.defaultdict(lambda: False)
        if os.path.exists(os.path.join(self._teamOnes_dir, self._user_config)):
            with open(os.path.join(self._teamOnes_dir, self._user_config), "r") as f:
                user_data = json.load(f)
                user_dict["auto_login"] = user_data["auto_login"]
                user_dict["user_name"] = user_data["user_name"]
                user_dict["user_password"] = user_data["user_password"]
                user_dict["url"] = user_data["url"]

                self.loggingNameLine.setText(user_data["user_name"])
                self.loggingPasswordLine.setText(user_data["user_password"])
                self.urlLine.setText(user_dict["url"])

            if os.path.exists(self._user_pix):
                self.avatarLabel.set_dayu_image(dy.qt.MPixmap(self._user_pix))

        return user_dict["auto_login"], user_dict["user_name"], user_dict["user_password"], user_dict["url"]

    def _create_dir(self):
        """
        create dir
        :return:
        """
        if not os.path.exists(self._teamOnes_dir):
            os.makedirs(self._teamOnes_dir)
        return True

    def _remember_user(self):
        #  todo: 是否要记录多个人的密码

        if self.rememberCheckBox.isChecked():
            user_data = {
                        "user_name": self.loggingNameLine.text(),
                        "user_password": self.loggingPasswordLine.text(),
                        "url": self.urlLine.text(),
                        "auto_login": self.autoLogging.isChecked()
                         }
            with open(os.path.join(self._teamOnes_dir, self._user_config), "w") as f:
                json.dump(user_data, f)

        return True

    def _theme_apply(self):
        self.theme.apply(self)

    def logging(self):
        if not self._user_name or not self._user_password or not self._url:
            self._user_name = self.loggingNameLine.text()
            self._user_password = self.loggingPasswordLine.text()
            self._url = self.urlLine.text()
        self._remember_user()

        try:
            print self._user_name, self._user_password

            MyTeamones = TeamOnes(base_url=self._url,
                                  username=self._user_name,
                                  password=self._user_password)

            dy.MMessage.success(u"登录成功", self)

            self.hide()

        except RuntimeError as e:
            dy.MMessage.error(u"用户不存在或密码错误", self)

        self.TeamOnesWindow = TeamonesFoo(MyTeamones)
        self.TeamOnesWindow.show()

        return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Alert_Example = TeamOnesLog()
    Alert_Example.show()
    app.exec_()
