# -*- coding: UTF-8 -*-
import os,re,shutil,json,random,threading,socket,sys,time#,requests
import unreal

class StaticTextureMeshTask:
    def __init__(self):
        #self.MaterialLoaderData = 'I:\\svnDir\\ue422_epic_1\\Engine\\Plugins\\zhuohua\\CGGameWork\\Content\\MaterialLoaderData.xml'
        self.MaterialLoaderData = r'I:\svnDir\ue425_epic\Engine\Plugins\Teamones\Content\MaterialLoaderData.xml'
        #self.Material_Template = '/Game/Game/Game_Resources/MapsResources/PublicResources/Materiral_Template/PBR_Mat_Template/Mat_Master/PublicMetallic'
        self.Material_Template = '/Game/ZHAssets/MaterialTemplate/RealisticTemplate/ScenceMaterial/PublicMetallic/PublicMetallic_Inst'
        self.MaterialsTemplateArr = []

        self.Bone_list = []
        self.Bone_list.append('ToseEnd_R')
        self.Bone_list.append('ToseEnd_L')
        self.Bone_list.append('Knee_R')
        self.Bone_list.append('Knee_L')
        self.Bone_list.append('Spine1_M')
        self.Bone_list.append('Chest_M')
        self.Bone_list.append('Shoulder_R')
        self.Bone_list.append('Shoulder_L')
        self.Bone_list.append('Elbow_R')
        self.Bone_list.append('Elbow_L')
        self.Bone_list.append('Wrist_R')
        self.Bone_list.append('Wrist_L')
        self.Bone_list.append('MiddleFinger4_R')
        self.Bone_list.append('MiddleFinger4_L')
        self.Bone_list.append('Neck_M')
        self.Bone_list.append('Eye_R')
        self.Bone_list.append('Eye_L')
        self.Bone_list.append('JawEnd_M')

    # def CreateInstanceOfMaterial(materialFileName,newAssetName,destination_path,_textureTargetNameList,textureFileNameList):
    def CreateInstanceOfMaterial(self, materialFileName, newAssetName, destination_path, textureFileNameList, material_template):
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

        newAsset = asset_tools.create_asset(newAssetName, destination_path, None, factory) # add by chenganggui
        unreal.MaterialEditingLibrary.set_material_instance_parent(newAsset, selectedAsset)# add by chenganggui

        for textureFileName in textureFileNameList:
            for Minslot in material_template['Minslots']:
                if (textureFileName.find(Minslot) != -1) and newAssetName in textureFileName:
                    print('textureFileName is {}, Minslot is {}, newAsset is {}'.format(
                        textureFileName, Minslot, newAssetName
                    ))
                    texture_asset = unreal.Texture.cast(unreal.load_asset(textureFileName))
                    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(newAsset, Minslot, texture_asset)
        # for MaterialsTemplate in self.MaterialsTemplateArr:
        #     if (newAssetName.find(MaterialsTemplate['mat_Inst'].split("_")[0]) != -1):
        #         for textureFileName in textureFileNameList:
        #             # print "newAssetName::"+newAssetName+"  MaterialsTemplate.mat_Inst::"+MaterialsTemplate.mat_Inst+"  textureFileName::"+textureFileName+"  "
        #             for Minslot in MaterialsTemplate['Minslots']:
        #
        #                 if (textureFileName.find(Minslot) != -1) and newAssetName[:-5] in textureFileName:
        #                     # print('textureFileName is {} minslot is {}, newAssetName is {}'.format(
        #                     #     textureFileName,
        #                     #     Minslot,
        #                     #     newAssetName[:-5]
        #                     # ))
        #                     texture_asset = unreal.Texture.cast(unreal.load_asset(textureFileName))
        #                     unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(newAsset,
        #                                                                                                 Minslot,
        #                                                                                                 texture_asset)
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

    def resetStaticMeshMaterial(self, package_path):
        # def __init__(self, package_names=[], package_paths=[], object_paths=[], class_names=[], recursive_classes_exclusion_set=[], recursive_paths=False, recursive_classes=False, include_only_on_disk_assets=False):
        filter_staticmesh = unreal.ARFilter([], [package_path], [], [unreal.StaticMesh.static_class().get_name()], [], True)
        filter_materialIns = unreal.ARFilter([], [package_path], [],
                                             [unreal.MaterialInstanceConstant.static_class().get_name()], [], True)
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        MaterialInsDataArr = AssetRegistry.get_assets(filter_materialIns)
        StaticMeshAssetDataArr = AssetRegistry.get_assets(filter_staticmesh)

        print('MaterialInsDataArr len is {}, StaticMeshAssetDataArr is {}'.format(
            len(MaterialInsDataArr), len(StaticMeshAssetDataArr)
        ))

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

    def resetSkeletonMeshMaterial(self, package_path):
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

    def buildImportTask(self, filename, destination_path, options=None):
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

    def executeImportTasks(self, tasks):
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
        for task in tasks:
            for path in task.get_editor_property('imported_object_paths'):
                print 'Imported: %s' % path

    def buildTextureImportOptions(self):
        options = unreal.TextureFactory()
        options.set_editor_property('create_material', False)
        return options

    def buildStaticMeshImportOptions(self, bCombine_meshs=False):
        options = unreal.FbxImportUI()
        static_mesh_import_data = unreal.FbxStaticMeshImportData()
        static_mesh_import_data.set_editor_property('combine_meshes', False)

        if bCombine_meshs:
            static_mesh_import_data.set_editor_property('combine_meshes', True)

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

    def refreshIMGAsset(self, IMGFileName):
        # Get texture
        texture_asset = unreal.Texture.cast(unreal.load_asset(IMGFileName))
        print('success refresh')
        texture_asset_str = texture_asset.get_name()
        if (texture_asset_str.find("BaseColor") != -1 or texture_asset_str.find("BentNormal") != -1):
            texture_asset.srgb = True
        else:
            texture_asset.srgb = False
        # unreal.ImportSubsystem.on_asset_reimport(texture_asset)

    def importIMGAsset(self, IMGList, destination_path):
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

    def importStaticMesh(self, MeshFileName, destination_path, bCombine_meshs = False):
        taskList = []
        taskList.append(self.buildImportTask(MeshFileName, destination_path, self.buildStaticMeshImportOptions(bCombine_meshs)))
        self.executeImportTasks(taskList)

    def importSkeletalMesh(self, MeshFileName, destination_path):
        taskList = []
        taskList.append(self.buildImportTask(MeshFileName, destination_path, self.buildSkeletalMeshImportOptions()))
        self.executeImportTasks(taskList)

    # def importMeshAsset():
    #     static_mesh_fbx = 'I:\\unrealwork\\test424BP\\pyscripts\\SM_StatocMesh.FBX'
    #     skeletal_mesh_fbx = 'I:\\unrealwork\\test424BP\\pyscripts\\SM_skeletal.FBX'
    #     static_mesh_task = buildImportTask(static_mesh_fbx,'/Game/StaticMeshes')
    #     skeletal_mesh_task = buildImportTask(skeletal_mesh_fbx,'/Game/SkeletalMeshes')
    #     executeImportTasks([static_mesh_task,skeletal_mesh_task])
    def get_material_template(self, material):
        print(material)

        template_material_inst = material.split('_')
        if len(template_material_inst) < 2 or template_material_inst[-1] != 'Inst':
            return None, None
        material_inst = template_material_inst[-2] + '_' + template_material_inst[-1]

        package_path = '/Game/ZHAssets/MaterialTemplate/'
        filter_staticmesh = unreal.ARFilter(
            [], [package_path], [], [unreal.MaterialInstanceConstant.static_class().get_name()], [], True)


        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        MaterialInsDataArr = AssetRegistry.get_assets(filter_staticmesh)

        for material in MaterialInsDataArr:
            if str(material.package_name).split('/')[-1] == material_inst:

                return str(material.package_name), material_inst

        return None, None

    def create_material_instance(self, Material_matName, Pic_destination_path, texArr):

        template_material_inst = Material_matName.split('_')
        if len(template_material_inst) < 3:
            return

        print('Material_matName : {}'.format(Material_matName))
        material_inst = template_material_inst[-2] + '_' + template_material_inst[-1]
        for material_template in self.MaterialsTemplateArr:
            if material_template['mat_inst'] == material_inst:
                print('create instance')
                self.CreateInstanceOfMaterial(material_template['mat_inst_path'], Material_matName,
                                              Pic_destination_path, texArr, material_template)  # add by chenganggui

    def add_slots(self, asset_path):
        filter_skeletalmesh = unreal.ARFilter(
            [], [asset_path], [], [unreal.SkeletalMesh.static_class().get_name()], [], True)
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        MaterialInsDataArr = AssetRegistry.get_assets(filter_skeletalmesh)

        print(len(MaterialInsDataArr))

        for material in MaterialInsDataArr:
            print('material.package_name is xxx{}'.format(
                str(material.get_full_name()).split(' ')[1]
            ))

            unreal.PythonCallLibrary.create_socket(str(material.get_full_name()).split(' ')[1], self.Bone_list)

    def importAsset(self, targetDir):
        import xml.etree.ElementTree as ET
        root = ET.parse(targetDir + '\\Description.xml').getroot()

        # print textureTargetNameList

        textureTargetNameList = []
        material_template_lists = list()
        for elem in root.iter():
            if (elem.tag == "Material"):
                material = elem.attrib.get('matName')
                material_template_path, material_template = self.get_material_template(material)

                if not material_template:
                    continue

                if material_template not in material_template_lists:
                    material_template_lists.append(material_template)
                else:
                    continue

                Minslots = set()
                for elem_Inst in elem.iter():

                    for Pic in elem_Inst.iter():
                        Usage = Pic.attrib.get('Usage')
                        if Usage:
                            Minslots.add(Usage)


                self.MaterialsTemplateArr.append(
                    {
                        'mat_inst' : material_template,
                        'mat_inst_path' : material_template_path,
                        'Minslots' : list(Minslots)
                    }
                )


        # for template in self.MaterialsTemplateArr:
        #     print('xx' + str(template))
        # return

        # targetDir = 'M:\\DLQ2\\asset_work\\props\\hw\\Model\\texture\\publish'

        root = ET.parse(targetDir + '\\Description.xml').getroot()
        picList = []

        destination_path = "/Game" + targetDir.replace("\\", "/").split(":")[1]
        importType = 0
        # print os.path.exists('M:\\DLQ2\\asset_work\\props\\hw\\Model\\texture\\publish\\Description.xml')
        # print root,root.tag, root.attrib
        # for child_of_root in root:
        #     print child_of_root.tag, child_of_root.attrib
        MeshFileName = ""
        is_character_type = False
        is_Combine_meshs = False
        dict_static_type = {
            'Character': False,
            'Environment': False,
            'Props': False
        }

        for elem in root.iter():
            # print elem.tag, elem.attrib
            if (elem.tag == "Pic"):
                Pic_Path = elem.attrib.get('Path')
                # print Pic_Path
                picList.append(Pic_Path)
                # destination_path = "/"+os.path.dirname(Pic_Path).replace('M:',"Game")
            elif (elem.tag == "StaticMesh"):
                MeshFileName = elem.attrib.get('Path')
                print('MeshFileName is {}'.format(
                    MeshFileName
                ))
                static_type = elem.attrib.get('AssetType')
                dict_static_type[static_type] = True

                importType = 1
            elif (elem.tag == "SkeletalMesh"):
                MeshFileName = elem.attrib.get('Path')
                print('MeshFileName is {}'.format(
                    MeshFileName
                ))
                if elem.attrib.get('AssetType') == 'character':
                    is_character_type = True;
                importType = 2

        # print "importType" + str(importType)
        #self.importIMGAsset(picList, destination_path) #// by chenganggui
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
                # print('Material_matName is {} '.format(Material_matName))

                Pic_destination_path = destination_path
                #self.create_material_instance(Material_matName, Pic_destination_path, texArr) # add by chenganggui


        # for f in os.listdir(targetDir):
        #     # print f
        #     if (f.find(".fbx") != -1):
        #         MeshFileName = targetDir + "\\" + f

        # print MeshFileName

        if MeshFileName == "":
            print('canot find fbx file')
            return

        if importType == 1:
            package_path = "/Game" + os.path.dirname(targetDir).replace("\\", "/").split(":")[1]
            package_path = package_path.replace(".", "_")

            # EditorAssetLibrary = unreal.EditorAssetLibrary()
            # if (EditorAssetLibrary.does_directory_exist(package_path)):
            #     EditorAssetLibrary.delete_directory(package_path)

            if dict_static_type['Environment']:
                print('not conbine' + '**'*10)
                self.importStaticMesh(MeshFileName, destination_path) # add by chenganggui
            else:
                print('need conbine' + '**'*10)
                self.importStaticMesh(MeshFileName, destination_path, bCombine_meshs=True)  # add by chenganggui


            print('package_path is {}'.format(package_path))
            self.resetStaticMeshMaterial(
                package_path)  # '/Game/DLQ2/asset_work/props/hw/Model/texture/publish/image/hw_Texture_V01_fbx'
            # unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

        elif importType == 2:
            package_path = "/Game" + os.path.dirname(targetDir).replace("\\", "/").split(":")[1]
            package_path = package_path.replace(".", "_")

            # EditorAssetLibrary = unreal.EditorAssetLibrary()
            # if (EditorAssetLibrary.does_directory_exist(package_path)):
            #     EditorAssetLibrary.delete_directory(package_path)

            print('import skeletal mesh')
            self.importSkeletalMesh(MeshFileName, destination_path)
            # self.resetSkeletonMeshMaterial(
            #     package_path)  # '/Game/DLQ2/asset_work/props/hw/Model/texture/publish/image/hw_Texture_V01_fbx'

            unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
            #判断是否是character类型，所以为skeletalmesh 添加插槽
            if is_character_type:
                print('this is is_character_type')
                self.add_slots(package_path)


# import_task = StaticTextureMeshTask()
# dir = r'P:\TestProject\asset_work\Character\luban\texture\Publish'
# import_task.importAsset(dir)