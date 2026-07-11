import pytest
import allure

from testcase.omicscloud.interpretation_CS.interpretation_CS_data import InterpretationData
from utils.tools import calculate_file_buffer, replace_none
from utils.logger import logger_t as logger
from time import sleep


@allure.feature("解读中心-携带者")
class TestInterpretationCS:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", InterpretationData.search_data)
    def test_search(self, res, data):
        search_item = data["search_item"]
        search_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 200,
            "pageSize": 200
        }
        search_data.update(search_item)
        response = res.post_request(url="/api/interpretation/cs/task/list", json=search_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查看-qc")
    @allure.title("查看-qc")
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 1)], indirect=True)
    def test_qc_info(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/task/carrier/qc/infos", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查看-其他CNV")
    @allure.title("查看-其他CNV")
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 3)], indirect=True)
    def test_cnv_info(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"page": 1, "pageNum": 1, "limit": 50, "pageSize": 50, "showDiseaseList": "Y",
                     "taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/variant/otherCnv/list", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("批量解读")
    @allure.title("批量解读")
    @pytest.mark.parametrize("handle_task", [("interpret", "operate", 2)], indirect=True)
    def test_batch_interpret(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/task/batch/interpret", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("批量审核")
    @allure.title("批量审核")
    @pytest.mark.parametrize("handle_task", [("review", "operate", 2)], indirect=True)
    def test_batch_review(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/task/batch/review", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("任务统筹-加急")
    @allure.title("任务统筹-加急")
    @pytest.mark.parametrize("handle_task", [("interpret", "urgent", 1)], indirect=True)
    def test_urgent(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"taskIds": task_ids}
        response = res.post_request("/api/interpretation/cs/task/taskUrgent", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("任务统筹-批量备注")
    @allure.title("任务统筹-批量备注")
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 2)], indirect=True)
    def test_batch_remark(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        remark_data = {"remark": "自动化测试批量备注内容。", "taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/task/batch/remark", json=remark_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("任务统筹-自动分配")
    @allure.title("任务统筹-自动分配")
    def test_auto_assign(self, res):
        submit_data = {"sampleNo": "25X1015", "status": ["ReadyForInterpret"]}  # 入参先写死
        response = res.post_request(url="/api/interpretation/cs/task/assign/tasks/auto", json=submit_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("任务统筹-手动分配")
    @allure.title("任务统筹-{handle_task[1]}样本手动分配")
    @pytest.mark.parametrize("handle_task",
                             [("allocate-positive", "allocate", 1), ("allocate-negative", "allocate", 2)],
                             indirect=True)
    def test_task_allocate(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        # 查询当前项目可分配的用户
        response = res.get_request(url="/api/interpretation/core/info/users", params={"projectCode": "CS"})
        # 获取自动化用户的user_id
        interpreter = [i for i in response.json()["result"] if i["userRealName"] == "自动化测试_中心交付"][0]
        reviewer = [i for i in response.json()["result"] if i["userRealName"] == "自动化测试_中心交付1"][0]
        # 阴/阳性样本的入参不一样
        negative_allocate_data = {
            "projectCode": "CS",
            "taskAssignQo": {
                "negativeTaskQo": {
                    "reviewer": str(interpreter["userId"]),
                    "reviewerName": interpreter["userRealName"],
                    "taskIds": task_ids
                },
                "positiveTaskQo": {
                    "interpreter": "",
                    "reviewer": "",
                    "taskIds": []
                }
            }
        }
        positive_allocate_data = {
            "projectCode": "CS",
            "taskAssignQo": {
                "negativeTaskQo": {
                    "reviewer": "",
                    "taskIds": []
                },
                "positiveTaskQo": {
                    "interpreter": str(interpreter["userId"]),
                    "reviewer": str(reviewer["userId"]),
                    "interpreterName": interpreter["userRealName"],
                    "reviewerName": reviewer["userRealName"],
                    "taskIds": task_ids
                }
            }
        }
        response = res.post_request(url="/api/interpretation/cs/task/assign/tasks",
                                    json=positive_allocate_data if dict(handle_task[0])["sample_data_tag"] == "Positive"
                                    else negative_allocate_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("导出-解读结果")
    @allure.title("导出-解读结果")
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 3)], indirect=True)
    def test_export_result(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        export_data = {"taskIds": task_ids}
        response = res.post_request("/api/interpretation/cs/task/export", json=export_data)
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("导出-原始结果")
    @allure.title("导出-原始结果")
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 3)], indirect=True)
    def test_export_original_result(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        export_data = {"taskIds": task_ids}
        response = res.post_request("/api/interpretation/cs/task/original/export", json=export_data)
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("其他异常处理")
    @allure.title("其他异常处理-{data[case_name]}")
    @pytest.mark.parametrize("handle_task", [("interpret", "operate", 2)], indirect=True)
    @pytest.mark.parametrize("data", InterpretationData.other_exception_data)
    def test_handle_exception(self, res, data, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {
            "taskIds": task_ids,
            "projectCode": "CS",
            "mailInfo": {
                "attachment": [],
                "content": "各位好！ \r\n此乃自动化测试邮件\r\n \r\n此邮件由系统自动发送，请勿单独回复！！",
                "copyer": "huangyan10@bgi.com",
                "mailType": "Interpretation" + data["reason_items"]["exceptionType"],
                "receiver": "huangyan10@bgi.com",
                "sender": "huangyan10@bgi.com",
                "title": "解读中心其他异常处理-autotest"
            }
        }
        json_data.update(data["reason_items"])
        response = res.post_request("/api/interpretation/cs/task/handle/otherException", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("其他异常处理-获取样本信息")
    @allure.title("其他异常处理-获取样本信息")
    @pytest.mark.parametrize("handle_task", [("interpret", "operate", 1)], indirect=True)
    def test_get_sample_info(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"taskIdList": task_ids}
        response = res.post_request("/api/interpretation/cs/task/resetSample", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("其他异常处理-取消异常")
    @allure.title("其他异常处理-取消异常")
    @pytest.mark.parametrize("handle_task", [("interpret", "operate", 2)], indirect=True)
    def test_delete_tags(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"taskIds": task_ids,
                     "tagNames": ["ExperimentAbnormal", "AnalysisAbnormal", "SampleAbnormal", "Delay"]}
        response = res.post_request("/api/interpretation/core/task/tag/delete", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("更多-重解析")
    @allure.title("更多-重解析")
    @pytest.mark.parametrize("handle_task", [("allocate", "reparse", 1)], indirect=True)
    def test_reparsing(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        json_data = {"taskIds": task_ids}
        response = res.post_request("/api/interpretation/cs/task/reparse", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.story("更多-报告重新推送")
    # @allure.title("更多-报告重新推送")
    # @pytest.mark.parametrize("handle_task", [("finish", "recomplete", 1)], indirect=True)
    # def test_recomplete_report(self, res, handle_task):
    #     json_data = [item["task_id"] for item in handle_task if len(handle_task) > 0]
    #     response = res.post_request("/api/interpretation/cs/task/reComplete/report", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"
    #
    # @allure.severity(allure.severity_level.NORMAL)
    # @allure.story("更多-解读终止")
    # @allure.title("更多-解读终止")
    # @pytest.mark.parametrize("handle_task", [("interpret", "terminate", 1)], indirect=True)
    # def test_terminate_task(self, res, handle_task):
    #     task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
    #     json_data = {
    #         "taskIds": task_ids,
    #         "projectCode": "CS",
    #         "mailInfo": {
    #             "attachment": [],
    #             "content": "各位好！\r\ntesttest此邮件由系统自动发送，请勿单独回复！",
    #             "copyer": "huangyan10@bgi.com",
    #             "mailType": "InterpretationTerminate",
    #             "receiver": "huangyan10@bgi.com",
    #             "sender": "huangyan10@bgi.com",
    #             "title": "【解读终止】test"
    #         }
    #     }
    #     response = res.post_request("/api/interpretation/cs/task/terminate", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"
    #
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.story("专家云-完成服务")
    # @allure.title("专家云-完成服务")
    # def test_finish_task(self, res_cloud, mysql_connect):
    #     query_data = {
    #         "status": ["ReadyForReview", "Reviewing"],
    #         "page": 1, "pageNum": 1, "limit": 200, "pageSize": 200
    #     }
    #     query = res_cloud.post_request("/api/interpretation/cs/task/list", json=query_data)
    #     task_id = query.json()['result']['records'][0]['taskId']
    #     # 将任务的解读人设置为自动化测试-专家云账号
    #     mysql_connect.execute(f"update interpretation_task set reviewer = 567289559516319744,"
    #                           f"reviewer_name = '自动化测试-专家云' where task_id = '{task_id}'")
    #     json_data = {"taskIds": [task_id]}
    #     response = res_cloud.post_request("/api/interpretation/cs/task/interpretationCloud/finish", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("报告预览")
    @allure.title("报告预览")
    @pytest.mark.parametrize("handle_task", [("review", "operate", 1)], indirect=True)  # 查询当前用户待审核、审核中的任务
    def test_report_preview(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        task_data = {"taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/task/validate/task", json=task_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        # 调用查询报告内容接口
        response = res.post_request(url="/api/interpretation/cs/task/view/report/info", json=task_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        # 报告预览，重复调用查询状态，直到返回报告状态为成功
        for i in range(15):
            logger.info(f"第{i + 1}次请求报告预览接口！")
            report_data = {"reportResultVos": response.json()["result"]}
            response = res.post_request(url="/api/interpretation/cs/task/view/report", json=report_data)
            assert response.json()["retCode"] == 0
            assert response.json()["retInfo"] == "success"
            if response.json()["result"][0]["whaleFallReportStatus"] == "Generated":
                logger.info(f"第{i + 1}次请求报告预览接口！报告生成成功！")
                break
            if i == 14 and response.json()["result"][0]["whaleFallReportStatus"] != "Generated":
                pytest.fail("请求报告预览接口15次，未生成报告成功，请检查！")
            sleep(0.5)

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("提交审核")
    @allure.title("提交审核")
    @pytest.mark.parametrize("handle_task", [("interpret", "submit_review", 1)], indirect=True)  # 查询当前用户待解读、解读中的任务
    def test_submit_review(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        submit_data = {"taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/task/review/submit", json=submit_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("任务转发")
    @allure.title("任务转发：{handle_task[0]}任务转发")
    @pytest.mark.parametrize("handle_task",
                             [("interpret", "operate", 1), ("review", "operate", 2)], indirect=True)
    def test_task_retweet(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        # 查询当前项目可分配的用户
        response = res.get_request(url="/api/interpretation/core/info/users", params={"projectCode": "CS"})
        # 获取转发用户的user_id
        retweet_user = [i for i in response.json()["result"] if i["userRealName"] == "徐枫4"][0]
        # 解读、审核任务的入参一样
        retweet_data = {
            "forwardUserId": str(retweet_user["userId"]),
            "forwardUserName": retweet_user["userRealName"],
            "taskIds": task_ids
        }
        response = res.post_request(url="/api/interpretation/cs/task/forward", json=retweet_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("配对分析")
    @allure.title("配对分析")
    @pytest.mark.parametrize("handle_task", [("interpret", "couple_merge", 1)], indirect=True)
    def test_couple_merge(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        submit_data = {"taskIds": task_ids}
        response = res.post_request(url="/api/interpretation/cs/task/carrier/merge/couple", json=submit_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-退回解读")
    @allure.title("解读详情-退回解读")
    @pytest.mark.parametrize("handle_task",
                             [("fallback-positive", "fallback", 2), ("fallback-negative", "fallback", 1)],
                             indirect=True)  # 查询当前用户待审核、审核中的任务
    def test_return_interpretation(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        # 查询当前项目可分配的用户
        response = res.get_request(url="/api/interpretation/core/info/users", params={"projectCode": "CS"})
        # 获取自动化用户的user_id
        interpreter = [i for i in response.json()["result"] if i["userRealName"] == "自动化测试_中心交付1"][0]
        return_data = {"taskIds": task_ids}
        # 阴性样本没有解读人，退回解读时需要选择解读人
        interpretation_data = {
            "interpreter": str(interpreter["userId"]),
            "interpreterName": interpreter["userRealName"]
        }
        if dict(handle_task[0])["sample_data_tag"] == "Negative":
            return_data.update(interpretation_data)
        response = res.post_request("/api/interpretation/cs/task/review/fallback", json=return_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-注释状态查询")
    @allure.title("解读详情-注释状态查询")
    @pytest.mark.parametrize("data", [("CarrierOtherCnv", "otherCnvTaskList"), ("CarrierCpra", "mergeSnvTaskList"),
                                      ("CarrierExonGraph", "depthImageTaskList"), ("CarrierVcf", "repeatAnnoTaskList"),
                                      ("CarrierCnv", "exonCnvTaskList"), ("CarrierSnv", "addSnvTaskList"),
                                      ("CarrierReadsGraph", "readsGraphTaskList")])
    def test_query_anno_task(self, res, data, mysql_connect):
        task_ids = mysql_connect.select(
            f"select task_id from interpretation_task where project_code = 'CS' and task_id in "
            f"(select task_id from interpretation_anno_single_task where variant_type = '{data[0]}')")
        task_id = task_ids[0]['task_id']
        response = res.post_request("/api/interpretation/cs/task/carrier/anno/tasks", json={"taskIds": [task_id]})
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"][data[1]] is not None

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-批量看图")
    @allure.title("解读详情-批量看图-{data}")
    @pytest.mark.parametrize("data", ["query", "update"])
    def test_view_thalassemia(self, res, data, mysql_connect):
        task_ids = mysql_connect.select(f"select task_id from interpretation_task_item iti where iti.project_code='CS'"
                                        f" and iti.task_item_info ->> '$.thalassemiaPlotId' is not null")
        task_id = task_ids[0]['task_id']
        response = res.post_request(f"/api/interpretation/cs/exoncnvandsnv/batch/view/thalassemia",
                                    json={"taskIds": [task_id]})
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"] is not None
        if data == "update":
            update_data = response.json()["result"][0]
            update_res = res.post_request("/api/interpretation/cs/exoncnvandsnv/batch/view/abnormal", json=update_data)
            assert update_res.json()["retCode"] == 0
            assert update_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-提交验证")
    @allure.title("解读详情-提交验证-{pre_validate_task}")
    @pytest.mark.parametrize("pre_validate_task", ["ExonCnvOther", "ExonCnv", "SNV"], indirect=True)
    def test_commit_validate(self, res, pre_validate_task):
        response = res.post_request("/api/interpretation/cs/task/carrier/verify/submission", json=[pre_validate_task])
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-批量报出/批量不报出")
    @allure.title("解读详情-批量报出/批量不报出-{data}")
    @pytest.mark.parametrize("data", ["Y", "N"])
    def test_report_flag(self, res, data, mysql_connect):
        variant_ids = mysql_connect.select(f"select iv.variant_id from interpretation_task it inner join "
                                           f"interpretation_variant iv on it.task_id = iv.task_id where "
                                           f"it.project_code ='CS'")
        variant_id = variant_ids[0]['variant_id']
        json_data = {"reportFlag": data, "variantIds": [variant_id]}
        response = res.post_request("/api/interpretation/cs/exoncnvandsnv/batch/reportFlag", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-ExonCNV/SNV查询")
    @allure.title("ExonCNV/SNV查询：{data[case_name]}")
    @pytest.mark.parametrize("data", InterpretationData.detail_search_data)
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 1)], indirect=True)
    def test_search_exon_cnv(self, res, data, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        search_item = data["search_item"]
        search_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 50,
            "pageSize": 50,
            "taskIds": task_ids
        }
        search_data.update(search_item)
        response = res.post_request(url="/api/interpretation/cs/exoncnvandsnv/list", json=search_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-更新报出信息")
    @allure.title("更新报出信息-其他CNV")
    @pytest.mark.parametrize("data", ["Update/reportFlag", "Update/interpretResultDesc", "update"])
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_update_other_cnv(self, res, data, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        search_data = {"page": 1, "pageNum": 1, "limit": 50, "pageSize": 50, "taskIds": task_ids}
        response = res.post_request("/api/interpretation/cs/variant/otherCnv/list", json=search_data)
        update_data = response.json()["result"]["records"][0]
        update_res = res.post_request(f"/api/interpretation/cs/variant/otherCnv/{data}", json=update_data)
        assert update_res.json()["retCode"] == 0
        assert update_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-更新报出信息")
    @allure.title("更新报出信息-ExonCNV/SNV")
    @pytest.mark.parametrize("handle_task", [("interpret", "query", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_update_exon_cnv(self, res, handle_task):
        task_ids = [item["task_id"] for item in handle_task if len(handle_task) > 0]
        search_data = {"page": 1, "pageNum": 1, "limit": 50, "pageSize": 50, "taskIds": task_ids}
        response = res.post_request("/api/interpretation/cs/exoncnvandsnv/list", json=search_data)
        update_data = response.json()["result"]["records"][0]
        update_res = res.post_request("/api/interpretation/cs/exoncnvandsnv/update", json=update_data)
        assert update_res.json()["retCode"] == 0
        assert update_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("ExonCNV/SNV详情查看")
    @allure.title("ExonCNV/SNV详情查看-基本信息")
    @pytest.mark.parametrize("handle_task", [("interpret", "variant_detail", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_view_detail(self, res, handle_task):
        variant_id = dict(handle_task[0])["variant_id"]
        detail_res = res.get_request(url=f"/api/interpretation/cs/exoncnvandsnv/{variant_id}/detail")
        assert detail_res.json()["retCode"] == 0
        assert detail_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("ExonCNV/SNV详情查看")
    @allure.title("ExonCNV/SNV详情查看-证据项-{data}")
    @pytest.mark.parametrize("data", ["Original", "Interpret"])
    @pytest.mark.parametrize("handle_task", [("interpret", "variant_detail", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_view_evidence(self, res, data, handle_task):
        variant_id = dict(handle_task[0])["variant_id"]
        json_data = {"variantId": variant_id, "purpose": data}
        detail_res = res.post_request(url="/api/interpretation/cs/variant/detail/evidence/list", json=json_data)
        assert detail_res.json()["retCode"] == 0
        assert detail_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("ExonCNV/SNV详情查看")
    @allure.title("ExonCNV/SNV详情查看-ACMG")
    @pytest.mark.parametrize("handle_task", [("interpret", "variant_detail", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_view_acmg(self, res, handle_task):
        variant_id = dict(handle_task[0])["variant_id"]
        json_data = {"variantId": variant_id, "purpose": "Interpret"}
        detail_res = res.post_request(url="/api/interpretation/cs/variant/detail/acmg/list", json=json_data)
        assert detail_res.json()["retCode"] == 0
        assert detail_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("ExonCNV/SNV详情查看")
    @allure.title("ExonCNV/SNV详情查看-KnowLiterInfo")
    @pytest.mark.parametrize("handle_task", [("interpret", "variant_detail", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_view_know_liter(self, res, handle_task):
        variant_id = dict(handle_task[0])["variant_id"]
        json_data = {"variantId": variant_id}
        detail_res = res.post_request(url="/api/interpretation/cs/variant/detail/snvKnowLiterInfo", json=json_data)
        assert detail_res.json()["retCode"] == 0
        assert detail_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("ExonCNV/SNV详情查看")
    @allure.title("ExonCNV/SNV详情查看-疾病")
    @pytest.mark.parametrize("handle_task", [("interpret", "variant_detail", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_view_disease(self, res, handle_task):
        variant_id = dict(handle_task[0])["variant_id"]
        detail_res = res.get_request(url=f"/api/interpretation/cs/variant/detail/disease/List?variantId={variant_id}")
        assert detail_res.json()["retCode"] == 0
        assert detail_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("ExonCNV/SNV详情查看")
    @allure.title("ExonCNV/SNV详情查看-计算致病性")
    @pytest.mark.parametrize("handle_task", [("interpret", "variant_detail", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_view_pathogenicity(self, res, handle_task):
        variant_id = dict(handle_task[0])["variant_id"]
        detail_res = res.post_request(
            f"/api/interpretation/cs/variant/detail/acmg/calculatePathogenicity?variantId={variant_id}"
        )
        assert detail_res.json()["retCode"] == 0
        assert detail_res.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("ExonCNV/SNV详情查看")
    @allure.title("ExonCNV/SNV详情查看-同Codon突变")
    @pytest.mark.parametrize("handle_task", [("interpret", "variant_detail", 1)], indirect=True)  # 当前场景下第三个参数无用
    def test_view_protein(self, res, handle_task):
        variant_id = dict(handle_task[0])["variant_id"]
        detail_res = res.post_request(
            f"/api/interpretation/cs/variant/detail/sameProteinPositionVar?variantId={variant_id}"
        )
        assert detail_res.json()["retCode"] == 0
        assert detail_res.json()["retInfo"] == "success"
