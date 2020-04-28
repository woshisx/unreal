import os
import time
def ueNode():
    UE4Editor = 'D:/UE_4.24/Engine/Binaries/Win64/UE4Editor-Cmd.exe'
    uproject = 'D:/UEPro/server/server.uproject'
    pythonscript = '//192.168.1.2/LocalShare/teamones/UnrealNode.py'
    # batContent = '"%s" "%s" -run=pythonscript -script="%s"'%(UE4Editor,uproject,pythonscript)
    batContent = '"%s" "%s" -ExecutePythonScript="%s"'%(UE4Editor,uproject,pythonscript)
    batPath = os.path.join(os.path.dirname(__file__),'excu.bat').replace('\\','/')
    with open(batPath,'w') as fb:
        fb.write(batContent)
    os.system(batPath)
ueNode()

