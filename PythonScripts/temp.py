import os
import time
def ueNode():
    UE4Editor = 'D:/Program Files/UE_4.24/Engine/Binaries/Win64/UE4Editor-Cmd.exe'
    uproject = 'C:/Users/chenxing/Documents/Unreal Projects/server/server.uproject'
    pythonscript = 'C:/Users/chenxing/PycharmProjects/UnrealPython/PythonScripts/UnrealNode.py'
    # batContent = '"%s" "%s" -run=pythonscript -script="%s"'%(UE4Editor,uproject,pythonscript)
    batContent = '"%s" "%s" -ExecutePythonScript="%s"'%(UE4Editor,uproject,pythonscript)
    batPath = os.path.join(os.path.dirname(__file__),'excu.bat').replace('\\','/')
    with open(batPath,'w') as fb:
        fb.write(batContent)
    os.system(batPath)

def mayaNode():
    mayapy = 'C:/Program Files/Autodesk/Maya2015/bin/mayapy.exe'
    pythonscript = 'C:/Users/chenxing/PycharmProjects/qt/server/maya_excute_02.py'
    batContent = '"%s" "%s"'%(mayapy,pythonscript)
    batPath = os.path.join(os.path.dirname(__file__), 'excu.bat').replace('\\', '/')
    with open(batPath, 'w') as fb:
        fb.write(batContent)
    os.system(batPath)
ueNode()

