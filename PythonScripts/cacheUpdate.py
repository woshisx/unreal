# -*- coding: utf-8 -*-
import sys,os,json,threading
cofig = json.loads(open(os.path.dirname(__file__).replace('\\','/')+'/config.json').read())
public_disk = cofig.get('public_disk')
node_server = cofig.get('node_server')
sys.path.append('//%s/LocalShare/py27/Lib'%public_disk)
sys.path.append('//%s/LocalShare/py27/Lib/site-packages'%public_disk)
sys.path.append(os.path.dirname(__file__).replace('\\','/'))
import re,shutil,json,random,threading,socket,time,datetime
from strack_api.strack import Strack
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

def dataInit():
    myStrack = strack("https://strack.teamones.com/", 'strack', 'strack')
    cacheFile = os.path.dirname(__file__).replace('\\', '/') + '/cache.json'
    asset_data = myStrack.asset_task()
    shot_data = myStrack.shot_task()
    level_data = myStrack.level_task()
    project_data = myStrack.projectTable()
    status_data = myStrack.statusTable()
    episode_data = myStrack.episodeTable()
    session_data = myStrack.sessionTable()
    cache = {
        'asset_data': asset_data, 'shot_data': shot_data, 'level_data': level_data,
        'project_data': project_data, 'status_data': status_data,
        'episode_data': episode_data, 'session_data': session_data
    }
    with open(cacheFile, 'w') as fileobject:
        fileobject.write(json.dumps(cache))
        fileobject.close()
while True:
    time.sleep(10)
    dataInit()
    print('cache success at %s'%datetime.datetime.now())