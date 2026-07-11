from random import sample
from urllib.parse import urlencode

import allure
import pytest

from data_generate.nifty.datagenerate import DataGenerate

test_user = 'testuser1'

@allure.feature("主流程测试")
class TestKeyProcess:
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景1")
    @allure.title("路径：0:提交送检单--1:技术路线确认--2:血浆分离--3:建库--4:BMG--5:Pooling--6:单链环化--7:MakeDNB-8:上机--9:信息分析--10：数据审核")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 10, 'run_time': 1, 'user_name': test_user, 'istest':True}],
                             indirect=True)
    def test_from_submit_inspection_to_data_review(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的样例编号，用于查询数据审核状态并断言
        samples = generate_steps[0]['sample']
        if samples:
            query_data = {
                "task": {"zsample": ",".join(samples)},
                "pageNumber": 1,
                "zgxbh": "InsSheetCycle",
                "pageSize": 10000,
                "token": token,
                "menuId": "MdInfoQuery_InsSheetCycle"
            }
            response = res.post_request("/presap/webintf.do?method=query_samples_of_cycle", data=urlencode(query_data))
            response_json = response.json()
            if response_json["code"] == "200" and len(response_json["data"]) > 0:
                for i in range(len(response_json["data"])):
                    assert response_json["data"][i]["mca_zjobcode"] == "已审核", f"主流程测试场景1异常：数据审核断言失败，原因：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景2")
    @allure.title("路径：0:提交送检单--1:技术路线确认--2:血浆分离--3:建库--4:BMG--5:Pooling--6：质检产物")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 6, 'run_time': 1, 'user_name': test_user, 'istest':True}],
                             indirect=True)
    def test_from_submit_inspection_to_quality_inspection_products(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的样例编号，用于查询质检产物并断言
        samples = generate_steps[0]['sample']
        if samples:
            query_data = {
                "task": {"zsample": ",".join(samples),"zzjcwbs":"X"},
                "pageNumber": 1,
                "zgxbh": "InsSheetCycle",
                "pageSize": 10000,
                "token": token,
                "menuId": "MdInfoQuery_InsSheetCycle"
            }
            response = res.post_request("/presap/webintf.do?method=query_samples_of_cycle", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["code"] == "200" and len(response_json["data"]) == len(samples), f"主流程测试场景2异常：质检产物断言失败，原因：{response_json}"


    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景3")
    @allure.title("路径：0:提交送检单--1:技术路线确认--2:血浆分离--3：重复质控品")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path3', 'last_step': 3, 'run_time': 1, 'user_name': test_user, 'istest':True}],
                             indirect=True)
    def test_from_submit_inspection_to_repeat_controller(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的样例编号，用于查询重复质控品并断言
        samples = generate_steps[0]['sample']
        if samples:
            query_data = {
                "task": {"zsample": ",".join(samples)},
                "pageNumber": 1,
                "pageSize": 10000,
                "zgxbh": "MAE",
                "token": token,
                "menuId": "MSTaskMaster_JK_JKFDealOrder"
            }
            # 在建库-新建任务单环节查询样例的zguid字段，用于查询重复质控品信息
            response = res.post_request("/presap/webintf.do?method=task_assign_samplems", data=urlencode(query_data))
            response_json = response.json()
            zguid = []
            if response_json["code"] == "200" and len(response_json["data"]) >0:
                for i in range(len(response_json["data"])):
                    zguid.append(response_json["data"][i]["zguid"])
            query_data = {
                "zguid": ",".join(zguid),
                "token": token,
                "menuId": "MSTaskMaster_JK_JKFDealOrder"

            }
            # 在建库-任务下达环节查询重复质控品列表
            response = res.post_request("/presap/webintf.do?method=query_zkp_by_zguid", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["code"] == "200" and len(response_json["data"]) >= len(samples), f"主流程测试场景3异常：重复质控品断言失败，原因：{response_json}"


    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景4")
    @allure.title("路径：0:提交送检单--1:技术路线确认--2:血浆分离--3：产物补录")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path4', 'last_step': 3, 'run_time': 1, 'user_name': test_user, 'istest':True}],
                             indirect=True)
    def test_from_submit_inspection_to_product_supplement(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的样例编号，用于查询产物并断言
        samples = generate_steps[0]['sample']
        if samples:
            query_data = {
                "task": {"zsample": ",".join(samples), "zsfbd": "X"},
                "pageNumber": 1,
                "pageSize": 10000,
                "token": token,
                "menuId": "MSTaskProduct_RepeatController"
            }
            response = res.post_request("/presap/webintf.do?method=get_repeat_controllers", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["code"] == "200" and len(
                response_json["data"]) >= len(samples), f"主流程测试场景4异常：产物补录断言失败，原因：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景5")
    @allure.title("路径：0:提交送检单--1:技术路线确认--2:血浆分离--3:建库--4:BMG--5:Pooling--6:单链环化--7:MakeDNB-8:上机--9:信息分析--10：数据审核--11：报告生成--12：报告确认--13：报告审核--14：报告认领--15：报告复核")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path5', 'last_step': 15, 'run_time': 1, 'user_name': test_user, 'istest':True}],
                             indirect=True)
    def test_from_submit_inspection_to_report_composite(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的样例编号，用于查询报告状态并断言
        samples = generate_steps[0]['sample']
        if samples:
            query_data = {
                "task": {"zsample": ",".join(samples)},
                "pageNumber": 1,
                "zgxbh": "InsSheetCycle",
                "pageSize": 10000,
                "token": token,
                "menuId": "MdInfoQuery_InsSheetCycle"
            }
            response = res.post_request("/presap/webintf.do?method=query_samples_of_cycle", data=urlencode(query_data))
            response_json = response.json()
            if response_json["code"] == "200" and len(response_json["data"]) > 0:
                for i in range(len(response_json["data"])):
                    assert response_json["data"][i][
                               "rt_zjobcode"] == "已完成", f"主流程测试场景5异常：报告复核断言失败，原因：{response_json}"
