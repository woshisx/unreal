#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unreal
import os

class ImportShotsTools:
    # '自动导入镜头'

    def __init__(self):
        pass
    def __del__(self):
        pass

    def spawnAnimInTargetWorld(self, animationStr):
        #animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animationStr))
        animation_asset = unreal.AnimationAsset.cast(unreal.load_asset(animationStr))
        skeleton = unreal.Skeleton.cast(animation_asset.get_editor_property('skeleton'))
        EditorLevelLibrary = unreal.EditorLevelLibrary()
        #EditorLevelLibrary.spawn_actor_from_object()
        #world = EditorLevelLibrary.get_editor_world()
        #world = unreal.World.cast(unreal.load_asset(worldStr))
        #unreal.GameplayStatics.begin
        anim_class = unreal.SkeletalMeshActor.static_class()
        anim_location = unreal.Vector(0,0,0)
        #anim_rotation = unreal.Rotator(0,0,0)
        #anim_scale =  unreal.Vector(1.0,1.0,1.0)
        actor = EditorLevelLibrary.spawn_actor_from_class(anim_class,anim_location)
        anim_actor = unreal.SkeletalMeshActor.cast(actor)
        SingleAnimationPlayData = unreal.SingleAnimationPlayData()
        SingleAnimationPlayData.set_editor_property('anim_to_play',animation_asset)
        skeletal_mesh_component = unreal.SkeletalMeshComponent.cast(anim_actor.get_editor_property('skeletal_mesh_component'))
        #skeletal_mesh_component.set_editor_property('skeletal_mesh',skeletal_mesh)
        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        AssetRegistryDataArr = AssetRegistry.get_assets_by_class(unreal.SkeletalMesh.static_class().get_name())
        #SkeletonAssets = []
        skeletalMesh_asset = None
        for AssetRegistryData in AssetRegistryDataArr:
            #if str(AssetRegistryData.package_name).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1 :
            skeletalMesh_asset = unreal.SkeletalMesh.cast(unreal.load_asset(AssetRegistryData.package_name))
            if skeletalMesh_asset.skeleton == skeleton:
                skeletal_mesh_component.set_editor_property('skeletal_mesh',skeletalMesh_asset)
                break

        skeletal_mesh_component.set_editor_property('animation_mode',unreal.AnimationMode.ANIMATION_SINGLE_NODE)
        skeletal_mesh_component.set_editor_property('animation_data',SingleAnimationPlayData)
        return anim_actor

    def spawnSequencerInTargetWorld(self, SequenceName,destination_path,StartFrame,EndFrame):
        factory = unreal.LevelSequenceFactoryNew()
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        newSequence = asset_tools.create_asset(SequenceName, destination_path, unreal.LevelSequence, factory)
        FrameRate = unreal.FrameRate(25,1)
        # MovieSceneSequence = unreal.MovieSceneSequence.cast(newSequence)
        # MovieSceneSequence.set_editor_property('set_display_rate',FrameRate)
        #newSequence.__class__ = unreal.MovieSceneSequence
        #newSequence.set_editor_property('set_display_rate',FrameRate)
        newSequence.set_display_rate(FrameRate)
        #newSequence.set_playback_range(float(StartFrame),float(EndFrame))
        newSequence.set_playback_start(float(StartFrame))
        newSequence.set_playback_end(float(EndFrame))
        return newSequence


    def buildAnimationImportOptions(self, skeleton):
        skeletal_mesh_import_data = unreal.FbxSkeletalMeshImportData()
        skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose',False)
        skeletal_mesh_import_data.set_editor_property('import_meshes_in_bone_hierarchy',True)
        skeletal_mesh_import_data.set_editor_property('use_t0_as_ref_pose',False)
        skeletal_mesh_import_data.set_editor_property('preserve_smoothing_groups',True)
        skeletal_mesh_import_data.set_editor_property('import_morph_targets',True)
        import_translation = unreal.Vector(0,0,0)
        skeletal_mesh_import_data.set_editor_property('import_translation',import_translation)
        import_rotation = unreal.Rotator(0,0,0)
        skeletal_mesh_import_data.set_editor_property('import_rotation',import_rotation)
        skeletal_mesh_import_data.set_editor_property('import_uniform_scale',1.0)
        skeletal_mesh_import_data.set_editor_property('convert_scene',True)
        skeletal_mesh_import_data.set_editor_property('force_front_x_axis',False)
        skeletal_mesh_import_data.set_editor_property('convert_scene_unit',False)
        # skeletal_mesh_import_data.set_editor_property('combine_meshes',False)
        # skeletal_mesh_import_data.set_editor_property('remove_degenerates',True)
        #skeletal_mesh_import_data.set_editor_property('build_adjacency_buffer',True)
        skeletal_mesh_import_data.set_editor_property('normal_import_method',unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS)
        
        FbxAnimSequenceImportData = unreal.FbxAnimSequenceImportData()
        FbxAnimSequenceImportData.set_editor_property('animation_length',unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
        FbxAnimSequenceImportData.set_editor_property('import_meshes_in_bone_hierarchy',True)
        Int32Interval = unreal.Int32Interval()
        Int32Interval.set_editor_property('max',0)
        Int32Interval.set_editor_property('min',0)
        FbxAnimSequenceImportData.set_editor_property('frame_import_range',Int32Interval)
        FbxAnimSequenceImportData.set_editor_property('use_default_sample_rate',False)
        FbxAnimSequenceImportData.set_editor_property('import_custom_attribute',True)
        FbxAnimSequenceImportData.set_editor_property('import_bone_tracks',True)
        FbxAnimSequenceImportData.set_editor_property('set_material_drive_parameter_on_custom_attribute',False)
        FbxAnimSequenceImportData.set_editor_property('material_curve_suffixes',['_mat'])
        FbxAnimSequenceImportData.set_editor_property('remove_redundant_keys',True)
        FbxAnimSequenceImportData.set_editor_property('delete_existing_morph_target_curves',False)
        FbxAnimSequenceImportData.set_editor_property('do_not_import_curve_with_zero',True)
        FbxAnimSequenceImportData.set_editor_property('preserve_local_transform',False)
        vector = unreal.Vector(0,0,0)
        FbxAnimSequenceImportData.set_editor_property('ImportTranslation',vector)
        rotator = unreal.Rotator(0,0,0)
        FbxAnimSequenceImportData.set_editor_property('import_rotation',rotator)
        FbxAnimSequenceImportData.set_editor_property('import_uniform_scale',1.0)
        FbxAnimSequenceImportData.set_editor_property('convert_scene',True)
        FbxAnimSequenceImportData.set_editor_property('force_front_x_axis',False)
        FbxAnimSequenceImportData.set_editor_property('convert_scene_unit',False)
        
        #SkeletalMeshImportData->bImportAsScene = false;
        options = unreal.FbxImportUI()
        options.set_editor_property('skeletal_mesh_import_data',skeletal_mesh_import_data)
        options.set_editor_property('anim_sequence_import_data',FbxAnimSequenceImportData)
        options.set_editor_property('import_mesh',False)
        options.set_editor_property('import_textures',False)
        options.set_editor_property('import_materials',False)
        options.set_editor_property('import_as_skeletal',False)
        options.set_editor_property('skeleton',skeleton)
        options.set_editor_property('original_import_type',unreal.FBXImportType.FBXIT_ANIMATION)
        options.set_editor_property('mesh_type_to_import',unreal.FBXImportType.FBXIT_ANIMATION)
        options.set_editor_property('create_physics_asset',False)
        options.set_editor_property('physics_asset',None)
        options.set_editor_property('auto_compute_lod_distances',False)
        options.set_editor_property('lod_number',0)
        options.set_editor_property('minimum_lod_number',0)
        options.set_editor_property('import_animations',True)
        options.set_editor_property('import_rigid_mesh',False)
        options.set_editor_property('import_materials',False)
        options.set_editor_property('import_textures',False)
        options.set_editor_property('override_full_name',True)
        #没这句就自动生成skeleton mesh了
        options.set_editor_property('automated_import_should_detect_type',False)
        #options.set_editor_property('normal_generation_method',unreal.FBXNormalGenerationMethod.BUILT_IN)
        #options.set_editor_property('normal_import_method',unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS)
        return options

    def buildImportAnimationTask(self, filename,destination_path,options=None):
        task = unreal.AssetImportTask()
        #task = unreal.AutomatedAssetImportData()
        task.set_editor_property('automated',True)
        task.set_editor_property('destination_name','')
        task.set_editor_property('destination_path',destination_path)
        task.set_editor_property('filename',filename)
        task.set_editor_property('replace_existing',True)
        task.set_editor_property('save',True)
        #task.set_editor_property('skip_read_only',True)
        task.set_editor_property('options',options)
        return task
        
    def GetImportAnimationTask(self, AnimationFileNameList,destination_path,Skeleton_Reference):
        EditorAssetLibrary = unreal.EditorAssetLibrary()
        if(EditorAssetLibrary.does_directory_exist(destination_path)):
            EditorAssetLibrary.delete_directory(destination_path)

        AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
        #print "destination_path.replace" + destination_path
        if not EditorAssetLibrary.does_directory_exist(destination_path):
            EditorAssetLibrary.make_directory(destination_path)

        AssetRegistryDataArr = AssetRegistry.get_assets_by_class(unreal.SkeletalMesh.static_class().get_name())
        SkeletonAssets = []
        for AssetRegistryData in AssetRegistryDataArr:
            #if str(AssetRegistryData.package_name).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1 :
            skeletalMesh_asset = unreal.SkeletalMesh.cast(unreal.load_asset(AssetRegistryData.package_name))
            SkeletonAssets.append(skeletalMesh_asset.skeleton)
        
        for SkeletonIndex in range(0,len(SkeletonAssets),1):
            #print SkeletonIndex
            Skeleton = SkeletonAssets[SkeletonIndex]
            for AnimationIndex in range(0,len(AnimationFileNameList),1):
                AnimationFileName = AnimationFileNameList[AnimationIndex]
                #print 'Skeleton.get_name     '+str(Skeleton.get_name())+'   Skeleton_Reference::'+os.path.splitext(os.path.basename(Skeleton_Reference))[0]
                if str(Skeleton.get_name()).find(os.path.splitext(os.path.basename(Skeleton_Reference))[0]) != -1 :
                    return self.buildImportAnimationTask(AnimationFileName,destination_path,self.buildAnimationImportOptions(Skeleton))
        
        #importAnimation(SkeletonAssets,AnimationFileNameList,destination_path,Skeleton_Reference)
        return None

    # sequence_path: str : The level sequence asset path
    # actor: obj unreal.Actor: The actor you want to add into (or get from) the sequence asset
    # return: obj unreal.SequencerBindingProxy: The actor binding
    # def getOrAddPossessableInSequenceAsset(sequence_path = '',actor = None):
    #     sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
    #     possessable = sequence_asset.add_possessable(actor)
    #     return possessable
    
    def addSkeletalAnimationTrackOnPossessable(self, sequence_asset,StartFrame,EndFrame,animation_asset,possessable=None):
        # Get Animation
        #animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
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
        animation_section.set_editor_property('Params',params)
        #print 'StartFrame   '+StartFrame+ 'EndFrame   '+EndFrame
        animation_section.set_range(float(StartFrame),float(EndFrame))
        #print "animation_asset.get_editor_property('sequence_length')     "+str(animation_asset.get_editor_property('sequence_length'))
        #seconds
        #animation_section.set_range(0,animation_asset.get_editor_property('sequence_length'))

    def addCameraTrack(self, sequence,StartFrame,EndFrame,cameraFBXFile):
        r"""
        增加镜头，从fbx导入到定序器，在关卡中创建新的镜头
        Returns:
            
        """
        #camera_location = unreal.Vector(0,0,0)
        #actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CameraActor.static_class(),camera_location)
        #binding = sequence.add_possessable(actor)
        world = unreal.EditorLevelLibrary.get_editor_world()
        import_fbx_settings = unreal.MovieSceneUserImportFBXSettings()
        #import_options.set_editor_property("create_cameras",True)
        #import_fbx_settings.set_editor_property("reduce_keys",True)
        import_fbx_settings.set_editor_property("create_cameras",True)
        SequencerTools = unreal.SequencerTools()
        #bindings = [binding]
        bindings = []
        SequencerTools.import_fbx(world, sequence, bindings, import_fbx_settings, cameraFBXFile)
        # Import
        #SequencerTools.import_fbx(world, sequence, [binding], import_options, cameraFBXFile)
        #try:
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

            #bindings = sequence.get_bindings()
            # Set Options

        #except TypeError:
            #pass
        pass
    #,animation_pathList
    def addSkeletalAnimationTrackOnActors(self, sequence_asset,StartFrame,EndFrame):

        world = unreal.EditorLevelLibrary.get_editor_world()
        actorList = unreal.GameplayStatics.get_all_actors_of_class(world,unreal.SkeletalMeshActor.static_class())
        for anim_actor in actorList:
            #anim_actor.set_folder_path(sequence_asset.get_name())
            possessable_in_sequence = sequence_asset.add_possessable(anim_actor)
            # anim_actor.AnimSequence
            # anim_actor.get_animation_asset()
            skeletal_mesh_component = unreal.SkeletalMeshComponent.cast(anim_actor.get_editor_property('skeletal_mesh_component'))
            SingleAnimationPlayData = skeletal_mesh_component.get_editor_property('animation_data')
            animation_asset = unreal.AnimationAsset.cast(SingleAnimationPlayData.get_editor_property('anim_to_play'))
            self.addSkeletalAnimationTrackOnPossessable(sequence_asset,StartFrame,EndFrame,animation_asset,possessable_in_sequence)





    def importShots(self, targetDir):
        import xml.etree.ElementTree as ET
        root = ET.parse(targetDir+'\\Description.xml').getroot()
        taskList=[]
        # 导入动画
        SkeletalAnimation_destination_path =''
        for elem in root.iter():
            print elem.tag, elem.attrib
            if elem.tag=='SkeletalAnimation':
                SkeletalAnimation_Path = elem.attrib.get('Path')
                SkeletalAnimation_Reference = elem.attrib.get('Reference')
                pro = SkeletalAnimation_Path.split('/')[1]
                ep = SkeletalAnimation_Path.split('/')[4]
                shot = SkeletalAnimation_Path.split('/')[5]
                #level_path = '/Game/%s/shot_work/keyLight/map/%s/%s-%s-%s'%(pro,ep,pro,ep,shot)
                SkeletalAnimation_destination_path='/Game/%s/shot_work/animation/%s/%s'%(pro,ep,shot)
                SkeletalAnimation_destination_path= str(os.path.dirname(SkeletalAnimation_destination_path).replace('M:',"Game")).replace("\\","/")
                #print 'SkeletalAnimation_destination_path::   '+SkeletalAnimation_destination_path
                if not unreal.EditorAssetLibrary.does_directory_exist(SkeletalAnimation_destination_path):
                    taskList.append(self.GetImportAnimationTask([SkeletalAnimation_Path],SkeletalAnimation_destination_path,SkeletalAnimation_Reference))
                pass
        
        if len(taskList) >0:
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(taskList)
        # 导入动画
        for elem in root.iter():
            if elem.tag=='Camera':
                Camera_path= elem.attrib.get('Path')
                StartFrame = (float)(elem.attrib.get('StartFrame'))
                EndFrame = (float)(elem.attrib.get('EndFrame'))
                CameraStr_Arr = Camera_path.split('/')
                pro = CameraStr_Arr[1]
                ep = CameraStr_Arr[4]
                shot = CameraStr_Arr[5]
                level_path = '/Game/%s/shot_work/keyLight/map/%s/%s-%s-%s'%(pro,ep,pro,ep,shot)
                sequence_destination_path = '/Game/%s/shot_work/keyLight/Sequence/%s'%(pro,ep)
                
                sequence_Name = '%s-%s-%s'%(pro,ep,shot)
                
                if not unreal.EditorAssetLibrary.does_asset_exist(level_path):
                    unreal.EditorLevelLibrary.new_level(level_path)
                    pass
                else:
                    #unreal.EditorLevelLibrary.load_level(level_path)
                    return

                #print 'SkeletalAnimation_destination_path str' + str(SkeletalAnimation_destination_path)
                filter_animation = unreal.ARFilter([],[SkeletalAnimation_destination_path],[],[unreal.AnimSequence.static_class().get_name()])
                AssetRegistry = unreal.AssetRegistryHelpers().get_asset_registry()
                animationAssetDataArr = AssetRegistry.get_assets(filter_animation)
                #print 'animationAssetDataArr len' + str(len(animationAssetDataArr))
                for animationAssetData in animationAssetDataArr:
                    animationStr = str(animationAssetData.package_name)
                    animationActor = self.spawnAnimInTargetWorld(animationStr)
                    animationActor.set_folder_path(sequence_Name)
                newSequence = None
                #print 'sequence_destination_path  :::'+sequence_destination_path+' sequence_Name:::  '+sequence_Name
                if not unreal.EditorAssetLibrary.does_asset_exist(sequence_destination_path+'/'+sequence_Name):
                    newSequence = self.spawnSequencerInTargetWorld(sequence_Name,sequence_destination_path,StartFrame,EndFrame)
                    if not newSequence == None:
                        self.addSkeletalAnimationTrackOnActors(newSequence,StartFrame,EndFrame)
                        self.addCameraTrack(newSequence,StartFrame,EndFrame,Camera_path)
                    pass
                else:
                    # newSequence = unreal.LevelSequence.cast(unreal.load_asset(sequence_destination_path+'/'+sequence_Name))
                    # if not newSequence == None:
                    #     addSkeletalAnimationTrackOnActors(newSequence,StartFrame,EndFrame)
                    pass
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
        return






_targetDir = 'M:/DLQ2/shot_work/animation/EP013/sc017shot0004/publish'
# lsdz lsdzgn
#M:\DLQ2\shot_work\animation\EP013\sc017shot0004\publish\Description.xml
# M:\DLQ2\asset_work\character\cfy\Model\rig\publish
# M:\DLQ2\asset_work\props\m02\Model\rig\publish
# M:\DLQ2\asset_work\props\sq\Model\rig\publish
importShotsTools = ImportShotsTools()
importShotsTools.importShots(_targetDir)