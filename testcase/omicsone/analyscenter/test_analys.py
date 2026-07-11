import json
from datetime import date
from time import sleep

import pytest
import allure

from testcase.omicsone.conftest import pre_field_config
from testcase.omicsone.analyscenter.analys_data import DataList


@pytest.mark.usefixtures("res", "res_file")
class TestAnalys:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("分析中心-查询")
    @allure.title("分析中心-查询：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search_analys(self, res, data):
        """
        分析中心查询，只做了任务编号、样本编号、芯片号字段搜索
        :param res:
        :param data:
        :return:
        """
        tmp = data['search_items']
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100
        }
        json_data.update(tmp)
        response = res.post_request("/api/analysis/taskManager/list", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-核对列表字段配置")
    @allure.title("核对列表字段配置")
    @pytest.mark.parametrize("product", ['CNV-seq', 'NIFTY', 'CS', 'NBS'])
    @pytest.mark.parametrize("data", DataList.field_config)
    def test_check_field_config(self, product, data):
        response_data = next(pre_field_config(product, data["page"]))
        assert response_data[0] == data["field_base_data"]
        assert response_data[1] == data["field_project_data"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-更新配置信息")
    @allure.title("更新配置信息")
    def test_update_field_config(self, res):
        query_data = {"configModule": "AnalysisList"}
        query_response = res.post_request("/api/base/searchconfig/config/list", json=query_data)
        update_data = query_response.json()['result']['configInfo']
        query_data.update(json.loads(update_data))
        response = res.post_request("/api/base/searchconfig/config/update", json=query_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-获取配置信息")
    @allure.title("获取配置信息")
    def test_query_search_config(self, res):
        response = res.post_request("/api/base/searchconfig/config/list", json={"configModule": "AnalysisList"})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("分析中心-查看分析详情")
    @allure.title("查看分析详情")
    def test_query_task_detail(self, res):
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100
        }
        query_response = res.post_request("/api/analysis/taskManager/list", json=json_data)
        task_id = query_response.json()['result']['records'][0]['taskId']
        response = res.post_request("/api/analysis/taskManager/detail", json={"taskId": task_id})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-更新备注")
    @allure.title("更新备注")
    def test_update_remark(self, res):
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100
        }
        query_response = res.post_request("/api/analysis/taskManager/list", json=json_data)
        task_id = query_response.json()['result']['records'][0]['taskId']
        response = res.post_request("/api/analysis/taskManager/updateTaskRemark",
                                    json={"taskId": task_id, "remark": f"自动化测试{date.today()}"})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.MINOR)
    @allure.feature("分析中心-查看分析失败详情")
    @allure.title("查看分析失败详情")
    def test_update_remark(self, res):
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100,
            "taskStatus": ["Failed"]
        }
        query_response = res.post_request("/api/analysis/taskManager/list", json=json_data)
        task_id = query_response.json()['result']['records'][0]['taskId']
        response = res.post_request("/api/analysis/taskManager/findTaskFailLog", json={"taskId": task_id})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @pytest.mark.run(order=1)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("分析中心-加急分析")
    @allure.title("加急分析")
    def test_emerge_analysis(self, res, res_file, pre_analysis):
        # 校验前置任务状态是否正确
        if pre_analysis['task_status'] != 'Running':
            assert False, f"任务状态有误，任务状态：{pre_analysis['task_status']}"

        else:
            response = res.post_request("/api/analysis/taskManager/emergencyAnalysis",
                                        json=[{"taskId": pre_analysis['task_id']}])
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'

    @pytest.mark.run(order=2)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-停止分析")
    @allure.title("停止分析")
    def test_stop_analysis(self, res, res_file, pre_analysis):
        # 校验前置任务状态是否正确
        if pre_analysis['task_status'] != 'Running':
            assert False, f"任务状态有误，任务状态：{pre_analysis['task_status']}"

        else:
            response = res.post_request("/api/analysis/taskManager/stopAnalysis",
                                        json=[{"taskId": pre_analysis['task_id']}])
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'

    @pytest.mark.run(order=3)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-剔除样本")
    @allure.title("剔除样本")
    def test_remove_sample(self, res, res_file, pre_analysis):
        # 校验前置任务状态是否正确，前置任务创建成功再往下校验
        if pre_analysis['task_status'] != 'Running':
            assert False, f"任务状态有误，任务状态：{pre_analysis['task_status']}"
        # 校验当前任务状态是否为分析停止
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100,
            "taskCode": [pre_analysis['task_code']]
        }
        query_response = res.post_request("/api/analysis/taskManager/list", json=json_data)
        new_status = query_response.json()['result']['records'][0]['taskStatus']
        if new_status != 'Stop':
            assert False, f"任务状态有误，任务状态：{new_status}"

        else:
            detail = res.post_request("/api/analysis/taskManager/detail", json={"taskId": pre_analysis['task_id']})
            detail_id = detail.json()['result'][0]['taskDetailId']
            response = res.post_request("/api/analysis/taskManager/remove",
                                        json={"taskId": pre_analysis['task_id'], "taskDetailIdList": [detail_id]})
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'

    @pytest.mark.run(order=4)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("分析中心-重分析")
    @allure.title("重分析")
    def test_restart_analysis(self, res, res_file, pre_analysis):
        # 校验前置任务状态是否正确，前置任务创建成功再往下校验
        if pre_analysis['task_status'] != 'Running':
            assert False, f"任务状态有误，任务状态：{pre_analysis['task_status']}"
        # 校验当前任务状态是否为分析停止
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100,
            "taskCode": [pre_analysis['task_code']]
        }
        query_response = res.post_request("/api/analysis/taskManager/list", json=json_data)
        new_status = query_response.json()['result']['records'][0]['taskStatus']
        if new_status != 'Stop':
            assert False, f"任务状态有误，任务状态：{new_status}"

        json_data = [{
            "taskId": pre_analysis['task_id'],
            "stepName":"fq",
            "belongStep":"从FQ重分析",
            "sortIndex":-1
        }]
        response = res.post_request("/api/analysis/taskManager/reanalysis", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @pytest.mark.run(order=5)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-终止分析")
    @allure.title("终止分析")
    def test_terminate_analysis(self, res, res_file, pre_analysis):
        # 校验前置任务状态是否正确，前置任务创建成功再往下校验
        if pre_analysis['task_status'] != 'Running':
            assert False, f"任务状态有误，任务状态：{pre_analysis['task_status']}"
        # 校验当前任务状态是否为分析中（前一个case已经重分析了）
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100,
            "taskCode": [pre_analysis['task_code']]
        }
        for i in range(12):
            query_response = res.post_request("/api/analysis/taskManager/list", json=json_data)
            new_status = query_response.json()['result']['records'][0]['taskStatus']
            if new_status == 'Pending':
                sleep(5)
            elif new_status == 'Running':
                break
            else:
                assert False, f"任务状态有误，任务状态：{new_status}"

        res.post_request("/api/analysis/taskManager/stopAnalysis", json=[{"taskId": pre_analysis['task_id']}])
        response = res.post_request("/api/analysis/taskManager/terminatedAnalysis",
                                    json=[{"taskId": pre_analysis['task_id']}])
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
