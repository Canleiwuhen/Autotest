import json

import pytest
import allure
import os

from testcase.omicsone.conftest import pre_field_config
from utils.tools import calculate_file_buffer
from testcase.omicsone.experimentaltask.experiment_data import DataList
from testcase.omicsone.experimentaltask.conftest import handle_upload_file


@pytest.mark.usefixtures("res", "res_file")
class TestExperiment:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-查询")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search(self, res, data):
        tmp = data['search_items']
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100
        }
        json_data.update(tmp)
        response = res.post_request("/api/experiment/queryTaskList", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("自动化实验任务-创建实验任务")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.experiment_data)
    def test_create_task(self, res, handle_experiment_task, data):
        status_code = handle_experiment_task["status_code"]
        json = handle_experiment_task["json"]
        assert status_code == 200
        assert json['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-关闭实验任务")
    @allure.title("关闭实验任务")
    @pytest.mark.parametrize("data", DataList.close_data)
    def test_close_task(self, res, handle_experiment_task, data):
        task_id = handle_experiment_task["task_id"]
        response = res.post_request("/api/experiment/close", json={"taskId": task_id})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-删除实验任务")
    @allure.title("删除实验任务")
    @pytest.mark.parametrize("data", DataList.init_data)
    def test_delete_task(self, res, handle_experiment_task, data):
        task_id = handle_experiment_task["task_id"]
        close_response = res.post_request("/api/experiment/close", json={"taskId": task_id})
        if close_response.status_code == 200:
            response = res.post_request("/api/experiment/delete", json={"taskId": task_id})
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-重投递实验任务")
    @allure.title("重投递实验任务")
    @pytest.mark.parametrize("data", DataList.experiment_data[0:1])
    def test_redelivery_task(self, res, handle_experiment_task, data):
        task_id = handle_experiment_task["task_id"]
        close_response = res.post_request("/api/experiment/close", json={"taskId": task_id})
        if close_response.status_code == 200:
            response = res.post_request("/api/experiment/redelivery", json={"taskId": task_id})
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("自动化实验任务-查看实验详情")
    @allure.title("查看实验详情")
    @pytest.mark.parametrize("data", DataList.experiment_data[0:1])
    def test_query_task_detail(self, res, handle_experiment_task, data):
        task_id = handle_experiment_task["task_id"]
        response = res.post_request("/api/experiment/queryTaskDetailList", json={"taskId": task_id})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("自动化实验任务-导出实验任务")
    @allure.title("导出实验任务")
    @pytest.mark.parametrize("data", DataList.experiment_data[0:1])
    def test_export_task(self, res, handle_experiment_task, data):
        task_id = handle_experiment_task["task_id"]
        response = res.post_request("/api/experiment/exportTask", json={"taskIdList": [task_id]})
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("自动化实验任务-编辑实验任务")
    @allure.title("编辑实验任务")
    @pytest.mark.parametrize("data", DataList.close_data)
    def test_edit_task(self, res, handle_experiment_task, data):
        task_id = handle_experiment_task["task_id"]
        task_code = handle_experiment_task["task_code"]
        close_response = res.post_request("/api/experiment/close", json={"taskId": task_id})
        if close_response.status_code == 200:
            tmp = data['task_items']
            json_data = {
                "taskId": task_id,
                "taskCode": task_code,
                "experimentalState": "Close"
            }
            json_data.update(tmp)
            response = res.post_request("/api/experiment/edit", json=json_data)
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("自动化实验任务-下载模板")
    @allure.title("下载模板")
    @pytest.mark.parametrize("data", ["Libraryprep", "Hybridization"])
    def test_export_template(self, res, data):
        """
        导出所有模板，校验导出非空文件
        :param res:
        :return:
        """
        response = res.post_request("/api/experiment/download", json={"type": data})
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-获取待选样本")
    @allure.title("获取待选样本")
    @pytest.mark.parametrize("data", ["Sample", "Experiment", "Interp"])
    def test_query_sample(self, res, data):
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 96,
            "pageSize": 96,
            "status": data,
            "autoProjectCode": "CS,NBS,CNV-seq,NIFTY"
        }
        response = res.post_request(f'/api/experiment/querySampleList/{data}', json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-获取技术路线")
    @allure.title("获取技术路线")
    def test_query_route(self, res):
        json_data = {
            "instrumentId": "SIRO16_202409110001"
        }
        response = res.post_request('/api/experiment/getRouteList', json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-获取质控品/标准品")
    @allure.title("获取质控品/标准品")
    @pytest.mark.parametrize("data", ["Qc", "Standard"])
    def test_query_qc(self, res, data):
        json_data = {
            "projectCodeList": ["CS", "CNV-seq"],
            "inspectionType": data
        }
        response = res.post_request("/api/experiment/getQcSampleList", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-获取待选板号")
    @allure.title("获取待选板号")
    @pytest.mark.parametrize("data", ["SequencingPrep", "Hybridization"])
    def test_query_plate(self, res, data):
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100,
            "autoProjectCode": "NBS",
            "experimentalProcedure": data
        }
        response = res.post_request("/api/experiment/queryPlateList", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-添加手工板")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.upload_plate_config)
    def test_upload_plate(self, res_file, data):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(parent_dir, 'import_files')
        file_path = os.path.join(base_path, data["plate_type"])
        pre_upload = handle_upload_file(data["product"], file_path)
        if pre_upload:
            json_data = {
                "experimentalProcedure": data["procedure"],
                "instrumentType": "SIRO-48"
            }
            response = res_file.post_request(f"/api/experiment/plate/import/{data['product']}",
                                             data=json_data, file_path=file_path)
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'
            assert len(response.json()['result']['sampleList']) != 0    # 正常导入成功，返回是非空列表

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-查询自动化设备")
    @allure.title("查询自动化设备")
    def test_query_instrument(self, res):
        json_data = {"pageNum": 1, "pageSize": 100}
        response = res.post_request("/api/base/device/ipipette/instrument/page", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-查询检测项目")
    @allure.title("查询检测项目")
    def test_query_project(self, res):
        json_data = {"pageNum": 1, "pageSize": 100}
        response = res.post_request("/api/base/projects/page", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-产品套餐筛选项下拉")
    @allure.title("产品套餐筛选项下拉")
    def test_query_product(self, res):
        response = res.get_request("/api/sample/category/list/productNo")
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-样本类型筛选项下拉")
    @allure.title("样本类型筛选项下拉")
    def test_query_sample_type(self, res):
        response = res.get_request("/api/sample/category/list/sampleTypeCode")
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-获取实验流程")
    @allure.title("获取实验流程")
    def test_query_experiment_flow(self, res):
        response = res.get_request("/api/base/configItem/itemType/NIFTY/experimentFlow")
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-核对列表字段配置")
    @allure.title("核对列表字段配置")
    @pytest.mark.parametrize("product", ['CNV-seq', 'NIFTY', 'CS', 'NBS'])
    @pytest.mark.parametrize("data", DataList.field_config)
    def test_check_field_config(self, product, data):
        response_data = next(pre_field_config(product, data["page"]))
        assert response_data[0] == data["field_base_data"]
        assert response_data[1] == data["field_project_data"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-更新配置信息")
    @allure.title("更新配置信息")
    @pytest.mark.parametrize("data", ["ExperimentList", "Experiment"])
    def test_update_field_config(self, res, data):
        query_data = {"configModule": data}
        query_response = res.post_request("/api/base/searchconfig/config/list", json=query_data)
        update_data = query_response.json()['result']['configInfo']
        query_data.update(json.loads(update_data))
        response = res.post_request("/api/base/searchconfig/config/update", json=query_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-获取配置信息")
    @allure.title("获取配置信息")
    @pytest.mark.parametrize("data", ["ExperimentList", "Experiment"])
    def test_query_search_config(self, res, data):
        response = res.post_request("/api/base/searchconfig/config/list", json={"configModule": data})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
