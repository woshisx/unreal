# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/23 17:22
# @FileName     :Teamones.py
# @Author       :LiuYang
import os,sys,time,datetime,functools,collections,shutil,re,json,requests
import dayu_widgets as dy
from PySide2 import QtWidgets
from Core import Teamones_UI
from Libs import File
from Libs import package
from tool_widgets import card
from dayu_widgets import dayu_theme
from functools import partial
from xml.etree.ElementTree import Element, SubElement, ElementTree
local = os.path.dirname(__file__).replace('\\','/')
cofig = json.loads(open('%s/config.json'%local).read())
public_disk = cofig.get('public_disk')
node_server = cofig.get('node_server')
try:
    import unreal
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

def timer(a_func):
    """
    一个计时器装饰器
    :param a_func:
    :return:
    """
    @functools.wraps(a_func)
    def wrap_the_function(obj, path):
        start_time = time.time()
        a_func(obj, path)
        end_time = time.time()
        run_time = (end_time - start_time)
        print(run_time)
    return wrap_the_function


class TeamonesFoo(Teamones_UI.TeamonesUI):
    step_mapping = {
        "asset": File.File(package.get("Data/asset_task_fields_header.yaml")).read_data_from_file(),
        "level": File.File(package.get("Data/level_task_fields_header.yaml")).read_data_from_file(),
        "sequence": File.File(package.get("Data/sequence_task_fields_header.yaml")).read_data_from_file(),
        "shot": File.File(package.get("Data/shot_task_fields_header.yaml")).read_data_from_file(),
    }

    def __init__(self, server):
        """
        初始化
        :param server:
        """
        super(TeamonesFoo, self).__init__()
        self.server = server

        self.cur_user = self.server.get_user_info()["user"]

        self.user = {user.id: user.name for user in self.server.user.find().entities}

        self.user.update({0: u"未分配"})

        self.status = [status.name for status in self.server.status.find().entities]

        self.menuWidget.userLabel.setText(self.cur_user["name"])

        self._set_project_widget()

        self._set_default_search_data()

        self._cur_project = None

        self._cur_step_category = "asset"

        self._set_menu()

        self.connect_ui()

    @property
    def project_id(self):
        return self._cur_project

    @property
    def step_category(self):
        return self._cur_step_category

    def connect_ui(self):
        self.menuWidget.closeButton.clicked.connect(self.close)

        # 切换项目，实体界面
        self.tableWidget.button_clicked.connect(self._switch_stack)

        self.informationWidget.task_table.data_change.connect(self._update_task)
        self.informationWidget.page_widget.page.sig_page_changed.connect(self._change_page)
        self.informationWidget.task_table.double_click.connect(self.show_task_widget)

        self.taskSideWidget.LeftWidget.hideButton.left_clicked.connect(self.taskSideWidget.hide)

        # 搜索功能
        self.informationWidget.executor_search.connect(partial(self.search_executor, "executor"))
        self.informationWidget.status_search.connect(partial(self.search_executor, "status"))
        self.informationWidget.type_search.connect(partial(self.search_executor, "type"))
        self.informationWidget.search.connect(partial(self.search_executor, "search"))

    def search_executor(self, search_type, data):
        entity_mapping = {"asset": self._get_asset_data,
                          "level": self._get_level_data,
                          "sequence": self._get_level_data}

        search_mapping = {"name": "entity.name", "code": "entity.code"}

        filters = None
        page = [1, 25]
        if data:
            if search_type == "executor":
                mid_user = list(self.user.keys())[list(self.user.values()).index(data)]
                filters = ["task.executor", "is", mid_user]
            elif search_type == "status":
                filters = ["task.task_status", "is", data]
            elif search_type == "type":
                print unicode(data)
                filters = ["entity.asset_category", "is", unicode(data)]
            elif search_type == "search":
                filters = [
                    search_mapping[self.informationWidget.searchWidget.otherSearch.SearchCombobox.currentText()],
                    "like", data
                ]
            page = []

        task_data = entity_mapping[self._cur_step_category](self.project_id, new_filters=filters, page=page)

        self.informationWidget.set_model(task_data)

    @staticmethod
    def __format_heard(heard):
        """
        格式话表单heard
        :return:
        """
        def score_color(score, data):
            """
            通过时间去计算颜色
            :param score:
            :param data:
            :return:
            """
            # if data["status"] not in [u"进行中", u"反馈", u"审核中"]:
            #     return "#323232"

            time_array = time.localtime(int(time.time()))

            other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)

            day_01 = datetime.datetime.strptime(other_style_time, '%Y-%m-%d %H:%M:%S')

            if data["plan_end_time"]:
                day_02 = datetime.datetime.strptime(data["plan_end_time"], '%Y-%m-%d %H:%M:%S')
                time_difference = (day_01 - day_02).days
            else:
                time_difference = 4

            if time_difference > 3:
                return "#323232"
            elif 0 < time_difference < 2:
                return dayu_theme.warning_color

            elif time_difference <= 0:
                return dayu_theme.error_color
            return dayu_theme.info_color

        new_heard = []
        for item in heard:
            item["align"] = "QtCore.Qt.AlignCenter"

            if item["key"] != "status":
                new_heard.append(item)
            else:
                # try:
                item["bg_color"] = score_color
                new_heard.append(item)
                # except:
                #     pass

        return new_heard

    def _set_project_widget(self):
        """
        设置project面板
        return:
        """
        project_iter = self.server.project.find(filters=[["is_demo", "is", "no"]],
                                                fields=["id", "code", "name", "description"]).entities

        self._set_card(project_iter)

    def _set_card(self, project_iter):
        """
        设置project card
        :param project_iter: 后台请求的项目数据
        :return:
        """
        for project_object in project_iter:
            meta_card = card.Card(project_object)
            meta_card.left_clicked.connect(self._set_task_data_to_model)
            self.projectWidget.ProjectCardLayout.addWidget(meta_card)

    def _set_default_search_data(self):
        # 若存在两个同名用户 会报错
        # self.informationWidget.searchWidget.excuteSearch.set_combobox(self.user.values())

        self.informationWidget.searchWidget.statusSearch.set_combobox(self.status)

    def _set_menu(self):
        """
        :return:
        """
        for executor in self.user.values():
            executor_action = self.informationWidget.task_table.executor_menu.addAction(executor)
            executor_action.triggered.connect(functools.partial(self._change_executor, executor))

        for status in self.status:
            status_action = self.informationWidget.task_table.status_menu.addAction(status)
            status_action.triggered.connect(functools.partial(self._change_status, status))

    def _change_executor(self, data):
        """
        修改执行人
        :param data:  修改的数据
        :return:
        """
        executors = [select_index for select_index in self.informationWidget.task_table.selectedIndexes()
                     if select_index.column() == self.informationWidget.task_table.selectedIndexes()[-1].column()]
        for executor in executors:
            self.informationWidget.task_table.model().setData(executor, data)

    def _change_status(self, data):
        """
        修改任务状态
        :param data:  修改的数据
        :return:
        """
        statuses = [select_index for select_index in self.informationWidget.task_table.selectedIndexes()
                    if select_index.column() == self.informationWidget.task_table.selectedIndexes()[-2].column()]
        for status in statuses:
            self.informationWidget.task_table.model().setData(status, data)

    def _switch_stack(self, table_index):
        """
        切换stack 面板
        :return:
        """
        if not self._cur_project:
            dy.MMessage.warning(u"请先选择项目", self)
            return True

        mapping = ["asset", "level", "sequence", "shot"]

        if table_index == 0:
            self.stackedWidget.setCurrentIndex(0)
            self.taskSideWidget.hide()

        else:
            task_data = self._get_task_data(self._cur_project, entity_module=mapping[table_index - 1])

            self._cur_step_category = mapping[table_index - 1]

            table_headers = self.__format_heard(self.step_mapping[mapping[table_index - 1]])

            self.informationWidget.set_header(table_headers)

            self.informationWidget.set_model(task_data)
            self.informationWidget.task_table.hideColumn(0)

            self.informationWidget.searchWidget.change_search(mapping[table_index - 1])
            self.stackedWidget.setCurrentIndex(1)

    def _set_task_data_to_model(self, project_data, entity_module="asset"):
        """
        获取选定项目任务信息并设置给model
        :param project_data: (dict)
        :param entity_module: 当前实体类型
        :return:
        """
        self.menuWidget.projectLabel.setText(project_data["name"])

        self._cur_project = project_data["id"]

        self._cur_step_category = entity_module

        episode_names = self._get_episode(self._cur_project)

        self.informationWidget.searchWidget.episodesSearch.set_combobox(episode_names)

        self._switch_stack(1)

    def _get_episode(self, project_id):
        """
        获取当前项目集数
        :param project_id: 项目id
        :return:
        """
        episode_names = [episode.name for episode in
                         self.server.episode.find(filters=[["project_id", "is", project_id]]).entities]
        return episode_names

    def _get_task_data(self, project_id, entity_module, page=None):
        """
        获取当前项目任务信息
        :param project_id:  (int) 项目id
        :param entity_module:  (str) 工序模块
        :param page: 分页数
        :return: task data
        """

        if not page:
            page = [1, 25]

        entity_mapping = {"asset": self._get_asset_data,
                          "level": self._get_level_data,
                          "sequence":  self._get_sequence_data,
                          "shot":  self._get_shot_data,
                          }

        data = entity_mapping[entity_module](project_id, page=page)

        if self.informationWidget.page_widget.page.field("current_page") == 0:
            self.informationWidget.page_widget.page.set_field('current_page', 1)

        return data

    def _get_asset_data(self, project_id, new_filters=None, page=None):
        """
        获取当前项目资产任务信息
        :param project_id:  (int) 项目id
        :param page: 分页数
        :return: task data
        """
        data_list = []

        filters = [
            ["task.entity_module_id", "is", 43],
            ["task.project_id", "is", project_id],
            ["step.name", "not is", ""]
                   ]

        if new_filters:
            filters.append(new_filters)

        if not page:
            page = [1, 25]
        tasks = self.server.task.find(filters=filters,
                                      fields=[
                                                "task.id",
                                                "step.name",
                                                "task.man_hour",
                                                "task.plan_start_time",
                                                "task.plan_end_time",
                                                "task.task_status",
                                                "task.executor",
                                                "entity.name",
                                                "entity.asset_category",
                                                "entity.asset_grade"
                                                    ],
                                      page=page)

        while True:
            try:
                task = next(tasks.entities)
                task_data = {
                    "task_id": task.task.id,
                    "task_name": u"{}_{}".format(task.entity.name, task.step.name),
                    "status": task.task_status.name,
                    "executor": self.user[task.task.executor],
                    "plan_start_time": task.task.plan_start_time,
                    "plan_end_time": task.task.plan_end_time,
                    "asset_category": task.entity.asset_category,
                    "asset_grade": task.entity.asset_grade
                             }

                data_list.append(task_data)
            except StopIteration:
                break

        self.informationWidget.page_widget.page.set_total(tasks.total)

        return data_list

    def _get_level_data(self, project_id, new_filters=None, page=None):
        """
        获取当前项目关卡任务信息
        :param project_id:  (int) 项目id
        :param page: 分页数
        :return: task data
        """

        data_list = []
        filters = [["task.entity_module_id", "is", 44],
                   ["task.project_id", "is", project_id],
                   ["step.name", "not is", ""]]

        if new_filters:
            filters.append(new_filters)

        if not page:
            page = [1, 25]
        tasks = self.server.task.find(filters=filters,
                                      fields=[
                                                "step.id",
                                                "step.name",
                                                "task.man_hour",
                                                "task.plan_start_time",
                                                "task.plan_end_time",
                                                "task.task_status",
                                                "entity.name",
                                                "entity.asset_grade",
                                                "user.name"
                                            ],
                                      page=page)

        while True:
            try:
                task = next(tasks.entities)

                task_data = {
                    "task_id": task.step.id,
                    "task_name": u"{}_{}".format(task.entity.name, task.step.name),
                    "level_grade": task.entity.asset_grade,
                    "plan_start_time": task.task.plan_start_time,
                    "plan_end_time": task.task.plan_end_time,
                    "status": task.task_status.name,
                    "executor": task.user.name,
                             }

                data_list.append(task_data)

            except StopIteration:
                break

        self.informationWidget.page_widget.page.set_total(tasks.total)

        return data_list

    def _get_sequence_data(self, project_id, new_filters=None, page=None):
        """
        获取当前项目序列任务信息
        :param project_id:  (int) 项目id
        :param page: 分页数
        :return: task data
        """
        data_list = []

        filters = [["task.entity_module_id", "is", 46],
                   ["task.project_id", "is", project_id],
                   ["step.name", "not is", ""]]

        if new_filters:
            filters.append(new_filters)

        if not page:
            page = [1, 25]
        tasks = self.server.task.find(filters=new_filters,
                                      fields=[
                                                "task.id",
                                                "step.name",
                                                "task.plan_start_time",
                                                "task.plan_end_time",
                                                "task.task_status",
                                                "entity.name",
                                                "user.name"
                                            ],
                                      page=page)

        while True:
            try:
                task = next(tasks.entities)

                task_data = {"task_id": task.task.id,
                             "task_name": u"{}_{}".format(task.entity.name, task.step.name),
                             "episodes": task.entity.name,
                             "plan_start_time": task.task.plan_start_time,
                             "plan_end_time": task.task.plan_end_time,
                             "status": "None",
                             "executor": task.user.name,
                             }

                data_list.append(task_data)

            except StopIteration:
                break

        return data_list, tasks.total

    def _get_shot_data(self, project_id, new_filters=None, page=None):
        """
        获取当前项目镜头任务信息
        :param project_id:  (int) 项目id
        :param page: 分页数
        :return: task data
        """
        data_list = []

        filters = [["task.entity_module_id", "is", 47],
                   ["task.project_id", "is", project_id],
                   ["step.name", "not is", ""]]

        if new_filters:
            filters.append(new_filters)

        if not page:
            page = [1, 25]
        tasks = self.server.task.find(filters=new_filters,
                                      fields=[
                                          "task.id",
                                          "step.name",
                                          "task.plan_start_time",
                                          "task.plan_end_time",
                                          "task.task_status",
                                          "entity.name",
                                          "entity.id",
                                          "user.name"
                                      ],
                                      page=page)

        while True:
            try:
                task = next(tasks.entities)

                episode_data = next(tm.sequence.find(filters=[["sequence.id", "is", task.entity.id]],
                                                     fields=["entity.name", "entity.id"]).entities)

                print episode_data.name

                task_data = {"task_id": task.task.id,
                             "task_name": u"{}_{}".format(task.entity.name, task.step.name),
                             "episodes": episode_data.name,
                             "sequence": task.entity.name,
                             "plan_start_time": task.task.plan_start_time,
                             "plan_end_time": task.task.plan_end_time,
                             "status": "None",
                             "executor": task.user.name,
                             }

                print task_data

                data_list.append(task_data)

            except StopIteration:
                break
        return data_list, tasks.total

    def _update_task(self, task_data):
        """
        更新任务信息
        :param task_data:
        :return:
        """
        key_id = int(task_data["task_id"])
        update_data = {}

        if task_data["executors"]:
            mid_user = list(self.user.keys())[list(self.user.values()).index(task_data["executors"])]
            update_data.update({"executor": mid_user})

        elif task_data["status"]:
            update_data.update({"task_status": task_data["status"]})

        self.server.task.update(key_id, update_data)

        dy.MMessage.success(u"修改完成", self)

    def _change_page(self, cur_page, page_num):
        """
        切换page
        :param cur_page: 当前页
        :param page_num: 每页数量
        :return:
        """
        page = [cur_page, page_num]

        task_data = self._get_task_data(project_id=self._cur_project, entity_module=self._cur_step_category, page=page)

        self.informationWidget.set_model(task_data)

    def show_task_widget(self, task_id):
        """
        显示任务侧边栏
        :param task_id: 任务id
        """
        task_data = self._get_task_information(task_id)
        task_info, task_path = self.__format_task_info(task_data)

        self.taskSideWidget.set_widget_data(task_id, task_info, task_path)
        self.taskSideWidget.show()

    def _get_task_information(self, task_id):
        """
        获取任务详细
        :param task_id: 任务id
        :return:
        """
        filters = [["task.id", "is", task_id]]
        fields = [
            "task.id",
            "step.name",
            "project.code",
            "step.code",
            "step_category.code",
            "task.man_hour",
            "task.plan_start_time",
            "task.plan_end_time",
            "task.task_status",
            "entity.name",
            "entity.code",
            "entity.module_id"
        ]
        if self._cur_step_category == "asset":
            fields.append("entity.asset_category")

        task_data = self.server.task.find(filters=filters, fields=fields, page=[1, 1])

        return task_data

    def __format_task_info(self, task_data):
        """
        格式化任务信息
        :param task_data:
        :return:
        """
        task_info = None
        path_info = None
        for entity in task_data.entities:
            task_info = collections.OrderedDict()
            task_info[u"编号"] = str(entity.task.id)
            task_info[u"名称"] = u"{0}_{1}".format(entity.entity.name, entity.step.name)
            task_info[u"编码"] = u"{0}_{1}".format(entity.entity.code, entity.step.code)
            task_info[u"任务状态"] = entity.task_status.name
            task_info[u"开始时间"] = entity.task.plan_start_time
            task_info[u"结束时间"] = entity.task.plan_end_time

            path_info = self.__format_task_path(entity)

        return task_info, path_info

    def __format_task_path(self, task_data):
        """
        获取任务路径
        :param task_data:
        :return:
        """
        mapping = {u"角色": "character", u"道具": "props", u"场景": "Environment"}
        path_data = []

        if task_data.entity.asset_category:
            # todo: 盘符要修改
            task_path = os.path.join(
                "D:/Event_Test",
                task_data.project.code,
                "work",
                "asset",
                mapping[task_data.entity.asset_category],
                task_data.entity.code,
                task_data.step_category.code,
                task_data.step.code
            ).replace("\\", "/")
        else:
            # todo: 盘符要修改
            task_path = os.path.join(
                "D:/Event_Test",
                task_data.project.code,
                "work",
                self.server.entity.find_one(filters=[["id", "is", task_data.entity.module_id]]).code,
                task_data.entity.code,
                task_data.step_category.code,
                task_data.step.code
            ).replace("\\", "/")

        if os.path.exists(task_path):
            for task_file in os.listdir(task_path):
                task_info = collections.OrderedDict()
                task_info[u"name"] = os.path.splitext(task_file)[0]
                task_info[u"path"] = os.path.join(task_path, task_file).replace("\\", "/")
                path_data.append(task_info)
        else:
            pass

        return path_data

class Maya:
    def __init__(self):
        pass
    def textureXml(self,item,file):
        day = str(datetime.datetime.now())
        root = Element('TaskList', {'releaseDate': day})
        tree = ElementTree(root)
        Task = SubElement(root, 'Task')
        Task.set('TaskId', item.get('uuid'))
        StaticMesh = SubElement(Task, 'StaticMesh')
        StaticMesh.set('Exporter','Maya')
        StaticMesh.set('AssetType', item.get('json').get('asset_type_code'))
        StaticMesh.set('Path', file)
        MaterialList = SubElement(StaticMesh, 'MaterialList')
        for each in mc.ls(type='lambert'):
            if each != 'lambert1':
                Material = SubElement(MaterialList, 'Material')
                Material.set('matName',each)
                if mc.listConnections(each,type='file'):
                    for slot in mc.listConnections(each,type='file'):
                        picPath = mc.getAttr('%s.fileTextureName'%slot)
                        if picPath:
                            newPath = '%s/images/%s_%s.%s'%(item.get('json').get('Publish_path'),each,slot.split('_')[-1],
                                                            picPath.split('.')[-1])
                            Pic = SubElement(Material, 'Pic')
                            Pic.set('Path',newPath)
                            Pic.set('Usage',slot.split('_')[-1])
                            if not os.path.exists('%s/images'%item.get('json').get('Publish_path')):
                                os.mkdir('%s/images'%item.get('json').get('Publish_path'))
                            shutil.copyfile(picPath, newPath)
        tree.write('%s/Description.xml'%item.get('json').get('Publish_path'), encoding='utf-8', xml_declaration=True)
    def backUp(self,path):
        if os.path.exists(path):
            dPath = os.path.dirname(path)
            file = os.path.basename(path)
            if not os.path.exists('%s/backup'%dPath):
                os.mkdir('%s/backup'%dPath)
            shutil.copyfile(path, '%s/backup/%s_%s'%(dPath,str(datetime.datetime.now()).replace(':','.'),file))
class Mobu:
    def __init__(self):
        pass
    def SetTimeSpan(self,start, end):
        fb.FBSystem().CurrentTake.LocalTimeSpan = fb.FBTimeSpan(fb.FBTime(0, 0, 0, start, 0), fb.FBTime(0, 0, 0, end, 0))
    def GetKeysFram(self, Cam):
        keyslist = []
        fcurve = Cam.Translation.GetAnimationNode().Nodes[0].FCurve
        for i in range(0, len(fcurve.Keys)):
            keyslist.append('%d' % fcurve.Keys[i].Time.GetFrame())
        return (keyslist[0], keyslist[-1])
    def ZoomTimeline(self,Cam):
        sartfram,endfram  = self.GetKeysFram(Cam)
        self.SetTimeSpan(int(sartfram),int(endfram))
        del(sartfram,endfram)
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
            del(lAlignTransPos,lAlignRotPos,lModelRotPos,pAlignTo,pModel)
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
        self.ZoomTimeline(sourcecamera)
        # creat camera forrow source
        oldcamname = sourcecamera.Name
        sourcecamera.Name = "Exrig_cam"
        ue4cam = fb.FBCamera(oldcamname)
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
            camoptions = fb.FBPlotOptions()
            camoptions.PlotLockedProperties = True
            camoptions.PlotPeriod = fb.FBTime(0, 0, 0, 1, 0, fb.FBPlayerControl().GetTransportFps())
            camoptions.UseConstantKeyReducer = False
            camoptions.ConstantKeyReducerKeepOneKey = True
            camoptions.RotationFilterToApply = fb.FBRotationFilter.kFBRotationFilterUnroll
            myTake.PlotTakeOnSelected(camoptions)
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
        # don't select camera
        lList = fb.FBComponentList()
        parentModel = fb.FBFindObjectsByName('*', lList, False, True)
        for item in lList:
            item.Selected = True
        for camera in fb.FBSystem().Scene.Cameras:
            camera.Selected = False
        for lcomp in lList:
            if lcomp.Name == 'Camera Switcher':
                lcomp.Selected = False
        # Plot Select options
        lFPS = fb.FBTime(0, 0, 0, 1, 0, fb.FBPlayerControl().GetTransportFps())
        loptions = fb.FBPlotOptions()
        loptions.PlotLockedProperties = True
        loptions.PlotPeriod = lFPS
        loptions.UseConstantKeyReducer = False
        loptions.ConstantKeyReducerKeepOneKey = True
        loptions.RotationFilterToApply = fb.FBRotationFilter.kFBRotationFilterUnroll
        currentTake = fb.FBSystem().CurrentTake
        currentTake.PlotTakeOnSelected(loptions)
        # delet all storytrack
        ltracklist = []
        allStoryTracks = fb.FBStory().RootFolder.Tracks
        for storyTrack in allStoryTracks:
            if storyTrack:
                ltracklist.append(storyTrack)
        for ldeted in ltracklist:
            ldeted.FBDelete()
        for camera in [c for c in fb.FBSystem().Scene.Cameras if not c.SystemCamera]:
            camera.Selected = True
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
        fb.FBFindObjectsByName('1:*', foundComponents, True, False)
        for ca in foundComponents:
            try:
                ca.FBDelete()
            except:
                pass
        # Face curve deleted
        exfoundComponents = fb.FBComponentList()
        fb.FBFindObjectsByName('*Exrig_*', exfoundComponents, True, True)
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
        del (soptions, loptions,lFPS)
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
        shutil.copyfile('C:/Users/Public/Documents/temp.fbx',filePath)
        del(soptions,filePath)
    def Reder(self,filePath):
        filePath = filePath.encode('ascii')
        proj = filePath.split('/')[1]
        ep = filePath.split('/')[3]
        sc = filePath.split('/')[4]
        seq = filePath.split('/')[5]
        # render something
        gSystem = fb.FBSystem()
        lControl = fb.FBPlayerControl()
        timeSpan = gSystem.CurrentTake.LocalTimeSpan
        lStart = timeSpan.GetStart()
        lStop = timeSpan.GetStop()
        lStepFrame = 1
        lFrameRate = lControl.GetTransportFpsValue()
        # Set VideoCodec Option:
        VideoManager = fb.FBVideoCodecManager()
        VideoManager.VideoCodecMode = fb.FBVideoCodecMode.FBVideoCodecStored
        lApp = fb.FBApplication()
        lOptions = fb.FBVideoGrabber().GetOptions()
        lOptions.ViewingMode = fb.FBVideoRenderViewingMode().FBViewingModeModelsOnly
        lOptions.TimeSpan = timeSpan
        lOptions.RenderAudio = fb.FBAudioRateMode.kFBAudioRateMode_48000
        lOptions.TimeSteps = fb.FBTime(0, 0, 0, 1)
        lOptions.CameraResolution = fb.FBCameraResolutionMode().kFBResolutionCustom
        lOptions.AntiAliasing = False
        lOptions.RenderAudio = True
        lOptions.FieldMode = fb.FBVideoRenderFieldMode().FBFieldModeNoField
        lOptions.BitsPerPixel = fb.FBVideoRenderDepth().FBVideoRender24Bits
        lOptions.ShowCameraLabel = False
        lOptions.ShowSafeArea = False
        lOptions.ShowTimeCode = True
        # Save path choose
        for group in fb.FBSystem().Scene.Groups:
            if group.Name == 'AllFace':
                group.Show = False
        lOptions.OutputFileName = 'C:/Users/Public/Documents/temp.mov'
        lApp.FileRender(lOptions)
        shutil.copyfile('C:/Users/Public/Documents/temp.mov', "%s/%s_%s_%s_%s.mov"%(filePath,proj,ep,sc,seq))

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
        for lTakeIndex in range(options.GetTakeCount()):
            options.SetTakeSelect(lTakeIndex, False)
        options.SetTakeSelect(0, False)
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
            if re.search('_moburig_',namespace.Name) and not re.search('_Ctrl',namespace.Name):
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
    def findOtherStepAsset(self,data,code,step):
        for item in data:
            if item.get('json').get('step_code')== step and item.get('json').get('asset_code')==code:
                return item
    def xml(self,item,data):
        outPath = item.get('json').get('Publish_path')
        pro = outPath.split('/')[1]
        ep = outPath.split('/')[3]
        sc = outPath.split('/')[4]
        seq = outPath.split('/')[5]
        self.bakeClean()
        fb.FBApplication().FileNew()
        self.openFile('C:/Users/Public/Documents/temp.fbx')
        for camera in [c for c in fb.FBSystem().Scene.Cameras if not c.SystemCamera]:
            name = camera.Name
            self.Match_Camera(name)
            self.camExport('%s/%s_%s_%s_%s_%s.fbx'%(outPath,pro,ep,sc,seq,name),name)
        char = self.exportFile(outPath,pro,ep,sc,seq)

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
            SkeletalAnimation.set('name',each)
            SkeletalAnimation.set('Path', '%s/%s_%s_%s_%s_%s.fbx'%(outPath,pro,ep,sc,seq,each))
            rigItem = self.findOtherStepAsset(data, code, 'rig')
            SkeletalAnimation.set('Reference',
                                  '%s/%s_rig_%s.fbx' % (rigItem.get('json').get('Publish_path'), code, version))
        for camera in [c for c in fb.FBSystem().Scene.Cameras if not c.SystemCamera]:
            name = camera.Name
            temp = SubElement(Task, 'Camera')
            StartFrame,EndFrame = self.GetKeysFram(camera)
            temp.set('Path','%s/%s_%s_%s_%s_%s.fbx'%(outPath,pro,ep,sc,seq,name))
            temp.set('StartFrame',str(StartFrame))
            temp.set('EndFrame', str(EndFrame))
            temp.set('CharactersNumber', str(1))
            temp.set('CharactersActType', 'Drama')
            temp.set('CharacterMoveSpeed','Slow')
            temp.set('LensType', 'SCU01')
            temp.set('name', name)
        tree.write(outPath + '/Description.xml', encoding='utf-8', xml_declaration=True)
    def backUp(self,path):
        if os.path.exists(path):
            dPath = os.path.dirname(path)
            file = os.path.basename(path)
            if not os.path.exists('%s/backup'%dPath):
                os.mkdir('%s/backup'%dPath)
            shutil.copyfile(path, '%s/backup/%s_%s'%(dPath,str(datetime.datetime.now()).replace(':','.'),file))
    def getShotChar(self):
        data = {}
        temp = []
        for camera in [c for c in fb.FBSystem().Scene.Cameras if not c.SystemCamera]:
           temp.append(camera.Name)
        data['shot'] = temp
        temp = []
        for namespace in fb.FBSystem().Scene.Namespaces:
            if re.search('_moburig_', namespace.Name) and not re.search('Ctrl', namespace.Name):
                temp.append(namespace.Name)
        data['char'] = temp
        return data
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

class MayaMenu(TeamonesFoo):
    work_menu_data = [u"打开文件", u"打开文件路径", u"导入Maya文件"]
    publish_menu_data = []

    def __init__(self, server):
        super(MayaMenu, self).__init__(server)
        # 设置工作界面菜单
        self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.set_menu(self.work_menu_data)

    def connect_ui(self):
        super(MayaMenu, self).connect_ui()
        # 菜单功能
        self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.action_clicked.connect(self.execute_action)

    def execute_action(self, data):
        fun_mapping = {u"打开文件": self.open_file, u"打开目录": self.open_dir, u"导入Maya文件": self.import_maya_file}

        try:
            row = self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.selectedIndexes()[0].row()
            file_path = self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.selectedIndexes()[0].model().index(row, 1).data()

            return fun_mapping[data](file_path)

        except IndexError:
            dy.MMessage.warning(u"请选择一个文件", self)

    @staticmethod
    def open_dir(file_path):
        """
        打开文件文件夹
        :return:
        """
        file_dir = os.path.split(file_path)[0]
        os.startfile(file_dir)

    @staticmethod
    def open_file(file_path):
        print file_path

    def import_maya_file(self):
        pass

class MobuMenu(TeamonesFoo):

    def __init__(self, server):
        super(MobuMenu, self).__init__(server)
        self.mobu = Mobu()
        # 设置工作界面菜单
        self.mapping = {u"保存版本": self.saveAction, u"提交审核": self.postCheck, u"合并文件": self.mergeAction,
                        u"替换文件": self.replaceAction, u"拍频": self.renderAction,u"打开目录": self.opendir,
                        u"打开文件": self.openAction,u"提交动画导出": self.commitAnimExport,u"提交布料烘焙": self.commitAnimBake,
                        }
        self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.set_menu(self.mapping.keys())

    def connect_ui(self):
        super(MobuMenu, self).connect_ui()
        # 菜单功能
        self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.action_clicked.connect(self.execute_action)

    def execute_action(self, data):
        try:
            self.mapping[data]
        except IndexError:
            dy.MMessage.warning(u"请选择一个文件", self)

    def saveAction(self):
        item = self.taskSideWidget.task_data
        selected = self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.selectedIndexes()
        if self._cur_step_category == 'asset':
            code = item.get('code')
            file_name = '%s_V##.fbx' % code
            check_name = '%s_V\d\d.fbx' % code
            my_str, ok = QtWidgets.QInputDialog.getText(self, u'名字过滤', u'输入文件名,请把##改为版本序号', QtWidgets.QLineEdit.Normal,
                                                        file_name)
            if re.search(check_name, str(my_str)) and ok:
                newpath = '%s/%s' % (item.get('work_path'), str(my_str))
                self.mobu.backUp(newpath)
                self.mobu.saveFile(newpath)

        if self._cur_step_category == 'sequence':
            newpath = '%s/%s_%s_%s.fbx' % (item.get('work_path'), item.get('project_code'),item.get('episodes_code'), item.get('sequence_code'))
            self.mobu.backUp(newpath)
            self.mobu.saveFile(newpath)


    def postCheck(self):
        item = self.taskSideWidget.task_data
        update_data = {"task_status": self.status[u"进行中"]}
        self.server.task.update(item.get('task_id'), update_data)
        dy.MMessage.warning(u"提交成功", self)

    def mergeAction(self):
        item = self.taskSideWidget.task_data
        selected = self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.selectedIndexes()
        row = selected[0].row()
        path = ''
        if selected:
            path = '%s/%s' % (item.get('work_path'), str(selected[0].model().index(row, 1).data()))
        else:
            path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
        if path:
            self.mobu.mergeFile(path)
    def replaceAction(self):
        item = self.taskSideWidget.task_data
        selected = self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.selectedIndexes()
        row = selected[0].row()
        path = ''
        if selected:
            path = '%s/%s' % (item.get('work_path'), str(selected[0].model().index(row, 1).data()))
        else:
            path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
        if path:
            self.mobu.replaceFile(path)
    def renderAction(self):
        item = self.taskSideWidget.task_data
        if self._cur_step_category == 'sequence':
            self.mobu.Reder(item.get('work_path'))
            dy.MMessage.warning(u"拍频成功", self)
    def opendir(self):
        item = self.taskSideWidget.task_data
        os.startfile(item.get('work_path'))
    def openAction(self):
        item = self.taskSideWidget.task_data
        selected = self.taskSideWidget.existingVersionWidget.fileListWidget.work_list.selectedIndexes()
        row = selected[0].row()
        path = ''
        if selected:
            path = '%s/%s' % (item.get('work_path'), str(selected[0].model().index(row, 1).data()))
        else:
            path = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
        if path:
            self.mobu.openFile(path)
    def commitAnimExport(self):
        item = self.taskSideWidget.task_data
        input_file = '%s/%s_%s_%s.fbx' % (item.get('work_path'), item.get('project_code'),item.get('episodes_code'), item.get('sequence_code'))
        if item.get('step_code') == 'animation' and os.path.exists(input_file):
            dic = {'taskStatus': 'wait', 'TaskType': 'AnimateExport', 'input_file': input_file,
                   'Publish_path': item.get('json').get('publish_path'),
                   'TaskId': item.get('uuid'), 'project': item.get('project_code').get('code'),
                   'episode': item.get('episodes_code'),
                   'sequence': item.get('sequence_code'),
                   'entity_id': item.get('entity_id')
                   }
            r_json = requests.post('http://%s:5000/mobu/con?action=post' % node_server,json.dumps(dic))
            dy.MMessage.warning(json.loads(r_json.content).get('info'), self)

    def commitAnimBake(self):
        item = self.taskSideWidget.task_data
        input_file = '%s/%s_%s_%s.fbx' % (
        item.get('work_path'), item.get('project_code'), item.get('episodes_code'), item.get('sequence_code'))
        if item.get('step_code') == 'animation' and os.path.exists(input_file):
            dic = {'taskStatus': 'transVersion', 'TaskType': 'AnimateExport', 'input_file': input_file,
                   'Publish_path': item.get('json').get('publish_path'),
                   'TaskId': item.get('uuid'), 'project': item.get('project_code').get('code'),
                   'episode': item.get('episodes_code'),
                   'sequence': item.get('sequence_code'),
                   'entity_id': item.get('entity_id')
                   }
            r_json = requests.post('http://%s:5000/bake/con?action=post' % node_server, json.dumps(dic))
            dy.MMessage.warning(json.loads(r_json.content).get('info'), self)

class Ue4Widget(TeamonesFoo):
    def __init__(self, server):
        super(Ue4Widget, self).__init__(server)


if __name__ == "__main__":
    sys.path.append("D:/SMWH_project/teamones_sdk")

    from teamones_api import teamnoes

    app = QtWidgets.QApplication(sys.argv)
    tm = teamnoes.TeamOnes(base_url="http://10.168.30.17:18101", username="18107414338", password="123456")

    Alert_Example = Maya(tm)
    Alert_Example.show()
    app.exec_()
