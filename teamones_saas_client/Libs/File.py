# -*- coding: utf-8 -*-
# @Time : 2020/7/3 10:02
# @Author : LiuYang
# @email : 317431629@qq.com
# @FileName: file_fun.py

# _+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+
import os
import json
import yaml


class File(object):
    def __init__(self, file_path):
        self.__path = file_path
        self.__file_type = os.path.splitext(self.__path)[-1]
        self.__parent_dir, self.__file_name = os.path.split(file_path)

    @property
    def file_path(self):
        return self.__path

    @property
    def file_type(self):
        return self.__file_type

    @property
    def parent_dir(self):
        return self.__parent_dir

    @property
    def file_name(self):
        return self.__file_name

    def write_data_to_file(self, data, write_mode="a", ):
        """
        write data to file
        :param data:
        :param write_mode:
        :return:
        """
        if self.file_type == ".txt":
            with open(self.file_path, write_mode) as f:
                f.write(data)
        elif self.file_type == ".json":
            with open(self.file_path, write_mode) as f:
                json.dump(data, f)
        elif self.file_type == ".yaml":
            with open(self.file_path, write_mode) as f:
                yaml.dump(data, f)
        return True

    def read_data_from_file(self, read_mode="r"):
        """
        read data from file
        :param read_mode
        :return: data
        """
        data = ''
        if self.file_type == ".txt":
            with open(self.file_path, read_mode) as f:
                data = f.read()
        elif self.file_type == ".json":
            with open(self.file_path, read_mode) as f:
                data = json.load(f)
        elif self.file_type == ".yaml":
            with open(self.file_path, read_mode) as f:
                data = yaml.load(f, Loader=yaml.Loader)

        return data

    def is_exist(self):
        """
        Determine if the file exists
        :return: bool
        """
        if os.path.exists(self.file_path):
            return True
        else:
            return False

    def del_file(self):
        if self.is_exist():
            os.remove(self.file_path)
            return True
        else:
            print("file doesn't exist")
            return False
