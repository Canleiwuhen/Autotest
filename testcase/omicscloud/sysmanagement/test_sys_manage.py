import pytest
import allure


@pytest.mark.usefixtures("res")
class TestSys:
    comdata = {
        "userName": "test_apiforward",
        "userRealName": "测试123123",
        "projectCodeList": [
            "CNV-seq",
            "NIFTY",
            "NBS",
            "CS"
        ],
        "rolesIdList": [
            "514496125806444544"
        ],
        "password": "test123123@123",
        "passwordConfirm": "test123123@123",
        "userMobile": "15361476671",
        "userEmail": "15361476671@163.com",
        "userId": ""
    }

    institution_data = {
            "instId": "", "instCode": "", "instName": "autotest", "appList": [
                {"appName": "autotest", "appKey": "", "appSecret": "", "resourceIds": "", "accessMode": "FixedIP",
                 "ipAddress": "10.227.0.1", "locked": 0}]
        }

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-新增用户")
    def test_add_user(self, res):
        """
        用例上包含新增用户、删除用户的场景验证
        :param res:
        :return:
        """
        data = self.comdata
        # 新增用户操作
        response = res.post_request("/api/base/user/add", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        # 后处理，删除已新增的用户确保用例可以重复执行
        # 先查询出用户ID，再执行删除
        search_data = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        delete_data = {"userId": userid}
        delete_res = res.post_request("/api/base/user/delete", json=delete_data)
        assert delete_res.status_code == 200
        assert delete_res.json()['retInfo'] == 'success'
        search_res_again = res.post_request("/api/base/user/list", json=search_data).json()
        assert search_res_again['result']['total'] == 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-查询用户")
    def test_search_user(self, res):
        """
        用例包含按用户名、姓名和角色查询
        :param res:
        :return:
        """
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        # 按用户名查询
        search_data1 = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res1 = res.post_request("/api/base/user/list", json=search_data1).json()
        assert search_res1['result']['total'] == 1
        assert search_res1['result']['records'][0]['userName'] == 'test_apiforward'
        # 按用户姓名查询
        search_data2 = {"page": 1, "pageNum": 1, "limit": 100, "userRealName": "测试123123"}
        search_res2 = res.post_request("/api/base/user/list", json=search_data2).json()
        assert search_res2['result']['total'] != 0
        assert search_res2['result']['records'][0]['userRealName'] == '测试123123'
        # 按角色查询
        search_data3 = {"page": 1, "pageNum": 1, "limit": 100, "roleIdList": ['444516187007746048']}
        search_res3 = res.post_request("/api/base/user/list", json=search_data3).json()
        assert search_res3['result']['total'] != 0
        assert search_res3['result']['records'][0]['roleId'] == '444516187007746048'
        # 最后执行删除
        userid = search_res1['result']['records'][0]['userId']
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-编辑用户")
    def test_edit_user(self, res):
        """
        编辑用户信息操作
        :param res:
        :return:
        """
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        search_data = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        # 编辑操作
        edit_data = {
            "userName": "test_apiforward",
            "userRealName": "测试123123",
            "projectCodeList": [
                "CNV-seq",
                "CS",
                "NBS",
                "NIFTY"
            ],
            "rolesIdList": [
                "514496125806444544"
            ],
            "userMobile": "153614766712",
            "userEmail": "15361476671@163.com",
            "userId": userid
        }
        edit_res = res.post_request("/api/base/user/update", json=edit_data)
        assert edit_res.status_code == 200
        assert edit_res.json()['retInfo'] == 'success'
        search_data = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-重置密码")
    def test_update_pwd(self, res, res_cus):
        """
        重置用户密码操作
        :param res:
        :return:
        """
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        search_data = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        # 重置操作
        update_data = {"userId": userid, "password": "test123123@555",
                       "passwordConfirm": "test123123@555"}
        update_res = res.post_request("/api/base/user/reSetPassword", json=update_data)
        assert update_res.status_code == 200
        assert update_res.json()['retInfo'] == 'success'
        # 验证重置密码后是否可登录账号
        username = "test_apiforward"
        pwd = "test123123@555"
        login_res = res_cus(username, pwd)
        assert login_res.status_code == 200
        assert login_res.json()["retInfo"] == 'success'
        # 测试后删除数据
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-禁用用户")
    def test_suspend_user(self, res, res_cus):
        """
        禁用用户操作
        :param res:
        :return:
        """
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        search_data = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        # 禁用操作
        suspend_data = {"userId": userid, "status": 1}
        suspend_res = res.post_request("/api/base/user/enable", json=suspend_data)
        assert suspend_res.status_code == 200
        assert suspend_res.json()['retInfo'] == 'success'
        # 验证禁用账号不可登录
        username = data['userName']
        pwd = data['password']
        login_res = res_cus(username, pwd)
        assert login_res.status_code == 200
        assert login_res.json()["retInfo"] == '账号已被禁用，无法使用'
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-校验新增相同用户")
    def test_add_identical_user(self, res):
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        # 重新新增相同用户
        ret_res = res.post_request("/api/base/user/add", json=data)
        assert ret_res.status_code == 200
        assert '用户已存在' in ret_res.json()['retInfo']
        search_data = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-设置业务范围为{data}")
    @pytest.mark.parametrize("business", ["bgiCenterDelivery", "bgiExpertServices", "siteInterpretationLib"])
    def test_edit_user_business(self, res, business):
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        search_data = {"userName": "test_apiforward", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        business_res = res.post_request(f"/api/base/user/configUserBusiness/{userid}/{business}")
        assert business_res.status_code == 200
        assert business_res.json()['retInfo'] == 'success'
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-查询角色")
    def test_search_role(self, res):
        data = {"roleName": "测试角色", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/role/findRoleAll", json=data)
        assert search_res.status_code == 200
        assert search_res.json()['result']['records'][0]['roleName'] == '测试角色'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-新增角色")
    def test_touch_role(self, res):
        touch_data = {"roleName": "test_apiforward_role", "menuIdList": ["101", "102", "10202", "10301", "10302"]}
        touch_res = res.post_request("/api/base/role/insertRole", json=touch_data)
        assert touch_res.status_code == 200
        assert touch_res.json()['retInfo'] == 'success'
        # 查询已新增的角色
        search_data = {"roleName": "test_apiforward_role", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/role/findRoleAll", json=search_data)
        role_id = search_res.json()['result']['records'][0]['id']
        # 新增后删除数据
        delete_data = {"roleId": role_id}
        delete_res = res.post_request("/api/base/role/delRoleById", json=delete_data)
        assert delete_res.status_code == 200
        assert delete_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-编辑角色")
    def test_edit_role(self, res):
        # 先新增角色
        touch_data = {"roleName": "test_apiforward_role", "menuIdList": ["101", "102", "10202", "10301", "10302"]}
        res.post_request("/api/base/role/insertRole", json=touch_data)
        # 查询已新增的角色
        search_data = {"roleName": "test_apiforward_role", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/role/findRoleAll", json=search_data)
        role_id = search_res.json()['result']['records'][0]['id']
        # 编辑角色
        edit_data = {"id": role_id, "menuIdList": ["101", "102", "10201", "10202", "10301", "10302"],
                     "roleName": "test_apiforward_role"}
        edit_res = res.post_request("/api/base/role/updateRole", json=edit_data)
        assert edit_res.status_code == 200
        assert edit_res.json()['result'] == '修改成功'
        # 新增后删除数据
        delete_data = {"roleId": role_id}
        delete_res = res.post_request("/api/base/role/delRoleById", json=delete_data)
        assert delete_res.status_code == 200
        assert delete_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-权限管理")
    @allure.title("系统管理-权限管理-禁用角色")
    def test_suspend_role(self, res):
        # 先新增角色
        touch_data = {"roleName": "test_apiforward_role", "menuIdList": ["101", "102", "10202", "10301", "10302"]}
        res.post_request("/api/base/role/insertRole", json=touch_data)
        # 查询已新增的角色
        search_data = {"roleName": "test_apiforward_role", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/role/findRoleAll", json=search_data)
        role_id = search_res.json()['result']['records'][0]['id']
        suspend_data = {"roleId": role_id, "status": 1}
        suspend_res = res.post_request("/api/base/role/enable", json=suspend_data)
        assert suspend_res.status_code == 200
        assert suspend_res.json()['retInfo'] == 'success'
        # 新增后删除数据
        delete_data = {"roleId": role_id}
        delete_res = res.post_request("/api/base/role/delRoleById", json=delete_data)
        assert delete_res.status_code == 200
        assert delete_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-医院管理")
    @allure.title("系统管理-医院管理-新增医院+科室+医生")
    def test_add_hospital(self, res):
        # 新增医院
        add_data = {"hospitalName": "test_apiforward_hospital", "status": 1}
        add_res = res.post_request("/api/base/hospitals/add", json=add_data)
        assert add_res.status_code == 200
        assert add_res.json()['result']['hospitalName'] == 'test_apiforward_hospital'
        # 查询新增医院的id
        search_data = {"hospitalName": "test_apiforward_hospital", "pageNum": 1, "pageSize": 1000}
        search_res = res.post_request("/api/base/hospitals/page", json=search_data)
        hospitalid = search_res.json()['result']['records'][0]['hospitalId']
        # 新增医院下的科室
        adddep_data = {"hospitalId": hospitalid, "departmentName": "test_apiforward_dep", "status": 1,
                       "parentId": 0}
        adddep_res = res.post_request("/api/base/departments/add", json=adddep_data)
        assert adddep_res.status_code == 200
        assert adddep_res.json()['result']['departmentName'] == 'test_apiforward_dep'
        depid = adddep_res.json()['result']['departmentId']
        # 新增医生
        adddoc_data = {"hospitalId": hospitalid, "departmentId": depid,
                       "doctorName": "test_docter_api", "status": 1}
        adddoc_res = res.post_request("/api/base/hospital/doctors/add", json=adddoc_data)
        assert adddoc_res.status_code == 200
        assert adddoc_res.json()['result']['doctorName'] == 'test_docter_api'
        # 删除已新增的数据
        delete_url = '/api/base/hospitals/delete/' + hospitalid
        delete_res = res.post_request(url=delete_url)
        assert delete_res.status_code == 200
        assert delete_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-医院管理")
    @allure.title("系统管理-医院管理-禁用医院")
    def test_suspend_hospital(self, res):
        # 新增医院
        add_data = {"hospitalName": "test_apiforward_hospital", "status": 1}
        add_res = res.post_request("/api/base/hospitals/add", json=add_data)
        assert add_res.status_code == 200
        assert add_res.json()['result']['hospitalName'] == 'test_apiforward_hospital'
        # 查询新增医院的id
        search_data = {"hospitalName": "test_apiforward_hospital", "pageNum": 1, "pageSize": 1000}
        search_res = res.post_request("/api/base/hospitals/page", json=search_data)
        hospitalid = search_res.json()['result']['records'][0]['hospitalId']
        # 禁用医院
        suspend_url = '/api/base/hospitals/disable/' + hospitalid
        suspend_res = res.post_request(url=suspend_url)
        assert suspend_res.status_code == 200
        assert suspend_res.json()['retInfo'] == 'success'
        # 查询对应医院状态是否禁用
        search_res_tmp = res.post_request("/api/base/hospitals/page", json=search_data)
        assert search_res_tmp.json()['result']['records'][0]['status'] == 0
        # 删除已新增的数据
        delete_url = '/api/base/hospitals/delete/' + hospitalid
        delete_res = res.post_request(url=delete_url)
        assert delete_res.status_code == 200
        assert delete_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-医院管理")
    @allure.title("系统管理-医院管理-禁用科室+医生")
    def test_suspend_data(self, res):
        # 新增医院
        add_data = {"hospitalName": "test_apiforward_hospital", "status": 1}
        add_res = res.post_request("/api/base/hospitals/add", json=add_data)
        # 查询新增医院的id
        search_data = {"hospitalName": "test_apiforward_hospital", "pageNum": 1, "pageSize": 1000}
        search_res = res.post_request("/api/base/hospitals/page", json=search_data)
        hospitalid = search_res.json()['result']['records'][0]['hospitalId']
        # 新增医院下的科室
        adddep_data1 = {"hospitalId": hospitalid, "departmentName": "test_apiforward_dep1", "status": 1,
                        "parentId": 0}
        adddep_data2 = {"hospitalId": hospitalid, "departmentName": "test_apiforward_dep2", "status": 1,
                        "parentId": 0}
        adddep_res1 = res.post_request("/api/base/departments/add", json=adddep_data1)
        depid1 = adddep_res1.json()['result']['departmentId']
        adddep_res2 = res.post_request("/api/base/departments/add", json=adddep_data2)
        depid2 = adddep_res2.json()['result']['departmentId']
        # 新增医生
        adddoc_data1 = {"hospitalId": hospitalid, "departmentId": depid1,
                        "doctorName": "test_docter_api1", "status": 1}
        adddoc_res1 = res.post_request("/api/base/hospital/doctors/add", json=adddoc_data1)
        docid1 = adddoc_res1.json()['result']['doctorId']
        adddoc_data2 = {"hospitalId": hospitalid, "departmentId": depid1,
                        "doctorName": "test_docter_api2", "status": 1}
        adddoc_res2 = res.post_request("/api/base/hospital/doctors/add", json=adddoc_data2)
        docid2 = adddoc_res2.json()['result']['doctorId']
        # 禁用科室2
        suspend_dep2_url = '/api/base/departments/disable/' + depid2
        suspend_dep2_res = res.post_request(url=suspend_dep2_url)
        assert suspend_dep2_res.status_code == 200
        assert suspend_dep2_res.json()['retInfo'] == 'success'
        # 查询对应科室状态是否禁用
        search_dep_data = {"hospitalId": hospitalid, "parentId": 0, "pageNum": 1, "pageSize": 1000}
        search_dep_res = res.post_request("/api/base/departments/page", json=search_dep_data)
        dep_list = search_dep_res.json()['result']['records']
        new_dep_list = {}
        for i in dep_list:
            new_dep_list[i['departmentId']] = i['status']
        assert new_dep_list[depid2] == 0  # 校验科室2的状态是否为禁用
        assert new_dep_list[depid1] == 1  # 校验科室1的状态是否为启用
        # 禁用科室1下的医生1
        suspend_doc2_url = '/api/base/hospital/doctors/disable/' + docid1
        suspend_doc2_res = res.post_request(url=suspend_doc2_url)
        assert suspend_doc2_res.status_code == 200
        assert suspend_doc2_res.json()['retInfo'] == 'success'
        # 查询对应医生1状态是否禁用
        search_doc_data = {"hospitalId": hospitalid, "departmentId": depid1, "pageNum": 1, "pageSize": 1000}
        search_doc_res = res.post_request("/api/base/hospital/doctors/page", json=search_doc_data)
        doc_list = search_doc_res.json()['result']['records']
        new_doc_list = {}
        for i in doc_list:
            new_doc_list[i['doctorId']] = i['status']
        assert new_doc_list[docid1] == 0  # 校验科室2的状态是否为禁用
        assert new_doc_list[docid2] == 1  # 校验科室1的状态是否为启用
        # 删除已新增的数据
        delete_url = '/api/base/hospitals/delete/' + hospitalid
        delete_res = res.post_request(url=delete_url)
        assert delete_res.status_code == 200
        assert delete_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-运维管理")
    @allure.title("系统管理-运维管理-查询")
    def test_search_configItem(self, res):
        # 系统设置页面查询
        search_data1 = {"type": "Sys"}
        search_data1_res = res.post_request("/api/base/configItem/page", json=search_data1)
        assert search_data1_res.status_code == 200
        search_data1_list = search_data1_res.json()['result']['records']
        config_data = {}
        for i in search_data1_list:
            config_data[i['configItemId']] = i['configName']
        assert config_data['1'] == "系统区域设置"
        assert config_data['2'] == "系统时间设置"
        # 检测项目设置页面查询
        search_data2 = {"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100, "type": "ProjectCode"}
        search_data2_res = res.post_request("/api/base/projects/page", json=search_data2)
        assert search_data2_res.status_code == 200
        assert search_data2_res.json()['result']['total'] > 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-运维管理")
    @allure.title("系统管理-运维管理-检测项目设置-项目设置")
    def test_project_config(self, res):
        projectCode = {"1": "CNV-seq", "2": "NIFTY", "3": "NBS", "4": "CS"}
        search_data = {"type": "ProjectCode", "projectCode": ""}
        # 检查CNVSEQ
        search_data['projectCode'] = projectCode['1']
        search_data_cnvseq_res = res.post_request("/api/base/configItem/page", json=search_data)
        assert search_data_cnvseq_res.status_code == 200
        assert search_data_cnvseq_res.json()['result']['records'][0]['projectCode'] == 'CNV-seq'
        assert search_data_cnvseq_res.json()['result']['records'][0]['configName'] == '实验流程'
        # 检查NIFTY
        search_data['projectCode'] = projectCode['2']
        search_data_nifty_res = res.post_request("/api/base/configItem/page", json=search_data)
        assert search_data_nifty_res.status_code == 200
        assert search_data_nifty_res.json()['result']['records'][0]['projectCode'] == 'NIFTY'
        list_tmp1 = []
        for i in search_data_nifty_res.json()['result']['records']:
            list_tmp1.append(i['configName'])
        assert list_tmp1 == ['nifty实验方法配置', 'nifty pro实验方法配置', '全因及团标 其他CNV展示', 'NIFTY基础 其他CNV展示', '过滤前CNV开关',
                             '性别（仅国际可以开）', 'chrX/Y浓度', 'Z值', '检测日期', 'DMD', '重分析', '结果编辑', '实验流程', '查询CNV']
        # 检查NBS
        search_data['projectCode'] = projectCode['3']
        search_data_nbs_res = res.post_request("/api/base/configItem/page", json=search_data)
        assert search_data_nbs_res.status_code == 200
        assert search_data_nbs_res.json()['result']['records'][0]['projectCode'] == 'NBS'
        list_tmp2 = []
        for i in search_data_nbs_res.json()['result']['records']:
            list_tmp2.append(i['configName'])
        assert list_tmp2 == ['实验流程', '待选板号-实验工序']
        # 检查CS
        search_data['projectCode'] = projectCode['4']
        search_data_cs_res = res.post_request("/api/base/configItem/page", json=search_data)
        assert search_data_cs_res.status_code == 200
        assert search_data_cs_res.json()['result']['records'][0]['projectCode'] == 'CS'
        list_tmp3 = []
        for i in search_data_cs_res.json()['result']['records']:
            list_tmp3.append(i['configName'])
        assert list_tmp3 == ['实验流程', '待选板号-实验工序', '是否自动配对分析']

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-客户端管理")
    @allure.title("系统管理-客户端管理-查询")
    def test_search_institution(self, res):
        response = res.post_request("/api/base/authInstitution/pageInstitutions",
                                    json={"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-客户端管理")
    @allure.title("系统管理-客户端管理-新增机构")
    def test_add_institution(self, res, mysql_connect):
        save_data = self.institution_data
        save_data_res = res.post_request("/api/base/authInstitution", json=save_data)
        assert save_data_res.status_code == 200
        assert save_data_res.json()['retInfo'] == 'success'
        # 删除已新增的数据
        mysql_connect.execute("delete from base_auth_institution where inst_name ='autotest'")
        mysql_connect.execute("delete from base_auth_app where app_name ='autotest'")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-客户端管理")
    @allure.title("系统管理-客户端管理-编辑/禁用机构")
    def test_disable_institution(self, res, mysql_connect):
        save_data = self.institution_data
        save_data_res = res.post_request("/api/base/authInstitution", json=save_data)
        assert save_data_res.status_code == 200
        assert save_data_res.json()['retInfo'] == 'success'
        # 查询已新增的机构
        search_data = {"instName": "autotest", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/authInstitution/pageInstitutions", json=search_data)
        # 编辑机构
        edit_data = search_res.json()['result']['records'][0]
        tmp = {"status": 0}
        edit_data.update(tmp)
        edit_res = res.post_request("/api/base/authInstitution/edit", json=edit_data)
        assert edit_res.status_code == 200
        assert edit_res.json()['retInfo'] == 'success'
        # 新增后删除数据
        mysql_connect.execute("delete from base_auth_institution where inst_name ='autotest'")
        mysql_connect.execute("delete from base_auth_app where app_name ='autotest'")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("系统管理-客户端管理")
    @allure.title("系统管理-客户端管理-编辑/启用机构")
    def test_enable_institution(self, res, mysql_connect):
        save_data = self.institution_data
        save_data_res = res.post_request("/api/base/authInstitution", json=save_data)
        assert save_data_res.status_code == 200
        assert save_data_res.json()['retInfo'] == 'success'
        # 查询已新增的机构
        search_data = {"instName": "autotest", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/authInstitution/pageInstitutions", json=search_data)
        # 编辑机构
        edit_data = search_res.json()['result']['records'][0]
        tmp = {"status": 1}
        edit_data.update(tmp)
        edit_res = res.post_request("/api/base/authInstitution/edit", json=edit_data)
        assert edit_res.status_code == 200
        assert edit_res.json()['retInfo'] == 'success'
        # 新增后删除数据
        mysql_connect.execute("delete from base_auth_institution where inst_name ='autotest'")
        mysql_connect.execute("delete from base_auth_app where app_name ='autotest'")
