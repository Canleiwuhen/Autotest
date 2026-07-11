import pytest
import allure
from urllib.parse import urlencode
from utils.tools import replace_none


@allure.feature("接收确认")
@pytest.mark.usefixtures("res")
class TestReceiveConfirm:
    query_outbound_apply_form_data_list = [
        {
            "case_name": "输入出库申请单号",
            "data": {
                "task": {"zybzx": "X", "zscdh": "OBR241000000438"}
            }
        },
        {
            "case_name": "输入样本编号",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "24X101700011"}
            }
        },
        {
            "case_name": "输入申请人",
            "data": {
                "task": {"zybzx": "X", "zcjnam": "autotest1"}
            }
        },
        {
            "case_name": "输入申请日期起",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "20241016"}
            }
        },
        {
            "case_name": "输入申请日期止",
            "data": {
                "task": {"zybzx": "X", "zcjdatend": "20241001"}
            }
        },
        {
            "case_name": "输入接收确认状态",
            "data": {
                "task": {"zybzx": "X", "zrecstat": "20"}  # 全部接收
            }
        },
        {
            "case_name": "输入出库原因",
            "data": {
                "task": {"zybzx": "X", "zreson": "研发出库"}
            }
        },
        {
            "case_name": "输入出库日期",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "20241017"}
            }
        }
    ]

    query_outbound_apply_form_data_list_fail = [
        {
            "case_name": "输入不存在的出库申请单号，该查询无值.",
            "msg": "该查询无值.",
            "data": {
                "task": {"zybzx": "X", "zscdh": "OBR2410000004388"}
            }
        }
    ]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("搜索")
    @allure.title("搜索-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_outbound_apply_form_data_list)
    def test_query_outbound_apply_form(self, res, token, data):
        """
        出库申请单查询
        :param res:
        :param token:
        :param data:
        :return:
        """
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound", data=urlencode(query_data))
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
            "msg"] == "success", f"查询出库申请单失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("搜索")
    @allure.title("搜索-异常场景-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_outbound_apply_form_data_list_fail)
    def test_query_outbound_apply_form_fail(self, res, token, data):
        """
        出库申请单查询-异常场景
        :param res:
        :param token:
        :param data:
        :return:
        """
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound", data=urlencode(query_data))
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == data["msg"], f"查询出库申请单失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("接收确认")
    @allure.title("接收确认-用例名称：接收确认主流程")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 7, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_receive_confirm(self, res, token, generate_steps):
        """
        测试接收确认主流程
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        outbound_apply_order_number = generate_steps[0]["outbound_apply_order_number"]  # 拿到已出库审核的出库申请单号
        # 查询出库申请单内样本信息
        query_data = {
            "zscdh": outbound_apply_order_number,
            "token": token,
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_sample_by_sqdh", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()[
            "code"] == "200", f"查询出库申请单内样本信息失败！response：{query_response.json()}"
        query_response_data = query_response.json()["data"]
        # 基于查询的样本提交接收确认
        confirm_data = {
            "datas": [
                {
                    "zscdh": query_response_data[i]["zscdh"],
                    "zscdh_item": query_response_data[i]["zscdh_item"],
                    "zstatus": "20",
                    "zexc_text": "",
                    "zkeep_site": query_response_data[i]["zkeep_site"]
                }
                for i in range(len(query_response_data))
            ],
            "token": token,
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        confirm_data = replace_none(confirm_data)  # 替换data中的None为""
        confirm_response = res.post_request("/ybzx/webintf.do?method=submit_chuku", data=urlencode(confirm_data))
        assert confirm_response.status_code == 200 and confirm_response.json()["code"] == "200" and \
               confirm_response.json()["msg"] == "success", f"接收确认失败！response：{confirm_response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("接收确认")
    @allure.title("接收确认-用例名称：接收确认->标记异常")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 7, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_receive_confirm_mark_abnormal(self, res, token, generate_steps):
        """
        测试接收确认->标记异常
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        outbound_apply_order_number = generate_steps[0]["outbound_apply_order_number"]  # 拿到已出库审核的出库申请单号
        # 查询出库申请单内样本信息
        query_data = {
            "zscdh": outbound_apply_order_number,
            "token": token,
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_sample_by_sqdh", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()[
            "code"] == "200", f"查询出库申请单内样本信息失败！response：{query_response.json()}"
        query_response_data = query_response.json()["data"]
        # 基于查询的样本提交接收确认
        confirm_data = {
            "datas": [
                {
                    "zscdh": query_response_data[i]["zscdh"],
                    "zscdh_item": query_response_data[i]["zscdh_item"],
                    "zstatus": "10",
                    "zexc_text": "样本/文库有异物",
                    "zkeep_site": query_response_data[i]["zkeep_site"]
                }
                for i in range(len(query_response_data))
            ],
            "token": token,
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        confirm_data = replace_none(confirm_data)  # 替换data中的None为""
        confirm_response = res.post_request("/ybzx/webintf.do?method=submit_chuku", data=urlencode(confirm_data))
        assert confirm_response.status_code == 200 and confirm_response.json()["code"] == "200" and \
               confirm_response.json()["msg"] == "success", f"接收确认->标记异常失败！response：{confirm_response.json()}"
