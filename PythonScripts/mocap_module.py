# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:36:44 2020

@author: yanglong
"""


import unreal
import os

class mocap:
    def modify_ue_config(self, mocap_path, mocap_part):
        section = 'CGTeamWorks'
        key_mocap_part = 'mocap_part'
        key_taskid = 'mocap_taskid'
        key_level = 'mocap_shotlevel'
        key_sequencer = 'mocap_sequencer'
        
        value_mocap_part = mocap_part
        value_taskid = '3ECA3EA3-7B0A-5B12-7CAC-41E295FA1E82'
        value_level = mocap_path + 'ShotLevel'
        value_sequencer = mocap_path + 'Sequencer'
        
        unreal.PythonCallLibrary.moidffy_config(section, key_mocap_part, value_mocap_part)
        unreal.PythonCallLibrary.moidffy_config(section, key_taskid, value_taskid)
        unreal.PythonCallLibrary.moidffy_config(section, key_level, value_level)
        unreal.PythonCallLibrary.moidffy_config(section, key_sequencer, value_sequencer)
    
    def create_level(self, shotlevel):
        unreal.EditorLevelLibrary.new_level(shotlevel)
        
    def create_directory(self, mocap_path):
        mocap_ShotLevel_path = mocap_path + 'ShotLevel'
        mocap_Sound_path = mocap_path + 'Sound'
        mocap_Sequencer_path = mocap_path + 'Sequencer'
        mocap_Animation_path = mocap_path + 'Animation'
        
        paths = []
        paths.append(mocap_ShotLevel_path)
        paths.append(mocap_Sound_path)
        paths.append(mocap_Sequencer_path)
        paths.append(mocap_Animation_path)
        
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path.decode('utf-8'))