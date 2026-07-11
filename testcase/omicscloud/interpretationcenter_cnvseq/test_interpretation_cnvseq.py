import pytest
import allure

from testcase.omicscloud.interpretationcenter_cnvseq.interpretation_cnvseq_data import InterpretationData
from utils.logger import logger_t as logger
from utils.tools import calculate_file_buffer, replace_none
from time import sleep


@allure.feature("解读中心-康孕")
class TestInterpretation:

    large_cnv_id = None

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
        response = res.post_request(url="/api/interpretation/cnv-seq/task/list", json=search_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("提交审核")
    @allure.title("提交审核")
    @pytest.mark.parametrize("search_test_data", ["interpretation"], indirect=True)  # 查询当前用户待解读、解读中的任务
    def test_submit_review(self, res, search_test_data):
        task_id = search_test_data[0]
        submit_data = {
            "taskIds": [
                task_id
            ]
        }
        response = res.post_request(url="/api/interpretation/cnv-seq/task/review/submit", json=submit_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("报告预览")
    @allure.title("报告预览")
    @pytest.mark.parametrize("search_test_data", ["review"], indirect=True)  # 查询当前用户待审核、审核中的任务
    def test_report_preview(self, res, search_test_data):
        task_id = search_test_data[0]
        # 查询是否有电子核型图任务，没有后台会自动下任务，有的话直接报告预览，此处不关心该接口的结果
        task_data = {
            "taskIds": [
                task_id
            ]
        }
        response = res.post_request(url="/api/interpretation/cnv-seq/task/validate/task", json=task_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        # 调用报告生成接口
        response = res.post_request(url="/api/interpretation/cnv-seq/task/generate/report", json=task_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        report_data = response.json()["result"]
        # 报告预览，重复调用查询状态，直到返回报告状态为成功
        for i in range(15):
            logger.info(f"第{i + 1}次请求报告预览接口！")
            response = res.post_request(url="/api/interpretation/cnv-seq/task/view/report", json=report_data)
            assert response.json()["retCode"] == 0
            assert response.json()["retInfo"] == "success"
            if response.json()["result"][0]["reportStatus"] == "Finish":
                logger.info(f"第{i + 1}次请求报告预览接口！报告生成成功！")
                break
            if i == 14 and response.json()["result"][0]["reportStatus"] != "Finish":
                pytest.fail("请求报告预览接口15次，未生成报告成功，请检查！")
            sleep(0.5)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("任务统筹-手动分配")
    @allure.title("任务统筹-{search_test_data[1]}样本手动分配")
    @pytest.mark.parametrize("search_test_data", ["allocate-Positive", "allocate-Negative"], indirect=True)  # 查询待分配的任务
    def test_task_allocate(self, res, search_test_data):
        task_id = search_test_data[0]
        cnv_data_tag = search_test_data[1]  # 阴/阳性样本标签
        # 查询当前项目可分配的用户
        response = res.get_request(url="/api/interpretation/core/info/users", params={"projectCode": "CNV-seq"})
        # 获取自动化用户的user_id
        interpreter = [i for i in response.json()["result"] if i["userRealName"] == "自动化测试_中心交付"][0]
        reviewer = [i for i in response.json()["result"] if i["userRealName"] == "自动化测试_中心交付1"][0]
        # 阴/阳性样本的入参不一样
        negative_allocate_data = {
            "projectCode": "CNV-seq",
            "taskAssignQo": {
                "negativeTaskQo": {
                    "reviewer": str(interpreter["userId"]),
                    "reviewerName": interpreter["userRealName"],
                    "taskIds": [str(task_id)]
                },
                "positiveTaskQo": {
                    "interpreter": "",
                    "reviewer": "",
                    "taskIds": []
                }
            }
        }
        positive_allocate_data = {
            "projectCode": "CNV-seq",
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
                    "taskIds": [str(task_id)]
                }
            }
        }
        response = res.post_request(url="/api/interpretation/cnv-seq/task/assign/tasks",
                                    json=positive_allocate_data if cnv_data_tag == "Positive" else negative_allocate_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("任务统筹-自动分配")
    @allure.title("任务统筹-自动分配")
    def test_auto_allocate(self, res):
        allocate_data = {"sampleNo": "25B1211"}  # 入参写死
        response = res.post_request(url="/api/interpretation/cnv-seq/task/assign/tasks/auto", json=allocate_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("任务统筹-批量备注")
    @allure.title("任务统筹-批量备注")
    @pytest.mark.parametrize("search_test_data", ["all"], indirect=True)
    def test_batch_remark(self, res, search_test_data):
        task_id = search_test_data[0]
        remark_data = {
            "remark": "测试批量备注内容。",
            "taskIds": [
                task_id
            ]
        }
        response = res.post_request(url="/api/interpretation/cnv-seq/task/batch/remark", json=remark_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("任务转发")
    @allure.title("任务转发：{search_test_data[2]}任务转发")
    @pytest.mark.parametrize("search_test_data", ["interpretation-RT", "review-RT"], indirect=True)  # 查询当前用户待审核、审核中的任务
    def test_task_retweet(self, res, search_test_data):
        task_id = search_test_data[0]
        # 查询当前项目可分配的用户
        response = res.get_request(url="/api/interpretation/core/info/users", params={"projectCode": "CNV-seq"})
        # 获取转发用户的user_id
        retweet_user = [i for i in response.json()["result"] if i["userRealName"] == "徐枫4"][0]
        # 解读、审核任务的入参一样
        retweet_data = {
            "forwardUserId": str(retweet_user["userId"]),
            "forwardUserName": retweet_user["userRealName"],
            "taskIds": [task_id]
        }
        # if search_test_data[2] == "interpretation-RT":
        #     response = res.post_request(url="/api/interpretation/cnv-seq/task/forward", json=retweet_data)
        # else:
        response = res.post_request(url="/api/interpretation/cnv-seq/task/forward", json=retweet_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("导出-解读结果")
    @allure.title("导出-解读结果")
    @pytest.mark.parametrize("search_test_data", ["all"], indirect=True)
    def test_export_result(self, res, search_test_data):
        task_id = search_test_data[0]
        export_data = {
            "taskIds": [
                task_id
            ]
        }
        response = res.post_request("/api/interpretation/cnv-seq/task/export", json=export_data)
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("更多-重解析")
    @allure.title("更多-重解析")
    @pytest.mark.parametrize("search_test_data", ["allocate"], indirect=True)  # 查询待分配的任务
    def test_reparsing(self, res, search_test_data):
        task_id = search_test_data[0]
        reparse_data = {
            "taskIds": [
                task_id
            ]
        }
        response = res.post_request("/api/interpretation/cnv-seq/task/reparse", json=reparse_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("解读详情-CNV页")
    @allure.title("解读详情-CNV页数据查询")
    @pytest.mark.parametrize("search_test_data", ["all"], indirect=True)
    def test_cnv_list(self, res, search_test_data):
        task_id = search_test_data[0]
        response = res.get_request("/api/interpretation/cnv-seq/largecnv/list", params={"taskId": task_id})
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("解读详情-倍型页")
    @allure.title("解读详情-倍型页数据查询")
    @pytest.mark.parametrize("search_test_data", ["all"], indirect=True)
    def test_ploidy_list(self, res, search_test_data):
        task_id = search_test_data[0]
        response = res.get_request("/api/interpretation/cnv-seq/ploidy/ploidyInfo", params={"taskId": task_id})
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("解读详情-LOH页")
    @allure.title("解读详情-LOH页数据查询")
    @pytest.mark.parametrize("search_test_data", ["all"], indirect=True)
    def test_loh_list(self, res, search_test_data):
        task_id = search_test_data[0]
        response = res.get_request("/api/interpretation/cnv-seq/roh/rohInfo", params={"taskId": task_id})
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("解读详情-病原页")
    @allure.title("解读详情-病原页数据查询")
    @pytest.mark.parametrize("search_test_data", ["all"], indirect=True)
    def test_pathogen_list(self, res, search_test_data):
        task_id = search_test_data[0]
        response = res.get_request("/api/interpretation/cnv-seq/pathogen/pathogenInfo", params={"taskId": task_id})
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-退回解读")
    @allure.title("解读详情-退回解读")
    @pytest.mark.parametrize("search_test_data", ["review"], indirect=True)  # 查询当前用户待审核、审核中的任务
    def test_return_interpretation(self, res_1, search_test_data):
        task_id = search_test_data[0]
        is_interpreter = search_test_data[3]  # 是否存在解读人
        # 查询当前项目可分配的用户
        response = res_1.get_request(url="/api/interpretation/core/info/users", params={"projectCode": "CNV-seq"})
        return_data = {
            "taskIds": [
                task_id
            ]
        }
        if not is_interpreter:
            # 不存在解读人时，退回解读需要选择解读人，获取自动化用户的user_id
            interpreter = [i for i in response.json()["result"] if i["userRealName"] == "自动化测试_中心交付"][0]
            # 阴性样本没有解读人，退回解读时需要选择解读人
            interpretation_data = {
                "interpreter": str(interpreter["userId"]),
                "interpreterName": interpreter["userRealName"]
            }
            return_data.update(interpretation_data)
        response = res_1.post_request("/api/interpretation/cnv-seq/task/review/fallback", json=return_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-提交验证")
    @allure.title("解读详情-提交验证")
    @pytest.mark.parametrize("handle_task",
                             [("interpret", "validate", "roh"), ("interpret", "validate", "pathogen"),
                              ("interpret", "validate", "cnv"), ("interpret", "validate", "ploidy")],
                             indirect=True)
    def test_commit_validate(self, res, handle_task):
        task_id = dict(handle_task)['task_id']
        submit_data = [
            {
                "variationId": dict(handle_task)['variationId'],
                "validationType": dict(handle_task)['validationType'],
                "validationObj": dict(handle_task)['validationObj'],
                "sampleProductId": dict(handle_task)['sampleProductId'],
                "samplePatientId": dict(handle_task)['samplePatientId'],
                "sampleInspectionId": dict(handle_task)['sampleInspectionId'],
                "sampleNo": dict(handle_task)['sampleNo'],
                "validationStatus": "ToBeValidate",
                "svType": dict(handle_task)['svType'],
                "instanceNo": dict(handle_task)['instanceNo'],
                "applyRemark": "自动化测试提交验证"
            }
        ]
        response = res.post_request(f"/api/interpretation/cnv-seq/task/checkTaskBatch/{task_id}", json=submit_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-重置解读")
    @allure.title("解读详情-重置解读")
    @pytest.mark.parametrize("handle_task", [("interpret", "reset", "cnv")], indirect=True)
    def test_reset_interpretation(self, res, handle_task):
        variant_id = dict(handle_task)['variationId']
        json_data = {"largeCnvIds": [variant_id]}
        response = res.post_request("/api/interpretation/cnv-seq/largecnv/reset", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-重新生成核型图")
    @allure.title("解读详情-重新生成核型图")
    @pytest.mark.parametrize("handle_task", [("interpret", "redraw", "cnv")], indirect=True)
    def test_redraw(self, res, handle_task):
        task_id = dict(handle_task)['task_id']
        json_data = {}
        response = res.post_request(f"/api/interpretation/cnv-seq/largecnv/redraw/{task_id}", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-查看全局图")
    @allure.title("解读详情-查看全局图")
    @pytest.mark.parametrize("handle_task", [("interpret", "scatter", "cnv")], indirect=True)
    def test_scatter(self, res, handle_task):
        task_id = dict(handle_task)['task_id']
        json_data = {}
        response = res.post_request(f"/api/interpretation/cnv-seq/largecnv/plotCnvScatterAll/{task_id}", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("其他异常处理")
    @allure.title("其他异常处理-{data[case_name]}")
    @pytest.mark.parametrize("handle_task", [("interpret", "exception", "default")], indirect=True)
    @pytest.mark.parametrize("data", InterpretationData.other_exception_data)
    def test_handle_exception(self, res, data, handle_task):
        task_id = dict(handle_task)['task_id']
        json_data = {
            "taskIds": [task_id],
            "projectCode": "CNV-seq",
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
        response = res.post_request("/api/interpretation/cnv-seq/task/handle/otherException", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("其他异常处理-获取样本信息")
    @allure.title("其他异常处理-获取样本信息")
    @pytest.mark.parametrize("handle_task", [("interpret", "get_sample", "default")], indirect=True)
    def test_get_sample_info(self, res, handle_task):
        task_id = dict(handle_task)['task_id']
        json_data = {"taskIdList": [task_id]}
        response = res.post_request("/api/interpretation/cnv-seq/task/resetSample", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("任务统筹-加急")
    @allure.title("任务统筹-加急")
    @pytest.mark.parametrize("handle_task", [("interpret", "urgent", "default")], indirect=True)
    def test_urgent(self, res, handle_task):
        task_id = dict(handle_task)['task_id']
        json_data = {"taskIds": [task_id]}
        response = res.post_request("/api/interpretation/cnv-seq/task/taskUrgent", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-注释状态查询")
    @allure.title("解读详情-注释状态查询")
    def test_query_anno_task(self, res, mysql_connect):
        task_ids = mysql_connect.select(
            "select task_id from interpretation_task where project_code = 'CNV-seq' and status in "
            "('ReadyForInterpret','Interpreting') and task_id in (select task_id from interpretation_anno_single_task)")
        task_id = task_ids[0]['task_id']
        response = res.get_request(f"/api/interpretation/cnv-seq/anno/annotation?taskId={task_id}")
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"] is not None

    # @allure.severity(allure.severity_level.NORMAL)
    # @allure.story("更多-解读终止")
    # @allure.title("更多-解读终止")
    # @pytest.mark.parametrize("handle_task", [("interpret", "terminate", "default")], indirect=True)
    # def test_terminate_task(self, res, handle_task):
    #     task_id = dict(handle_task)['task_id']
    #     json_data = {
    #         "taskIds": [task_id],
    #         "projectCode": "CNV-seq",
    #         "mailInfo": {
    #             "attachment": [],
    #             "content": "各位好！\r\ntesttest此邮件由系统自动发送，请勿单独回复！",
    #             "copyer": "huangyan10@bgi.com",
    #             "mailType": "InterpretationTerminate",
    #             "receiver": "huangyan10@bgi.com",
    #             "sender": "huangyan10@bgi.com",
    #             "title": "【解读终止】test"
    #         },
    #         "terminateReasonType": "RenderInconsistent",
    #         "otherReason": ""
    #     }
    #     response = res.post_request("/api/interpretation/cnv-seq/task/terminate", json=json_data)
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
    #     query = res_cloud.post_request("/api/interpretation/cnv-seq/task/list", json=query_data)
    #     task_id = query.json()['result']['records'][0]['taskId']
    #     # 将任务的解读人设置为自动化测试-专家云账号
    #     mysql_connect.execute(f"update interpretation_task set reviewer = 567289559516319744,"
    #                           f"reviewer_name = '自动化测试-专家云' where task_id = '{task_id}'")
    #     json_data = {"taskIds": [task_id]}
    #     response = res_cloud.post_request("/api/interpretation/cnv-seq/task/interpretationCloud/finish", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"
    #
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.story("更多-报告重新推送")
    # @allure.title("更多-报告重新推送")
    # @pytest.mark.parametrize("handle_task", [("finish", "recomplete", "push_fail")], indirect=True)
    # def test_recomplete_report(self, res, handle_task):
    #     json_data = [dict(handle_task)['task_id']]
    #     response = res.post_request("/api/interpretation/cnv-seq/task/reComplete/report", json=json_data)
    #     assert response.json()["retCode"] == 0
    #     assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("三级详情页-重新生成结果说明")
    @allure.title("三级详情页-重新生成结果说明")
    @pytest.mark.parametrize("data", ["allUpdate", "onlyVariantSource", "breakpointLimitation"])
    def test_update_result_desc(self, res, mysql_connect, data):
        large_cnv_ids = mysql_connect.select("select ilc.large_cnv_id from interpretation_task it "
                                             "inner join interpretation_large_cnv ilc on it.task_id = ilc.task_id "
                                             "where it.product_no is not null and ilc.sv_type ='CNV' and "
                                             "it.project_code = 'CNV-seq' and it.status in ('ReadyForInterpret',"
                                             "'Interpreting','ReadyForReview','Reviewing')")
        large_cnv_id = large_cnv_ids[0]['large_cnv_id']
        detail = res.get_request(f"/api/interpretation/cnv-seq/largecnv/detail/info?largeCnvId={large_cnv_id}")
        json_data = detail.json()['result']
        large_cnv_over_laps = json_data['largeCnvOverlaps'] if json_data['largeCnvOverlaps'] else []
        validation_result = json_data['validationResult'] if json_data['validationResult'] else []
        tmp = {
            "updateFlag": data,
            "largeCnvOverlaps": large_cnv_over_laps,
            "validationResult": validation_result
        }
        json_data.update(tmp)
        response = res.post_request("/api/interpretation/cnv-seq/largecnv/detail/update", json=replace_none(json_data))
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("三级详情页-添加/编辑证据项")
    @allure.title("三级详情页-添加/编辑证据项")
    def test_add_evidence(self, res, mysql_connect):
        large_cnv_ids = mysql_connect.select("select ilc.task_id, ilc.large_cnv_id from interpretation_task it "
                                             "inner join interpretation_large_cnv ilc on it.task_id = ilc.task_id "
                                             "where it.product_no is not null and ilc.sv_type ='CNV' and "
                                             "it.project_code = 'CNV-seq' and it.status in ('ReadyForInterpret',"
                                             "'Interpreting','ReadyForReview','Reviewing') and it.task_source='Centre';")
        TestInterpretation.large_cnv_id = large_cnv_ids[0]['large_cnv_id']
        task_id = large_cnv_ids[0]['task_id']
        detail = res.get_request(f"/api/interpretation/cnv-seq/largecnv/detail/info?"
                                 f"largeCnvId={TestInterpretation.large_cnv_id}")
        effect_type = detail.json()['result']['effectType']
        json_data = {
            "taskId": task_id,
            "largeCnvId": TestInterpretation.large_cnv_id,
            "effectType": effect_type,
            "acmgCriteria": "Other", "acmgScore": 1, "description": "test", "delEvidenceIds": [],
            "evidenceList": [{"score": 1, "literatureMeta": "", "explanation": "test", "literatureReportFlag": "Y",
                              "type": "pmid", "id": "11122", "literatureCitation": "V L Del Pino, H M Bolt. [Effect of"
                                                                                   " liver damage by thioacetamide on "
                                                                                   "microsomal aromatization of "
                                                                                   "testosterone in rats (author's "
                                                                                   "transl)][J]. Experientia, 1976,11: 1456-7.",
                              "literatureFilePath": "", "literatureFileName": '', "attachmentFilePath": "",
                              "attachmentFileName": "", "evidenceType": "Literature", "firstAuthor": "V L Del Pino",
                              "year": "1976", "description": "test", "pmid": "11122", "doi": "", "literatureUrl": ""}],
            "score": 1, "section": "0"
        }
        response = res.post_request("/api/interpretation/cnv-seq/largecnv/detail/evidence/addOrUpdate", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @pytest.mark.run(after='test_add_evidence')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("三级详情页-删除证据项")
    @allure.title("三级详情页-删除证据项")
    def test_delete_evidence(self, res):
        large_cnv_acmg_id = None
        detail = res.get_request(f"/api/interpretation/cnv-seq/largecnv/detail/acmg/interpret?"
                                 f"largeCnvId={TestInterpretation.large_cnv_id}")
        for item in detail.json()['result']:
            if item['acmgCriteria'] == 'Other':
                large_cnv_acmg_id = item['largeCnvAcmgId']
                break
        json_data = {
            "largeCnvAcmgId": large_cnv_acmg_id,
            "largeCnvId": TestInterpretation.large_cnv_id,
        }
        response = res.post_request("/api/interpretation/cnv-seq/largecnv/detail/acmg/remove", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-更新检出信息")
    @allure.title("解读详情-更新检出信息")
    @pytest.mark.parametrize("handle_task",
                             [("interpret", "update_result", "roh"), ("interpret", "update_result", "pathogen"),
                              ("interpret", "update_result", "cnv"), ("interpret", "update_result", "ploidy")],
                             indirect=True)
    def test_update_result(self, res, handle_task):
        update_url = dict(handle_task)['update_url']
        json_data = dict(handle_task)['part_result']
        response = res.post_request(f"/api/interpretation/cnv-seq/{update_url}", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"] == "编辑成功"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("解读详情-更新CNV拷贝数、嵌合比例")
    @allure.title("解读详情-更新CNV拷贝数、嵌合比例")
    def test_update_result(self, res, mysql_connect):
        large_cnv_ids = mysql_connect.select("select ilc.task_id, ilc.large_cnv_id from interpretation_task it "
                                             "inner join interpretation_large_cnv ilc on it.task_id = ilc.task_id "
                                             "where it.product_no is not null and ilc.sv_type !='CNV' and "
                                             "ilc.variant_source = 'Manual' and it.project_code = 'CNV-seq' and "
                                             "it.status in ('ReadyForInterpret','Interpreting','ReadyForReview','Reviewing')")
        large_cnv_id = large_cnv_ids[0]['large_cnv_id']
        task_id = large_cnv_ids[0]['task_id']
        detail = res.get_request(f"/api/interpretation/cnv-seq/largecnv/list?taskId={task_id}")
        json_data = {}
        for item in detail.json()['result']:
            if item['largeCnvId'] == str(large_cnv_id):
                json_data = item['largeCnvAggregationVos'][0]
                tmp = {'variantInfo': item['variantInfo']}
                json_data.update(tmp)
                break
        response = res.post_request("/api/interpretation/cnv-seq/largecnv/aggregation/update", json=json_data)
        assert response.json()["retCode"] == 0
        assert response.json()["retInfo"] == "success"
        assert response.json()["result"] == "编辑成功"
