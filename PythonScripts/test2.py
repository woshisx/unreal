import requests,json,os
from datetime import datetime, timedelta
def task_post():
    url = 'http://192.168.1.32:5000/ue/con?action=post'
    data_json = {'TaskType': 'LayoutTask','TaskId':'dsde','XmlFile':'P:\CSXXM\shot_work\EP001\SC01\P40\Layout\Pulish','taskStock':'gotOne','taskStatus':'wait','date':str(datetime.now()).split('.')[0]}
    r_json = requests.post(url, json.dumps(data_json))
    print(r_json.content)

def task_del():
    url = 'http://192.168.1.32:5000/ue/con?action=del'
    data_json = {'TaskId':'1wesd'}
    r_json = requests.post(url, json.dumps(data_json))
    print(r_json.content)

def task_update():
    url = 'http://192.168.1.32:5000/ue/con?action=update'
    data_json = {'TaskId':'fsaf','info':{'taskStatus':'failed'}}
    r_json = requests.post(url, json.dumps(data_json))
    print(r_json.content)

url = 'https://strack.teamones.com/api/login/in'
headers = {'Content-Type':'application/json'}
data_json = {"login_name": "strack","password": "strack","from": "api","method": "","server_id": 0}
r_json = requests.post(url,headers=headers,data=json.dumps(data_json))
print(r_json.content)
token  = json.loads(r_json.content).get('data').get('token')
url = 'https://strack.teamones.com/api/task/find'
headers = {'Content-Type':'application/json','token':token}
data_json = {"param": {"filter" : {"id":["-eq","6"]},"fields" : ""}}
r_json = requests.post(url,headers=headers,data=json.dumps(data_json))
print(r_json.content)