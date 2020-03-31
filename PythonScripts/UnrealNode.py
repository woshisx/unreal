# -*- coding: UTF-8 -*-
import os,re,shutil,json,random,threading,socket,sys,time,requests
from datetime import datetime, timedelta
import unreal

class StaticTextureMeshTask:
    def __init__(self):
        self.MaterialLoaderData = 'I:\\svnDir\\ue422_epic_1\\Engine\\Plugins\\zhuohua\\CGGameWork\\Content\\MaterialLoaderData.xml'
        self.Material_Template = '/Game/Game/Game_Resources/MapsResources/PublicResources/Materiral_Template/PBR_Mat_Template/Mat_Master/PMat'
        self.MaterialsTemplateArr = []
    # def CreateInstanceOfMaterial(materialFileName,newAssetName,destination_path,_textureTargetNameList,textureFileNameList):
    def CreateInstanceOfMaterial(self,materialFileName, newAssetName, destination_path, textureFileNameList):
        selectedAsset = unreal.load_asset(materialFileName)
        # newAssetName = ""
        # newAssetName = selectedAsset.get_name() + "_%s"
        # "_%s_%d"
        asset_import_task = unreal.AssetImportTask()
        asset_import_task.set_editor_property("save", True)
        asset_import_task.set_editor_property("automated", True)
        asset_import_task.set_editor_property("replace_existing", True)
        factory = unreal.MaterialInstanceConstantFactoryNew()
        factory.set_editor_property("asset_import_task", asset_import_task)
        factory.set_editor_property("create_new", True)
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        # createdAssetsPath = materialFileName.replace(selectedAsset.get_name(), "-")
        # createdAssetsPath = createdAssetsPath.replace("-.-", "")newAssetName %("inst")
        newAsset = asset_tools.create_asset(newAssetName, destination_path, None, factory)
        unreal.MaterialEditingLibrary.set_material_instance_parent(newAsset, selectedAsset)
        for MaterialsTemplate in self.MaterialsTemplateArr:
            if (newAssetName.find(MaterialsTemplate['mat_Inst'].split("_")[0]) != -1):
                for textureFileName in textureFileNameList:
                    # print "newAssetName::"+newAssetName+"  MaterialsTemplate.mat_Inst::"+MaterialsTemplate.mat_Inst+"  textureFileName::"+textureFileName+"  "
                    for Minslot in MaterialsTemplate['Minslots']:
                        if (textureFileName.find(Minslot) != -1):
                            texture_asset = unreal.Texture.cast(unreal.load_asset(textureFileName))
                            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(newAsset, Minslot,
                                                                                                        texture_asset)
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

    def resetStaticMeshMaterial(self,package_path):
        # def __init__(self, package_names=[], package_paths=[], object_paths=[], class_names=[], recursive_classes_exclusion_set=[], recursive_paths=False, recursive_classes=False, include_only_on_disk_assets=False):
        filter_staticmesh = unreal.ARFilter([], [package_path], [], [unreal.StaticMesh.static_class().get_name()])
        filter_materialIns = unreal.ARFilter([], [package_path], [],
                                             [unreal.MaterialInstanceConstant.static_class().get_name()])
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        MaterialInsDataArr = AssetRegistry.get_assets(filter_materialIns)
        StaticMeshAssetDataArr = AssetRegistry.get_assets(filter_staticmesh)
        for StaticMeshAssetData in StaticMeshAssetDataArr:
            # print StaticMeshAssetData
            StaticMeshStr = str(StaticMeshAssetData.package_name)
            # print StaticMeshStr
            StaticMeshAsset = unreal.StaticMesh.cast(unreal.load_asset(StaticMeshStr))
            if (StaticMeshAsset != None):
                for MaterialInsData in MaterialInsDataArr:
                    # print MaterialInsData.asset_name
                    materialIndex = StaticMeshAsset.get_material_index(MaterialInsData.asset_name)
                    if (materialIndex != -1):
                        MaterialInsStr = str(MaterialInsData.package_name)
                        targetMaterial = unreal.MaterialInstance.cast(unreal.load_asset(MaterialInsStr))
                        StaticMeshAsset.set_material(materialIndex, targetMaterial)
                        print MaterialInsStr
                    # print materialIndex


    def resetSkeletonMeshMaterial(self,package_path):
        # def __init__(self, package_names=[], package_paths=[], object_paths=[], class_names=[], recursive_classes_exclusion_set=[], recursive_paths=False, recursive_classes=False, include_only_on_disk_assets=False):
        filter_skeletalMesh = unreal.ARFilter([], [package_path], [], [unreal.SkeletalMesh.static_class().get_name()])
        filter_materialIns = unreal.ARFilter([], [package_path], [],
                                             [unreal.MaterialInstanceConstant.static_class().get_name()])
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        MaterialInsDataArr = AssetRegistry.get_assets(filter_materialIns)
        SkeletalMeshAssetDataArr = AssetRegistry.get_assets(filter_skeletalMesh)

        for SkeletalMeshAssetData in SkeletalMeshAssetDataArr:
            # print StaticMeshAssetData
            SkeletalMeshStr = str(SkeletalMeshAssetData.package_name)
            # print StaticMeshStr
            SkeletalMeshAsset = unreal.SkeletalMesh.cast(unreal.load_asset(SkeletalMeshStr))
            materials = SkeletalMeshAsset.materials
            if (SkeletalMeshAsset != None):
                for MaterialInsData in MaterialInsDataArr:
                    # print MaterialInsData.asset_name
                    materialIndex = SkeletalMeshAsset.get_material_index(MaterialInsData.asset_name)
                    if (materialIndex != -1):
                        MaterialInsStr = str(MaterialInsData.package_name)
                        targetMaterial = unreal.MaterialInstance.cast(unreal.load_asset(MaterialInsStr))
                        # SkeletalMeshAsset.set_material(materialIndex,targetMaterial)
                        for SkeletalMeshMaterialIndex in range(materials):
                            if (materials[
                                SkeletalMeshMaterialIndex].imported_material_slot_name == MaterialInsData.asset_name):
                                targetSkeltalMaterial = unreal.SkeletalMaterial(targetMaterial, materials[
                                    SkeletalMeshMaterialIndex].material_slot_name(), materials[
                                                                                    SkeletalMeshMaterialIndex].uv_channel_data())
                                materials[SkeletalMeshMaterialIndex] = targetSkeltalMaterial
                        print MaterialInsStr
                    # print materialIndex


    def buildImportTask(self,filename, destination_path, options=None):
        task = unreal.AssetImportTask()
        # task = unreal.AutomatedAssetImportData()
        task.set_editor_property('automated', True)
        task.set_editor_property('destination_name', '')
        task.set_editor_property('destination_path', destination_path)
        task.set_editor_property('filename', filename)
        task.set_editor_property('replace_existing', True)
        task.set_editor_property('save', True)
        # task.set_editor_property('skip_read_only',True)
        task.set_editor_property('options', options)
        return task


    def executeImportTasks(self,tasks):
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
        for task in tasks:
            for path in task.get_editor_property('imported_object_paths'):
                print 'Imported: %s' % path


    def buildTextureImportOptions(self):
        options = unreal.TextureFactory()
        options.set_editor_property('create_material', False)
        return options


    def buildStaticMeshImportOptions(self):
        options = unreal.FbxImportUI()
        static_mesh_import_data = unreal.FbxStaticMeshImportData()
        static_mesh_import_data.set_editor_property('combine_meshes', False)
        options.set_editor_property('import_mesh', True)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_as_skeletal', False)

        # options.static_mesh_import_data.set_edtitor_property('import_translation')
        # options.static_mesh_import_data.set_edtitor_property('import_rotation')
        # options.static_mesh_import_data.set_edtitor_property('import_uniform_scale')
        options.set_editor_property('static_mesh_import_data', static_mesh_import_data)

        # options.static_mesh_import_data.set_edtitor_property('generate_lightmap_u_v')
        # options.static_mesh_import_data.set_edtitor_property('generate_lightmap')
        return options


    def buildSkeletalMeshImportOptions(self):
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
        # SkeletalMeshImportData->bImportAsScene = false;
        options = unreal.FbxImportUI()

        options.set_editor_property('skeletal_mesh_import_data', skeletal_mesh_import_data)
        options.set_editor_property('import_mesh', True)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_as_skeletal', True)
        options.set_editor_property('skeleton', None)
        # options.skeletal_mesh_import_data.set_edtitor_property('import_translation')
        # options.skeletal_mesh_import_data.set_edtitor_property('import_rotation')
        # options.skeletal_mesh_import_data.set_edtitor_property('import_uniform_scale')

        # options.skeletal_mesh_import_data.set_edtitor_property('combine_meshes',False)
        # options.skeletal_mesh_import_data.set_edtitor_property('generate_lightmap_u_v')
        # options.skeletal_mesh_import_data.set_edtitor_property('generate_lightmap')
        return options


    def refreshIMGAsset(self,IMGFileName):
        # Get texture
        texture_asset = unreal.Texture.cast(unreal.load_asset(IMGFileName))
        texture_asset_str = texture_asset.get_name()
        if (texture_asset_str.find("BaseColor") != -1 or texture_asset_str.find("BentNormal") != -1):
            texture_asset.srgb = True
        else:
            texture_asset.srgb = False
        # unreal.ImportSubsystem.on_asset_reimport(texture_asset)


    def importIMGAsset(self,IMGList, destination_path):
        #  print "pwd=" + os.path.abspath('.')
        taskList = []
        clearNameList = []
        for IMG_FileName in IMGList:
            taskList.append(self.buildImportTask(IMG_FileName, destination_path, self.buildTextureImportOptions()))
            clearNameList.append(os.path.splitext(os.path.basename(IMG_FileName))[0])
        self.executeImportTasks(taskList)

        gamePath = destination_path.replace(".", "_")
        for clearName in clearNameList:
            texutureFileName = gamePath + "/" + clearName + ""
            print 'texutureFileName::: ' + texutureFileName + "  :::"
            self.refreshIMGAsset(texutureFileName)


    def importStaticMesh(self,MeshFileName, destination_path):
        taskList = []
        taskList.append(self.buildImportTask(MeshFileName, destination_path, self.buildStaticMeshImportOptions()))
        self.executeImportTasks(taskList)


    def importSkeletalMesh(self,MeshFileName, destination_path):
        taskList = []
        taskList.append(self.buildImportTask(MeshFileName, destination_path, self.buildSkeletalMeshImportOptions()))
        self.executeImportTasks(taskList)


    # def importMeshAsset():
    #     static_mesh_fbx = 'I:\\unrealwork\\test424BP\\pyscripts\\SM_StatocMesh.FBX'
    #     skeletal_mesh_fbx = 'I:\\unrealwork\\test424BP\\pyscripts\\SM_skeletal.FBX'
    #     static_mesh_task = buildImportTask(static_mesh_fbx,'/Game/StaticMeshes')
    #     skeletal_mesh_task = buildImportTask(skeletal_mesh_fbx,'/Game/SkeletalMeshes')
    #     executeImportTasks([static_mesh_task,skeletal_mesh_task])

    def importAsset(self,targetDir):
        import xml.etree.ElementTree as ET
        MaterialLoaderData = ET.parse(self.MaterialLoaderData).getroot()

        # print textureTargetNameList

        textureTargetNameList = []
        for elem in MaterialLoaderData.iter():
            # print elem.tag
            if (elem.tag == "textureTargetNameList"):
                for elem_tex in elem.iter():
                    # print elem_tex.tag
                    textureTargetNameList.append(elem_tex.tag)

            if (elem.tag == "MaterialsTemplate"):
                for elem_Inst in elem.iter():
                    if (elem_Inst.tag.find("_Inst") != -1):
                        mat_Inst = str(elem_Inst.tag)
                        Minslots = []
                        for each in list(elem_Inst):
                            for Minslot in list(each):
                                Minslots.append(str(Minslot.tag))
                        self.MaterialsTemplateArr.append({'mat_Inst':mat_Inst,'Minslots':Minslots})

        # targetDir = 'M:\\DLQ2\\asset_work\\props\\hw\\Model\\texture\\publish'

        root = ET.parse(targetDir + '\\Description.xml').getroot()
        picList = []
        destination_path = str("/" + targetDir.replace('M:', "Game")).replace("\\", "/")
        importType = 0
        # print os.path.exists('M:\\DLQ2\\asset_work\\props\\hw\\Model\\texture\\publish\\Description.xml')
        # print root,root.tag, root.attrib
        # for child_of_root in root:
        #     print child_of_root.tag, child_of_root.attrib
        for elem in root.iter():
            # print elem.tag, elem.attrib
            if (elem.tag == "Pic"):
                Pic_Path = elem.attrib.get('Path')
                # print Pic_Path
                picList.append(Pic_Path)
                # destination_path = "/"+os.path.dirname(Pic_Path).replace('M:',"Game")
            elif (elem.tag == "StaticMesh"):
                importType = 1
            elif (elem.tag == "SkeletalMesh"):
                importType = 2

        # print "importType" + str(importType)
        self.importIMGAsset(picList, destination_path)
        EditorAssetLibrary = unreal.EditorAssetLibrary()
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        # print "destination_path.replace" + destination_path
        if not EditorAssetLibrary.does_directory_exist(destination_path):
            EditorAssetLibrary.make_directory(destination_path)

        AssetRegistryDataArr = AssetRegistry.get_assets_by_path(destination_path)
        texArr = []
        # print AssetRegistryDataArr
        for AssetRegistryData in AssetRegistryDataArr:
            # print AssetRegistryData.package_name
            # print 'AssetRegistryData.package_name '+ AssetRegistryData.package_name
            texArr.append(str(AssetRegistryData.package_name))
        # print destination_path
        # print texArr

        for elem in root.iter():
            if (elem.tag == "Material"):
                Material_matName = elem.attrib.get('matName')
                # print "Material_matName::  "+Material_matName
                Material_TemplateList = self.Material_Template.split("/")
                if (Material_matName.find(Material_TemplateList[-1]) != -1):
                    # destination_path = "/"+os.path.dirname(Pic_Path).replace('M:',"Game")
                    Pic_destination_path = "/" + os.path.dirname(Pic_Path).replace('M:', "Game")
                    # CreateInstanceOfMaterial(Material_Template,Material_matName,Pic_destination_path,textureTargetNameList,texArr)
                    self.CreateInstanceOfMaterial(self.Material_Template, Material_matName, Pic_destination_path, texArr)
                    pass
        MeshFileName = ""
        for f in os.listdir(targetDir):
            # print f
            if (f.find(".fbx") != -1):
                MeshFileName = targetDir + "\\" + f
        # print MeshFileName

        if importType == 1:
            package_path = "/" + os.path.dirname(targetDir).replace('M:', "Game")
            package_path = package_path.replace(".", "_")
            EditorAssetLibrary = unreal.EditorAssetLibrary()
            if (EditorAssetLibrary.does_directory_exist(package_path)):
                EditorAssetLibrary.delete_directory(package_path)

            self.importStaticMesh(MeshFileName, destination_path)
            # get_material_index
            self.resetStaticMeshMaterial(
                package_path)  # '/Game/DLQ2/asset_work/props/hw/Model/texture/publish/image/hw_Texture_V01_fbx'
            unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
            pass
        elif importType == 2:
            package_path = "/" + os.path.dirname(targetDir).replace('M:', "Game")
            package_path = package_path.replace(".", "_")
            EditorAssetLibrary = unreal.EditorAssetLibrary()
            if (EditorAssetLibrary.does_directory_exist(package_path)):
                EditorAssetLibrary.delete_directory(package_path)

            self.importSkeletalMesh(MeshFileName, destination_path)
            self.resetSkeletonMeshMaterial(
                package_path)  # '/Game/DLQ2/asset_work/props/hw/Model/texture/publish/image/hw_Texture_V01_fbx'
            unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
            pass

        # print destination_path
        pass

class ImportShotsTools:
    # '自动导入镜头'

    def __init__(self):
        pass

    def __del__(self):
        pass

    def spawnAnimInTargetWorld(self, animationStr):
        # animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animationStr))
        animation_asset = unreal.AnimationAsset.cast(unreal.load_asset(animationStr))
        skeleton = unreal.Skeleton.cast(animation_asset.get_editor_property('skeleton'))
        EditorLevelLibrary = unreal.EditorLevelLibrary()
        # EditorLevelLibrary.spawn_actor_from_object()
        # world = EditorLevelLibrary.get_editor_world()
        # world = unreal.World.cast(unreal.load_asset(worldStr))
        # unreal.GameplayStatics.begin
        anim_class = unreal.SkeletalMeshActor.static_class()
        anim_location = unreal.Vector(0, 0, 0)
        # anim_rotation = unreal.Rotator(0,0,0)
        # anim_scale =  unreal.Vector(1.0,1.0,1.0)
        actor = EditorLevelLibrary.spawn_actor_from_class(anim_class, anim_location)
        anim_actor = unreal.SkeletalMeshActor.cast(actor)
        SingleAnimationPlayData = unreal.SingleAnimationPlayData()
        SingleAnimationPlayData.set_editor_property('anim_to_play', animation_asset)
        skeletal_mesh_component = unreal.SkeletalMeshComponent.cast(
            anim_actor.get_editor_property('skeletal_mesh_component'))
        # skeletal_mesh_component.set_editor_property('skeletal_mesh',skeletal_mesh)
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        AssetRegistryDataArr = AssetRegistry.get_assets_by_class(unreal.SkeletalMesh.static_class().get_name())
        # SkeletonAssets = []
        skeletalMesh_asset = None
        for AssetRegistryData in AssetRegistryDataArr:
            # if str(AssetRegistryData.package_name).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1 :
            skeletalMesh_asset = unreal.SkeletalMesh.cast(unreal.load_asset(AssetRegistryData.package_name))
            if skeletalMesh_asset.skeleton == skeleton:
                skeletal_mesh_component.set_editor_property('skeletal_mesh', skeletalMesh_asset)
                break

        skeletal_mesh_component.set_editor_property('animation_mode', unreal.AnimationMode.ANIMATION_SINGLE_NODE)
        skeletal_mesh_component.set_editor_property('animation_data', SingleAnimationPlayData)
        return anim_actor

    def spawnSequencerInTargetWorld(self, SequenceName, destination_path, StartFrame, EndFrame):
        factory = unreal.LevelSequenceFactoryNew()
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        newSequence = asset_tools.create_asset(SequenceName, destination_path, unreal.LevelSequence, factory)
        FrameRate = unreal.FrameRate(25, 1)
        # MovieSceneSequence = unreal.MovieSceneSequence.cast(newSequence)
        # MovieSceneSequence.set_editor_property('set_display_rate',FrameRate)
        # newSequence.__class__ = unreal.MovieSceneSequence
        # newSequence.set_editor_property('set_display_rate',FrameRate)
        newSequence.set_display_rate(FrameRate)
        # newSequence.set_playback_range(float(StartFrame),float(EndFrame))
        newSequence.set_playback_start(float(StartFrame))
        newSequence.set_playback_end(float(EndFrame))
        return newSequence

    def buildAnimationImportOptions(self, skeleton):
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

        # SkeletalMeshImportData->bImportAsScene = false;
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
        # options.set_editor_property('normal_generation_method',unreal.FBXNormalGenerationMethod.BUILT_IN)
        # options.set_editor_property('normal_import_method',unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS)
        return options

    def buildImportAnimationTask(self, filename, destination_path, options=None):
        task = unreal.AssetImportTask()
        # task = unreal.AutomatedAssetImportData()
        task.set_editor_property('automated', True)
        task.set_editor_property('destination_name', '')
        task.set_editor_property('destination_path', destination_path)
        task.set_editor_property('filename', filename)
        task.set_editor_property('replace_existing', True)
        task.set_editor_property('save', True)
        # task.set_editor_property('skip_read_only',True)
        task.set_editor_property('options', options)
        return task

    def GetImportAnimationTask(self, AnimationFileNameList, destination_path, Skeleton_Reference):
        EditorAssetLibrary = unreal.EditorAssetLibrary()
        if (EditorAssetLibrary.does_directory_exist(destination_path)):
            EditorAssetLibrary.delete_directory(destination_path)

        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        # print "destination_path.replace" + destination_path
        if not EditorAssetLibrary.does_directory_exist(destination_path):
            EditorAssetLibrary.make_directory(destination_path)

        AssetRegistryDataArr = AssetRegistry.get_assets_by_class(unreal.SkeletalMesh.static_class().get_name())
        SkeletonAssets = []
        for AssetRegistryData in AssetRegistryDataArr:
            # if str(AssetRegistryData.package_name).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1 :
            skeletalMesh_asset = unreal.SkeletalMesh.cast(unreal.load_asset(AssetRegistryData.package_name))
            SkeletonAssets.append(skeletalMesh_asset.skeleton)

        for SkeletonIndex in range(0, len(SkeletonAssets), 1):
            # print SkeletonIndex
            Skeleton = SkeletonAssets[SkeletonIndex]
            for AnimationIndex in range(0, len(AnimationFileNameList), 1):
                AnimationFileName = AnimationFileNameList[AnimationIndex]
                # print 'Skeleton.get_name     '+str(Skeleton.get_name())+'   Skeleton_Reference::'+os.path.splitext(os.path.basename(Skeleton_Reference))[0]
                if str(Skeleton.get_name()).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1:
                    return self.buildImportAnimationTask(AnimationFileName, destination_path,
                                                         self.buildAnimationImportOptions(Skeleton))

        # importAnimation(SkeletonAssets,AnimationFileNameList,destination_path,Skeleton_Reference)
        return None

    # sequence_path: str : The level sequence asset path
    # actor: obj unreal.Actor: The actor you want to add into (or get from) the sequence asset
    # return: obj unreal.SequencerBindingProxy: The actor binding
    # def getOrAddPossessableInSequenceAsset(sequence_path = '',actor = None):
    #     sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
    #     possessable = sequence_asset.add_possessable(actor)
    #     return possessable

    def addSkeletalAnimationTrackOnPossessable(self, sequence_asset, StartFrame, EndFrame, animation_asset,
                                               possessable=None):
        # Get Animation
        # animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
        '''
        - ``sequence_asset`` (unreal.LevelSequence): 定序器
        - ``StartFrame`` (float):镜头开始帧
        - ``EndFrame`` (float): 镜头结束帧
        - ``possessable`` (SequencerBindingProxy): The object that this sequence should possess when evaluating
        '''

        params = unreal.MovieSceneSkeletalAnimationParams(animation_asset)
        # Add track
        animationo_track = possessable.add_track(unreal.MovieSceneSkeletalAnimationTrack)
        # Add section
        animation_section = animationo_track.add_section()
        animation_section.set_editor_property('Params', params)
        # print 'StartFrame   '+StartFrame+ 'EndFrame   '+EndFrame
        animation_section.set_range(float(StartFrame), float(EndFrame))
        # print "animation_asset.get_editor_property('sequence_length')     "+str(animation_asset.get_editor_property('sequence_length'))
        # seconds
        # animation_section.set_range(0,animation_asset.get_editor_property('sequence_length'))

    def addCameraTrack(self, sequence, StartFrame, EndFrame, cameraFBXFile):
        r"""
        增加镜头，从fbx导入到定序器，在关卡中创建新的镜头
        Returns:

        """
        # camera_location = unreal.Vector(0,0,0)
        # actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CameraActor.static_class(),camera_location)
        # binding = sequence.add_possessable(actor)
        world = unreal.EditorLevelLibrary.get_editor_world()
        import_fbx_settings = unreal.MovieSceneUserImportFBXSettings()
        # import_options.set_editor_property("create_cameras",True)
        # import_fbx_settings.set_editor_property("reduce_keys",True)
        import_fbx_settings.set_editor_property("create_cameras", True)
        SequencerTools = unreal.SequencerTools()
        # bindings = [binding]
        bindings = []
        SequencerTools.import_fbx(world, sequence, bindings, import_fbx_settings, cameraFBXFile)
        # Import
        # SequencerTools.import_fbx(world, sequence, [binding], import_options, cameraFBXFile)
        # try:
        # camera = unreal.CameraActor.cast(actor)
        # camera_cut_track = sequence.add_master_track(unreal.MovieSceneCameraCutTrack)

        # # Add a camera cut track for this camera
        # camera_cut_section = camera_cut_track.add_section()
        # camera_cut_section.set_start_frame_seconds(float(StartFrame))
        # camera_cut_section.set_end_frame_seconds(float(EndFrame))

        # camera_binding_id = unreal.MovieSceneObjectBindingID()
        # camera_binding_id.set_editor_property("Guid", binding.get_id())
        # camera_cut_section.set_editor_property("CameraBindingID", camera_binding_id)

        # # Add a current focal length track to the cine camera component
        # camera_component = actor.get_cine_camera_component()
        # camera_component_binding = sequence.add_possessable(camera_component)
        # camera_component_binding.set_parent(binding)
        # focal_length_track = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)
        # focal_length_track.set_property_name_and_path('CurrentFocalLength', 'CurrentFocalLength')
        # focal_length_section = focal_length_track.add_section()
        # focal_length_section.set_start_frame_bounded(0)
        # focal_length_section.set_end_frame_bounded(0)

        # bindings = sequence.get_bindings()
        # Set Options

        # except TypeError:
        # pass
        pass

    # ,animation_pathList
    def addSkeletalAnimationTrackOnActors(self, sequence_asset, StartFrame, EndFrame):

        world = unreal.EditorLevelLibrary.get_editor_world()
        actorList = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.SkeletalMeshActor.static_class())
        for anim_actor in actorList:
            # anim_actor.set_folder_path(sequence_asset.get_name())
            possessable_in_sequence = sequence_asset.add_possessable(anim_actor)
            # anim_actor.AnimSequence
            # anim_actor.get_animation_asset()
            skeletal_mesh_component = unreal.SkeletalMeshComponent.cast(
                anim_actor.get_editor_property('skeletal_mesh_component'))
            SingleAnimationPlayData = skeletal_mesh_component.get_editor_property('animation_data')
            animation_asset = unreal.AnimationAsset.cast(SingleAnimationPlayData.get_editor_property('anim_to_play'))
            self.addSkeletalAnimationTrackOnPossessable(sequence_asset, StartFrame, EndFrame, animation_asset,
                                                        possessable_in_sequence)

    def importShots(self, targetDir):
        import xml.etree.ElementTree as ET
        root = ET.parse(targetDir + '\\Description.xml').getroot()
        taskList = []
        # 导入动画
        SkeletalAnimation_destination_path = ''
        for elem in root.iter():
            print elem.tag, elem.attrib
            if elem.tag == 'SkeletalAnimation':
                SkeletalAnimation_Path = elem.attrib.get('Path')
                SkeletalAnimation_Reference = elem.attrib.get('Reference')
                pro = SkeletalAnimation_Path.split('/')[1]
                ep = SkeletalAnimation_Path.split('/')[4]
                shot = SkeletalAnimation_Path.split('/')[5]
                # level_path = '/Game/%s/shot_work/keyLight/map/%s/%s-%s-%s'%(pro,ep,pro,ep,shot)
                SkeletalAnimation_destination_path = '/Game/%s/shot_work/animation/%s/%s' % (pro, ep, shot)
                SkeletalAnimation_destination_path = str(
                    os.path.dirname(SkeletalAnimation_destination_path).replace('M:', "Game")).replace("\\", "/")
                # print 'SkeletalAnimation_destination_path::   '+SkeletalAnimation_destination_path
                # if not unreal.EditorAssetLibrary.does_directory_exist(SkeletalAnimation_destination_path):
                taskList.append(
                    self.GetImportAnimationTask([SkeletalAnimation_Path], SkeletalAnimation_destination_path,
                                                SkeletalAnimation_Reference))

        if len(taskList) > 0:
            print('--------------***********************  '+str(len(taskList)))
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(taskList)
        # 导入动画
        for elem in root.iter():
            if elem.tag == 'Camera':
                Camera_path = elem.attrib.get('Path')
                StartFrame = (float)(elem.attrib.get('StartFrame'))
                EndFrame = (float)(elem.attrib.get('EndFrame'))
                CameraStr_Arr = Camera_path.split('/')
                pro = CameraStr_Arr[1]
                ep = CameraStr_Arr[4]
                shot = CameraStr_Arr[5]
                level_path = '/Game/%s/shot_work/keyLight/map/%s/%s-%s-%s' % (pro, ep, pro, ep, shot)
                sequence_destination_path = '/Game/%s/shot_work/keyLight/Sequence/%s' % (pro, ep)

                sequence_Name = '%s-%s-%s' % (pro, ep, shot)

                if not unreal.EditorAssetLibrary.does_asset_exist(level_path):
                    unreal.EditorLevelLibrary.new_level(level_path)
                    pass
                else:
                    # unreal.EditorLevelLibrary.load_level(level_path)
                    return

                # print 'SkeletalAnimation_destination_path str' + str(SkeletalAnimation_destination_path)
                filter_animation = unreal.ARFilter([], [SkeletalAnimation_destination_path], [],
                                                   [unreal.AnimSequence.static_class().get_name()])
                AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
                animationAssetDataArr = AssetRegistry.get_assets(filter_animation)
                # print 'animationAssetDataArr len' + str(len(animationAssetDataArr))
                for animationAssetData in animationAssetDataArr:
                    animationStr = str(animationAssetData.package_name)
                    animationActor = self.spawnAnimInTargetWorld(animationStr)
                    animationActor.set_folder_path(sequence_Name)
                newSequence = None
                # print 'sequence_destination_path  :::'+sequence_destination_path+' sequence_Name:::  '+sequence_Name
                if not unreal.EditorAssetLibrary.does_asset_exist(sequence_destination_path + '/' + sequence_Name):
                    newSequence = self.spawnSequencerInTargetWorld(sequence_Name, sequence_destination_path, StartFrame,
                                                                   EndFrame)
                    if not newSequence == None:
                        self.addSkeletalAnimationTrackOnActors(newSequence, StartFrame, EndFrame)
                        self.addCameraTrack(newSequence, StartFrame, EndFrame, Camera_path)
                    pass
                else:
                    # newSequence = unreal.LevelSequence.cast(unreal.load_asset(sequence_destination_path+'/'+sequence_Name))
                    # if not newSequence == None:
                    #     addSkeletalAnimationTrackOnActors(newSequence,StartFrame,EndFrame)
                    pass
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
        return

class LayoutImportTools:
    # 'Layout阶段自动复制镜头和关卡文件到本地'

    def __init__(self):
        pass

    def __del__(self):
        pass

    def spawnAnimInTargetWorld(self, animationStr):
        # animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animationStr))
        animation_asset = unreal.AnimationAsset.cast(unreal.load_asset(animationStr))
        skeleton = unreal.Skeleton.cast(animation_asset.get_editor_property('skeleton'))
        EditorLevelLibrary = unreal.EditorLevelLibrary()
        # EditorLevelLibrary.spawn_actor_from_object()
        # world = EditorLevelLibrary.get_editor_world()
        # world = unreal.World.cast(unreal.load_asset(worldStr))
        # unreal.GameplayStatics.begin
        anim_class = unreal.SkeletalMeshActor.static_class()
        anim_location = unreal.Vector(0, 0, 0)
        # anim_rotation = unreal.Rotator(0,0,0)
        # anim_scale =  unreal.Vector(1.0,1.0,1.0)
        actor = EditorLevelLibrary.spawn_actor_from_class(anim_class, anim_location)
        anim_actor = unreal.SkeletalMeshActor.cast(actor)
        SingleAnimationPlayData = unreal.SingleAnimationPlayData()
        SingleAnimationPlayData.set_editor_property('anim_to_play', animation_asset)
        skeletal_mesh_component = unreal.SkeletalMeshComponent.cast(
            anim_actor.get_editor_property('skeletal_mesh_component'))
        # skeletal_mesh_component.set_editor_property('skeletal_mesh',skeletal_mesh)
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        AssetRegistryDataArr = AssetRegistry.get_assets_by_class(unreal.SkeletalMesh.static_class().get_name())
        # SkeletonAssets = []
        skeletalMesh_asset = None
        for AssetRegistryData in AssetRegistryDataArr:
            # if str(AssetRegistryData.package_name).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1 :
            skeletalMesh_asset = unreal.SkeletalMesh.cast(unreal.load_asset(AssetRegistryData.package_name))
            if skeletalMesh_asset.skeleton == skeleton:
                skeletal_mesh_component.set_editor_property('skeletal_mesh', skeletalMesh_asset)
                break

        skeletal_mesh_component.set_editor_property('animation_mode', unreal.AnimationMode.ANIMATION_SINGLE_NODE)
        skeletal_mesh_component.set_editor_property('animation_data', SingleAnimationPlayData)
        return anim_actor

    def spawnSequencerInTargetWorld(self, SequenceName, destination_path, StartFrame, EndFrame):
        factory = unreal.LevelSequenceFactoryNew()
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        newSequence = asset_tools.create_asset(SequenceName, destination_path, unreal.LevelSequence, factory)
        FrameRate = unreal.FrameRate(25, 1)
        # MovieSceneSequence = unreal.MovieSceneSequence.cast(newSequence)
        # MovieSceneSequence.set_editor_property('set_display_rate',FrameRate)
        # newSequence.__class__ = unreal.MovieSceneSequence
        # newSequence.set_editor_property('set_display_rate',FrameRate)
        newSequence.set_display_rate(FrameRate)
        # newSequence.set_playback_range(float(StartFrame),float(EndFrame))
        newSequence.set_playback_start(float(StartFrame))
        newSequence.set_playback_end(float(EndFrame))
        return newSequence

    def buildAnimationImportOptions(self, skeleton):
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

        # SkeletalMeshImportData->bImportAsScene = false;
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
        # options.set_editor_property('normal_generation_method',unreal.FBXNormalGenerationMethod.BUILT_IN)
        # options.set_editor_property('normal_import_method',unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS)
        return options

    def buildImportAnimationTask(self, filename, destination_path, options=None):
        task = unreal.AssetImportTask()
        # task = unreal.AutomatedAssetImportData()
        task.set_editor_property('automated', True)
        task.set_editor_property('destination_name', '')
        task.set_editor_property('destination_path', destination_path)
        task.set_editor_property('filename', filename)
        task.set_editor_property('replace_existing', True)
        task.set_editor_property('save', True)
        # task.set_editor_property('skip_read_only',True)
        task.set_editor_property('options', options)
        return task

    def GetImportAnimationTask(self, AnimationFileNameList, destination_path, Skeleton_Reference):
        EditorAssetLibrary = unreal.EditorAssetLibrary()
        if (EditorAssetLibrary.does_directory_exist(destination_path)):
            EditorAssetLibrary.delete_directory(destination_path)

        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        # print "destination_path.replace" + destination_path
        if not EditorAssetLibrary.does_directory_exist(destination_path):
            EditorAssetLibrary.make_directory(destination_path)

        AssetRegistryDataArr = AssetRegistry.get_assets_by_class(unreal.SkeletalMesh.static_class().get_name())
        SkeletonAssets = []
        for AssetRegistryData in AssetRegistryDataArr:
            # if str(AssetRegistryData.package_name).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1 :
            skeletalMesh_asset = unreal.SkeletalMesh.cast(unreal.load_asset(AssetRegistryData.package_name))
            SkeletonAssets.append(skeletalMesh_asset.skeleton)

        for SkeletonIndex in range(0, len(SkeletonAssets), 1):
            # print SkeletonIndex
            Skeleton = SkeletonAssets[SkeletonIndex]
            for AnimationIndex in range(0, len(AnimationFileNameList), 1):
                AnimationFileName = AnimationFileNameList[AnimationIndex]
                # print 'Skeleton.get_name     '+str(Skeleton.get_name())+'   Skeleton_Reference::'+os.path.splitext(os.path.basename(Skeleton_Reference))[0]
                if str(Skeleton.get_name()).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1:
                    return self.buildImportAnimationTask(AnimationFileName, destination_path,
                                                         self.buildAnimationImportOptions(Skeleton))

        # importAnimation(SkeletonAssets,AnimationFileNameList,destination_path,Skeleton_Reference)
        return None

    # sequence_path: str : The level sequence asset path
    # actor: obj unreal.Actor: The actor you want to add into (or get from) the sequence asset
    # return: obj unreal.SequencerBindingProxy: The actor binding
    # def getOrAddPossessableInSequenceAsset(sequence_path = '',actor = None):
    #     sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
    #     possessable = sequence_asset.add_possessable(actor)
    #     return possessable

    def addSkeletalAnimationTrackOnPossessable(self, sequence_asset, StartFrame, EndFrame, animation_asset,
                                               possessable=None):
        # Get Animation
        # animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
        '''
        - ``sequence_asset`` (unreal.LevelSequence): 定序器
        - ``StartFrame`` (float):镜头开始帧
        - ``EndFrame`` (float): 镜头结束帧
        - ``possessable`` (SequencerBindingProxy): The object that this sequence should possess when evaluating
        '''

        params = unreal.MovieSceneSkeletalAnimationParams(animation_asset)
        # Add track
        animation_track = possessable.add_track(unreal.MovieSceneSkeletalAnimationTrack)
        # Add section
        animation_section = animation_track.add_section()
        animation_section.set_editor_property('Params', params)
        # print 'StartFrame   '+StartFrame+ 'EndFrame   '+EndFrame
        animation_section.set_range(float(StartFrame), float(EndFrame))
        # print "animation_asset.get_editor_property('sequence_length')     "+str(animation_asset.get_editor_property('sequence_length'))
        # seconds
        # animation_section.set_range(0,animation_asset.get_editor_property('sequence_length'))

    def addCameraTrack(self, sequence, StartFrame, EndFrame, cameraFBXFile):
        r"""
        增加镜头，从fbx导入到定序器，在关卡中创建新的镜头
        Returns:

        """
        # camera_location = unreal.Vector(0,0,0)
        # actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CameraActor.static_class(),camera_location)
        # binding = sequence.add_possessable(actor)
        world = unreal.EditorLevelLibrary.get_editor_world()
        import_fbx_settings = unreal.MovieSceneUserImportFBXSettings()
        # import_options.set_editor_property("create_cameras",True)
        # import_fbx_settings.set_editor_property("reduce_keys",True)
        import_fbx_settings.set_editor_property("create_cameras", True)
        SequencerTools = unreal.SequencerTools()
        # bindings = [binding]
        bindings = []
        SequencerTools.import_fbx(world, sequence, bindings, import_fbx_settings, cameraFBXFile)
        pass

    # ,animation_pathList
    def addSkeletalAnimationTrackOnActors(self, sequence_asset, StartFrame, EndFrame):

        world = unreal.EditorLevelLibrary.get_editor_world()
        actorList = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.SkeletalMeshActor.static_class())
        for anim_actor in actorList:
            # anim_actor.set_folder_path(sequence_asset.get_name())
            possessable_in_sequence = sequence_asset.add_possessable(anim_actor)
            # anim_actor.AnimSequence
            # anim_actor.get_animation_asset()
            skeletal_mesh_component = unreal.SkeletalMeshComponent.cast(
                anim_actor.get_editor_property('skeletal_mesh_component'))
            SingleAnimationPlayData = skeletal_mesh_component.get_editor_property('animation_data')
            animation_asset = unreal.AnimationAsset.cast(SingleAnimationPlayData.get_editor_property('anim_to_play'))
            self.addSkeletalAnimationTrackOnPossessable(sequence_asset, StartFrame, EndFrame, animation_asset,
                                                        possessable_in_sequence)

    def buildSoundImportOptions(self):
        options = unreal.SoundFactory()
        options.set_editor_property('create_new', True)
        options.set_editor_property('editor_import', True)
        options.set_editor_property('auto_create_cue', True)
        return options

    def GetImportSoundTask(self, SoundFileName, destination_path):
        task = unreal.AssetImportTask()
        # task = unreal.AutomatedAssetImportData()
        task.set_editor_property('automated', True)
        task.set_editor_property('destination_name', '')
        task.set_editor_property('destination_path', destination_path)
        task.set_editor_property('filename', SoundFileName)
        task.set_editor_property('replace_existing', True)
        task.set_editor_property('save', True)
        # task.set_editor_property('skip_read_only',True)
        task.set_editor_property('options', self.buildSoundImportOptions())
        return task

    def addSoundTrack(self, sequence_asset, sound_asset):
        # Get Animation
        # animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
        '''
        - ``sequence_asset`` (unreal.LevelSequence): 定序器
        - ``sound_asset`` (SoundBase): 声音资产
        '''
        # sequence = unreal.LevelSequence.cast(unreal.load_asset(sequence_asset))
        # Add track
        sound_track = sequence_asset.add_master_track(unreal.MovieSceneAudioTrack)
        if sound_track:
            # Add section
            # sound_section = unreal.MovieSceneAudioSection.cast(sound_track.add_section())
            sound_section = unreal.MovieSceneAudioSection.cast(
                unreal.MovieSceneTrackExtensions.add_section(sound_track))
            sound_section.set_editor_property('sound', sound_asset)

    def importShots(self, targetDir):
        import xml.etree.ElementTree as ET
        root = ET.parse(targetDir + '\\Description.xml').getroot()
        taskList = []
        # 导入动画
        SkeletalAnimation_destination_path = ''
        newSequence = None
        StartFrame = 0
        EndFrame = 0
        FPS = 25
        for elem in root.iter():
            if elem.tag == 'Task':
                StartFrame = (float)(elem.attrib.get('StartFrame'))
                EndFrame = (float)(elem.attrib.get('EndFrame'))
                FPS = (int)(elem.attrib.get('FPS'))
                break

        for elem in root.iter():
            print elem.tag, elem.attrib
            if elem.tag == 'SkeletalAnimation':
                SkeletalAnimation_Path = elem.attrib.get('Path')
                SkeletalAnimation_Reference = elem.attrib.get('Reference')
                pro = SkeletalAnimation_Path.split('/')[1]
                ep = SkeletalAnimation_Path.split('/')[3]
                sc = SkeletalAnimation_Path.split('/')[4]
                shot = SkeletalAnimation_Path.split('/')[5]
                # level_path = '/Game/%s/shot_work/keyLight/map/%s/%s-%s-%s'%(pro,ep,pro,ep,shot)
                SkeletalAnimation_destination_path = '/Game/%s/shot_work/%s/%s/%s/Animation' % (pro, ep, sc, shot)
                # print 'SkeletalAnimation_destination_path::   '+SkeletalAnimation_destination_path
                # if not unreal.EditorAssetLibrary.does_directory_exist(SkeletalAnimation_destination_path):
                taskList.append(
                    self.GetImportAnimationTask([SkeletalAnimation_Path], SkeletalAnimation_destination_path,
                                                SkeletalAnimation_Reference))

                Sound_Path = elem.attrib.get('Sound')
                Sound_pro = Sound_Path.split('/')[1]
                Sound_ep = Sound_Path.split('/')[3]
                Sound_sc = Sound_Path.split('/')[4]
                Sound_shot = Sound_Path.split('/')[5]
                Sound_destination_path = '/Game/%s/shot_work/%s/%s/%s/Sound' % (
                Sound_pro, Sound_ep, Sound_sc, Sound_shot)
                taskList.append(self.GetImportSoundTask(Sound_Path, Sound_destination_path))
        print('--------------***********************  ' + str(len(taskList)))
        if len(taskList) > 0:
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(taskList)

        # <ShotLevel Ref="DLQ2_Ep004_Sc01_P01" Path="DLQ/Shot_Work/KeyLight/Level/Ep004/Sc01/DLQ2_Ep004_Sc01_P01.umap"/>

        # <Sequencer Ref="DLQ2_Ep004_Sc01_P01" Path="DLQ/Shot_Work/KeyLight/Sequence/Ep004/Sc01/DLQ2_Ep004_Sc01_P01.uasset"/>
        for elem in root.iter():
            print elem.tag, elem.attrib
            if elem.tag == 'ShotLevel':
                src_ShotLevel = str(elem.attrib.get('Path'))
                dst_ShotLevel = str(unreal.SystemLibrary.convert_to_absolute_path(unreal.Paths.project_content_dir())) + \
                                src_ShotLevel.replace("\\", "/").split(":")[1].replace("/", "", 1)
                dst_ShotLevel_path = os.path.dirname(os.path.realpath(dst_ShotLevel))
                # print 'src_ShotLevel:::' + str(src_ShotLevel)
                # print 'dst_ShotLevel:::' + str(dst_ShotLevel)

                isExists = os.path.exists(dst_ShotLevel_path)
                # 判断结果
                if not isExists:
                    # 如果不存在则创建目录 创建目录操作函数
                    os.makedirs(dst_ShotLevel_path)
                    print dst_ShotLevel_path + ' 创建成功'
                else:
                    # 如果目录存在则不创建，并提示目录已存在
                    print dst_ShotLevel_path + ' 目录已存在'

                shutil.copyfile(src_ShotLevel, dst_ShotLevel)

                level_path = "/Game" + src_ShotLevel.replace("\\", "/").split(":")[1].split(".")[0]
                # print 'level_path:::' + str(level_path)
                unreal.EditorLevelLibrary.load_level(level_path)
            if elem.tag == 'Sequencer':
                src_Sequencer = str(elem.attrib.get('Path'))
                dst_Sequencer = str(unreal.SystemLibrary.convert_to_absolute_path(unreal.Paths.project_content_dir())) + \
                                src_Sequencer.replace("\\", "/").split(":")[1].replace("/", "", 1)
                dst_Sequencer_path = os.path.dirname(os.path.realpath(dst_Sequencer))
                isExists = os.path.exists(dst_Sequencer_path)
                # 判断结果
                if not isExists:
                    # 如果不存在则创建目录 创建目录操作函数
                    os.makedirs(dst_Sequencer_path)
                    print dst_Sequencer_path + ' 创建成功'
                else:
                    # 如果目录存在则不创建，并提示目录已存在
                    print dst_Sequencer_path + ' 目录已存在'

                shutil.copyfile(src_Sequencer, dst_Sequencer)
                sequence_destination_path = "/Game" + src_Sequencer.replace("\\", "/").split(":")[1].split(".")[0]
                # print 'sequence_destination_path:::' + str(sequence_destination_path)
                # newSequence = unreal.LevelSequence.cast(unreal.load_asset(sequence_destination_path))
        # if not unreal.EditorAssetLibrary.does_asset_exist(level_path):
        #     unreal.EditorLevelLibrary.new_level(level_path)
        #     pass
        # else:
        #     # unreal.EditorLevelLibrary.load_level(level_path)
        #     return

        # print 'SkeletalAnimation_destination_path str' + str(SkeletalAnimation_destination_path)
        # filter_animation = unreal.ARFilter([], [SkeletalAnimation_destination_path], [],
        #                                     [unreal.AnimSequence.static_class().get_name()])
        # AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        # animationAssetDataArr = AssetRegistry.get_assets(filter_animation)
        # # print 'animationAssetDataArr len' + str(len(animationAssetDataArr))
        # for animationAssetData in animationAssetDataArr:
        #     animationStr = str(animationAssetData.package_name)
        #     animationActor = self.spawnAnimInTargetWorld(animationStr)
        # animationActor.set_folder_path(sequence_Name)

        # print 'sequence_destination_path  :::'+sequence_destination_path+' sequence_Name:::  '+sequence_Name
        # if not unreal.EditorAssetLibrary.does_asset_exist(sequence_destination_path + '/' + sequence_Name):
        #     newSequence = self.spawnSequencerInTargetWorld(sequence_Name, sequence_destination_path, StartFrame,
        #                                                     EndFrame)

        # else:
        #     # newSequence = unreal.LevelSequence.cast(unreal.load_asset(sequence_destination_path+'/'+sequence_Name))
        #     # if not newSequence == None:
        #     #     addSkeletalAnimationTrackOnActors(newSequence,StartFrame,EndFrame)
        #     pass

        # 导入动画
        # for elem in root.iter():
        #     if elem.tag == 'Camera':
        #         Camera_path = elem.attrib.get('Path')

        #         CameraStr_Arr = Camera_path.split('/')
        #         pro = CameraStr_Arr[1]
        #         ep = CameraStr_Arr[4]
        #         shot = CameraStr_Arr[5]
        #         # level_path = '/Game/%s/shot_work/keyLight/level/%s/%s-%s-%s' % (pro, ep, pro, ep, shot)
        #         # sequence_destination_path = '/Game/%s/shot_work/keyLight/Sequence/%s' % (pro, ep)
        #         if newSequence:
        #                 #self.addSkeletalAnimationTrackOnActors(newSequence, StartFrame, EndFrame)
        #                 self.addCameraTrack(newSequence, StartFrame, EndFrame, Camera_path)
        #             pass
        #         #sequence_Name = '%s-%s-%s' % (pro, ep, shot)

        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
        return

class UnrealNode():
    def __init__(self):
        self.url = 'http://192.168.1.32:5000'

    def StaticTextureMeshTask(self,r_json):
        print('StaticTextureMeshTask is start')
        task = StaticTextureMeshTask()
        # task.importAsset(xml)
        time.sleep(3)
    def SkeletonMeshTask(self,r_json):
        time.sleep(10)
        print('SkeletonMeshTask')
    def LayoutTask(self,r_json):
        task = LayoutImportTools()
        task.importShots(r_json.get('XmlFile'))

    def AnimateTask(self,r_json):
        task = ImportShotsTools()
        task.importShots(r_json.get('XmlFile'))
        time.sleep(10)


    def main(self,r_json):
        if r_json.get('TaskType') == 'StaticTextureMeshTask':
            self.StaticTextureMeshTask(r_json)
        if r_json.get('TaskType') == 'SkeletonMeshTask':
            self.SkeletonMeshTask(r_json)
        if r_json.get('TaskType') == 'AnimateTask':
            self.AnimateTask(r_json)
        if r_json.get('TaskType') == 'LayoutTask':
            self.LayoutTask(r_json)
        url = '%s/ue/con?action=update' % self.url
        data_json = {'TaskId': r_json.get('TaskId'), 'info': {'taskStatus': 'success','date':str(datetime.now()).split('.')[0]}}
        r_json = requests.post(url, json.dumps(data_json))
        print(r_json.content)

node = UnrealNode()

while True:
    data_json = json.dumps({'info': 'getUnrealTask'})
    try:
        r_json = requests.post('%s/ue/con?action=get'%node.url, data_json)
    except:
        print('connect failed')
        break
    r_json = json.loads(r_json.content)
    if r_json.get('taskStock') == 'taskEmpty' or None:
        print('task is Empty ')
        time.sleep(10)
    else:
        node.main(r_json)

