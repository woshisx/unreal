# -*- coding: utf-8 -*-
import os


def liber():
    liber_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
    liber_dir = liber_dir.replace("\\", "/")
    return liber_dir


def get(name):
    liber_dir = liber()
    package = "{0}/{1}".format(liber_dir, name)
    package = package.replace("\\", "/")
    return package


if __name__ == "__main__":
    print(get("liberPackages/aaa.png"))
