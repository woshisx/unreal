import sys,json,os
from strack_api.strack import Strack
st = Strack(base_url="https://strack.teamones.com/", login_name="strack", password="strack")
# pro = st.adv_select('project', [['code', 'is',  'TestProject']])
# id= st.adv_select('project_', [['id', 'is',  1]]).get('rows')[0].get('project_disk').get('config').get('default').get('id')

# print(build_full_template_path(pro, 'asset_work_file'))

# print(str(st.modules)).decode('unicode_escape')
# user = st.find('user', [['login_name', 'is', 'chenxing']])
# print(user)
# temp ={}
#

# asset_list = st.select('department').get('rows')
# print(str(asset_list).decode('unicode_escape'))
# list = st.select('session'[['code' , 'is' , 'sc01'],['project_id' , 'is' , 1],['parent_id' , 'is' , 14]]).get('rows')
list = st.select('episode')
print list
data ={
    'project_id':1,
    'code':'seq04',
    'name':'seq04',
    'parent_id':10,
    'module_id':58
}

# print(st.create('sequence',data))
# print(str(st.select('project',fields=['id','code','name'])).decode('unicode_escape'))
# print(st.select('base',[['code', 'is',  'kxm_design']]))
# print(str(st.select('status')).decode('unicode_escape'))
# asset_id_list = [asset.get('id') for asset in asset_list]
# asset_task = st.adv_select('base', [['entity_id', 'in',  asset_id_list]])
# print(str(asset_task)).decode('unicode_escape')

# task=st.adv_select('base',[['entity_id','is',493],['step_id','is',32]])
# print st.find('asset',[['id', 'is',  242]])
# print(task)

# print(st.find('episode',[['id', 'is',  14]]))
# asset_type = st.find('asset_type',[['id', 'is',  242]])
# print(asset_type)
# task = st.adv_select('base',[['entity_id','is',493],['step_id','is',32]])
# st.update('base',[['entity_id','is',493],['step_id','is',32]],data)
# print(st.adv_select('base',[['entity_id','is',493],['step_id','is',32]]))
# print(st.find('project_disk', [['project_id', 'is', 1]]).get('config').get('default').get('id'))
# print(st.find('project_disk', [['project_id', 'is', 1]]).get('config').get('default').get('id'))