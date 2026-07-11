import json

import pytest
import allure
import os

from testcase.omicsone.conftest import pre_field_config
from testcase.omicsone.sequencetask.conftest import search_sequence_task, handle_upload_file
from utils.tools import calculate_file_buffer, replace_none
from testcase.omicsone.sequencetask.sequence_data import DataList


@pytest.mark.usefixtures("res", "res_file")
class TestSequence:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-查询")
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
        response = res.post_request("/api/sequencing/page", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("测序任务-创建任务")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.sequence_data)
    def test_create_task(self, res, handle_sequence_task, data):
        status_code = handle_sequence_task["status_code"]
        json = handle_sequence_task["json"]
        assert status_code == 200
        assert json['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-复用任务")
    @allure.title("复用任务")
    def test_reuse_task(self, res):
        data = {}
        response_result_before = next(search_sequence_task(res, data))
        task_id = response_result_before["task_id"]
        response = res.post_request("/api/sequencing/reuse", json={"seqTaskId": task_id})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        # 后置把复用的任务删掉
        response_result_after = next(search_sequence_task(res, data))
        task_code = response_result_after["task_code"]
        res.post_request(f"/api/sequencing/delete/{task_code}")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-删除任务")
    @allure.title("删除任务")
    @pytest.mark.parametrize("data", DataList.delete_data)
    def test_delete_task(self, res, handle_sequence_task, data):
        task_code = handle_sequence_task["task_code"]
        if task_code:
            response = res.post_request(f"/api/sequencing/delete/{task_code}")
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-查看任务详情")
    @allure.title("查看任务详情")
    def test_query_task_detail(self, res):
        data = {}
        response_result = next(search_sequence_task(res, data))
        task_code = response_result["task_code"]
        response = res.post_request(f"/api/sequencing/page/detail/{task_code}",
                                    json={"pageNum": 1, "pageSize": 9999, "instanceNo": [""]})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-停止任务")
    @allure.title("停止任务")
    @pytest.mark.parametrize("data", DataList.sequence_data[0:1])
    def test_stop_task(self, res, handle_sequence_task, data):
        task_id = handle_sequence_task["task_id"]
        response = res.post_request("/api/sequencing/stop", json={"seqTaskId": task_id})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-启动任务")
    @allure.title("启动任务")
    @pytest.mark.parametrize("data", DataList.sequence_data[1:2])
    def test_start_task(self, res, handle_sequence_task, data):
        task_id = handle_sequence_task["task_id"]
        response = res.post_request("/api/sequencing/start", json={"seqTaskId": task_id})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-编辑任务")
    @allure.title("编辑任务")
    @pytest.mark.parametrize("data", DataList.sequence_data[0:1])
    def test_edit_task(self, res, handle_sequence_task, data):
        task_id = handle_sequence_task["task_id"]
        task_code = handle_sequence_task["task_code"]
        detail_response = res.post_request(f"/api/sequencing/page/detail/{task_code}",
                                           json={"pageNum": 1, "pageSize": 9999, "instanceNo": [""]})
        detail = replace_none(detail_response.json()['result'])
        edit_json = {
            "chips": detail,
            "seqTaskCode": task_code
        }
        # 等待状态无法编辑，要先停止
        res.post_request("/api/sequencing/stop", json={"seqTaskId": task_id})
        response = res.post_request("/api/sequencing/edit", json=edit_json)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-获取待选样本")
    @allure.title("获取待选样本")
    def test_query_sample(self, res):
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 96,
            "pageSize": 96
        }
        response = res.post_request("/api/sequencing/page/querySample", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-获取设备信息")
    @allure.title("获取设备信息")
    def test_query_device(self, res):
        response = res.post_request("/api/base/device/sequence/list", json={})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-核对列表字段配置")
    @allure.title("核对列表字段配置")
    @pytest.mark.parametrize("product", ['CNV-seq', 'NIFTY', 'CS', 'NBS'])
    @pytest.mark.parametrize("data", DataList.field_config)
    def test_check_field_config(self, product, data):
        response_data = next(pre_field_config(product, data["page"]))
        assert response_data[0] == data["field_base_data"]
        assert response_data[1] == data["field_project_data"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-获取配置信息")
    @allure.title("获取配置信息")
    @pytest.mark.parametrize("data", ["SequencingList", "Sequencing"])
    def test_query_search_config(self, res, data):
        response = res.post_request("/api/base/searchconfig/config/list", json={"configModule": data})
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-更新配置信息")
    @allure.title("更新配置信息")
    @pytest.mark.parametrize("data", ["SequencingList", "Sequencing"])
    def test_update_field_config(self, res, data):
        query_data = {"configModule": data}
        query_response = res.post_request("/api/base/searchconfig/config/list", json=query_data)
        update_data = query_response.json()['result']['configInfo']
        query_data.update(json.loads(update_data))
        response = res.post_request("/api/base/searchconfig/config/update", json=query_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-查询产品套餐")
    @allure.title("查询产品套餐")
    def test_query_product(self, res):
        response = res.get_request("/api/base/products/query/CNV-seq,CS,NBS,NIFTY")
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("测序任务-下载模板")
    @allure.title("下载模板-{data}")
    @pytest.mark.parametrize("data", ["SequencingTaskTemplate_SingleMolecule", "SequencingTaskTemplate_HighThroughput"])
    def test_export_template(self, res, data):
        """
        导出所有模板，校验导出非空文件
        :param res:
        :return:
        """
        response = res.get_request(f"/api/base/file/downloadFile?filePathOrBusinessType={data}")
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("测序任务-导入测序任务")
    @allure.title("导入测序任务-{data}")
    @pytest.mark.parametrize("data", ["SingleMolecule", "HighThroughput"])
    def test_upload_task(self, res, res_file, data):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(parent_dir, 'import_files')
        file_path = os.path.join(base_path, 'sequence_import_' + data + '.xlsx')
        pre_upload = handle_upload_file(file_path)
        if pre_upload:
            json_data = {"sequencingTechType": data}
            response = res_file.post_request("/api/sequencing/import", data=json_data, file_path=file_path)
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'
            assert len(response.json()['result']['successfulList']) != 0    # 正常导入成功，返回是非空列表
        # 后置把导入的任务删掉
        response_after_import = next(search_sequence_task(res, {}))
        task_code = response_after_import["task_code"]
        res.post_request(f"/api/sequencing/delete/{task_code}")
