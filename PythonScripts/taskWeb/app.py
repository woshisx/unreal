# -*- coding: utf-8 -*-
import sys,os,json
config = json.loads(open(os.path.dirname(os.path.dirname(__file__)).replace('\\','/')+'/config.json').read())
ip = config.get('public_disk')
sys.path.append('//%s/LocalShare/py27/Lib'%ip)
sys.path.append('//%s/LocalShare/py27/Lib/site-packages'%ip)
from flask import Flask,render_template,url_for,request,redirect,Blueprint,session,flash
from datetime import datetime, timedelta
from pymongo import MongoClient
app = Flask(__name__)
conn = MongoClient('localhost', 27017)
db = conn.TaskList
@app.route('/')
def index():
    return render_template('index.html', title=u'欢迎到来到灼华俱乐部')
@app.route('/test')
def test():
    dic = {}
    Realistic = []
    Cartoon = []
    ThreeShadingTwo = []
    for each in db.uemat.find({}, {'_id': 0}):
        if each.get('matType') == 'Realistic':
            Realistic.append(each)
        if each.get('matType') == 'Cartoon':
            Cartoon.append(each)
        if each.get('matType') == 'ThreeShadingTwo':
            ThreeShadingTwo.append(each)
    dic['Realistic'] = Realistic
    dic['Cartoon'] = Cartoon
    dic['ThreeShadingTwo'] = ThreeShadingTwo
    return render_template('test.html', title=u'欢迎到来到灼华俱乐部',dic=dic)
@app.route('/uemat')
def ueMat():
    dic = {}
    Realistic = []
    Cartoon = []
    ThreeShadingTwo = []
    for each in db.uemat.find({},{'_id': 0}):
        if each.get('matType') == 'Realistic':
            Realistic.append(each)
        if each.get('matType') == 'Cartoon':
            Cartoon.append(each)
        if each.get('matType') == 'ThreeShadingTwo':
            ThreeShadingTwo.append(each)
    dic['Realistic'] = Realistic
    dic['Cartoon'] = Cartoon
    dic['ThreeShadingTwo'] = ThreeShadingTwo
    return render_template('ue_mat.html', title=u'欢迎到来到灼华俱乐部',dic=dic)
@app.route('/uemat/add')
def ueMatAdd():
    return render_template('ue_matadd.html', title=u'欢迎到来到灼华俱乐部')
@app.route('/uemat/update')
def ueMatUpdate():
    matCode = request.args.get('matCode')
    dic = db.uemat.find_one({'matCode': matCode},{'_id': 0})
    jsonDic = json.dumps(dic)
    return render_template('ue_matupdate.html', title=u'欢迎到来到灼华俱乐部',dic=dic,jsonDic= jsonDic)
@app.route('/uemat/ad_post',methods=['POST'])
def ueMatAddPost():
    action = request.args.get('action')
    if action == 'add':
        form_data = request.form.to_dict()
        if db.uemat.find({'matCode': form_data['matCode']}).count():
            return '材质模板编码已经存在'
        elif form_data.get('matCn') and form_data.get('matType') and form_data.get('matCode') and form_data.get('img64'):
            db.uemat.insert(form_data)
            return '材质模板创建成功'
        else:
            return '数据不符合要求'
    if action == 'update':
        form_data = request.form.to_dict()
        item = db.uemat.find_one({}, {'_id': 0, 'matCode': form_data['matCode']})
        if item:
            db.uemat.update({'matCode': form_data['matCode']}, {'$set': form_data})
            return '材质模板更新成功'
        else:
            return '材质模板更新失败'
    if action == 'del':
        form_data = request.form.to_dict()
        db.uemat.remove({'matCode': form_data['matCode']})
        return '删除成功'
@app.route('/uemat/json',methods=['get'])
def ueMatJson():
    temp = []
    for each in db.uemat.find({}, {'_id': 0}):
        temp.append(each)
    return json.dumps(temp)
@app.route('/maya/con',methods=['POST'])
def maya_task():
    action = request.args.get('action')
    if action == 'get':
        item = db.maya.find_one({'taskStatus': 'wait'}, {'_id': 0})
        if item:
            db.maya.update({'TaskId': item['TaskId']},{'$set': {'taskStatus': 'cleaned', 'date': str(datetime.now()).split('.')[0]}})
            print('%s is sent' % item)
            return json.dumps(item)
        else:
            item = db.maya.find_one({'taskStatus': 'cleaned'}, {'_id': 0})
            if item:
                db.maya.update({'TaskId': item['TaskId']},{'$set': {'taskStatus': 'running', 'date': str(datetime.now()).split('.')[0]}})
                print('%s is sent' % item)
                return json.dumps(item)
            else:
                print('maya taskEmpty')
                return json.dumps({'taskStock': 'taskEmpty'})
    if action == 'post':
        data = json.loads(request.data)
        if db.maya.find({'TaskId': data['TaskId']}).count():
            return u'任务已存在，不要重复提交'
        else:
            data['date'] = str(datetime.now()).split('.')[0]
            db.maya.insert(data)
            return u'任务提交成功'
    if action == 'del':
        data = request.form.to_dict()
        if not db.maya.find({'TaskId': data['TaskId']}).count():
            return json.dumps({'info':'task is not exist'})
        else:
            db.maya.remove({'TaskId': data['TaskId']})
            return json.dumps({'info': 'delete success'})
    if action == 'update':
        data = json.loads(request.data)
        item = db.maya.find_one({}, {'_id': 0, 'TaskId': data['TaskId']})
        if not item:
            return json.dumps({'info': 'task is not exist'})
        else:
            db.maya.update({'TaskId': data['TaskId']}, {'$set': data['info']})
            return json.dumps({'info': 'update success'})
    if action == 'repost':
        form_data = request.form.to_dict()
        item = db.maya.find_one({}, {'_id': 0, 'TaskId': form_data['TaskId']})
        if not item:
            return json.dumps({'info': 'task is not exist'})
        else:
            db.maya.update({'TaskId': form_data['TaskId']}, {'$set': {'taskStatus': 'wait'}})
            return json.dumps({'info': 'update success'})
@app.route('/maya/task',methods=['GET', 'POST', 'PUT'])
def maya_web():
    temp_list = []
    dic={}
    now = datetime.now()
    for each in db.maya.find({'taskStatus':'wait'}, {'_id': 0}):
        temp_list.append(each)
    dic['wait'] = temp_list
    temp_list = []
    for each in db.maya.find({'taskStatus':'cleaned'}, {'_id': 0}):
        temp_list.append(each)
    dic['cleaned'] = temp_list
    temp_list = []
    for each in db.maya.find({'taskStatus':'running'}, {'_id': 0}):
        delta = now - datetime.strptime(each['date'], "%Y-%m-%d %H:%M:%S")
        if delta.seconds < 4000:
            temp_list.append(each)
        else:
            db.maya.update({'TaskId': each['TaskId']},
                            {'$set': {'taskStatus': 'failed', 'date': str(datetime.now()).split('.')[0]}})
    dic['running'] = temp_list
    temp_list = []
    for each in db.maya.find({'taskStatus':'success'}, {'_id': 0}):
        delta = now - datetime.strptime(each['date'], "%Y-%m-%d %H:%M:%S")
        if delta.seconds < 50000:
            temp_list.append(each)
        else:
            db.maya.remove({'TaskId': each['TaskId']})
    dic['success'] = temp_list
    temp_list = []
    for each in db.maya.find({'taskStatus': 'failed'}, {'_id': 0}):
        temp_list.append(each)
    dic['failed'] = temp_list
    return render_template('task.html',title=u'欢迎到来到灼华俱乐部',dic = dic)

@app.route('/admin/ad_post',methods=['POST'])
def ad_action():
    action = request.args.get('action')
    dic = request.form.to_dict()
    if action == 'delete':
        try:
            if dic:
                db.col.remove({'TaskId':dic['TaskId']})
                return '删除成功'
        except:
            return '删除出错'

    if action == 'delete_fail':
        try:
            if dic:
                db.failded.remove({'TaskId':dic['TaskId']})
                return '删除成功'
        except:
            return '删除出错'
    if action == 'commit':
        try:
            data = db.failded.find_one({'TaskId':dic['TaskId']},{'_id': 0 })
            db.failded.remove({'TaskId':dic['TaskId']})
            data['date'] = str(datetime.now()).split('.')[0]
            if db.col.find({'TaskId': data['TaskId']}).count() or db.cloth.find({'TaskId': data['TaskId']}).count() or db.runing.find({'TaskId': data['TaskId']}).count():
                return '记录重复'
            else:
                if data['info'] == 'animate_commit':
                    db.cleaned.insert(data)
                if data['info'] == 'cloth_commit':
                    db.cloth.insert(data)
                return '提交成功'
        except:
            return '提交出错'

    if action == 'recommit':
        try:
            data = db.runing.find_one({'TaskId': dic['TaskId']}, {'_id': 0})
            db.runing.remove({'TaskId': dic['TaskId']})
            data['date'] = str(datetime.now()).split('.')[0]
            if data['info'] == 'animate_commit':
                db.cleaned.insert(data)
            if data['info'] == 'cloth_commit':
                db.cloth.insert(data)
            return '提交成功'
        except:
            return '提交出错'

    if action == 'ueRenderWaitDelete':
        try:
            if dic:
                db.render_wait.remove({'TaskId':dic['TaskId']})
                return '删除成功'
        except:
            return '删除出错'

    if action == 'ueRenderFailedDelete':
        try:
            if dic:
                db.render_failed.remove({'TaskId':dic['TaskId']})
                return '删除成功'
        except:
            return '删除出错'

    if action == 'ueRenderCommit':
        try:
            data = db.render_failed.find_one({'TaskId':dic['TaskId']},{'_id': 0 })
            db.render_failed.remove({'TaskId':dic['TaskId']})
            data['date'] = str(datetime.now()).split('.')[0]
            data['info'] = 'render_wait'
            if db.render_wait.find({'TaskId': data['TaskId']}).count() or db.rendering.find({'TaskId': data['TaskId']}).count():
                return '记录重复'
            else:
                db.render_wait.insert(data)
                return '提交成功'
        except:
            return '提交出错'
    else:
        return 'you will never know'

@app.route('/uepro',methods=['GET', 'POST', 'PUT'])
def ueData():
    action = request.args.get('request_type')
    dic = json.loads(request.data)
    print(dic)
    if action == 'insert':
        try:
            db.uepro.insert(dic)
            return 'data insert success'
        except:
            return 'data insert failded'
    if action == 'query':
        temp = []
        for each in db.uepro.find(dic,{'_id': 0}):
            temp.append(each)
        return json.dumps(temp)
    if action == 'update':
        try:
            db.uepro.update(dic[0],dic[1])
            return json.dumps(dic)+ ' update success'
        except:
            return json.dumps(dic)+' update failded'
    if action == 'del':
        try:
            db.uepro.remove(dic)
            return json.dumps(dic)+ ' delete success'
        except:
            return json.dumps(dic)+' delete failded'

@app.route('/ue/render')
def ue_render():
    temp_list = []
    dic = {}
    now = datetime.now()
    for each in db.render_wait.find({}, {'_id': 0}):
        temp_list.append(each)
    dic['render_wait'] = temp_list

    temp_list = []
    for each in db.rendering.find({}, {'_id': 0}):
        delta = now - datetime.strptime(each['date'], "%Y-%m-%d %H:%M:%S")
        if delta.seconds < 4000:
            temp_list.append(each)
        else:
            db.render_failed.insert(each)
            db.rendering.remove({'TaskId': each['TaskId']})
    dic['rendering'] = temp_list

    temp_list = []
    for each in db.render_success.find({}, {'_id': 0}):
        delta = now - datetime.strptime(each['date'], "%Y-%m-%d %H:%M:%S")
        if delta.seconds < 50000:
            temp_list.append(each)
        else:
            db.render_success.remove({'TaskId': each['TaskId']})
    dic['render_success'] = temp_list

    temp_list = []
    for each in db.render_failed.find({}, {'_id': 0}):
        delta = now - datetime.strptime(each['date'], "%Y-%m-%d %H:%M:%S")
        if delta.seconds < 50000:
            temp_list.append(each)
        else:
            db.render_failed.remove({'TaskId': each['TaskId']})
    dic['render_failed'] = temp_list
    return render_template('ue_reader.html', title=u'欢迎到来到灼华俱乐部', dic=dic)

@app.route('/ue/con',methods=['GET', 'POST', 'PUT'])
def unreal_task():
    action = request.args.get('action')
    if action == 'get':
        item = db.uepro.find_one({'taskStatus':'wait'}, {'_id': 0})
        if item:
            db.uepro.update({'TaskId': item['TaskId']},{'$set': {'taskStatus': 'running','date':str(datetime.now()).split('.')[0]}})
            print('%s is sent'%item)
            return json.dumps(item)
        else:
            print('task is Empty')
            return json.dumps({'taskStock':'taskEmpty'})
    if action == 'post':
        data = json.loads(request.data)
        if db.uepro.find({'TaskId': data['TaskId']}).count():
            return json.dumps({'info':'task is exist,do not repeat upload'})
        else:
            data['date'] = str(datetime.now()).split('.')[0]
            db.uepro.insert(data)
            return json.dumps({'info': 'upload success'})
    if action == 'del':
        form_data = request.form.to_dict()
        if not db.uepro.find({'TaskId': form_data['TaskId']}).count():
            return json.dumps({'info':'task is not exist'})
        else:
            db.uepro.remove({'TaskId': form_data['TaskId']})
            return json.dumps({'info': 'delete success'})
    if action == 'update':
        data = json.loads(request.data)
        item = db.uepro.find_one({}, {'_id': 0, 'TaskId': data['TaskId']})
        if not item:
            return json.dumps({'info':'task is not exist'})
        else:
            db.uepro.update({'TaskId': data['TaskId']}, {'$set': data['info']})
            return json.dumps({'info': 'update success'})

    if action == 'repost':
        form_data = request.form.to_dict()
        item = db.uepro.find_one({}, {'_id': 0, 'TaskId': form_data['TaskId']})
        if not item:
            return json.dumps({'info':'task is not exist'})
        else:
            db.uepro.update({'TaskId': form_data['TaskId']}, {'$set': {'taskStatus':'wait'}})
            return json.dumps({'info': 'update success'})

@app.route('/ue/task',methods=['GET', 'POST', 'PUT'])
def unreal_web():
    temp_list = []
    dic ={}
    now = datetime.now()
    for each in db.uepro.find({'taskStatus':'wait'}, {'_id': 0}):
        temp_list.append(each)
    dic['wait'] = temp_list
    temp_list = []
    for each in db.uepro.find({'taskStatus':'running'}, {'_id': 0}):
        delta = now - datetime.strptime(each['date'], "%Y-%m-%d %H:%M:%S")
        if delta.seconds < 4000:
            temp_list.append(each)
        else:
            db.uepro.update({'TaskId': each['TaskId']},
                            {'$set': {'taskStatus': 'failed', 'date': str(datetime.now()).split('.')[0]}})
    dic['running'] = temp_list
    temp_list = []
    for each in db.uepro.find({'taskStatus':'success'}, {'_id': 0}):
        delta = now - datetime.strptime(each['date'], "%Y-%m-%d %H:%M:%S")
        if delta.seconds < 50000:
            temp_list.append(each)
        else:
            db.uepro.remove({'TaskId': each['TaskId']})
    dic['success'] = temp_list
    temp_list = []
    for each in db.uepro.find({'taskStatus': 'failed'}, {'_id': 0}):
        temp_list.append(each)
    dic['failed'] = temp_list
    return render_template('ue_task.html', title=u'欢迎到来到灼华俱乐部', dic=dic)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
