import time
from random import sample
from urllib.parse import urlencode

import allure
import pytest

from data_generate.samplecenter.datagenerate import DataGenerate

test_user = 'testuser1'

@allure.feature("主流程测试")
class TestKeyProcess:
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景1")
    @allure.title("路径：0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:新增容器--5:医学到样定位（新）--6:出库申请--7:出库审核-8:入库申请--9:入库审核")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 9, 'run_time': 1, 'user_name': test_user}],
                             indirect=True)
    def test_from_submit_inspection_to_inbound_audit(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的入库申请单号，用于查询入库申请单状态并断言
        inbound_apply_order_number = generate_steps[0]['inbound_apply_order_number']
        if inbound_apply_order_number:
            query_data = {
                "task": {"zybzx": "X", "zscdh": inbound_apply_order_number},
                "pageNumber": 1,
                "pageSize": 50,
                "token": token,
                "menuId": "inBound",
                "zsjd_type": "YX"
            }
            response = res.post_request("/ybzx/webintf.do?method=query_in_bound_apply_bill", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["data"][0]["zreqstat_t"] == "已审核", f"主流程测试场景1异常：入库审核失败，原因：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景2")
    @allure.title("路径：0:包裹补录--1:医学拆包")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 1, 'run_time': 1, 'user_name': test_user}],
                             indirect=True)
    def test_from_replenish_record_to_unpack(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的物流单号，用于查询到达序列号和物流单号并断言
        expressnum = generate_steps[0]['expressnum']
        if expressnum:
            query_data = {
                "expressNumber": expressnum,
                "type": 3,
                "token": token
            }
            response = res.post_request("/ybzx/pos/query/kddh.do", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["data"]["zexpressnumber"] == expressnum and response_json["data"]["zarrvseries"] is not None, f"主流程测试场景2异常：补录失败，原因：{response_json}"


    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景3")
    @allure.title(
        "路径：0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:新增容器--5:医学到样定位（新））--6:出库申请--7:出库审核--8:接收确认")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path3', 'last_step': 8, 'run_time': 1, 'user_name': test_user}],
                             indirect=True)
    def test_from_submit_inspection_to_receipt_confirmation(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的出库申请单号，用于查询出库单状态并断言
        outbound_apply_order_number = generate_steps[0]['outbound_apply_order_number']
        if outbound_apply_order_number:
            query_data = {
                "task": {"zybzx": "X","zscdh": outbound_apply_order_number},
                "pageNumber": 1,
                "pageSize": 50,
                "token": token,
                "menuId": "OutBoundAffirm",
                "zsjd_type": "YX"
            }
            time.sleep(5)
            response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["data"][0]["zrecstat_t"] == "全部接收", f"主流程测试场景3异常：接收确认失败，原因：{response_json}"


    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景4")
    @allure.title("0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:新增容器--5:医学到样定位（新）--6:医学信息审核")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path4', 'last_step': 6, 'run_time': 1, 'user_name': test_user}],
                             indirect=True)
    def test_from_submit_inspection_to_medical_audit(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的样本编号，用于查询样本审核状态并断言
        sample = generate_steps[0]['sample'][0]
        if sample:
            query_data = {
                "task": {"zybzx": "X", "zcatalo": sample},
                "pageNumber": 1,
                "pageSize": 50,
                "token": token,
                "menuId": "informationAudit",
                "zsjd_type": "YX"
            }
            response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["data"][0]["zybzt"] == "已审核", f"主流程测试场景4异常：医学审核失败，原因：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("主流程测试场景5")
    @allure.title("路径：0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:样本批量接收")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path5', 'last_step': 4, 'run_time': 1, 'user_name': test_user}],
                             indirect=True)
    def test_from_submit_inspection_to_sample_batch_receive(self, res, token, generate_steps):
        token = token(test_user)['token']
        # 获取造数工具返回结果中的样本编号，用于查询样本定位状态并断言
        sample = generate_steps[0]['sample'][0]
        if sample:
            query_data = {
                "task": {"zybzx": "X", "zcatalo": sample, "zsjdType": "YX", "zsfxhfy": "否"},
                "pageNumber": 1,
                "pageSize": 50,
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"
            }
            response = res.post_request("/ybzx/webintf.do?method=query_all_samples", data=urlencode(query_data))
            response_json = response.json()
            assert response_json["data"][0][
                       "zdwxx"] == "已定位", f"主流程测试场景5异常：原因：{response_json}"

    # @pytest.mark.skip("暂不需要实现")
    # @allure.severity(allure.severity_level.BLOCKER)
    # @allure.story("主流程测试场景6")
    # @allure.title("路径：包裹接收->医学拆包->无单样本添加->MYBGI补录送检单->医学到样定位（新）")
    # def test_from_package_receive_to_none_inspection_add_and_finally_to_sample_location(self, res, token):
    #     pass
    #
    # @pytest.mark.skip("暂不需要实现")
    # @allure.severity(allure.severity_level.BLOCKER)
    # @allure.story("主流程测试场景7")
    # @allure.title("路径：包裹接收->医学拆包->无单样本添加->MYBGI补录送检单->无单自动到样->医学信息审核")
    # def test_from_package_receive_to_none_inspection_add_and_finally_to_medical_audit(self, res, token):
    #     pass
    #
    # @pytest.mark.skip("暂不需要实现")
    # @allure.severity(allure.severity_level.BLOCKER)
    # @allure.story("主流程测试场景8")
    # @allure.title("路径：包裹接收->医学拆包->无单样本添加->MYBGI补录送检单->无单自动到样->出库审核->接收确认")
    # def test_from_package_receive_to_none_inspection_add_and_finally_to_receipt_confirmation(self, res, token):
    #     pass
    #
    # @pytest.mark.skip("暂不需要实现")
    # @allure.severity(allure.severity_level.BLOCKER)
    # @allure.story("主流程测试场景9")
    # @allure.title("路径：包裹接收->医学拆包->无单样本添加->MYBGI补录送检单->无单自动到样->出库审核->入库申请->入库审核")
    # def test_from_package_receive_to_none_inspection_add_and_finally_to_inbound_audit(self, res, token):
    #     pass
    #
    # @pytest.mark.skip("暂不需要实现")
    # @allure.severity(allure.severity_level.BLOCKER)
    # @allure.story("主流程测试场景10")
    # @allure.title("路径：包裹接收->医学拆包->无单样本添加->MYBGI补录送检单->样本批量接收")
    # def test_from_package_receive_to_none_inspection_add_and_finally_to_sample_batch_receive(self, res, token):
    #     pass