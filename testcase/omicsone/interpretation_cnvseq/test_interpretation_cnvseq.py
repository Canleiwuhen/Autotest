from time import sleep

import pytest
import allure
from testcase.omicsone.interpretation_cnvseq.interpretation_cnvseq_data import DataList
from utils.tools import calculate_file_buffer


@pytest.mark.usefixtures("res")
class TestInterpretationCnvseq:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-康孕-查询")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search(self, res, data):
        tmp = data['search_items']
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 200,
            "pageSize": 200
        }
        json_data.update(tmp)
        response = res.post_request("/api/interpretation/cnv-seq/task/list", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-康孕-修改医生意见")
    @allure.title("修改医生意见为{data}")
    @pytest.mark.parametrize("data", ["ReSequence", "ReBuild", "Refund", "NoNeed", "Pass"])
    def test_edit_opinion(self, res, handle_task, data):
        json_data = {
            "taskIds": [handle_task["task_id"]],
            "doctorOpinion": data,
            "remark": "自动化测试"
        }
        response = res.post_request("/api/interpretation/cnv-seq/task/opinion", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-康孕-任务转发")
    @allure.title("任务转发")
    @pytest.mark.parametrize("data", [{"黄雁": "427868391118864384"}])
    def test_task_forward(self, res, handle_task, data):
        json_data = {
            "taskIds": [handle_task["task_id"]],
            "forwardUserId": list(data.values())[0],
            "forwardUserName": list(data.keys())[0]
        }
        response = res.post_request("/api/interpretation/cnv-seq/task/forward", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-康孕-提交云服务")
    @allure.title("提交云服务")
    def test_submit_cloud_service(self, res, handle_task):
        json_data = [{"remark": "自动化测试", "taskId": handle_task["task_id"]}]
        response = res.post_request("/api/interpretation/cnv-seq/task/interpretationCloud", json=json_data)
        service_status = "Uploading"
        while service_status == "Uploading":
            sleep(3)
            query = res.post_request("/api/interpretation/cnv-seq/task/list", json={
                "page": 1,
                "pageNum": 1,
                "limit": 200,
                "pageSize": 200,
                "instanceNo": handle_task["instance_no"]
            })
            service_status = query.json()['result']['records'][0]['manualServiceStatus']
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        assert service_status == "InService"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-康孕-导出解读结果")
    @allure.title("导出解读结果-{data}个样本")
    @pytest.mark.parametrize("data", [1, 2])
    def test_export_result(self, res, data):
        query = res.post_request("/api/interpretation/cnv-seq/task/list", json={
            "page": 1,
            "pageNum": 1,
            "limit": 200,
            "pageSize": 200,
        })
        records = query.json()['result']['records']
        task_ids = [record['taskId'] for record in records[:2]]
        response = res.post_request("/api/interpretation/cnv-seq/task/export", json={"taskIds": task_ids[0: data]})
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件
