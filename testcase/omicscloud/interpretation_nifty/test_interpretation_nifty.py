import pytest
import allure

from testcase.omicscloud.interpretation_nifty.interpretation_nifty_data import InterpretationData
from utils.tools import calculate_file_buffer


@allure.feature("解读中心-nifty")
class TestInterpretationNifty:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", InterpretationData.search_data)
    def test_search(self, res_cloud, data):
        search_item = data["search_item"]
        search_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 200,
            "pageSize": 200
        }
        search_data.update(search_item)
        response = res_cloud.post_request(url="/api/interpretation/nifty/batch/list", json=search_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("重复样-全部展开/全部收起")
    @allure.title("重复样-全部展开/全部收起")
    @pytest.mark.parametrize("handle_task", ["query"], indirect=True)
    def test_repeat(self, res_cloud, handle_task):
        task_id = dict(handle_task)['task_id']
        json_data = {"taskIds": [task_id]}
        response = res_cloud.post_request(url="/api/interpretation/nifty/task/repeat", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("更多-任务转发")
    @allure.title("更多-任务转发")
    @pytest.mark.parametrize("handle_task", ["forward"], indirect=True)
    def test_task_retweet(self, res_cloud, handle_task):
        task_id = dict(handle_task)['task_id']
        retweet_data = {
            "forwardUserId": "476430062711865344",
            "forwardUserName": "黄雁-专家云",
            "taskIds": [task_id]
        }
        response = res_cloud.post_request(url="/api/interpretation/nifty/task/forward", json=retweet_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
    #
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.story("更多-重解析")
    # @allure.title("更多-重解析")
    # @pytest.mark.parametrize("handle_task", ["reparse"], indirect=True)
    # def test_reparsing(self, res_cloud, handle_task):
    #     task_id = dict(handle_task)['task_id']
    #     json_data = {"taskIds": [task_id]}
    #     response = res_cloud.post_request("/api/interpretation/nifty/task/reparse", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"

    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.story("更多-解读终止")
    # @allure.title("更多-解读终止")
    # @pytest.mark.parametrize("handle_task", ["terminate"], indirect=True)
    # def test_terminate_task(self, res_cloud, handle_task):
    #     task_id = dict(handle_task)['task_id']
    #     json_data = {"taskIds": [task_id]}
    #     response = res_cloud.post_request("/api/interpretation/nifty/task/terminate", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("导出-解读结果")
    @allure.title("导出-解读结果")
    @pytest.mark.parametrize("handle_task", ["query"], indirect=True)
    def test_export_result(self, res_cloud, handle_task):
        task_id = dict(handle_task)['task_id']
        export_data = {"taskIds": [task_id], "taggingTasks": []}
        response = res_cloud.post_request("/api/interpretation/nifty/task/export", json=export_data)
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("导出-过滤前CNV")
    @allure.title("导出-过滤前CNV")
    @pytest.mark.parametrize("handle_task", ["query"], indirect=True)
    def test_export_cnv(self, res_cloud, handle_task):
        task_id = dict(handle_task)['task_id']
        export_data = {"taskIds": [task_id]}
        response = res_cloud.post_request("/api/interpretation/nifty/task/exportCnv", json=export_data)
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("导出-染色体图")
    @allure.title("导出-染色体图")
    @pytest.mark.parametrize("handle_task", ["query"], indirect=True)
    def test_export_img(self, res_cloud, handle_task):
        task_id = dict(handle_task)['task_id']
        export_data = {"taskIds": [task_id]}
        response = res_cloud.post_request("/api/interpretation/nifty/task/exportChrImg", json=export_data)
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.story("完成服务")
    # @allure.title("完成服务")
    # @pytest.mark.parametrize("handle_task", ["finish"], indirect=True)
    # def test_finish_task(self, res_cloud, handle_task):
    #     task_id = dict(handle_task)['task_id']
    #     json_data = {"taskIds": [task_id]}
    #     response = res_cloud.post_request("/api/interpretation/nifty/task/interpretationCloud/finish", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("重置解读结果")
    @allure.title("重置解读结果")
    @pytest.mark.parametrize("handle_task", ["reset"], indirect=True)
    def test_reset_task(self, res_cloud, handle_task):
        task_id = dict(handle_task)['task_id']
        json_data = {"taskIdList": [task_id]}
        response = res_cloud.post_request("/api/interpretation/nifty/task/reanalysis/resetChr", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查看重分析状态弹窗")
    @allure.title("查看重分析状态弹窗")
    def test_remove_status(self, res_cloud):
        json_data = {"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        response = res_cloud.post_request("/api/interpretation/nifty/removecnv/page", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-注释状态查询")
    @allure.title("解读详情-注释状态查询")
    def test_query_anno_task(self, res_cloud, mysql_connect):
        task_ids = mysql_connect.select(
            "select task_id from interpretation_task where project_code = 'NIFTY' and status in "
            "('ReadyForInterpret','Interpreting') and task_id in (select task_id from interpretation_anno_single_task)")
        task_id = task_ids[0]['task_id']
        response = res_cloud.get_request(f"/api/interpretation/nifty/anno/annotation?taskId={task_id}")
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"] is not None

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-更新cnv检出内容")
    @allure.title("解读详情-更新cnv检出内容")
    def test_update_cnv(self, res_cloud, mysql_connect):
        task_ids = mysql_connect.select("select ilc.task_id, ilc.large_cnv_id from interpretation_task it "
                                        "inner join interpretation_large_cnv ilc on it.task_id = ilc.task_id "
                                        "where it.product_no is not null and ilc.sv_type ='CNV' and "
                                        "it.project_code = 'NIFTY' and it.status in ('ReadyForInterpret','Interpreting')")
        json_data = {
            "taskId": task_ids[0]['task_id'],
            "largeCnvId": task_ids[0]['large_cnv_id'],
            "reportFlag": "No"
        }
        response = res_cloud.post_request("/api/interpretation/nifty/largecnv/updateNiftyCnv", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"] == "编辑成功"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-更新chr结果")
    @allure.title("解读详情-更新chr{data[0]}结果为{data[1]}")
    @pytest.mark.parametrize("handle_task", ["query"], indirect=True)
    @pytest.mark.parametrize("data", [("1", "HS"), ("1", "HT"), ("1", "S"), ("1", "T"), ("1", "Negative"),
                                      ("X", "XML"), ("X", "Negative"), ("X", "NXY1"), ("X", "NXY3"),
                                      ("X", "XYY3"), ("X", "XO1")])
    def test_update_chr(self, res_cloud, data, handle_task):
        task_id = dict(handle_task)['task_id']
        chr_result = res_cloud.get_request(f"/api/interpretation/nifty/chr/list?taskId={task_id}")
        if data[0] == "X":
            chr = 23
        elif data[0] == "Y":
            chr = 24
        else:
            chr = int(data[0])
        chr_id = chr_result.json()['result'][chr-1]['chrId']
        json_data = {
            "result": data[1],
            "chr": data[0],
            "taskId": task_id,
            "chrId": chr_id
        }
        response = res_cloud.post_request("/api/interpretation/nifty/chr/update", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"] == "编辑成功"
