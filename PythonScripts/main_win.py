# -*- coding: utf-8 -*-
import sys,os,json
local = os.path.dirname(__file__).replace('\\','/')
cofig = json.loads(open('%s/config.json'%local).read())
public_disk = cofig.get('public_disk')
node_server = cofig.get('node_server')
globalData = []
sys.path.append('//%s/LocalShare/py27/Lib'%public_disk)
sys.path.append('//%s/LocalShare/py27/Lib/site-packages'%public_disk)
sys.path.append(os.path.dirname(__file__).replace('\\','/'))
import re,shutil,json,random,threading,socket,time,datetime,glob,base64
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.etree.ElementTree as ET
from strack_api.strack import Strack
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QSize, Property, QTimer, Qt,QThread,Signal,QUrl
from PySide2.QtGui import QColor, QPainter,QIcon,QFont,QPixmap
from PySide2.QtWidgets import QTableWidget,QTableWidgetItem,QAbstractItemView,QComboBox
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
try:
    import requests
except:
    pass
try:
    import unreal
    from import_staticmesh import StaticTextureMeshTask
except:
    pass
try:
    import pyfbsdk as fb
except:
    pass
try:
    import maya.cmds as mc
    import maya.mel as mel
except:
    pass
try:
    import mocap_module
except:
    pass
class ShotTable(QtWidgets.QMainWindow):
    def __init__(self,data):
        self.charActTpyeDict = {u'文戏':'Drama',u'动作戏':'Drama',u'武戏':'martialarts'}
        self.charMoveSpeedDict = {u'慢速': 'Slow', u'中速': 'Medium', u'快速': 'Fast', u'瞬速': 'Flash'}
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1000, 400)
        self.setWindowTitle('镜头表单')
        self.camList = data.get('shot')
        self.charList = data.get('char')
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 1000, 280))
        self.tableWidget.setObjectName("tableWidget")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(420, 320, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText('提交')
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(len(self.camList))
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(2, 60)
        self.tableWidget.setColumnWidth(3, 90)
        self.tableWidget.setColumnWidth(4, 90)
        self.tableWidget.setColumnWidth(5, 240)
        self.tableWidget.setColumnWidth(6, 150)
        self.tableWidget.setColumnWidth(7, 180)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["相机名", "开始帧", "结束帧", "角色表演类型", "角色运动速度","焦点", "镜头分类", "镜头类型"])
        self.table()
        self.pushButton.clicked.connect(self.infoSelect)
    def listFileByTimeReversed(self,path, reverse=False):
        return sorted(glob.glob(os.path.join(path, '*')),
                      key=lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(x))),
                      reverse=reverse)
    def table(self):
        for i,cam in enumerate(self.camList):
            twi = QTableWidgetItem(cam)
            twi.setFont(QFont("Times", 10, ))
            self.tableWidget.setItem(i,0,twi)
            self.tableWidget.setCellWidget(i, 1, self.frameInput())
            self.tableWidget.setCellWidget(i, 2, self.frameInput())
            self.tableWidget.setCellWidget(i, 3, self.CharacterActCombo())
            self.tableWidget.setCellWidget(i, 4, self.CharacterSpeedCombo())
            self.tableWidget.setCellWidget(i, 5, self.charWidget())
            Combo1 = self.LensTypeCombo(i)
            self.tableWidget.setCellWidget(i,6,Combo1)
            self.tableWidget.setCellWidget(i,7, self.LensitemsCombo(i))
            Combo1.currentIndexChanged.connect(self.refeshLensitemsCombo)
    def LensTypeCombo(self,index):
        cbw = QComboBox()
        for i,each in enumerate(self.listFileByTimeReversed('%s/images/LensType'%local)):
            code = os.path.basename(each).split('.')[0]
            cbw.addItem(code)
            cbw.setIconSize(QtCore.QSize(100, 100))
            icon = QIcon('%s/images/LensType/%s.png'%(local,code))
            cbw.setItemIcon(i,icon)
            cbw.setObjectName("checkBox_%s_01"%index)
        return cbw
    def LensitemsCombo(self,index):
        cbw = QComboBox()
        cbw.setIconSize(QtCore.QSize(100, 100))
        cbw.setObjectName("checkBox_%s_02" % index)
        for i, each in enumerate(self.listFileByTimeReversed('%s/images/SCU' % (local))):
            code = os.path.basename(each).split('.')[0]
            cbw.addItem(code)
            icon = QIcon('%s/images/SCU/%s.png' % (local,code))
            cbw.setItemIcon(i, icon)
        return cbw
    def refeshLensitemsCombo(self):
        Combo1 = self.sender()
        index = Combo1.objectName().split('_')[1]
        Combo2 = self.findChild(QComboBox,"checkBox_%s_02"%index)
        shotType = Combo1.currentText()
        Combo2.clear()
        for i, each in enumerate(self.listFileByTimeReversed('%s/images/%s' % (local,shotType))):
            code = os.path.basename(each).split('.')[0]
            Combo2.addItem(code)
            icon = QIcon('%s/images/%s/%s.png' % (local,shotType, code))
            Combo2.setItemIcon(i, icon)
    def LightTypeCombo(self):
        cbw = QComboBox()
        for i,each in enumerate(self.listFileByTimeReversed('%s/images/LightType'%local)):
            code = os.path.basename(each).split('.')[0]
            cbw.addItem(code)
            cbw.setIconSize(QtCore.QSize(150, 150))
            icon = QIcon('%s/images/LightType/%s.png'%(local,code))
            cbw.setItemIcon(i,icon)
        return cbw
    def CharacterSpeedCombo(self):
        cbw = QComboBox()
        cbw.addItem('慢速')
        cbw.addItem('中速')
        cbw.addItem('快速')
        cbw.addItem('瞬速')
        return cbw
    def CharacterActCombo(self):
        cbw = QComboBox()
        cbw.addItem('文戏')
        cbw.addItem('动作戏')
        cbw.addItem('武戏')
        return cbw
    def frameInput(self):
        sb = QtWidgets.QSpinBox()
        sb.setRange(0, 10000)
        sb.setValue(0)
        sb.setDisplayIntegerBase(10)
        sb.setSingleStep(1)
        return sb
    def charWidget(self):
        QHLayoutWidget = QtWidgets.QWidget()
        QHLayoutWidget.setGeometry(QtCore.QRect(300, 150, 0, 0))
        QHLayoutWidget.setObjectName("QHLayoutWidget")
        QHLayout = QtWidgets.QHBoxLayout(QHLayoutWidget)
        QHLayout.setContentsMargins(0, 0, 0, 0)
        QHLayout.setObjectName("QHLayout")
        for item in self.charList:
            checkBox = QtWidgets.QCheckBox(QHLayoutWidget)
            checkBox.setText(item)
            QHLayout.addWidget(checkBox)
        return QHLayoutWidget
    def infoSelect(self):
        info = []
        for i in range(0,self.tableWidget.rowCount()):
            temp = {}
            temp['shot'] = self.tableWidget.item(i,0).text()
            temp['StartFrame'] = self.tableWidget.cellWidget(i, 1).value()
            temp['EndFrame'] = self.tableWidget.cellWidget(i, 2).value()
            print(type(self.tableWidget.cellWidget(i, 3).currentText()))
            temp['CharactersActType'] = self.charActTpyeDict.get(self.tableWidget.cellWidget(i, 3).currentText())
            temp['CharacterMoveSpeed'] = self.charMoveSpeedDict.get(self.tableWidget.cellWidget(i, 4).currentText())
            focus = []
            for chbox in self.tableWidget.cellWidget(i, 5).findChildren(QtWidgets.QCheckBox,''):
                if chbox.checkState():
                    focus.append(chbox.text())
            temp['focus'] = focus
            temp['LensType'] = self.tableWidget.cellWidget(i, 6).currentText()
            temp['Lensitems'] = self.tableWidget.cellWidget(i, 7).currentText()
            info.append(temp)
        print(info)
        global globalData
        globalData = info

class Mobu:
    def __init__(self):
        pass
    def Match_Camera(self,CamName):
        def creatConstraint(consName):
            # consName = 'help' will return all constraint name
            cons = None
            m = fb.FBConstraintManager()
            count = m.TypeGetCount()
            consNameDict = {}
            for i in range(count):
                consNameRef = m.TypeGetName(i)
                consNameDict[consNameRef] = i
            if consName in consNameDict.keys():
                cons = m.TypeCreateConstraint(consNameDict[consName])
            if consName == 'help':
                cons = consNameDict.keys()
            return cons

        def AlignTR(pModel, pAlignTo):
            lAlignTransPos = fb.FBVector3d()
            lModelTransPos = fb.FBVector3d()
            lAlignRotPos = fb.FBVector3d()
            lModelRotPos = fb.FBVector3d()
            pAlignTo.GetVector(lAlignTransPos)
            pModel.GetVector(lModelTransPos)
            pAlignTo.GetVector(lAlignRotPos, fb.FBModelTransformationType.kModelRotation)
            pModel.GetVector(lModelRotPos, fb.FBModelTransformationType.kModelRotation)
            pModel.SetVector(lAlignTransPos)
            pModel.SetVector(lAlignRotPos, fb.FBModelTransformationType.kModelRotation)

        def CreatMarker():
            Amarker = "Exrig_SourcecameraTR"
            Bmarker = "Exrig_Roll"
            Cmarker = "Exrig_TargetcameraTR"
            Amark = fb.FBModelMarker(Amarker)
            Amark.Look = fb.FBMarkerLook.kFBMarkerLookNone
            Amark.Show = False
            Bmark = fb.FBModelMarker(Bmarker)
            Bmark.Look = fb.FBMarkerLook.kFBMarkerLookNone
            Bmark.Show = False
            Cmark = fb.FBModelMarker(Cmarker)
            Cmark.Look = fb.FBMarkerLook.kFBMarkerLookNone
            Cmark.Show = False
            Bmark.Parent = Amark
            Cmark.Parent = Bmark

        def FindByNameMobu(name, includeNamespace=True, modelsOnly=True):
            components = fb.FBComponentList()
            fb.FBFindObjectsByName(name, components, includeNamespace, modelsOnly)
            components = list(components)
            if len(components) == 0:
                components = None
            elif len(components) == 1:
                components = components[0]
            return components

        def FindAnimationNode(pParent, pName):
            lResult = None
            for lNode in pParent.Nodes:
                if lNode.Name == pName:
                    lResult = lNode
                    break
            return lResult

        def createSourceBox(sourceObj):
            sourceBox = camrelation.SetAsSource(sourceObj)
            sourceBox.UseGlobalTransforms = False
            return sourceBox

        def createTargetBox(targetObj):
            targetBox = camrelation.ConstrainObject(targetObj)
            targetBox.UseGlobalTransforms = False
            return targetBox

        def connectThem(sourceBox, sourceChannel, targetBox, targetChannel):
            OUT = FindAnimationNode(sourceBox.AnimationNodeOutGet(), sourceChannel)
            IN = FindAnimationNode(targetBox.AnimationNodeInGet(), targetChannel)
            fb.FBConnect(OUT, IN)

        # creatmarker and aligntr with sourcecamera
        CreatMarker()
        sourcemarker = FindByNameMobu('Exrig_SourcecameraTR')
        targetmarker = FindByNameMobu('Exrig_TargetcameraTR')
        sourcecamera = FindByNameMobu(CamName)
        AlignTR(sourcemarker, sourcecamera)
        sourceConstraint = creatConstraint('Parent/Child')
        sourceConstraint.Name = sourcemarker.Name + '-PC-' + sourcecamera.Name
        sourceConstraint.ReferenceAdd(0, sourcemarker)
        sourceConstraint.ReferenceAdd(1, sourcecamera)
        sourceConstraint.Weight = 100
        sourceConstraint.Active = True
        sourceConstraint.Snap()
        # creat camera forrow source
        ue4cam = fb.FBCamera(sourcecamera.Name)
        sourcecamera.Name = "Exrig_cam"
        Firstcamera = FindByNameMobu('Exrig_cam')
        ue4cam.Show = True
        ue4cam.UseFrameColor = True
        ue4cam.ViewShowTimeCode = True
        ue4cam.ViewShowGrid = True
        ue4cam.ViewDisplaySafeArea = False
        ue4cam.ApertureMode = fb.FBCameraApertureMode.kFBApertureHorizontal
        ue4cam.FilmBackType = fb.FBCameraFilmBackType.kFBFilmBack35mmFullAperture
        ue4cam.ResolutionMode = fb.FBCameraResolutionMode.kFBResolutionD1PAL
        ue4cam.PixelAspectRatio = 1.0
        ue4cam.NearPlaneDistance = 1.0
        ue4cam.FarPlaneDistance = 4000000000
        ue4cam.ResolutionHeight = Firstcamera.ResolutionHeight
        ue4cam.ResolutionWidth = Firstcamera.ResolutionWidth
        AlignTR(ue4cam, Firstcamera)
        ue4cam.FieldOfView.SetAnimated(True)
        # Pc with UEcamera
        targetcamera = FindByNameMobu(ue4cam.Name)
        targetConstraint = creatConstraint('Parent/Child')
        targetConstraint.Name = targetmarker.Name + '-PC-' + targetcamera.Name
        targetConstraint.ReferenceAdd(0, targetcamera)
        targetConstraint.ReferenceAdd(1, targetmarker)
        targetConstraint.Weight = 100
        targetConstraint.Active = True
        targetConstraint.Snap()
        # creat relation to connet source camera
        camrelation = fb.FBConstraintRelation('Exrig_camrelation')
        camrelation.Active = True
        ntvBox = camrelation.CreateFunctionBox('Converters', 'Number to Vector')
        ntvBox.Name = "Roll_Number to Vector"
        camrelation.SetBoxPosition(ntvBox, 500, 300)
        Soucam = createSourceBox(sourcecamera)
        camrelation.SetBoxPosition(Soucam, 0, 160)
        Targecam = createTargetBox(targetcamera)
        camrelation.SetBoxPosition(Targecam, 1400, 160)
        rollmarker = FindByNameMobu("Exrig_Roll")
        Targerollmarker = createTargetBox(rollmarker)
        camrelation.SetBoxPosition(Targerollmarker, 800, 500)
        connectThem(Soucam, "FieldOfView", Targecam, "FieldOfView")
        connectThem(Soucam, "Roll", ntvBox, "X")
        connectThem(ntvBox, "Result", Targerollmarker, "Lcl Rotation")
        targetcamera.Selected = True
        if targetcamera:
            myTake = fb.FBSystem().CurrentTake
            plotPeriod = fb.FBTime(0, 0, 0, 1)
            myTake.PlotTakeOnSelected(plotPeriod)
        foundComponents = fb.FBComponentList()
        includeNamespace = False
        modelsOnly = False
        fb.FBFindObjectsByName('Exrig_*', foundComponents, includeNamespace, modelsOnly)
        for cleancamera in foundComponents:
            try:
                cleancamera.FBDelete()
            except:
                pass
        ue4cam.LongName = ue4cam.Name + ":" + ue4cam.Name
    def bakeClean(self):
        def save():
            # Save options
            soptions = fb.FBFbxOptions(False)
            soptions.ShowOptionsDialog = False
            elemAction = fb.FBElementAction
            # Element options
            soptions.BaseCameras = False
            soptions.CameraSwitcherSettings = False
            soptions.CurrentCameraSettings = False
            soptions.GlobalLightingSettings = False
            soptions.TransportSettings = False
            soptions.UseASCIIFormat = False
            soptions.EmbedMedia = False
            # save selected
            soptions.SaveSelectedModelsOnly = True
            # Set the path to saveing
            fb.FBApplication().FileSave(('C:/Users/Public/Documents/temp.fbx'), soptions)
            fb.FBPlayerControl().SetTransportFps(fb.FBTimeMode.kFBTimeMode25Frames)
            fb.FBPlayerControl().SnapMode = fb.FBTransportSnapMode.kFBTransportSnapModeSnapOnFrames
        for ctake in fb.FBSystem().Scene.Takes:
            ctake.Selected = False
            ctake.Name = 'T1'
        lCurrentTakeName = fb.FBSystem().CurrentTake.Name
        if lCurrentTakeName != 'Take 001':
            ltake = lCurrentTakeName
        for take in fb.FBSystem().Scene.Takes:
            if take.Name != ltake:
                take.Selected = True
        lTakeLst = []
        for i in range(len(fb.FBSystem().Scene.Takes)):
            if fb.FBSystem().Scene.Takes[i].Selected == True:
                lTakeLst.extend([fb.FBSystem().Scene.Takes[i]])
            else:
                pass
        for dtake in lTakeLst:
            dtake.FBDelete()
        for rtake in fb.FBSystem().Scene.Takes:
            rtake.Name = 'Take 001'
        # don't select camera
        lList = fb.FBComponentList()
        parentModel = fb.FBFindObjectsByName('*', lList, False, True)
        for item in lList:
            item.Selected = True
        for camera in [c for c in fb.FBSystem().Scene.Cameras if c.SystemCamera]:
            camera.Selected = False
        for lcomp in lList:
            if lcomp.Name == 'Camera Switcher':
                lcomp.Selected = False
        # Plot Select options
        lFPS = fb.FBTime(0, 0, 0, 1, 0, fb.FBTimeMode().kFBTimeMode25Frames)
        loptions = fb.FBPlotOptions()
        loptions.PlotLockedProperties = True
        loptions.PlotPeriod = lFPS
        loptions.UseConstantKeyReducer = False
        loptions.ConstantKeyReducerKeepOneKey = True
        loptions.RotationFilterToApply = fb.FBRotationFilter.kFBRotationFilterUnroll
        currentTake = fb.FBSystem().CurrentTake
        currentTake.PlotTakeOnSelected(loptions)
        # Addnamespace to everything
        lNamespace = "1"
        for group in [group for group in fb.FBSystem().Scene.Groups]:
            group.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for wenj in [group for group in fb.FBSystem().Scene.Folders]:
            wenj.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for maps in [maps for maps in fb.FBSystem().Scene.Materials]:
            maps.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for poses in [poses for poses in fb.FBSystem().Scene.CharacterPoses]:
            poses.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for shader in [shader for shader in fb.FBSystem().Scene.Shaders]:
            shader.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for textures in [textures for textures in fb.FBSystem().Scene.Textures]:
            textures.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for face in [face for face in fb.FBSystem().Scene.CharacterFaces]:
            face.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for motion in [motion for motion in fb.FBSystem().Scene.MotionClips]:
            motion.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for videos in [videos for videos in fb.FBSystem().Scene.VideoClips]:
            videos.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for lights in [lights for lights in fb.FBSystem().Scene.Lights]:
            lights.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for IO in [IO for IO in fb.FBSystem().Scene.Devices]:
            IO.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for audio in [audio for audio in fb.FBSystem().Scene.AudioClips]:
            audio.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        for ctrlrig in [rig for rig in fb.FBSystem().Scene.ControlSets]:
            ctrlrig.ProcessObjectNamespace(fb.FBNamespaceAction.kFBConcatNamespace, lNamespace, None, False)
        # Add in to List findmatchlongname delete
        foundComponents = fb.FBComponentList()
        includeNamespace = True
        modelsOnly = False
        fb.FBFindObjectsByName('1:*', foundComponents, includeNamespace, modelsOnly)
        for ca in foundComponents:
            try:
                ca.FBDelete()
            except:
                pass
        # Face curve deleted
        exfoundComponents = fb.FBComponentList()
        includeNamespace = True
        modelsOnly = True
        fb.FBFindObjectsByName('*Exrig_*', exfoundComponents, includeNamespace, modelsOnly)
        for excomp in exfoundComponents:
            excomp.FBDelete()
        save()
    def movetake(self):
        for ctake in fb.FBSystem().Scene.Takes:
            ctake.Selected = False
            ctake.Name = 'T1'
        lCurrentTakeName = fb.FBSystem().CurrentTake.Name
        if lCurrentTakeName != 'Take 001':
            self.ltake = lCurrentTakeName
        for take in fb.FBSystem().Scene.Takes:
            if take.Name != self.ltake:
                take.Selected = True
        lTakeLst = []
        for i in range(len(fb.FBSystem().Scene.Takes)):
            if fb.FBSystem().Scene.Takes[i].Selected == True:
                lTakeLst.extend([fb.FBSystem().Scene.Takes[i]])
            else:
                pass
        for dtake in lTakeLst:
            dtake.FBDelete()
        for rtake in fb.FBSystem().Scene.Takes:
            rtake.Name = 'Take 001'
        ##Clean Up
        del (lTakeLst,lCurrentTakeName)
    def UnSelectAll(self):
        selectedModels = fb.FBModelList()
        fb.FBGetSelectedModels(selectedModels, None, True)
        for select in selectedModels:
            select.Selected = False
        del (selectedModels)
    def camExport(self,path,name):
        self.UnSelectAll()
        actionDiscard = fb.FBElementAction.kFBElementActionDiscard
        for camera in [c for c in fb.FBSystem().Scene.Cameras if not c.SystemCamera]:
            if camera.Name == name.encode('ascii'):
                camera.Selected = True
        listOfTakes = fb.FBSystem().Scene.Takes
        lFPS = fb.FBTime(0, 0, 0, 1, 0, fb.FBTimeMode().kFBTimeMode25Frames)
        plotOnEveryFrame = fb.FBTime(0, 0, 0, 1, )
        loptions = fb.FBPlotOptions()
        loptions.PlotLockedProperties = True
        loptions.PlotPeriod = lFPS
        loptions.UseConstantKeyReducer = False
        loptions.ConstantKeyReducerKeepOneKey = False
        loptions.RotationFilterToApply = fb.FBRotationFilter.kFBRotationFilterUnroll
        currentTake = fb.FBSystem().CurrentTake
        currentTake.PlotTakeOnSelected(plotOnEveryFrame)
        soptions = fb.FBFbxOptions(False)
        soptions.ShowOptionsDialog = False
        elemAction = fb.FBElementAction
        # Element options
        soptions.BaseCameras = False
        soptions.CameraSwitcherSettings = False
        soptions.CurrentCameraSettings = False
        soptions.GlobalLightingSettings = False
        soptions.TransportSettings = False
        soptions.UseASCIIFormat = False
        soptions.EmbedMedia = False
        # save selected model only
        soptions.SaveSelectedModelsOnly = True
        fb.FBApplication().FileSave('C:/Users/Public/Documents/temp.fbx', soptions)
        shutil.copyfile('C:/Users/Public/Documents/temp.fbx',path.encode('ascii'))
    def openFile(self,filePath):
        filePath = filePath.encode('ascii')
        options = fb.FBFbxOptions(True, filePath)
        actionDiscard = fb.FBElementAction.kFBElementActionDiscard
        options.BaseCameras = False
        options.CameraSwitcherSettings = False
        options.GlobalLightingSettings = False
        options.CurrentCameraSettings = False
        options.TransportSettings = False
        options.ShowOptionsDialog = False
        fb.FBApplication().FileOpen(filePath, True, options)
        del (options, filePath)
    def saveFile(self,filePath):
        filePath = filePath.encode('ascii')
        # Save options
        soptions = fb.FBFbxOptions(False)
        soptions.ShowOptionsDialog = False
        elemAction = fb.FBElementAction
        # Element options
        soptions.BaseCameras = False
        soptions.CameraSwitcherSettings = False
        soptions.CurrentCameraSettings = False
        soptions.GlobalLightingSettings = False
        soptions.TransportSettings = False
        soptions.UseASCIIFormat = False
        soptions.EmbedMedia = False
        # save selected
        soptions.SaveSelectedModelsOnly = False
        # Set the path to saveing
        fb.FBApplication().FileSave(('C:/Users/Public/Documents/temp.fbx'), soptions)
        shutil.move('C:/Users/Public/Documents/temp.fbx',filePath)
    def mergeFile(self, filePath):
        filePath = filePath.encode('ascii')
        options = fb.FBFbxOptions(True, filePath)
        actionDiscard = fb.FBElementAction.kFBElementActionDiscard
        options.BaseCameras = False
        options.CameraSwitcherSettings = False
        options.GlobalLightingSettings = False
        options.CurrentCameraSettings = False
        options.TransportSettings = False
        options.ShowOptionsDialog = False
        fb.FBApplication().FileAppend(filePath, True, options)
        fb.FBPlayerControl().SnapMode = fb.FBTransportSnapMode.kFBTransportSnapModeSnapOnFrames
        del (options, filePath)
    def replaceFile(self,filePath):
        filePath = filePath.encode('ascii')
        options = fb.FBFbxOptions(True, filePath)
        options.SetAll(fb.FBElementAction.kFBElementActionMerge, True)
        options.SetPropertyStaticIfPossible = False
        actionDiscard = fb.FBElementAction.kFBElementActionDiscard
        options.BaseCameras = False
        options.CameraSwitcherSettings = False
        options.GlobalLightingSettings = False
        options.CurrentCameraSettings = False
        options.TransportSettings = False
        options.ShowOptionsDialog = False
        for lTakeIndex in range(options.GetTakeCount()):
            options.SetTakeSelect(lTakeIndex, False)
        options.SetTakeSelect(0, False)
        fb.FBApplication().FileMerge(filePath, True, options)
        del (options, filePath)
    def exportFile(self,outPath,pro,ep,sc,seq):
        self.movetake()
        assetList = {}
        temp =[]
        for namespace in fb.FBSystem().Scene.Namespaces:
            if re.search('_moburig_',namespace.Name):
                self.UnSelectAll()
                foundComponents = fb.FBComponentList()
                fb.FBFindObjectsByName(("%s:*"%namespace.Name).encode('ascii'), foundComponents, True, True)
                for sel in foundComponents:
                    sel.Selected = True
                options = fb.FBFbxOptions(False)
                options.ShowOptionsDialog = False
                elemAction = fb.FBElementAction
                options.BaseCameras = False
                options.CameraSwitcherSettings = False
                options.CurrentCameraSettings = False
                options.GlobalLightingSettings = False
                options.TransportSettings = False
                options.UseASCIIFormat = False
                options.EmbedMedia = False
                options.SaveSelectedModelsOnly = True
                fb.FBApplication().FileSave('C:/Users/Public/Documents/temp_child.fbx', options)
                fb.FBGetSelectedModels(fb.FBModelList(), None, True)
                for model in fb.FBModelList():
                    model.Selected = False
                shutil.copyfile('C:/Users/Public/Documents/temp_child.fbx','%s/%s_%s_%s_%s_%s.fbx'%(outPath,pro,ep,sc,seq,namespace.Name))
                temp.append(namespace.Name)
                self.UnSelectAll()
        assetList['char'] = temp
        return assetList
    def findAsset(self,data,code):
        for item in data:
            if item.get('json').get('step_code')=='rig' and item.get('json').get('asset_code')==code:
                return item.get('json').get('Publish_path')
    def xml(self,item,data):
        global globalData
        self.bakeClean()
        self.openFile('C:/Users/Public/Documents/temp.fbx')
        outPath = item.get('json').get('Publish_path')
        pro = outPath.split('/')[1]
        ep = outPath.split('/')[3]
        sc = outPath.split('/')[4]
        seq = outPath.split('/')[5]
        char = self.exportFile(outPath,pro,ep,sc,seq)
        for camera in [c for c in fb.FBSystem().Scene.Cameras if not c.SystemCamera]:
            name = camera.Name
            self.Match_Camera(name)
            self.camExport('%s/%s_%s_%s_%s_%s.fbx'%(outPath,pro,ep,sc,seq,name),name)
        day = str(datetime.datetime.now())
        root = Element('TaskList', {'releaseDate': day})
        tree = ElementTree(root)
        Task = SubElement(root, 'Task')
        Task.set('Project',pro)
        Task.set('Episode', ep)
        Task.set('Sessions', sc)
        Task.set('Part', seq)
        Task.set('Type', 'layout')
        Task.set('FPS', str(fb.FBPlayerControl().GetTransportFpsValue()))
        Task.set('StartFrame', str(fb.FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()))
        Task.set('EndFrame', str(fb.FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()))
        Task.set('TaskId', item.get('uuid'))
        for each in char.get('char'):
            code = each.split('_')[0]
            version = each.split('_')[-1]
            SkeletalAnimation = SubElement(Task, 'SkeletalAnimation')
            SkeletalAnimation.set('Path', '%s/%s_%s_%s_%s_%s.fbx'%(outPath,pro,ep,sc,seq,each))
            SkeletalAnimation.set('Reference', '%s/%s_rig_%s.fbx'%(self.findAsset(data,code),code,version))
        for each in globalData:
            temp = SubElement(Task, 'Camera')
            temp.set('Path','%s/%s_%s_%s_%s_%s.fbx'%(outPath,pro,ep,sc,seq,each.get('shot')))
            temp.set('StartFrame',str(each.get('StartFrame')))
            temp.set('EndFrame', str(each.get('EndFrame')))
            temp.set('CharactersNumber', str(len(each.get('focus'))))
            temp.set('CharactersActType', each.get('CharactersActType'))
            temp.set('CharacterMoveSpeed',each.get('CharacterMoveSpeed'))
            temp.set('LensType', each.get('focus'))
            # temp.set('LightType', 'PV22_225_045')
            temp.set('name', each.get('shot'))
        tree.write(outPath + '/Description.xml', encoding='utf-8', xml_declaration=True)
    def backUp(self,path):
        if os.path.exists(path):
            dPath = os.path.dirname(path)
            file = os.path.basename(path)
            if not os.path.exists('%s/backup'%dPath):
                os.mkdir('%s/backup'%dPath)
            shutil.copyfile(path, '%s/backup/%s_%s'%(dPath,str(datetime.datetime.now()).replace(':','.'),file))
class UE:
    def __init__(self):
        pass
    def executeImportTasks(self,tasks):
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
        return [task.get_editor_property('imported_object_paths') for task in tasks]
    def buildImportTask(self,filename='', destination_path='',destination_name ='', options=None):
        task = unreal.AssetImportTask()
        task.set_editor_property('automated', True)
        task.set_editor_property('destination_name', destination_name)
        task.set_editor_property('destination_path', destination_path)
        task.set_editor_property('filename', filename)
        task.set_editor_property('replace_existing', True)
        task.set_editor_property('save', True)
        task.set_editor_property('options', options)
        return task

    def buildStaticMeshImportOptions(self):
        options = unreal.FbxImportUI()
        # unreal.FbxImportUI
        options.set_editor_property('import_mesh', True)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_as_skeletal', False)  # Static Mesh
        # unreal.FbxMeshImportData
        options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
        options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
        options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
        # unreal.FbxStaticMeshImportData
        options.static_mesh_import_data.set_editor_property('combine_meshes', True)
        options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
        options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
        return options

    def buildSkeletalMeshImportOptions(self):
        options = unreal.FbxImportUI()
        # unreal.FbxImportUI
        options.set_editor_property('import_mesh', True)
        options.set_editor_property('import_animations', False)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_as_skeletal', True)  # Skeletal Mesh
        # unreal.FbxMeshImportData
        options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
        options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
        options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
        # unreal.FbxSkeletalMeshImportData
        options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
        options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
        return options

    def buildAnimationImportOptions(self,skeleton):
        skeletal_mesh_import_data = unreal.FbxSkeletalMeshImportData()
        skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
        skeletal_mesh_import_data.set_editor_property('import_meshes_in_bone_hierarchy', True)
        skeletal_mesh_import_data.set_editor_property('use_t0_as_ref_pose', False)
        skeletal_mesh_import_data.set_editor_property('preserve_smoothing_groups', True)
        skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
        import_translation = unreal.Vector(0, 0, 0)
        skeletal_mesh_import_data.set_editor_property('import_translation', import_translation)
        import_rotation = unreal.Rotator(0, 0, 0)
        skeletal_mesh_import_data.set_editor_property('import_rotation', import_rotation)
        skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
        skeletal_mesh_import_data.set_editor_property('convert_scene', True)
        skeletal_mesh_import_data.set_editor_property('force_front_x_axis', False)
        skeletal_mesh_import_data.set_editor_property('convert_scene_unit', False)
        # skeletal_mesh_import_data.set_editor_property('combine_meshes',False)
        # skeletal_mesh_import_data.set_editor_property('remove_degenerates',True)
        # skeletal_mesh_import_data.set_editor_property('build_adjacency_buffer',True)
        skeletal_mesh_import_data.set_editor_property('normal_import_method',
                                                      unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS)

        FbxAnimSequenceImportData = unreal.FbxAnimSequenceImportData()
        FbxAnimSequenceImportData.set_editor_property('animation_length',
                                                      unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
        FbxAnimSequenceImportData.set_editor_property('import_meshes_in_bone_hierarchy', True)
        Int32Interval = unreal.Int32Interval()
        Int32Interval.set_editor_property('max', 0)
        Int32Interval.set_editor_property('min', 0)
        FbxAnimSequenceImportData.set_editor_property('frame_import_range', Int32Interval)
        FbxAnimSequenceImportData.set_editor_property('use_default_sample_rate', False)
        FbxAnimSequenceImportData.set_editor_property('import_custom_attribute', True)
        FbxAnimSequenceImportData.set_editor_property('import_bone_tracks', True)
        FbxAnimSequenceImportData.set_editor_property('set_material_drive_parameter_on_custom_attribute', False)
        FbxAnimSequenceImportData.set_editor_property('material_curve_suffixes', ['_mat'])
        FbxAnimSequenceImportData.set_editor_property('remove_redundant_keys', True)
        FbxAnimSequenceImportData.set_editor_property('delete_existing_morph_target_curves', False)
        FbxAnimSequenceImportData.set_editor_property('do_not_import_curve_with_zero', True)
        FbxAnimSequenceImportData.set_editor_property('preserve_local_transform', False)
        vector = unreal.Vector(0, 0, 0)
        FbxAnimSequenceImportData.set_editor_property('ImportTranslation', vector)
        rotator = unreal.Rotator(0, 0, 0)
        FbxAnimSequenceImportData.set_editor_property('import_rotation', rotator)
        FbxAnimSequenceImportData.set_editor_property('import_uniform_scale', 1.0)
        FbxAnimSequenceImportData.set_editor_property('convert_scene', True)
        FbxAnimSequenceImportData.set_editor_property('force_front_x_axis', False)
        FbxAnimSequenceImportData.set_editor_property('convert_scene_unit', False)
        options = unreal.FbxImportUI()
        options.set_editor_property('skeletal_mesh_import_data', skeletal_mesh_import_data)
        options.set_editor_property('anim_sequence_import_data', FbxAnimSequenceImportData)
        options.set_editor_property('import_mesh', False)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_as_skeletal', False)
        options.set_editor_property('skeleton', skeleton)
        options.set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_ANIMATION)
        options.set_editor_property('mesh_type_to_import', unreal.FBXImportType.FBXIT_ANIMATION)
        options.set_editor_property('create_physics_asset', False)
        options.set_editor_property('physics_asset', None)
        options.set_editor_property('auto_compute_lod_distances', False)
        options.set_editor_property('lod_number', 0)
        options.set_editor_property('minimum_lod_number', 0)
        options.set_editor_property('import_animations', True)
        options.set_editor_property('import_rigid_mesh', False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('override_full_name', True)
        # 没这句就自动生成skeleton mesh了
        options.set_editor_property('automated_import_should_detect_type', False)
        return options
class Thread(QThread):
    def __init__(self,fun):
        self.fun = fun
        super(Thread,self).__init__()
    def run(self):
        self.fun()
def threadWrap(fun):
    thread = Thread(fun)
    thread.start()
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 320)
        self.login_pushButton = QtWidgets.QPushButton(Form)
        self.login_pushButton.setGeometry(QtCore.QRect(100, 264, 200, 35))
        self.login_pushButton.setText("")
        self.login_pushButton.setIconSize(QtCore.QSize(195, 34))
        self.login_pushButton.setObjectName("login_pushButton")
        self.login_checkBox = QtWidgets.QCheckBox(Form)
        self.login_checkBox.setGeometry(QtCore.QRect(44, 277, 71, 16))
        self.login_checkBox.setObjectName("login_checkBox")
        self.usename_lineEdit = QtWidgets.QLineEdit(Form)
        self.usename_lineEdit.setGeometry(QtCore.QRect(101, 117, 200, 28))
        self.usename_lineEdit.setPlaceholderText("")
        self.usename_lineEdit.setObjectName("usename_lineEdit")
        self.password_lineEdit = QtWidgets.QLineEdit(Form)
        self.password_lineEdit.setGeometry(QtCore.QRect(101, 167, 200, 28))
        self.password_lineEdit.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setPlaceholderText("")
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.login_min_button = QtWidgets.QPushButton(Form)
        self.login_min_button.setGeometry(QtCore.QRect(340, 0, 27, 27))
        self.login_min_button.setText("")
        self.login_min_button.setIconSize(QtCore.QSize(23, 23))
        self.login_min_button.setObjectName("login_min_button")
        self.software_selector = QtWidgets.QComboBox(Form)
        self.software_selector.setGeometry(QtCore.QRect(101, 214, 200, 28))
        self.software_selector.setObjectName("software_selector")
        self.software_selector.addItem("")
        self.software_selector.addItem("")
        self.software_selector.addItem("")
        self.login_close_button = QtWidgets.QPushButton(Form)
        self.login_close_button.setGeometry(QtCore.QRect(370, 0, 27, 27))
        self.login_close_button.setText("")
        self.login_close_button.setIconSize(QtCore.QSize(23, 23))
        self.login_close_button.setObjectName("login_close_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.login_checkBox.setText(QtWidgets.QApplication.translate("Form", "记住", None, -1))
        self.software_selector.setItemText(0, QtWidgets.QApplication.translate("Form", "Unreal", None, -1))
        self.software_selector.setItemText(1, QtWidgets.QApplication.translate("Form", "Maya", None, -1))
        self.software_selector.setItemText(2, QtWidgets.QApplication.translate("Form", "Motionbuilder", None, -1))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.module_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.module_tab.setGeometry(QtCore.QRect(0, 33, 676, 565))
        self.module_tab.setObjectName("module_tab")
        self.Asset_tab = QtWidgets.QWidget()
        self.Asset_tab.setObjectName("Asset_tab")
        self.AssetSearchText = QtWidgets.QLineEdit(self.Asset_tab)
        self.AssetSearchText.setGeometry(QtCore.QRect(339, 0, 332, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.AssetSearchText.setFont(font)
        self.AssetSearchText.setObjectName("AssetSearchText")
        self.asset_proj_selector = QtWidgets.QComboBox(self.Asset_tab)
        self.asset_proj_selector.setGeometry(QtCore.QRect(0, 0, 90, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.asset_proj_selector.setFont(font)
        self.asset_proj_selector.setObjectName("asset_proj_selector")
        self.asset_proj_selector.addItem("")
        self.asset_treeWidget = QtWidgets.QTreeWidget(self.Asset_tab)
        self.asset_treeWidget.setGeometry(QtCore.QRect(0, 29, 674, 512))
        self.asset_treeWidget.setObjectName("asset_treeWidget")
        self.asset_type_selector = QtWidgets.QComboBox(self.Asset_tab)
        self.asset_type_selector.setGeometry(QtCore.QRect(91, 0, 85, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.asset_type_selector.setFont(font)
        self.asset_type_selector.setObjectName("asset_type_selector")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.addItem("")
        self.asset_type_selector.addItem("")
        self.asset_step_selector = QtWidgets.QComboBox(self.Asset_tab)
        self.asset_step_selector.setGeometry(QtCore.QRect(177, 0, 80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.asset_step_selector.setFont(font)
        self.asset_step_selector.setObjectName("asset_step_selector")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_step_selector.addItem("")
        self.asset_status_selector = QtWidgets.QComboBox(self.Asset_tab)
        self.asset_status_selector.setGeometry(QtCore.QRect(258, 0, 80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.asset_status_selector.setFont(font)
        self.asset_status_selector.setObjectName("asset_status_selector")
        self.asset_status_selector.addItem("")
        self.asset_status_selector.addItem("")
        self.asset_status_selector.addItem("")
        self.asset_status_selector.addItem("")
        self.asset_status_selector.addItem("")
        self.asset_status_selector.addItem("")
        self.module_tab.addTab(self.Asset_tab, "")
        self.Shot_tab = QtWidgets.QWidget()
        self.Shot_tab.setObjectName("Shot_tab")
        self.shot_proj_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_proj_selector.setGeometry(QtCore.QRect(0, 0, 90, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_proj_selector.setFont(font)
        self.shot_proj_selector.setObjectName("shot_proj_selector")
        self.shot_proj_selector.addItem("")
        self.shot_treeWidget = QtWidgets.QTreeWidget(self.Shot_tab)
        self.shot_treeWidget.setGeometry(QtCore.QRect(0, 29, 674, 512))
        self.shot_treeWidget.setObjectName("shot_treeWidget")
        self.ShotSearchText = QtWidgets.QLineEdit(self.Shot_tab)
        self.ShotSearchText.setGeometry(QtCore.QRect(411, 0, 263, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ShotSearchText.setFont(font)
        self.ShotSearchText.setObjectName("ShotSearchText")
        self.shot_episode_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_episode_selector.setGeometry(QtCore.QRect(91, 0, 78, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_episode_selector.setFont(font)
        self.shot_episode_selector.setObjectName("shot_episode_selector")
        self.shot_episode_selector.addItem("")
        self.shot_step_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_step_selector.setGeometry(QtCore.QRect(249, 0, 80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_step_selector.setFont(font)
        self.shot_step_selector.setObjectName("shot_step_selector")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_step_selector.addItem("")
        self.shot_session_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_session_selector.setGeometry(QtCore.QRect(170, 0, 78, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_session_selector.setFont(font)
        self.shot_session_selector.setObjectName("shot_session_selector")
        self.shot_session_selector.addItem("")
        self.shot_status_selector = QtWidgets.QComboBox(self.Shot_tab)
        self.shot_status_selector.setGeometry(QtCore.QRect(330, 0, 80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_status_selector.setFont(font)
        self.shot_status_selector.setObjectName("shot_status_selector")
        self.shot_status_selector.addItem("")
        self.shot_status_selector.addItem("")
        self.shot_status_selector.addItem("")
        self.shot_status_selector.addItem("")
        self.shot_status_selector.addItem("")
        self.shot_status_selector.addItem("")
        self.module_tab.addTab(self.Shot_tab, "")
        self.Level_tab = QtWidgets.QWidget()
        self.Level_tab.setObjectName("Level_tab")
        self.level_treeWidget = QtWidgets.QTreeWidget(self.Level_tab)
        self.level_treeWidget.setGeometry(QtCore.QRect(0, 29, 674, 512))
        self.level_treeWidget.setObjectName("level_treeWidget")
        self.level_step_selector = QtWidgets.QComboBox(self.Level_tab)
        self.level_step_selector.setGeometry(QtCore.QRect(91, 0, 90, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.level_step_selector.setFont(font)
        self.level_step_selector.setObjectName("level_step_selector")
        self.level_step_selector.addItem("")
        self.level_step_selector.addItem("")
        self.level_step_selector.addItem("")
        self.level_step_selector.addItem("")
        self.level_step_selector.addItem("")
        self.level_proj_selector = QtWidgets.QComboBox(self.Level_tab)
        self.level_proj_selector.setGeometry(QtCore.QRect(0, 0, 90, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.level_proj_selector.setFont(font)
        self.level_proj_selector.setObjectName("level_proj_selector")
        self.level_proj_selector.addItem("")
        self.LevelSearchText = QtWidgets.QLineEdit(self.Level_tab)
        self.LevelSearchText.setGeometry(QtCore.QRect(263, 0, 411, 25))
        self.LevelSearchText.setObjectName("LevelSearchText")
        self.level_status_selector = QtWidgets.QComboBox(self.Level_tab)
        self.level_status_selector.setGeometry(QtCore.QRect(182, 0, 80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.level_status_selector.setFont(font)
        self.level_status_selector.setObjectName("level_status_selector")
        self.level_status_selector.addItem("")
        self.level_status_selector.addItem("")
        self.level_status_selector.addItem("")
        self.level_status_selector.addItem("")
        self.level_status_selector.addItem("")
        self.level_status_selector.addItem("")
        self.module_tab.addTab(self.Level_tab, "")
        self.min_button = QtWidgets.QPushButton(self.centralwidget)
        self.min_button.setGeometry(QtCore.QRect(892, 1, 25, 25))
        self.min_button.setText("")
        self.min_button.setIconSize(QtCore.QSize(21, 21))
        self.min_button.setObjectName("min_button")
        self.close_button = QtWidgets.QPushButton(self.centralwidget)
        self.close_button.setGeometry(QtCore.QRect(923, 1, 25, 25))
        self.close_button.setMouseTracking(False)
        self.close_button.setText("")
        self.close_button.setIconSize(QtCore.QSize(21, 21))
        self.close_button.setObjectName("close_button")
        self.dealWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.dealWidget.setGeometry(QtCore.QRect(678, 52, 271, 545))
        self.dealWidget.setObjectName("dealWidget")
        self.filter_tab = QtWidgets.QWidget()
        self.filter_tab.setObjectName("filter_tab")
        self.todayTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.todayTaskBtn.setGeometry(QtCore.QRect(30, 242, 118, 31))
        self.todayTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.todayTaskBtn.setObjectName("todayTaskBtn")
        self.weekTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.weekTaskBtn.setGeometry(QtCore.QRect(30, 282, 118, 31))
        self.weekTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.weekTaskBtn.setObjectName("weekTaskBtn")
        self.monthTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.monthTaskBtn.setGeometry(QtCore.QRect(30, 322, 118, 31))
        self.monthTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.monthTaskBtn.setObjectName("monthTaskBtn")
        self.label = QtWidgets.QLabel(self.filter_tab)
        self.label.setGeometry(QtCore.QRect(10, 219, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.assignedTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.assignedTaskBtn.setGeometry(QtCore.QRect(34, 426, 118, 31))
        self.assignedTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.assignedTaskBtn.setObjectName("assignedTaskBtn")
        self.myTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.myTaskBtn.setGeometry(QtCore.QRect(34, 387, 118, 31))
        self.myTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.myTaskBtn.setObjectName("myTaskBtn")
        self.label_2 = QtWidgets.QLabel(self.filter_tab)
        self.label_2.setGeometry(QtCore.QRect(10, 360, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.allTaskBtn = QtWidgets.QCommandLinkButton(self.filter_tab)
        self.allTaskBtn.setGeometry(QtCore.QRect(34, 468, 118, 31))
        self.allTaskBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.allTaskBtn.setObjectName("allTaskBtn")
        self.label_cir = QtWidgets.QLabel(self.filter_tab)
        self.label_cir.setGeometry(QtCore.QRect(25, 10, 231, 205))
        self.label_cir.setText("")
        self.label_cir.setObjectName("label_cir")
        self.dealWidget.addTab(self.filter_tab, "")
        self.work_tab = QtWidgets.QWidget()
        self.work_tab.setObjectName("work_tab")
        self.workListWidget = QtWidgets.QListWidget(self.work_tab)
        self.workListWidget.setGeometry(QtCore.QRect(5, 10, 256, 420))
        self.workListWidget.setObjectName("workListWidget")
        self.dealWidget.addTab(self.work_tab, "")
        self.pubilsh_tab = QtWidgets.QWidget()
        self.pubilsh_tab.setObjectName("pubilsh_tab")
        self.pubilshListWidget = QtWidgets.QListWidget(self.pubilsh_tab)
        self.pubilshListWidget.setGeometry(QtCore.QRect(5, 10, 256, 420))
        self.pubilshListWidget.setObjectName("pubilshListWidget")
        self.dealWidget.addTab(self.pubilsh_tab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget = QtWidgets.QTabWidget(self.tab)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 271, 510))
        self.tabWidget.setObjectName("tabWidget")
        self.texture_tab = QtWidgets.QWidget()
        self.texture_tab.setObjectName("texture_tab")
        self.matEditBtn = QtWidgets.QCommandLinkButton(self.texture_tab)
        self.matEditBtn.setGeometry(QtCore.QRect(10, 20, 151, 41))
        self.matEditBtn.setObjectName("matEditBtn")
        self.tabWidget.addTab(self.texture_tab, "")
        self.layout_tab = QtWidgets.QWidget()
        self.layout_tab.setObjectName("layout_tab")
        self.tabWidget.addTab(self.layout_tab, "")
        self.anim_tab = QtWidgets.QWidget()
        self.anim_tab.setObjectName("anim_tab")
        self.tabWidget.addTab(self.anim_tab, "")
        self.server_tab = QtWidgets.QWidget()
        self.server_tab.setObjectName("server_tab")
        self.LinkServerBtn = QtWidgets.QCommandLinkButton(self.server_tab)
        self.LinkServerBtn.setGeometry(QtCore.QRect(20, 20, 151, 41))
        self.LinkServerBtn.setObjectName("LinkServerBtn")
        self.tabWidget.addTab(self.server_tab, "")
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setGeometry(QtCore.QRect(0, 508, 268, 20))
        self.progressBar.setProperty("value", 1)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.dealWidget.addTab(self.tab, "")
        self.refesh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refesh_button.setGeometry(QtCore.QRect(860, 1, 25, 25))
        self.refesh_button.setText("")
        self.refesh_button.setIconSize(QtCore.QSize(21, 21))
        self.refesh_button.setObjectName("refesh_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actiontemp = QtWidgets.QAction(MainWindow)
        self.actiontemp.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.actiontemp.setObjectName("actiontemp")
        self.actiontemp_2 = QtWidgets.QAction(MainWindow)
        self.actiontemp_2.setObjectName("actiontemp_2")
        self.actiontest = QtWidgets.QAction(MainWindow)
        self.actiontest.setObjectName("actiontest")
        self.actiontest_2 = QtWidgets.QAction(MainWindow)
        self.actiontest_2.setObjectName("actiontest_2")

        self.retranslateUi(MainWindow)
        self.module_tab.setCurrentIndex(0)
        self.dealWidget.setCurrentIndex(3)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.asset_proj_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "  项 目", None, -1))
        self.asset_treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "id", None, -1))
        self.asset_treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.asset_treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("MainWindow", "任务", None, -1))
        self.asset_treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("MainWindow", "执行人", None, -1))
        self.asset_treeWidget.headerItem().setText(4, QtWidgets.QApplication.translate("MainWindow", "工时", None, -1))
        self.asset_treeWidget.headerItem().setText(5, QtWidgets.QApplication.translate("MainWindow", "开始时间", None, -1))
        self.asset_treeWidget.headerItem().setText(6, QtWidgets.QApplication.translate("MainWindow", "结束时间", None, -1))
        self.asset_treeWidget.headerItem().setText(7, QtWidgets.QApplication.translate("MainWindow", "资产类型", None, -1))
        self.asset_treeWidget.headerItem().setText(8, QtWidgets.QApplication.translate("MainWindow", "项目", None, -1))
        self.asset_type_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "资产类型", None, -1))
        self.asset_type_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Character", None, -1))
        self.asset_type_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "Prop", None, -1))
        self.asset_type_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "Environment", None, -1))
        self.asset_type_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "Level", None, -1))
        self.asset_step_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "任务工序", None, -1))
        self.asset_step_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "design", None, -1))
        self.asset_step_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "model", None, -1))
        self.asset_step_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "texture", None, -1))
        self.asset_step_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "hair", None, -1))
        self.asset_step_selector.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "rig", None, -1))
        self.asset_step_selector.setItemText(6, QtWidgets.QApplication.translate("MainWindow", "engineset", None, -1))
        self.asset_status_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.asset_status_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "未开始", None, -1))
        self.asset_status_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "进行中", None, -1))
        self.asset_status_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "审核中", None, -1))
        self.asset_status_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "已完成", None, -1))
        self.asset_status_selector.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "已取消", None, -1))
        self.module_tab.setTabText(self.module_tab.indexOf(self.Asset_tab), QtWidgets.QApplication.translate("MainWindow", "Asset", None, -1))
        self.shot_proj_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "  项 目", None, -1))
        self.shot_treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "id", None, -1))
        self.shot_treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.shot_treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("MainWindow", "集数", None, -1))
        self.shot_treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("MainWindow", "场次", None, -1))
        self.shot_treeWidget.headerItem().setText(4, QtWidgets.QApplication.translate("MainWindow", "序列", None, -1))
        self.shot_treeWidget.headerItem().setText(5, QtWidgets.QApplication.translate("MainWindow", "任务", None, -1))
        self.shot_treeWidget.headerItem().setText(6, QtWidgets.QApplication.translate("MainWindow", "执行人", None, -1))
        self.shot_treeWidget.headerItem().setText(7, QtWidgets.QApplication.translate("MainWindow", "工时", None, -1))
        self.shot_treeWidget.headerItem().setText(8, QtWidgets.QApplication.translate("MainWindow", "开始时间", None, -1))
        self.shot_treeWidget.headerItem().setText(9, QtWidgets.QApplication.translate("MainWindow", "结束时间", None, -1))
        self.shot_treeWidget.headerItem().setText(10, QtWidgets.QApplication.translate("MainWindow", "项目", None, -1))
        self.shot_episode_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", " 集 数", None, -1))
        self.shot_step_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "任务工序", None, -1))
        self.shot_step_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "StoryBoard", None, -1))
        self.shot_step_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "mocap", None, -1))
        self.shot_step_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "layout", None, -1))
        self.shot_step_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "anim", None, -1))
        self.shot_step_selector.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "excloth", None, -1))
        self.shot_step_selector.setItemText(6, QtWidgets.QApplication.translate("MainWindow", "lighting", None, -1))
        self.shot_step_selector.setItemText(7, QtWidgets.QApplication.translate("MainWindow", "efx", None, -1))
        self.shot_session_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", " 场 次", None, -1))
        self.shot_status_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.shot_status_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "未开始", None, -1))
        self.shot_status_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "进行中", None, -1))
        self.shot_status_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "审核中", None, -1))
        self.shot_status_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "已完成", None, -1))
        self.shot_status_selector.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "已取消", None, -1))
        self.module_tab.setTabText(self.module_tab.indexOf(self.Shot_tab), QtWidgets.QApplication.translate("MainWindow", "Shot", None, -1))
        self.level_treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "id", None, -1))
        self.level_treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.level_treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("MainWindow", "任务", None, -1))
        self.level_treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("MainWindow", "执行人", None, -1))
        self.level_treeWidget.headerItem().setText(4, QtWidgets.QApplication.translate("MainWindow", "工时", None, -1))
        self.level_treeWidget.headerItem().setText(5, QtWidgets.QApplication.translate("MainWindow", "开始时间", None, -1))
        self.level_treeWidget.headerItem().setText(6, QtWidgets.QApplication.translate("MainWindow", "结束时间", None, -1))
        self.level_treeWidget.headerItem().setText(7, QtWidgets.QApplication.translate("MainWindow", "项目", None, -1))
        self.level_step_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "任务工序", None, -1))
        self.level_step_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "leveldesign", None, -1))
        self.level_step_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "levelart", None, -1))
        self.level_step_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "levellight", None, -1))
        self.level_step_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "levelefx", None, -1))
        self.level_proj_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "  项 目", None, -1))
        self.level_status_selector.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "任务状态", None, -1))
        self.level_status_selector.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "未开始", None, -1))
        self.level_status_selector.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "进行中", None, -1))
        self.level_status_selector.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "审核中", None, -1))
        self.level_status_selector.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "已完成", None, -1))
        self.level_status_selector.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "已取消", None, -1))
        self.module_tab.setTabText(self.module_tab.indexOf(self.Level_tab), QtWidgets.QApplication.translate("MainWindow", "Level", None, -1))
        self.todayTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "当天任务", None, -1))
        self.weekTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "本周任务", None, -1))
        self.monthTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "本月任务", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "任务周期", None, -1))
        self.assignedTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "我发布的", None, -1))
        self.myTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "指派给我的", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "我的任务", None, -1))
        self.allTaskBtn.setText(QtWidgets.QApplication.translate("MainWindow", "所有任务", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.filter_tab), QtWidgets.QApplication.translate("MainWindow", "我的任务", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.work_tab), QtWidgets.QApplication.translate("MainWindow", "work", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.pubilsh_tab), QtWidgets.QApplication.translate("MainWindow", "pubilsh", None, -1))
        self.matEditBtn.setText(QtWidgets.QApplication.translate("MainWindow", "材质模板编辑器", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.texture_tab), QtWidgets.QApplication.translate("MainWindow", "贴图", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.layout_tab), QtWidgets.QApplication.translate("MainWindow", "Layout", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.anim_tab), QtWidgets.QApplication.translate("MainWindow", "动画", None, -1))
        self.LinkServerBtn.setText(QtWidgets.QApplication.translate("MainWindow", "打开服务端", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.server_tab), QtWidgets.QApplication.translate("MainWindow", "服务端", None, -1))
        self.dealWidget.setTabText(self.dealWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "流程功能", None, -1))
        self.actionopen.setText(QtWidgets.QApplication.translate("MainWindow", "temp", None, -1))
        self.actiontemp.setText(QtWidgets.QApplication.translate("MainWindow", "打开", None, -1))
        self.actiontemp_2.setText(QtWidgets.QApplication.translate("MainWindow", "更新", None, -1))
        self.actiontest.setText(QtWidgets.QApplication.translate("MainWindow", "test", None, -1))
        self.actiontest_2.setText(QtWidgets.QApplication.translate("MainWindow", "test", None, -1))

class strack():
    def __init__(self,url,user,password):
        self.st = Strack(base_url=url, login_name=user, password=password)
        self.exrStatusIcon = {'work':'workStatus.png','update':'updateStatus.png'}
    def statusTable(self):
        return self.st.select('status').get('rows')
    def projectTable(self):
        return self.st.select('project', fields=['id', 'code', 'name']).get('rows')
    def episodeTable(self):
        return self.st.select('episode').get('rows')
    def sessionTable(self):
        return self.st.select('session').get('rows')
    def asset_task(self):
        list = self.st.select('asset',fields=['id']).get('rows')
        id_list = [asset.get('id') for asset in list]
        if id_list:
            task = self.st.adv_select('base', [['entity_id', 'in', id_list]])
            return task.get('rows')
        else:
            return []

    def shot_task(self):
        list = self.st.select('sequence',fields=['id']).get('rows')
        id_list = [shot.get('id') for shot in list]
        if id_list:
            task = self.st.adv_select('base', [['entity_id', 'in', id_list]])
            return task.get('rows')
        else:
            return []

    def level_task(self):
        list = self.st.select('level',fields=['id']).get('rows')
        id_list = [shot.get('id') for shot in list]
        if id_list:
            task = self.st.adv_select('base', [['entity_id', 'in', id_list]])
            return task.get('rows')
        else:
            return []
class matWidget(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.refesh_treeWidget()
        self.refesh_listWidget()
        self.pushButton.clicked.connect(self.convert)
        self.mat_listWidget.itemClicked.connect(self.selectMesh)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(843, 571)
        self.mat_listWidget = QtWidgets.QListWidget(Form)
        self.mat_listWidget.setGeometry(QtCore.QRect(10, 10, 311, 420))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.mat_listWidget.setFont(font)
        self.mat_listWidget.setObjectName("mat_listWidget")
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setGeometry(QtCore.QRect(328, 10, 511, 420))
        self.treeWidget.setObjectName("treeWidget")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(330, 490, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("Form", "id", None, -1))
        self.treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("Form", "微缩图", None, -1))
        self.treeWidget.headerItem().setText(2, QtWidgets.QApplication.translate("Form", "名称", None, -1))
        self.treeWidget.headerItem().setText(3, QtWidgets.QApplication.translate("Form", "编码", None, -1))
        self.treeWidget.headerItem().setText(4, QtWidgets.QApplication.translate("Form", "简述", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "转化", None, -1))
    def set_meshname(self,mat):
        if mc.listConnections(mc.listConnections(mat, type='shadingEngine'), type='mesh'):
            mesh_list = mc.listConnections(mc.listConnections(mat, type='shadingEngine'), type='mesh')
            for i in range(0, len(mesh_list)):
                if mc.objExists(mesh_list[i]):
                    mc.select(mesh_list[i])
                    mc.rename(mat + '_mesh' + str(i))
    def selectMesh(self):
        mat = self.mat_listWidget.selectedItems()[0].text()
        mesh_list = mc.listConnections(mc.listConnections(mat, type='shadingEngine'), type='mesh')
        if mesh_list:
            mc.select(mesh_list)

    def renameMat(self,mat,matTemp):
        filename = mc.file(q=1, sn=1, shortName=1).split('.')[0].split('_')[0]
        mc.select(mat)
        if mc.objExists(filename + '_part_' + matTemp):
            mc.select(filename +'_*_' + matTemp)
            newname = filename + '_part' + str(len(mc.ls(sl=1))) + '_' + matTemp
        else:
            newname = filename + '_part_' + matTemp
        mc.rename(newname)
        try:
            mc.rename(mc.listConnections(mc.ls(sl=1)[0], type='shadingEngine')[0], str(mc.ls(sl=1)[0]) + 'SG')
        except:
            pass
        return newname
    def refesh_listWidget(self):
        self.mat_listWidget.clear()
        mat = mc.ls(type='blinn')
        mat += mc.ls(type='lambert')
        mat += mc.ls(type='phong')
        for item in mat:
            temp = QtWidgets.QListWidgetItem()
            temp.setText(item)
            self.mat_listWidget.addItem(temp)
    def refesh_treeWidget(self):
        r_json = requests.get('http://%s:5000/uemat/json'%node_server)
        r_json = json.loads(r_json.content)
        self.treeWidget.setIconSize(QtCore.QSize(80, 80))
        self.treeWidget.hideColumn(0)
        for item in r_json:
            icon = QPixmap()
            icon.loadFromData(base64.b64decode(item.get('img64').split(',')[1]))
            child = QtWidgets.QTreeWidgetItem(self.treeWidget)
            child.setIcon(1,QIcon(icon))
            child.setText(2, item.get('matCn'))
            child.setText(3, item.get('matCode'))
            child.setText(4, item.get('matResume'))
    def convert(self):
        if self.mat_listWidget.selectedItems() and self.treeWidget.selectedItems():
            mat = self.mat_listWidget.selectedItems()[0].text()
            matTemp = self.treeWidget.selectedItems()[0].text(3)
            newname = self.renameMat(mat,matTemp)
            self.mat_listWidget.selectedItems()[0].setText(newname)
class mayaWidget(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,myStrack,local_path):
        self.taskServer = node_server
        self.strack = myStrack
        self.local_path = local_path
        self.now = datetime.datetime.now()
        self.deadline = self.now + datetime.timedelta(days=300)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.refeshShotTreeLock = False
        self.close_button.clicked.connect(self.close)
        self.min_button.clicked.connect(self.showMinimized)
        self.asset_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_treeWidget.customContextMenuRequested.connect(self.assetOpenMenu)
        self.shot_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shot_treeWidget.customContextMenuRequested.connect(self.shotOpenMenu)
        self.level_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.level_treeWidget.customContextMenuRequested.connect(self.levelOpenMenu)
        self.workListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workListWidget.customContextMenuRequested.connect(self.workOpenMenu)
        self.pubilshListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pubilshListWidget.customContextMenuRequested.connect(self.pubilshOpenMenu)
        self.AssetSearchText.textChanged.connect(self.refeshAssetTree)
        self.ShotSearchText.textChanged.connect(self.refeshShotTree)
        self.LevelSearchText.textChanged.connect(self.refeshLevelTree)
        self.asset_proj_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_type_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_step_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_status_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.shot_episode_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_session_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotEpisode)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotSession)
        self.shot_episode_selector.currentIndexChanged.connect(self.refeshShotSession)
        self.shot_step_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_status_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.level_step_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_proj_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_status_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.asset_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.shot_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.asset_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.shot_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.todayTaskBtn.clicked.connect(self.todayFilter)
        self.weekTaskBtn.clicked.connect(self.weekFilter)
        self.monthTaskBtn.clicked.connect(self.monthFilter)
        self.refesh_button.clicked.connect(self.refeshData)
        self.myTaskBtn.clicked.connect(self.myTask)
        self.allTaskBtn.clicked.connect(self.allTask)
        self.matEditBtn.clicked.connect(self.mat_win)
        self.LinkServerBtn.clicked.connect(self.server_win)
        self.worker = ''
        self.cirInit()
        self.Qpix = QtGui.QPixmap(201, 201)
        self.Qpix.fill(QtCore.Qt.transparent)
        self.dataInit()
    def dataInit(self):
        cacheFile = '//%s/LocalShare/teamones/cache.json'%public_disk
        if os.path.exists(cacheFile):
            cache = json.loads(open(cacheFile).read())
            self.asset_data = cache.get('asset_data')
            self.shot_data = cache.get('shot_data')
            self.level_data = cache.get('level_data')
            self.project_data = cache.get('project_data')
            self.status_data = cache.get('status_data')
            self.episode_data = cache.get('episode_data')
            self.session_data = cache.get('session_data')
            self.additem_init()
            self.refeshAssetTree()
            self.refeshShotTree()
            self.refeshLevelTree()
    def cirInit(self):
        self.angle = 1
        self.cirX = 0
        self.cirY = 0
        self.radius = 200
        self.lineWidth = 10
        self.timeLine = QtCore.QTimeLine(1000, self)
        self.timeLine.frameChanged.connect(self.updateTimeline)
        self.setAngle(100)
    def updateTimeline(self, frame):
        self.drawAngle = frame
        self.update()
    def setAngle(self,value):
        self.drawAngle = self.angle
        self.angle = value
        self.timeLine.stop()
        self.timeLine.setFrameRange(self.drawAngle, self.angle)
        # self.update()
        self.timeLine.start()
    def paintEvent(self, event):
        the_rect = QtCore.QRectF(self.cirX, self.cirX, self.radius, self.radius)
        if the_rect.isNull():
            return
        painter = QtGui.QPainter(self.Qpix)
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(60, 60, 60))
        painter.drawEllipse(QtCore.QRectF(self.cirX+2, self.cirY+2, self.radius-10, self.radius-10))
        painter.restore()
        painter.setPen(QtGui.QColor(QtCore.Qt.white))
        painter.setFont(QtGui.QFont('Times New Roman', 45))
        painter.drawText(55, 120, str(int(self.angle/3.6)) + "%")
        painter.restore()
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform, on=True)
        the_path = QtGui.QPainterPath()
        the_path.addEllipse(the_rect.adjusted(1, 1, -1, -1))
        the_path.addEllipse(the_rect.adjusted(
            1 + self.lineWidth, 1 + self.lineWidth, -1 - self.lineWidth, -1 - self.lineWidth))
        painter.fillPath(the_path, QtGui.QColor(190, 220, 215))
        the_gradient = QtGui.QConicalGradient(the_rect.center(), 90)
        the_angle = self.drawAngle / 360.0
        the_gradient.setColorAt(0, QtGui.QColor(12, 229, 194))
        the_gradient.setColorAt(the_angle, QtGui.QColor(7, 143, 121))
        if the_angle + 0.001 < 1:
            the_gradient.setColorAt(the_angle + 0.001, QtGui.QColor(0, 0, 0, 0))
        painter.fillPath(the_path, the_gradient)
        self.label_cir.setPixmap(self.Qpix)
    def myTask(self):
        self.worker = self.strack.st.login_name
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def allTask(self):
        self.worker = ''
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def excoutorCheck(self,item):
        if self.worker:
            if item.get('executor'):
                if re.search(self.worker,item.get('executor')[0].get('login_name')):
                    return True
                else:
                    return False
        else:
            return True
    def refeshShotEpisode(self):
        self.refeshShotTreeLock = True
        self.shot_episode_selector.clear()
        self.shot_episode_selector.addItem(u' 集 数')
        projCode = self.shot_proj_selector.currentText()
        if self.shot_proj_selector.currentIndex()>0:
            for item in self.episode_data:
                if item.get('project_id') == self.projCodeToItem(projCode).get('id'):
                    self.shot_episode_selector.addItem(item.get('code'))
        self.refeshShotTreeLock = False
    def refeshShotSession(self):
        self.refeshShotTreeLock = True
        self.shot_session_selector.clear()
        self.shot_session_selector.addItem(u' 场 次')
        projCode = self.shot_proj_selector.currentText()
        episodeCode = self.shot_episode_selector.currentText()
        if self.shot_proj_selector.currentIndex()>0 and self.shot_episode_selector.currentIndex()>0:
            for item in self.session_data:
                if item.get('project_id') == self.projCodeToItem(projCode).get('id') \
                        and item.get('parent_id')== self.findEpisode(episodeCode,item.get('project_id')).get('id'):
                    self.shot_session_selector.addItem(item.get('code'))
        self.refeshShotTreeLock = False
    def refeshData(self):
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable()
        self.status_data = self.strack.statusTable()
        self.episode_data = self.strack.episodeTable()
        self.session_data = self.strack.sessionTable()
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def findEpisode(self,code,projId):
        for item in self.episode_data:
            if item.get('code') == code and item.get('project_id')==projId:
                return item

    def findSession(self,code,projId,parent_id):
        for item in self.session_data:
            if item.get('code') == code and item.get('project_id')==projId and item.get('parent_id')==parent_id:
                return item

    def projCodeToItem(self,code):
        for item in self.project_data:
            if item.get('code') == code:
                return item

    def refeshWorkList(self):
            self.workListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)

    def refeshPubilshList(self):
            self.pubilshListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)

    def additem_init(self):
        for item in self.project_data:
            self.asset_proj_selector.addItem(item.get('code'))
            self.shot_proj_selector.addItem(item.get('code'))
            self.level_proj_selector.addItem(item.get('code'))

    def list_file(self, path):
        temp_list = []
        fs = os.listdir(path)
        if fs:
            for obj in fs:
                tmp_path = os.path.join(path, obj)
                if not os.path.isdir(tmp_path):
                    temp_list.append(obj)
        return temp_list

    def todayFilter(self):
        temp = str(datetime.datetime.now()).split(' ')[0] + ' 23:59:00'
        self.deadline = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def weekFilter(self):
        self.deadline =self.now + datetime.timedelta(days=7)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def monthFilter(self):
        self.deadline =self.now + datetime.timedelta(days=30)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def deadlineCheck(self,item):
        if item.get('end_time'):
            self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
        else:
            self.endTime = self.now + datetime.timedelta(days=6)
        return self.endTime < self.deadline
    def dataIdSelect(self,data,id):
        temp = {}
        for item in data:
            if item.get('id') ==int(id):
                temp = item
                break
        return temp

    def refeshAssetTree(self):
        word = self.AssetSearchText.text()
        self.asset_treeWidget.clear()
        self.asset_treeWidget.hideColumn(0)
        self.asset_treeWidget.setColumnWidth(1, 80)
        self.asset_treeWidget.setColumnWidth(2,170)
        self.asset_treeWidget.setColumnWidth(3, 55)
        self.asset_treeWidget.setColumnWidth(4, 45)
        self.asset_treeWidget.setColumnWidth(7, 60)
        assetType,step,proj,status= '','','',''
        if self.asset_type_selector.currentIndex():
            assetType = self.asset_type_selector.currentText()
        if self.asset_step_selector.currentIndex():
            step = self.asset_step_selector.currentText()
        if self.asset_proj_selector.currentIndex():
            proj = self.asset_proj_selector.currentText()
        if self.asset_status_selector.currentIndex():
            status = self.asset_status_selector.currentText()
        for i,item in enumerate(self.asset_data):
            if item.get('json'):
                status_name = self.dataIdSelect(self.status_data,item.get('status_id')).get('name')
                if (re.search(word,item.get('json').get('asset_code')) or re.search(word,item.get('json').get('asset_name')))\
                        and re.search(assetType, item.get('json').get('asset_type_code')) \
                        and re.search(step, item.get('json').get('step_code')) \
                        and re.search(proj, item.get('json').get('project_code')) \
                        and re.search(status, status_name) \
                        and self.deadlineCheck(item) \
                        and self.excoutorCheck(item):
                    child = QtWidgets.QTreeWidgetItem(self.asset_treeWidget)
                    child.setText(0, str(item.get('id')))
                    child.setText(1, status_name)
                    child.setIcon(1, QtGui.QIcon('%s/images/%s' % (self.local_path,
                                                                   self.strack.exrStatusIcon.get(
                                                                       item.get('json').get('exrStatus', 'work')))))
                    child.setText(2, item.get('json').get('task_name'))
                    if item.get('executor'):
                        child.setText(3, item.get('executor')[0].get('name'))
                    child.setText(4, item.get('duration'))
                    child.setText(5, item.get('start_time'))
                    child.setText(6, item.get('end_time'))
                    child.setText(7, item.get('json').get('asset_type_name'))
                    child.setText(8, item.get('json').get('project_name'))
                    if i%15==0:
                        QtWidgets.QApplication.processEvents()
    def refeshShotTree(self):
        if not self.refeshShotTreeLock:
            word = self.ShotSearchText.text()
            self.shot_treeWidget.clear()
            self.shot_treeWidget.hideColumn(0)
            self.shot_treeWidget.setColumnWidth(1, 80)
            self.shot_treeWidget.setColumnWidth(2, 60)
            self.shot_treeWidget.setColumnWidth(3, 60)
            self.shot_treeWidget.setColumnWidth(4, 60)
            self.shot_treeWidget.setColumnWidth(5, 100)
            self.shot_treeWidget.setColumnWidth(6, 60)
            self.shot_treeWidget.setColumnWidth(7, 50)
            proj, step,episode,session,status= '', '', '','',''
            if self.shot_step_selector.currentIndex():
                step = self.shot_step_selector.currentText()
            if self.shot_proj_selector.currentIndex():
                proj = self.shot_proj_selector.currentText()
            if self.shot_episode_selector.currentIndex():
                episode = self.shot_episode_selector.currentText()
            if self.shot_session_selector.currentIndex():
                session = self.shot_session_selector.currentText()
            if self.shot_status_selector.currentIndex():
                status = self.shot_status_selector.currentText()
            for i,item in enumerate(self.shot_data):
                if item.get('json'):
                    status_name = self.dataIdSelect(self.status_data, item.get('status_id')).get('name')
                    if (re.search(word,item.get('json').get('sequence_name')) or re.search(word,item.get('json').get('sequence_code'))) \
                            and re.search(step, item.get('json').get('step_code')) \
                            and re.search(proj, item.get('json').get('project_code')) \
                            and re.search(episode, item.get('json').get('episode_code')) \
                            and re.search(session, item.get('json').get('session_code')) \
                            and re.search(status, status_name) \
                            and self.deadlineCheck(item) \
                            and self.excoutorCheck(item):
                        child = QtWidgets.QTreeWidgetItem(self.shot_treeWidget)
                        child.setText(0, str(item.get('id')))
                        child.setText(1, status_name)
                        child.setIcon(1, QtGui.QIcon('%s/images/%s'%(self.local_path,
                                         self.strack.exrStatusIcon.get(item.get('json').get('exrStatus','work')))))
                        child.setText(2, item.get('json').get('episode_name'))
                        child.setText(3, item.get('json').get('session_name'))
                        child.setText(4, item.get('json').get('sequence_name'))
                        child.setText(5, item.get('json').get('task_name'))
                        if item.get('executor'):
                            child.setText(6, item.get('executor')[0].get('name'))
                        child.setText(7, item.get('duration'))
                        child.setText(8, item.get('start_time'))
                        child.setText(9, item.get('end_time'))
                        child.setText(10, item.get('json').get('project_name'))
                        if i%15==0:
                            QtWidgets.QApplication.processEvents()
    def refeshLevelTree(self):
        word = self.LevelSearchText.text()
        self.level_treeWidget.clear()
        self.level_treeWidget.hideColumn(0)
        self.level_treeWidget.setColumnWidth(1, 80)
        self.level_treeWidget.setColumnWidth(2, 100)
        self.level_treeWidget.setColumnWidth(3, 60)
        self.level_treeWidget.setColumnWidth(4, 50)
        proj, step,status= '', '',''
        if self.level_step_selector.currentIndex():
            step = self.level_step_selector.currentText()
        if self.level_proj_selector.currentIndex():
            proj = self.level_proj_selector.currentText()
        if self.level_status_selector.currentIndex():
            status = self.level_status_selector.currentText()
        for i,item in enumerate(self.level_data):
            if item.get('json'):
                status_name = self.dataIdSelect(self.status_data, item.get('status_id')).get('name')
                if (re.search(word,item.get('json').get('level_code')) or re.search(word,item.get('json').get('level_name')))\
                        and re.search(step, item.get('json').get('step_code')) \
                        and re.search(proj, item.get('json').get('project_code')) \
                        and re.search(status, status_name) \
                        and self.deadlineCheck(item) \
                        and self.excoutorCheck(item):
                    child = QtWidgets.QTreeWidgetItem(self.level_treeWidget)
                    child.setText(0, str(item.get('id')))
                    child.setText(1, status_name)
                    child.setIcon(1, QtGui.QIcon('%s/images/%s' % (self.local_path,
                                                                   self.strack.exrStatusIcon.get(
                                                                       item.get('json').get('exrStatus', 'work')))))
                    child.setText(2, item.get('json').get('task_name'))
                    if item.get('executor'):
                        child.setText(3, item.get('executor')[0].get('name'))
                    child.setText(4, item.get('duration'))
                    child.setText(5, item.get('start_time'))
                    child.setText(6, item.get('end_time'))
                    child.setText(7, item.get('json').get('project_name'))
                    if i%10==0:
                        QtWidgets.QApplication.processEvents()

    def assetOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.asset_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.asset_treeWidget.selectedItems():
                print(self.asset_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.asset_data, id))

    def shotOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.shot_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.shot_treeWidget.selectedItems():
                print(self.shot_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.shot_data, id))

    def levelOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.level_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.level_treeWidget.selectedItems():
                print(self.level_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.level_data, id))

    def workOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        openAction = menu.addAction("打开文件")
        importAction = menu.addAction("导入文件")
        exportAction = menu.addAction("导出文件")
        refAction = menu.addAction("引用文件")
        opendir = menu.addAction("打开目录")
        menu.addSeparator()
        commitAnimExport = menu.addAction("提交动画导出")
        localAnimExport = menu.addAction("本机自动导出")
        bqAnimImport = menu.addAction("表情导入")
        action = menu.exec_(self.workListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                file_name = '%s_%s_V##.mb'%(code,step)
                check_name = '%s_%s_V\d\d.mb'%(code,step)
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本序号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s'%(item.get('json').get('Work_path'),str(my_str))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshWorkList()

            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                proj = item.get('json').get('project_code')
                episode = item.get('json').get('episode_code')
                session = item.get('json').get('session_code')
                sequence = item.get('json').get('sequence_code')
                newpath = '%s/%s_%s_%s_%s.mb'%(item.get('json').get('Work_path'),proj,episode,session,sequence)
                mc.file(rename='C:/Users/Public/Documents/temp.mb')
                mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                self.refeshWorkList()
        if action == openAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, open=1, f=1)
        if action == importAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path,i=1, ignoreVersion=1)
        if action == exportAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('task_code')
                step = item.get('json').get('step_code')
                if step == 'rig':
                    file_name = '%s_##.fbx' %code
                    check_name = '%s_.+.\.fbx' %code
                else:
                    file_name = '%s_V##.fbx' %code
                    check_name = '%s_V\d\d.fbx' %code
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s' % (item.get('json').get('Work_path'), str(my_str))
                    mc.file(newpath, f=1, type='FBX export', pr=1, es=1)
                    self.refeshWorkList()
        if action == refAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, reference=1, namespace=path.split('.')[0].split('/')[-1])
        if action == opendir:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                os.startfile(item.get('json').get('Work_path'))
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                os.startfile(item.get('json').get('Work_path'))
        if action == commitAnimExport:
            if self.shot_treeWidget.selectedItems() and self.workListWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                step = item.get('json').get('step_code')
                if step == 'anim':
                    path = item.get('json').get('Work_path')+ '/'+ str(self.workListWidget.selectedItems()[0].text())
                    dic = {'taskStatus': 'wait', 'TaskType': 'AnimateTask', 'input_file': path,
                           'publish_dir': item.get('json').get('Publish_path'),
                           'TaskId': item.get('uuid'), 'db': item.get('json').get('project_code'),
                           'eps_cnname': item.get('json').get('episode_code'), 'asset_shot': item.get('json').get('sequence_code'),
                           'abc': 0}
                    r_json = requests.post('http://%s:5000/maya/con?action=post'%self.taskServer, json.dumps(dic))
                    msg_box = QtWidgets.QMessageBox
                    msg_box.question(self, '提示', r_json.content, msg_box.Ok)
        if action == localAnimExport:
            import sys
            sys.path.append("//%s//LocalShare/teamones/maya_script"%public_disk)
            # from maya_excute import *
            # main()
    def pubilshOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        openAction = menu.addAction("打开文件")
        importAction = menu.addAction("导入文件")
        exportAction = menu.addAction("导出文件")
        refAction = menu.addAction("引用文件")
        opendir = menu.addAction("打开目录")
        action = menu.exec_(self.pubilshListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('task_code')
                step = item.get('json').get('step_code')
                if step == 'rig':
                    file_name = '%s_V##.mb'%code
                    check_name = '%s_V\d\d.mb'%code
                    my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号',QtWidgets.QLineEdit.Normal, file_name)
                    if re.search(check_name, str(my_str)) and ok:
                        newpath = '%s/%s' % (item.get('json').get('Publish_path'), str(my_str))
                        mc.file(rename='C:/Users/Public/Documents/temp.mb')
                        mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                        shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                        self.refeshPubilshList()
                else:
                    file_name = '%s_V01.mb' %code
                    newpath = '%s/%s'%(item.get('json').get('Publish_path'),str(file_name))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshPubilshList()
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                if step == 'anim':
                    pass
                else:
                    file_name = '%s_%s_V01.mb' % (code, step)
                    newpath = '%s/%s'%(item.get('json').get('Publish_path'),str(file_name))
                    mc.file(rename='C:/Users/Public/Documents/temp.mb')
                    mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                    shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                    self.refeshPubilshList()
        if action == openAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, open=1, f=1)
        if action == exportAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('task_code')
                step = item.get('json').get('step_code')
                if step == 'rig':
                    file_name = '%s_##.fbx' %code
                    check_name = '%s_.+.\.fbx' %code
                    my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本号',QtWidgets.QLineEdit.Normal, file_name)
                    if re.search(check_name, str(my_str)) and ok:
                        newpath = '%s/%s' % (item.get('json').get('Publish_path'), str(my_str))
                        mc.file(newpath, f=1, type='FBX export', pr=1, es=1)
                else:
                    file_name = '%s/%s_V01.fbx' % (item.get('json').get('Publish_path'),code)
                    mc.file(file_name, f=1, type='FBX export', pr=1, es=1)
                self.refeshPubilshList()
        if action == refAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, reference=1, namespace=path.split('.')[0].split('/')[-1])
        if action == importAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                mc.file(path, i=1, ignoreVersion=1)
        if action == opendir:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                os.startfile(item.get('json').get('Publish_path'))
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                os.startfile(item.get('json').get('Publish_path'))
    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                    background-image:url('%s/images/04.jpg');
                }
                ''' % (self.local_path)
        self.refesh_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/03.jpg' % self.local_path)))
        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/12.jpg'%self.local_path)))
        self.min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/13.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/11.jpg);}' % self.local_path)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    def mat_win(self):
        self.matWin = matWidget()
        self.matWin.show()
        self.matWin.setFixedSize(843, 571)
    def server_win(self):
        self.serverWin = QWebEngineView()
        self.serverWin.load(QUrl("http://%s:5000"%node_server))
        self.serverWin.show()
        self.serverWin.setFixedSize(1400, 750)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def showColor(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '对话框','请输入序列名:')
        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

class mobuWidget(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,myStrack,local_path):
        self.taskServer = node_server
        self.mobu = Mobu()
        self.strack = myStrack
        self.local_path = local_path
        self.now = datetime.datetime.now()
        self.deadline = self.now + datetime.timedelta(days=300)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.refeshShotTreeLock = False
        self.close_button.clicked.connect(self.close)
        self.min_button.clicked.connect(self.showMinimized)
        self.asset_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_treeWidget.customContextMenuRequested.connect(self.assetOpenMenu)
        self.shot_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shot_treeWidget.customContextMenuRequested.connect(self.shotOpenMenu)
        self.level_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.level_treeWidget.customContextMenuRequested.connect(self.levelOpenMenu)
        self.workListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workListWidget.customContextMenuRequested.connect(self.workOpenMenu)
        self.pubilshListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pubilshListWidget.customContextMenuRequested.connect(self.pubilshOpenMenu)
        self.AssetSearchText.textChanged.connect(self.refeshAssetTree)
        self.ShotSearchText.textChanged.connect(self.refeshShotTree)
        self.LevelSearchText.textChanged.connect(self.refeshLevelTree)
        self.asset_proj_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_type_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_step_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_status_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.shot_episode_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_session_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotEpisode)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotSession)
        self.shot_episode_selector.currentIndexChanged.connect(self.refeshShotSession)
        self.shot_step_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_status_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.level_step_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_proj_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_status_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.asset_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.shot_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.asset_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.shot_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.todayTaskBtn.clicked.connect(self.todayFilter)
        self.weekTaskBtn.clicked.connect(self.weekFilter)
        self.monthTaskBtn.clicked.connect(self.monthFilter)
        self.refesh_button.clicked.connect(self.refeshData)
        self.myTaskBtn.clicked.connect(self.myTask)
        self.allTaskBtn.clicked.connect(self.allTask)
        self.LinkServerBtn.clicked.connect(self.server_win)
        self.worker = ''
        self.cirInit()
        self.Qpix = QtGui.QPixmap(201, 201)
        self.Qpix.fill(QtCore.Qt.transparent)
        self.dataInit()

    def dataInit(self):
        cacheFile = '//%s/LocalShare/teamones/cache.json' % public_disk
        if os.path.exists(cacheFile):
            cache = json.loads(open(cacheFile).read())
            self.asset_data = cache.get('asset_data')
            self.shot_data = cache.get('shot_data')
            self.level_data = cache.get('level_data')
            self.project_data = cache.get('project_data')
            self.status_data = cache.get('status_data')
            self.episode_data = cache.get('episode_data')
            self.session_data = cache.get('session_data')
            self.additem_init()
            self.refeshAssetTree()
            self.refeshShotTree()
            self.refeshLevelTree()
    def cirInit(self):
        self.angle = 1
        self.cirX = 0
        self.cirY = 0
        self.radius = 200
        self.lineWidth = 10
        self.timeLine = QtCore.QTimeLine(1000, self)
        self.timeLine.frameChanged.connect(self.updateTimeline)
        self.setAngle()
    def updateTimeline(self, frame):
        self.drawAngle = frame
        self.update()
    def setAngle(self):
        self.drawAngle = self.angle
        self.angle = 100
        self.timeLine.stop()
        self.timeLine.setFrameRange(self.drawAngle, self.angle)
        # self.update()
        self.timeLine.start()
    def paintEvent(self, event):
        the_rect = QtCore.QRectF(self.cirX, self.cirY, self.radius, self.radius)
        if the_rect.isNull():
            return
        painter = QtGui.QPainter(self.Qpix)
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(60, 60, 60))
        painter.drawEllipse(QtCore.QRectF(self.cirX+2, self.cirY+2, self.radius-10, self.radius-10))
        painter.setPen(QtGui.QColor(QtCore.Qt.white))
        painter.setFont(QtGui.QFont('Times New Roman', 45))
        painter.drawText(50, 120, "30%")
        painter.restore()
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform, on=True)
        the_path = QtGui.QPainterPath()
        the_path.addEllipse(the_rect.adjusted(1, 1, -1, -1))
        the_path.addEllipse(the_rect.adjusted(
            1 + self.lineWidth, 1 + self.lineWidth, -1 - self.lineWidth, -1 - self.lineWidth))
        painter.fillPath(the_path, QtGui.QColor(190, 220, 215))
        the_gradient = QtGui.QConicalGradient(the_rect.center(), 90)
        the_angle = self.drawAngle / 360.0
        the_gradient.setColorAt(0, QtGui.QColor(12, 229, 194))
        the_gradient.setColorAt(the_angle, QtGui.QColor(7, 143, 121))
        if the_angle + 0.001 < 1:
            the_gradient.setColorAt(the_angle + 0.001, QtGui.QColor(0, 0, 0, 0))
        painter.fillPath(the_path, the_gradient)
        self.label_cir.setPixmap(self.Qpix)

    def myTask(self):
        self.worker = self.strack.st.login_name
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def allTask(self):
        self.worker = ''
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def excoutorCheck(self,item):
        if self.worker:
            if item.get('executor'):
                if re.search(self.worker,item.get('executor')[0].get('login_name')):
                    return True
                else:
                    return False
        else:
            return True
    def findEpisode(self,code,projId):
        for item in self.episode_data:
            if item.get('code') == code and item.get('project_id')==projId:
                return item
    def findSession(self,code,projId,parent_id):
        for item in self.session_data:
            if item.get('code') == code and item.get('project_id')==projId and item.get('parent_id')==parent_id:
                return item
    def projCodeToItem(self,code):
        for item in self.project_data:
            if item.get('code') == code:
                return item
    def getSequenceLen(self,project_id,parent_id):
        count =1
        for item in self.strack.st.select('sequence').get('rows'):
            if item.get('project_id') ==project_id and item.get('parent_id') ==parent_id:
                count+=1
        return count
    def dataIdSelect(self,data,id):
        temp = {}
        for item in data:
            if item.get('id') ==int(id):
                temp = item
                break
        return temp
    def findShotItem(self,data,searcher):
        temp = {}
        for item in data:
            if item.get('json').get('project_code') ==searcher.get('proj') and \
                    item.get('entity_id') == searcher.get('entity_id') and \
                    item.get('json').get('step_code') == searcher.get('step'):
                temp = item
                break
        return temp
    def refeshShotEpisode(self):
        self.refeshShotTreeLock = True
        self.shot_episode_selector.clear()
        self.shot_episode_selector.addItem(u' 集 数')
        projCode = self.shot_proj_selector.currentText()
        if self.shot_proj_selector.currentIndex()>0:
            for item in self.episode_data:
                if item.get('project_id') == self.projCodeToItem(projCode).get('id'):
                    self.shot_episode_selector.addItem(item.get('code'))
        self.refeshShotTreeLock = False
    def refeshShotSession(self):
        self.refeshShotTreeLock = True
        self.shot_session_selector.clear()
        self.shot_session_selector.addItem(u' 场 次')
        projCode = self.shot_proj_selector.currentText()
        episodeCode = self.shot_episode_selector.currentText()
        if self.shot_proj_selector.currentIndex()>0 and self.shot_episode_selector.currentIndex()>0:
            for item in self.session_data:
                if item.get('project_id') == self.projCodeToItem(projCode).get('id') \
                        and item.get('parent_id')== self.findEpisode(episodeCode,item.get('project_id')).get('id'):
                    self.shot_session_selector.addItem(item.get('code'))
        self.refeshShotTreeLock = False
    def refeshData(self):
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable()
        self.status_data = self.strack.statusTable()
        self.episode_data = self.strack.episodeTable()
        self.session_data = self.strack.sessionTable()
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def refeshWorkList(self):
            self.workListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)

    def refeshPubilshList(self):
            self.pubilshListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)

    def additem_init(self):
        for item in self.project_data:
            self.asset_proj_selector.addItem(item.get('code'))
            self.shot_proj_selector.addItem(item.get('code'))
            self.level_proj_selector.addItem(item.get('code'))

    def list_file(self, path):
        temp_list = []
        fs = os.listdir(path)
        if fs:
            for obj in fs:
                tmp_path = os.path.join(path, obj)
                if not os.path.isdir(tmp_path):
                    temp_list.append(obj)
        return temp_list

    def todayFilter(self):
        temp = str(datetime.datetime.now()).split(' ')[0] + ' 23:59:00'
        self.deadline = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def weekFilter(self):
        print(self.deadline)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def monthFilter(self):
        self.deadline =self.now + datetime.timedelta(days=30)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def deadlineCheck(self,item):
        if item.get('end_time'):
            self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
        else:
            self.endTime = self.now + datetime.timedelta(days=6)
        return self.endTime < self.deadline

    def refeshAssetTree(self):
        word = self.AssetSearchText.text()
        self.asset_treeWidget.clear()
        self.asset_treeWidget.hideColumn(0)
        self.asset_treeWidget.setColumnWidth(1, 80)
        self.asset_treeWidget.setColumnWidth(2,170)
        self.asset_treeWidget.setColumnWidth(3, 55)
        self.asset_treeWidget.setColumnWidth(4, 45)
        self.asset_treeWidget.setColumnWidth(7, 60)
        assetType,step,proj,status= '','','',''
        if self.asset_type_selector.currentIndex():
            assetType = self.asset_type_selector.currentText()
        if self.asset_step_selector.currentIndex():
            step = self.asset_step_selector.currentText()
        if self.asset_proj_selector.currentIndex():
            proj = self.asset_proj_selector.currentText()
        if self.asset_status_selector.currentIndex():
            status = self.asset_status_selector.currentText()
        for i,item in enumerate(self.asset_data):
            if item.get('json'):
                status_name = self.dataIdSelect(self.status_data,item.get('status_id')).get('name')
                if (re.search(word,item.get('json').get('asset_code')) or re.search(word,item.get('json').get('asset_name')))\
                        and re.search(assetType, item.get('json').get('asset_type_code')) \
                        and re.search(step, item.get('json').get('step_code')) \
                        and re.search(proj, item.get('json').get('project_code')) \
                        and re.search(status, status_name) \
                        and self.deadlineCheck(item) \
                        and self.excoutorCheck(item):
                    child = QtWidgets.QTreeWidgetItem(self.asset_treeWidget)
                    child.setText(0, str(item.get('id')))
                    child.setText(1, status_name)
                    child.setIcon(1, QtGui.QIcon('%s/images/%s' % (self.local_path,
                                                                   self.strack.exrStatusIcon.get(
                                                                       item.get('json').get('exrStatus', 'work')))))
                    child.setText(2, item.get('json').get('task_name'))
                    if item.get('executor'):
                        child.setText(3, item.get('executor')[0].get('name'))
                    child.setText(4, item.get('duration'))
                    child.setText(5, item.get('start_time'))
                    child.setText(6, item.get('end_time'))
                    child.setText(7, item.get('json').get('asset_type_name'))
                    child.setText(8, item.get('json').get('project_name'))
                    if i%15==0:
                        QtWidgets.QApplication.processEvents()
    def refeshShotTree(self):
        if not self.refeshShotTreeLock:
            word = self.ShotSearchText.text()
            self.shot_treeWidget.clear()
            self.shot_treeWidget.hideColumn(0)
            self.shot_treeWidget.setColumnWidth(1, 80)
            self.shot_treeWidget.setColumnWidth(2, 60)
            self.shot_treeWidget.setColumnWidth(3, 60)
            self.shot_treeWidget.setColumnWidth(4, 60)
            self.shot_treeWidget.setColumnWidth(5, 100)
            self.shot_treeWidget.setColumnWidth(6, 60)
            self.shot_treeWidget.setColumnWidth(7, 50)
            proj, step,episode,session,status= '', '', '','',''
            if self.shot_step_selector.currentIndex():
                step = self.shot_step_selector.currentText()
            if self.shot_proj_selector.currentIndex():
                proj = self.shot_proj_selector.currentText()
            if self.shot_episode_selector.currentIndex():
                episode = self.shot_episode_selector.currentText()
            if self.shot_session_selector.currentIndex():
                session = self.shot_session_selector.currentText()
            if self.shot_status_selector.currentIndex():
                status = self.shot_status_selector.currentText()
            for i,item in enumerate(self.shot_data):
                if item.get('json'):
                    status_name = self.dataIdSelect(self.status_data, item.get('status_id')).get('name')
                    if (re.search(word,item.get('json').get('sequence_name')) or re.search(word,item.get('json').get('sequence_code'))) \
                            and re.search(step, item.get('json').get('step_code')) \
                            and re.search(proj, item.get('json').get('project_code')) \
                            and re.search(episode, item.get('json').get('episode_code')) \
                            and re.search(session, item.get('json').get('session_code')) \
                            and re.search(status, status_name) \
                            and self.deadlineCheck(item) \
                            and self.excoutorCheck(item):
                        child = QtWidgets.QTreeWidgetItem(self.shot_treeWidget)
                        child.setText(0, str(item.get('id')))
                        child.setText(1, status_name)
                        child.setIcon(1, QtGui.QIcon('%s/images/%s'%(self.local_path,
                                         self.strack.exrStatusIcon.get(item.get('json').get('exrStatus','work')))))
                        child.setText(2, item.get('json').get('episode_name'))
                        child.setText(3, item.get('json').get('session_name'))
                        child.setText(4, item.get('json').get('sequence_name'))
                        child.setText(5, item.get('json').get('task_name'))
                        if item.get('executor'):
                            child.setText(6, item.get('executor')[0].get('name'))
                        child.setText(7, item.get('duration'))
                        child.setText(8, item.get('start_time'))
                        child.setText(9, item.get('end_time'))
                        child.setText(10, item.get('json').get('project_name'))
                        if i%15==0:
                            QtWidgets.QApplication.processEvents()
    def refeshLevelTree(self):
        word = self.LevelSearchText.text()
        self.level_treeWidget.clear()
        self.level_treeWidget.hideColumn(0)
        self.level_treeWidget.setColumnWidth(1, 80)
        self.level_treeWidget.setColumnWidth(2, 100)
        self.level_treeWidget.setColumnWidth(3, 60)
        self.level_treeWidget.setColumnWidth(4, 50)
        proj, step,status= '', '',''
        if self.level_step_selector.currentIndex():
            step = self.level_step_selector.currentText()
        if self.level_proj_selector.currentIndex():
            proj = self.level_proj_selector.currentText()
        if self.level_status_selector.currentIndex():
            status = self.level_status_selector.currentText()
        for i,item in enumerate(self.level_data):
            if item.get('json'):
                status_name = self.dataIdSelect(self.status_data, item.get('status_id')).get('name')
                if (re.search(word,item.get('json').get('level_code')) or re.search(word,item.get('json').get('level_name')))\
                        and re.search(step, item.get('json').get('step_code')) \
                        and re.search(proj, item.get('json').get('project_code')) \
                        and re.search(status, status_name) \
                        and self.deadlineCheck(item) \
                        and self.excoutorCheck(item):
                    child = QtWidgets.QTreeWidgetItem(self.level_treeWidget)
                    child.setText(0, str(item.get('id')))
                    child.setText(1, status_name)
                    child.setIcon(1, QtGui.QIcon('%s/images/%s' % (self.local_path,
                                                                   self.strack.exrStatusIcon.get(
                                                                       item.get('json').get('exrStatus', 'work')))))
                    child.setText(2, item.get('json').get('task_name'))
                    if item.get('executor'):
                        child.setText(3, item.get('executor')[0].get('name'))
                    child.setText(4, item.get('duration'))
                    child.setText(5, item.get('start_time'))
                    child.setText(6, item.get('end_time'))
                    child.setText(7, item.get('json').get('project_name'))
                    if i%10==0:
                        QtWidgets.QApplication.processEvents()

    def assetOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.asset_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.asset_treeWidget.selectedItems():
                print(self.asset_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.asset_data, id))

    def shotOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        createSequence = menu.addAction("创建动画序列")
        action = menu.exec_(self.shot_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                if item.get('json').get('step_code') == 'layout':
                    orgPath = item.get('json').get('Publish_path').replace('layout', 'mocap')
                    root = ET.parse(orgPath + '/Description.xml').getroot()
                    for elem in root.iter():
                        if elem.tag == 'SkeletalAnimation':
                            self.mobu.mergeFile(elem.attrib.get('Path'))
        if action == createSequence:
            if self.shot_proj_selector.currentText() and self.shot_episode_selector.currentText() and self.shot_session_selector.currentText():
                projId = self.projCodeToItem(str(self.shot_proj_selector.currentText())).get('id')
                episode = self.findEpisode(str(self.shot_episode_selector.currentText()), projId)
                session = self.findSession(str(self.shot_session_selector.currentText()), projId, episode.get('id'))
                count = self.getSequenceLen(projId,session.get('id'))
                ok = QtWidgets.QMessageBox.question(self, '对话框', u'将要创建序列: %s %s 第%s序'%(episode.get('name'),session.get('name'),count),
                                                    QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                if ok.name == 'FirstButton':
                    data = {
                        'project_id': projId,
                        'code': 'seq%s'%count,
                        'name': '第%s序'%count,
                        'parent_id': session.get('id'),
                        'module_id': 58
                    }
                    self.strack.st.create('sequence',data)
    def server_win(self):
        self.serverWin = QWebEngineView()
        self.serverWin.load(QUrl("http://%s:5000"%node_server))
        self.serverWin.show()
        self.serverWin.setFixedSize(1400, 750)
    def levelOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.level_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.level_treeWidget.selectedItems():
                print(self.level_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.level_data, id))
    def workOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        openAction = menu.addAction("打开文件")
        mergeAction = menu.addAction("合并文件")
        replaceAction = menu.addAction("替换文件")
        opendir = menu.addAction("打开目录")
        action = menu.exec_(self.workListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('task_code')
                file_name = '%s_V##.fbx'%code
                check_name = '%s_V\d\d.fbx'%code
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本序号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s'%(item.get('json').get('Work_path'),str(my_str))
                    self.mobu.saveFile(newpath)
                    self.refeshWorkList()

            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                proj = item.get('json').get('project_code')
                episode = item.get('json').get('episode_code')
                session = item.get('json').get('session_code')
                sequence = item.get('json').get('sequence_code')
                newpath = '%s/%s_%s_%s_%s.fbx'%(item.get('json').get('Work_path'),proj,episode,session,sequence)
                self.mobu.backUp(newpath)
                self.mobu.saveFile(newpath)
                self.refeshWorkList()
        if action == openAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
                        print(path)

            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                self.mobu.openFile(path)
        if action == mergeAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                self.mobu.mergeFile(path)
        if action == replaceAction:
            path = ''
            if self.workListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.workListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.workListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                self.mobu.replaceFile(path)
        if action == opendir:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                os.startfile(item.get('json').get('Work_path'))
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                os.startfile(item.get('json').get('Work_path'))
    def pubilshOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        publishAction = menu.addAction("发布版本")
        openAction = menu.addAction("打开文件")
        mergeAction = menu.addAction("合并文件")
        replaceAction = menu.addAction("替换文件")
        opendir = menu.addAction("打开目录")
        action = menu.exec_(self.pubilshListWidget.mapToGlobal(position))
        if action == publishAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('task_code')
                file_name = '%s_V##.fbx'%code
                check_name = '%s_V\d\d.fbx'%code
                my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本序号', QtWidgets.QLineEdit.Normal,file_name)
                if re.search(check_name, str(my_str)) and ok:
                    newpath = '%s/%s'%(item.get('json').get('Publish_path'),str(my_str))
                    self.mobu.saveFile(newpath)
                    self.refeshWorkList()
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                if self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    if item.get('json').get('step_code') == 'layout':
                        self.mobu.xml(item,self.asset_data)
                        dic = {'taskStatus': 'wait', 'TaskType': 'LayoutTask', 'XmlFile': item.get('json').get('Publish_path'),
                               'TaskId': item.get('uuid'), 'db': item.get('json').get('project_code')}
                        r_json = requests.post('http://%s:5000/ue/con?action=post' % self.taskServer, json.dumps(dic))
                        searcher = {'proj':item.get('json').get('project_code'),'entity_id':item.get('entity_id'),
                                    'step':'lighting'}
                        lightItem = self.findShotItem(self.shot_data,searcher)
                        if lightItem:
                            temp = lightItem.get('json')
                            temp['exrStatus'] = 'update'
                            filters = [['entity_id','is',lightItem.get('entity_id')],
                                       ['project_id', 'is', lightItem.get('project_id')],
                                       ['step_id', 'is', lightItem.get('step_id')]]
                            self.strack.st.update('base',filters,{'json':temp})
        if action == openAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Publish_path'),str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))

            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                self.mobu.openFile(path)
        if action == mergeAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Work_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                    id = self.shot_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.shot_data, id)
                    path = '%s/%s' % (
                    item.get('json').get('Work_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                self.mobu.mergeFile(path)
        if action == replaceAction:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s'%(item.get('json').get('Work_path'),str(self.pubilshListWidget.selectedItems()[0].text()))
                if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                        id = self.shot_treeWidget.selectedItems()[0].text(0)
                        item = self.dataIdSelect(self.shot_data, id)
                        path = '%s/%s' % (item.get('json').get('Work_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                self.mobu.replaceFile(path)
        if action == opendir:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                os.startfile(item.get('json').get('Publish_path'))
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                os.startfile(item.get('json').get('Publish_path'))
    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                    background-image:url('%s/images/04.jpg');
                }
                ''' % (self.local_path)
        self.refesh_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/03.jpg' % self.local_path)))
        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/12.jpg'%self.local_path)))
        self.min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/13.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/11.jpg);}' % self.local_path)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def showColor(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '对话框',
                                        '请输入你的名字:')

        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

class unrealWidget(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,myStrack,local_path):
        self.ue = UE()
        self.strack = myStrack
        self.local_path = local_path
        self.now = datetime.datetime.now()
        self.deadline = self.now + datetime.timedelta(days=300)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.refeshShotTreeLock = False
        self.close_button.clicked.connect(self.close)
        self.min_button.clicked.connect(self.showMinimized)
        self.asset_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.asset_treeWidget.customContextMenuRequested.connect(self.assetOpenMenu)
        self.shot_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shot_treeWidget.customContextMenuRequested.connect(self.shotOpenMenu)
        self.level_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.level_treeWidget.customContextMenuRequested.connect(self.levelOpenMenu)
        self.workListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workListWidget.customContextMenuRequested.connect(self.workOpenMenu)
        self.pubilshListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pubilshListWidget.customContextMenuRequested.connect(self.pubilshOpenMenu)
        self.AssetSearchText.textChanged.connect(self.refeshAssetTree)
        self.ShotSearchText.textChanged.connect(self.refeshShotTree)
        self.LevelSearchText.textChanged.connect(self.refeshLevelTree)
        self.asset_proj_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_type_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_step_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.asset_status_selector.currentIndexChanged.connect(self.refeshAssetTree)
        self.shot_episode_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_session_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_proj_selector.currentIndexChanged.connect(self.refeshShotEpisode)
        self.shot_episode_selector.currentIndexChanged.connect(self.refeshShotSession)
        self.shot_step_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.shot_status_selector.currentIndexChanged.connect(self.refeshShotTree)
        self.level_step_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_proj_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.level_status_selector.currentIndexChanged.connect(self.refeshLevelTree)
        self.asset_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.shot_treeWidget.itemClicked.connect(self.refeshWorkList)
        self.asset_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.shot_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.level_treeWidget.itemClicked.connect(self.refeshPubilshList)
        self.todayTaskBtn.clicked.connect(self.todayFilter)
        self.weekTaskBtn.clicked.connect(self.weekFilter)
        self.monthTaskBtn.clicked.connect(self.monthFilter)
        self.refesh_button.clicked.connect(self.refeshData)
        self.myTaskBtn.clicked.connect(self.myTask)
        self.allTaskBtn.clicked.connect(self.allTask)
        self.LinkServerBtn.clicked.connect(self.server_win)
        self.worker = ''
        self.dataInit()

    def dataInit(self):
        cacheFile = '//%s/LocalShare/teamones/cache.json'%public_disk
        if os.path.exists(cacheFile):
            cache = json.loads(open(cacheFile).read())
            self.asset_data = cache.get('asset_data')
            self.shot_data = cache.get('shot_data')
            self.level_data = cache.get('level_data')
            self.project_data = cache.get('project_data')
            self.status_data = cache.get('status_data')
            self.episode_data = cache.get('episode_data')
            self.session_data = cache.get('session_data')
            self.additem_init()
            self.refeshAssetTree()
            self.refeshShotTree()
            self.refeshLevelTree()

    def myTask(self):
        self.worker = self.strack.st.login_name
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def allTask(self):
        self.worker = ''
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def excoutorCheck(self,item):
        if self.worker:
            if item.get('executor'):
                if re.search(self.worker,item.get('executor')[0].get('login_name')):
                    return True
                else:
                    return False
        else:
            return True
    def refeshShotEpisode(self):
        self.refeshShotTreeLock = True
        self.shot_episode_selector.clear()
        self.shot_episode_selector.addItem(u' 集 数')
        projCode = self.shot_proj_selector.currentText()
        if self.shot_proj_selector.currentIndex()>0:
            for item in self.episode_data:
                if item.get('project_id') == self.projCodeToItem(projCode).get('id'):
                    self.shot_episode_selector.addItem(item.get('code'))
        self.refeshShotTreeLock = False
    def refeshShotSession(self):
        self.refeshShotTreeLock = True
        self.shot_session_selector.clear()
        self.shot_session_selector.addItem(u' 场 次')
        projCode = self.shot_proj_selector.currentText()
        episodeCode = self.shot_episode_selector.currentText()
        if self.shot_proj_selector.currentIndex()>0 and self.shot_episode_selector.currentIndex()>0:
            for item in self.session_data:
                if item.get('project_id') == self.projCodeToItem(projCode).get('id') \
                        and item.get('parent_id')== self.findEpisode(episodeCode,item.get('project_id')).get('id'):
                    self.shot_session_selector.addItem(item.get('code'))
        self.refeshShotTreeLock = False
    def refeshData(self):
        self.asset_data = self.strack.asset_task()
        self.shot_data = self.strack.shot_task()
        self.level_data = self.strack.level_task()
        self.project_data = self.strack.projectTable()
        self.status_data = self.strack.statusTable()
        self.episode_data = self.strack.episodeTable()
        self.session_data = self.strack.sessionTable()
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()

    def findEpisode(self,code,projId):
        for item in self.episode_data:
            if item.get('code') == code and item.get('project_id')==projId:
                return item

    def findSession(self,code,projId,parent_id):
        for item in self.session_data:
            if item.get('code') == code and item.get('project_id')==projId and item.get('parent_id')==parent_id:
                return item
    def getSequenceLen(self,project_id,parent_id):
        count =1
        for item in self.strack.st.select('sequence').get('rows'):
            if item.get('project_id') ==project_id and item.get('parent_id') ==parent_id:
                count+=1
        return count

    def projCodeToItem(self,code):
        for item in self.project_data:
            if item.get('code') == code:
                return item

    def refeshWorkList(self):
            self.workListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Work_path')):
                    self.workListWidget.addItem(each)

    def refeshPubilshList(self):
            self.pubilshListWidget.clear()
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.asset_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.shot_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)
            if self.module_tab.currentIndex() == 2 and self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                for each in self.list_file(self.dataIdSelect(self.level_data, id).get('json').get('Publish_path')):
                    self.pubilshListWidget.addItem(each)

    def additem_init(self):
        for item in self.project_data:
            self.asset_proj_selector.addItem(item.get('code'))
            self.shot_proj_selector.addItem(item.get('code'))
            self.level_proj_selector.addItem(item.get('code'))
    def list_file(self, path):
        temp_list = []
        fs = os.listdir(path)
        if fs:
            for obj in fs:
                tmp_path = os.path.join(path, obj)
                if not os.path.isdir(tmp_path):
                    temp_list.append(obj)
        return temp_list

    def todayFilter(self):
        temp = str(datetime.datetime.now()).split(' ')[0] + ' 23:59:00'
        self.deadline = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def weekFilter(self):
        self.deadline =self.now + datetime.timedelta(days=7)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def monthFilter(self):
        self.deadline =self.now + datetime.timedelta(days=30)
        self.refeshAssetTree()
        self.refeshShotTree()
        self.refeshLevelTree()
    def deadlineCheck(self,item):
        if item.get('end_time'):
            self.endTime = datetime.datetime.strptime(item.get('end_time'), "%Y-%m-%d %H:%M:%S")
        else:
            self.endTime = self.now + datetime.timedelta(days=6)
        return self.endTime < self.deadline
    def dataIdSelect(self,data,id):
        temp = {}
        for item in data:
            if item.get('id') ==int(id):
                temp = item
                break
        return temp
    def getFbx(self,path,word):
        for each in self.list_file(path):
            if re.search(word,each):
                return '%s/%s'%(path,each)
    def refeshAssetTree(self):
        word = self.AssetSearchText.text()
        self.asset_treeWidget.clear()
        self.asset_treeWidget.hideColumn(0)
        self.asset_treeWidget.setColumnWidth(1, 80)
        self.asset_treeWidget.setColumnWidth(2,170)
        self.asset_treeWidget.setColumnWidth(3, 55)
        self.asset_treeWidget.setColumnWidth(4, 45)
        self.asset_treeWidget.setColumnWidth(7, 60)
        assetType,step,proj,status= '','','',''
        if self.asset_type_selector.currentIndex():
            assetType = self.asset_type_selector.currentText()
        if self.asset_step_selector.currentIndex():
            step = self.asset_step_selector.currentText()
        if self.asset_proj_selector.currentIndex():
            proj = self.asset_proj_selector.currentText()
        if self.asset_status_selector.currentIndex():
            status = self.asset_status_selector.currentText()
        for i,item in enumerate(self.asset_data):
            if item.get('json'):
                status_name = self.dataIdSelect(self.status_data,item.get('status_id')).get('name')
                if (re.search(word,item.get('json').get('asset_code')) or re.search(word,item.get('json').get('asset_name')))\
                        and re.search(assetType, item.get('json').get('asset_type_code')) \
                        and re.search(step, item.get('json').get('step_code')) \
                        and re.search(proj, item.get('json').get('project_code')) \
                        and re.search(status, status_name) \
                        and self.deadlineCheck(item) \
                        and self.excoutorCheck(item):
                    child = QtWidgets.QTreeWidgetItem(self.asset_treeWidget)
                    child.setText(0, str(item.get('id')))
                    child.setText(1, status_name)
                    child.setIcon(1, QtGui.QIcon('%s/images/%s' % (self.local_path,
                                                                   self.strack.exrStatusIcon.get(
                                                                       item.get('json').get('exrStatus', 'work')))))
                    child.setText(2, item.get('json').get('task_name'))
                    if item.get('executor'):
                        child.setText(3, item.get('executor')[0].get('name'))
                    child.setText(4, item.get('duration'))
                    child.setText(5, item.get('start_time'))
                    child.setText(6, item.get('end_time'))
                    child.setText(7, item.get('json').get('asset_type_name'))
                    child.setText(8, item.get('json').get('project_name'))
                    if i%15==0:
                        QtWidgets.QApplication.processEvents()
    def refeshShotTree(self):
        if not self.refeshShotTreeLock:
            word = self.ShotSearchText.text()
            self.shot_treeWidget.clear()
            self.shot_treeWidget.hideColumn(0)
            self.shot_treeWidget.setColumnWidth(1, 80)
            self.shot_treeWidget.setColumnWidth(2, 60)
            self.shot_treeWidget.setColumnWidth(3, 60)
            self.shot_treeWidget.setColumnWidth(4, 60)
            self.shot_treeWidget.setColumnWidth(5, 100)
            self.shot_treeWidget.setColumnWidth(6, 60)
            self.shot_treeWidget.setColumnWidth(7, 50)
            proj, step,episode,session,status= '', '', '','',''
            if self.shot_step_selector.currentIndex():
                step = self.shot_step_selector.currentText()
            if self.shot_proj_selector.currentIndex():
                proj = self.shot_proj_selector.currentText()
            if self.shot_episode_selector.currentIndex():
                episode = self.shot_episode_selector.currentText()
            if self.shot_session_selector.currentIndex():
                session = self.shot_session_selector.currentText()
            if self.shot_status_selector.currentIndex():
                status = self.shot_status_selector.currentText()
            for i,item in enumerate(self.shot_data):
                if item.get('json'):
                    status_name = self.dataIdSelect(self.status_data, item.get('status_id')).get('name')
                    if (re.search(word,item.get('json').get('sequence_name')) or re.search(word,item.get('json').get('sequence_code'))) \
                            and re.search(step, item.get('json').get('step_code')) \
                            and re.search(proj, item.get('json').get('project_code')) \
                            and re.search(episode, item.get('json').get('episode_code')) \
                            and re.search(session, item.get('json').get('session_code')) \
                            and re.search(status, status_name) \
                            and self.deadlineCheck(item) \
                            and self.excoutorCheck(item):
                        child = QtWidgets.QTreeWidgetItem(self.shot_treeWidget)
                        child.setText(0, str(item.get('id')))
                        child.setText(1, status_name)
                        child.setIcon(1, QtGui.QIcon('%s/images/%s'%(self.local_path,
                                         self.strack.exrStatusIcon.get(item.get('json').get('exrStatus','work')))))
                        child.setText(2, item.get('json').get('episode_name'))
                        child.setText(3, item.get('json').get('session_name'))
                        child.setText(4, item.get('json').get('sequence_name'))
                        child.setText(5, item.get('json').get('task_name'))
                        if item.get('executor'):
                            child.setText(6, item.get('executor')[0].get('name'))
                        child.setText(7, item.get('duration'))
                        child.setText(8, item.get('start_time'))
                        child.setText(9, item.get('end_time'))
                        child.setText(10, item.get('json').get('project_name'))
                        if i%15==0:
                            QtWidgets.QApplication.processEvents()
    def refeshLevelTree(self):
        word = self.LevelSearchText.text()
        self.level_treeWidget.clear()
        self.level_treeWidget.hideColumn(0)
        self.level_treeWidget.setColumnWidth(1, 80)
        self.level_treeWidget.setColumnWidth(2, 100)
        self.level_treeWidget.setColumnWidth(3, 60)
        self.level_treeWidget.setColumnWidth(4, 50)
        proj, step,status= '', '',''
        if self.level_step_selector.currentIndex():
            step = self.level_step_selector.currentText()
        if self.level_proj_selector.currentIndex():
            proj = self.level_proj_selector.currentText()
        if self.level_status_selector.currentIndex():
            status = self.level_status_selector.currentText()
        for i,item in enumerate(self.level_data):
            if item.get('json'):
                status_name = self.dataIdSelect(self.status_data, item.get('status_id')).get('name')
                if (re.search(word,item.get('json').get('level_code')) or re.search(word,item.get('json').get('level_name')))\
                        and re.search(step, item.get('json').get('step_code')) \
                        and re.search(proj, item.get('json').get('project_code')) \
                        and re.search(status, status_name) \
                        and self.deadlineCheck(item) \
                        and self.excoutorCheck(item):
                    child = QtWidgets.QTreeWidgetItem(self.level_treeWidget)
                    child.setText(0, str(item.get('id')))
                    child.setText(1, status_name)
                    child.setIcon(1, QtGui.QIcon('%s/images/%s' % (self.local_path,
                                                                   self.strack.exrStatusIcon.get(
                                                                       item.get('json').get('exrStatus', 'work')))))
                    child.setText(2, item.get('json').get('task_name'))
                    if item.get('executor'):
                        child.setText(3, item.get('executor')[0].get('name'))
                    child.setText(4, item.get('duration'))
                    child.setText(5, item.get('start_time'))
                    child.setText(6, item.get('end_time'))
                    child.setText(7, item.get('json').get('project_name'))
                    if i%10==0:
                        QtWidgets.QApplication.processEvents()
    def assetOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入/更新")
        action = menu.exec_(self.asset_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.asset_treeWidget.selectedItems():
                print('here')
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                step = item.get('json').get('step_code')
                if step == 'texture':
                    import_task = StaticTextureMeshTask()
                    import_task.importAsset(item.get('json').get('Publish_path'))

    def shotOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入/更新")
        menu.addSeparator()
        createSequence = menu.addAction("创建动画序列")
        rewriteSequence = menu.addAction("重拍动画序列")
        action = menu.exec_(self.shot_treeWidget.mapToGlobal(position))
        if self.shot_treeWidget.selectedItems():
            if action == importAction:
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                if item.get('json').get('step_code') == 'lighting':
                    workPath = item.get('json').get('Work_path')
                    PublishPath = item.get('json').get('Publish_path')
                    pro = item.get('json').get('project_code')
                    ep = item.get('json').get('episode_code')
                    sc = item.get('json').get('session_code')
                    seq = item.get('json').get('sequence_code')
                    unrealContent = unreal.SystemLibrary.convert_to_absolute_path(unreal.Paths.project_content_dir())
                    path = '%s%s/shot_work/%s/%s/%s/lighting'%(unrealContent,pro,ep,sc,seq)
                    if os.path.exists('%s/Animation' % path):
                        tasks = []
                        if os.path.exists(PublishPath.replace('lighting','anim')+'/Description.xml'):
                            for anim in self.list_file('%s/Animation' % path):
                                anim = anim.split('.')[0]
                                assetPath = '/Game/%s/shot_work/%s/%s/%s/lighting/Animation/%s'%(pro,ep,sc,seq,anim)
                                animation_sequence = unreal.AnimSequence.cast(unreal.load_asset(assetPath))
                                skeleton = animation_sequence.get_editor_property('skeleton')
                                word = '%s_rig_%s'%(anim.split('_')[-3],anim.split('_')[-1])
                                fbx = self.getFbx(PublishPath.replace('lighting','anim'),word)
                                if fbx:
                                    tasks.append(self.ue.buildImportTask(fbx,'/Game/%s/shot_work/%s/%s/%s/lighting/Animation'%(pro,ep,sc,seq),
                                                                         anim,self.ue.buildAnimationImportOptions(skeleton)))
                        elif os.path.exists(PublishPath.replace('lighting', 'layout')+'/Description.xml'):
                            for anim in self.list_file('%s/Animation' % path):
                                anim = anim.split('.')[0]
                                assetPath = '/Game/%s/shot_work/%s/%s/%s/lighting/Animation/%s'%(pro,ep,sc,seq,anim)
                                animation_sequence = unreal.AnimSequence.cast(unreal.load_asset(assetPath))
                                skeleton = animation_sequence.get_editor_property('skeleton')
                                tasks.append(self.ue.buildImportTask('%s/%s.fbx'%(PublishPath.replace('lighting', 'layout'),anim),
                                                                     '/Game/%s/shot_work/%s/%s/%s/lighting/Animation'%(pro,ep,sc,seq),
                                                                     anim,self.ue.buildAnimationImportOptions(skeleton)))
                        self.ue.executeImportTasks(tasks)
                    elif not os.path.exists('%s/Animation'%path) and os.path.exists('%s/Animation'%workPath) :
                        shutil.copytree('%s/Animation'%workPath,'%s/Animation'%path)
                    if not os.path.exists('%s/sequencer'%path) and os.path.exists('%s/sequencer'%workPath):
                        shutil.copytree('%s/sequencer'%workPath,'%s/sequencer'%path)
                    if not os.path.exists('%s/shot_level' % path) and os.path.exists('%s/shot_level' % workPath):
                        shutil.copytree('%s/shot_level' % workPath, '%s/shot_level' % path)
                    temp = item.get('json')
                    temp['exrStatus'] = 'work'
                    filters = [['entity_id', 'is', item.get('entity_id')],
                               ['project_id', 'is', item.get('project_id')],
                               ['step_id', 'is', item.get('step_id')]]
                    self.strack.st.update('base', filters, {'json': temp})
            if action == rewriteSequence:
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                ok = QtWidgets.QMessageBox.question(self, '对话框', u'将要重拍序列: %s %s %s' % (
                item.get('json').get('episode_name'), item.get('json').get('session_name'), item.get('json').get('sequence_name')),
                                                    QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                if ok.name == 'FirstButton':
                    mocap_path = item.get('json').get('Publish_path')+'/'
                    mocap_part = '%s_%s_%s_%s' %(item.get('json').get('project_code'),item.get('json').get('episode_code'),
                                                 item.get('json').get('session_code'),item.get('json').get('sequence_code'))
                    mocap_session = mocap_module.mocap()
                    mocap_session.modify_ue_config(mocap_path, mocap_part)
        if action == createSequence:
            if self.shot_proj_selector.currentText() and self.shot_episode_selector.currentText() and self.shot_session_selector.currentText():
                projId = self.projCodeToItem(str(self.shot_proj_selector.currentText())).get('id')
                episode = self.findEpisode(str(self.shot_episode_selector.currentText()), projId)
                session = self.findSession(str(self.shot_session_selector.currentText()), projId, episode.get('id'))
                count = self.getSequenceLen(projId,session.get('id'))
                ok = QtWidgets.QMessageBox.question(self, '对话框', u'将要创建序列: %s %s 第%s序'%(episode.get('name'),session.get('name'),count),
                                                    QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                if ok.name == 'FirstButton':
                    data = {
                        'project_id': projId,
                        'code': 'seq%s'%count,
                        'name': '第%s序'%count,
                        'parent_id': session.get('id'),
                        'module_id': 58
                    }
                    self.strack.st.create('sequence',data)
                    mocap_path = 'P:/%s/shot_work/%s/%s/%s/mocap/Publish/' % (
                    str(self.shot_proj_selector.currentText()),
                    str(self.shot_episode_selector.currentText()),
                    str(self.shot_session_selector.currentText()),
                    'seq%s'%count)
                    mocap_part = '%s_%s_%s_%s' % (str(self.shot_proj_selector.currentText()),
                                                  str(self.shot_episode_selector.currentText()),
                                                  str(self.shot_session_selector.currentText()),
                                                  'seq%s' % count)

                    shot_level = '/Game/%s/shot_work/%s/%s/%s/mocap/Publish/ShotLevel/' % (
                    str(self.shot_proj_selector.currentText()),
                    str(self.shot_episode_selector.currentText()),
                    str(self.shot_session_selector.currentText()),
                    'seq%s' % count)
                    shot_level = shot_level + mocap_part
                    mocap_session = mocap_module.mocap()
                    mocap_session.modify_ue_config(mocap_path, mocap_part)
                    mocap_session.create_level(shot_level)
                    mocap_session.create_directory(mocap_path)

    def levelOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        importAction = menu.addAction("导入")
        updateAction = menu.addAction("更新")
        action = menu.exec_(self.level_treeWidget.mapToGlobal(position))
        if action == importAction:
            if self.level_treeWidget.selectedItems():
                print(self.level_treeWidget.selectedItems()[0].text(1))
        if action == updateAction:
            if self.level_treeWidget.selectedItems():
                id = self.level_treeWidget.selectedItems()[0].text(0)
                print(self.dataIdSelect(self.level_data, id))
    def server_win(self):
        self.serverWin = QWebEngineView()
        self.serverWin.load(QUrl("http://%s:5000"%node_server))
        self.serverWin.show()
        self.serverWin.setFixedSize(1400, 750)
    def workOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        openAction = menu.addAction("打开文件")
        opendir = menu.addAction("打开目录")
        action = menu.exec_(self.workListWidget.mapToGlobal(position))
        if action == openAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                pass

            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                proj = item.get('json').get('project_code')
                episode = item.get('json').get('episode_code')
                session = item.get('json').get('session_code')
                sequence = item.get('json').get('sequence_code')
                newpath = '%s/%s_%s_%s_%s.mb'%(item.get('json').get('Work_path'),proj,episode,session,sequence)
                mc.file(rename='C:/Users/Public/Documents/temp.mb')
                mc.file(save=1, defaultExtensions=False, type='mayaBinary')
                shutil.copyfile('C:/Users/Public/Documents/temp.mb', newpath)
                self.refeshWorkList()
        if action == opendir:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                os.startfile(item.get('json').get('Work_path'))
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                os.startfile(item.get('json').get('Work_path'))
    def pubilshOpenMenu(self,position):
        menu = QtWidgets.QMenu()
        saveAction = menu.addAction("保存版本")
        importSkeletalMesh = menu.addAction("导入骨骼资产")
        opendir = menu.addAction("打开目录")
        action = menu.exec_(self.workListWidget.mapToGlobal(position))
        if action == saveAction:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                code = item.get('json').get('asset_code')
                step = item.get('json').get('step_code')
                pass
        if action == opendir:
            if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                id = self.asset_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.asset_data, id)
                os.startfile(item.get('json').get('Publish_path'))
            if self.module_tab.currentIndex() == 1 and self.shot_treeWidget.selectedItems():
                id = self.shot_treeWidget.selectedItems()[0].text(0)
                item = self.dataIdSelect(self.shot_data, id)
                os.startfile(item.get('json').get('Publish_path'))
        if action == importSkeletalMesh:
            path = ''
            if self.pubilshListWidget.selectedItems():
                if self.module_tab.currentIndex() == 0 and self.asset_treeWidget.selectedItems():
                    id = self.asset_treeWidget.selectedItems()[0].text(0)
                    item = self.dataIdSelect(self.asset_data, id)
                    path = '%s/%s' % (item.get('json').get('Publish_path'), str(self.pubilshListWidget.selectedItems()[0].text()))
            else:
                path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
            if path:
                tasks = [self.ue.buildImportTask(path,'/Game%s'%(os.path.dirname(path).replace('\\', '/').split(':')[1]),
                                                 '',self.ue.buildSkeletalMeshImportOptions())]
                self.ue.executeImportTasks(tasks)
    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                    background-image:url('%s/images/04.jpg');
                }
                ''' % (self.local_path)
        self.refesh_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/03.jpg'%self.local_path)))
        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/12.jpg'%self.local_path)))
        self.min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/13.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/11.jpg);}' % self.local_path)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def showColor(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.setStyleSheet(self.style + "#window{background:%s}" % col.name())

    def showDialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '对话框','请输入你的名字:')
        if ok:
            self.linet1.setText(str(text))

    def showFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.readline()
                self.linet1.setText(data)

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

class MyLogin(QtWidgets.QMainWindow,Ui_Form):
    def __init__(self):
        self.local_path = os.path.dirname(__file__).replace('\\','/')
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setIcon()
        self.set_style()
        self.remember()
        self.login_close_button.clicked.connect(self.close)
        self.login_min_button.clicked.connect(self.showMinimized)
        self.login_pushButton.clicked.connect(self.login)
    def remember(self):
        if os.path.exists('C:/Users/Public/Documents/user.txt'):
            self.usename_lineEdit.setText(open('C:/Users/Public/Documents/user.txt').read().split(' ')[0])
            self.password_lineEdit.setText(open('C:/Users/Public/Documents/user.txt').read().split(' ')[1])

    def login(self):
        user = self.usename_lineEdit.text()
        password = self.password_lineEdit.text()
        if self.login_checkBox.isChecked():
            with open('C:/Users/Public/Documents/user.txt', 'w') as fileobject:
                fileobject.write(str(user) + ' ' + str(password))
                fileobject.close()
        myStrack = None
        software = self.software_selector.currentText()
        try:
            myStrack = strack("https://strack.teamones.com/", user, password)
        except:
            QtWidgets.QMessageBox.warning(self,u"提示", u"用户名或密码错误")
        if myStrack:
            self.hide()
            if software == 'Unreal':
                self.window = unrealWidget(myStrack, self.local_path)
                self.window.show()
                self.window.setFixedSize(950, 600)
            if software == 'Maya':
                self.window = mayaWidget(myStrack,self.local_path)
                self.window.show()
                self.window.setFixedSize(950, 600)
            if software == 'Motionbuilder':
                self.window = mobuWidget(myStrack, self.local_path)
                self.window.show()
                self.window.setFixedSize(950, 600)
    def set_style(self):
        style = '''
                #login_pushButton{
                    border-radius:5px;
                }
                '''
        # self.login_pushButton.setStyleSheet(style)
        self.login_pushButton.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/04.jpg' % self.local_path)))
        self.login_close_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/09.jpg' % self.local_path)))
        self.login_min_button.setIcon(QtGui.QIcon(QtGui.QPixmap('%s/images/08.jpg' % self.local_path)))
        self.setStyleSheet('QMainWindow{border-image :url(%s/images/zhhy02.png);}' % self.local_path)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def setIcon(self):
        appIcon = QtGui.QIcon('%s/images/Icon128.png'%self.local_path)
        self.setWindowIcon(appIcon)

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        # this must excu or will crash
        app = QtWidgets.QApplication(sys.argv)
    log = MyLogin()
    log.show()
    log.setFixedSize(400, 320)
    sys.exit(app.exec_())
