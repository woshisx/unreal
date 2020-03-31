#!/usr/bin/env python
# coding=utf-8
import os,shutil
import sys
import unreal
des = unreal.SystemLibrary.get_project_content_directory()
shutil.copytree('C:/Users/chenxing/Documents/Unreal Projects/server/Content/CSXXM','%s/CSXXM'%des)
unreal.load_asset()
