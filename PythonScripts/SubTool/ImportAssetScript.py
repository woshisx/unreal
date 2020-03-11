def ImportAllAssets():
#This script was generated with the addons Blender for UnrealEngine : https://github.com/xavier150/Blender-For-UnrealEngine-Addons
#This script will import in unreal all camera in target sequencer
#The script must be used in Unreal Engine Editor with Python plugins : https://docs.unrealengine.com/en-US/Engine/Editor/ScriptingAndAutomation/Python
#Use this command : py "C:\Users\chenxing\Documents\ExportedFbx\ImportAssetScript.py"


	import os.path
	import ConfigParser
	import ast
	import unreal
	
	
	#Prepare var and def
	unrealImportLocation = r'/Game/ImportedFbx'
	ImportedList = []
	ImportFailList = []
	
	def GetOptionByIniFile(FileLoc, OptionName, literal = False):
		Config = ConfigParser.ConfigParser()
		Config.read(FileLoc)
		Options = []
		for option in Config.options(OptionName):
			if (literal == True):
				Options.append(ast.literal_eval(Config.get(OptionName, option)))
			else:
				Options.append(Config.get(OptionName, option))
		return Options
	
	
	#Process import
	print('========================= Import started ! =========================')
	
	
	
	
	'''
	<################################################################################>
	<#############################	             		#############################>
	<############################	             		 ############################>
	<############################	 SkeletalMesh tasks	 ############################>
	<############################	             		 ############################>
	<#############################	             		#############################>
	<################################################################################>
	'''
	
	SkeletalMesh_TasksList = []
	SkeletalMesh_PreImportPath = []
	print('========================= Creating SkeletalMesh tasks... =========================')
	
	def CreateTask_SK_Armature():
		################[ Import Armature as SkeletalMesh type ]################
		print('================[ New import task : Armature as SkeletalMesh type ]================')
		FilePath = os.path.join(r'C:\Users\chenxing\Documents\ExportedFbx\SkeletalMesh\Armature\SK_Armature.fbx')
		AdditionalParameterLoc = os.path.join(r'C:\Users\chenxing\Documents\ExportedFbx\SkeletalMesh\Armature\SK_Armature_AdditionalParameter.ini')
		AssetImportPath = (os.path.join(unrealImportLocation, r'').replace('\\','/')).rstrip('/')
		task = unreal.AssetImportTask()
		task.filename = FilePath
		task.destination_path = AssetImportPath
		task.automated = True
		task.save = True
		task.replace_existing = True
		task.set_editor_property('options', unreal.FbxImportUI())
		task.get_editor_property('options').set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_SKELETAL_MESH)
		task.get_editor_property('options').set_editor_property('import_materials', True)
		task.get_editor_property('options').set_editor_property('import_textures', False)
		task.get_editor_property('options').set_editor_property('import_animations', True)
		task.get_editor_property('options').set_editor_property('create_physics_asset', True)
		task.get_editor_property('options').set_editor_property('import_animations', True)
		task.get_editor_property('options').set_editor_property('import_mesh', True)
		task.get_editor_property('options').set_editor_property('create_physics_asset', True)
		task.get_editor_property('options').texture_import_data.set_editor_property('material_search_location', unreal.MaterialSearchLocation.LOCAL)
		task.get_editor_property('options').skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
		print('================[ import asset : Armature ]================')
		unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
		asset = unreal.find_asset(task.imported_object_paths[0])
		if asset == None:
			ImportFailList.append('Asset "Armature" not found for after inport')
			return
		print('========================= Imports of Armature completed ! Post treatment started...	=========================')
		skeleton = asset.get_editor_property('skeleton')
		lods_to_add = GetOptionByIniFile(AdditionalParameterLoc, 'LevelOfDetail')
		for x, lod in enumerate(lods_to_add):
			pass
		print('========================= Post treatment of Armature completed !	 =========================')
		ImportedList.append([asset, 'SkeletalMesh'])
	CreateTask_SK_Armature()
	
	
	
	
	print('========================= Full import completed !  =========================')
	
	StaticMesh_ImportedList = []
	SkeletalMesh_ImportedList = []
	Alembic_ImportedList = []
	Animation_ImportedList = []
	for asset in ImportedList:
		if asset[1] == 'StaticMesh':
			StaticMesh_ImportedList.append(asset[0])
		elif asset[1] == 'SkeletalMesh':
			SkeletalMesh_ImportedList.append(asset[0])
		elif asset[1] == 'Alembic':
			Alembic_ImportedList.append(asset[0])
		else:
			Animation_ImportedList.append(asset[0])
	
	print('Imported StaticMesh: '+str(len(StaticMesh_ImportedList)))
	print('Imported SkeletalMesh: '+str(len(SkeletalMesh_ImportedList)))
	print('Imported Alembic: '+str(len(Alembic_ImportedList)))
	print('Imported Animation: '+str(len(Animation_ImportedList)))
	print('Import failled: '+str(len(ImportFailList)))
	for error in ImportFailList:
		print(error)
	
	print('=========================')
	if len(ImportFailList) == 0:
		return 'Assets imported with success !' 
	else:
		return 'Some asset(s) could not be imported.' 
	
print(ImportAllAssets())
