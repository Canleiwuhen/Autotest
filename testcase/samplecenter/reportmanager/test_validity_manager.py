import pytest
import allure
import time
from urllib.parse import urlencode
from testcase.samplecenter.reportmanager.validity_manager_data import DataList


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("效期管理")
@pytest.mark.usefixtures("res", "token")
class TestValidityManager:
    @allure.story("搜索")
    @allure.title("搜索-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_validity_manager_list)
    def test_query_validity_manager_list(self, res, token, data):
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_ValidityManager",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_validity_manager", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200", f"查询失败！response：{response.json()}"

    @allure.story("搜索")
    @allure.title("搜索-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_validity_manager_fail_list)
    def test_query_validity_manager_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_ValidityManager",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_validity_manager", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data["msg"],\
            f"查询失败！response：{response.json()}"

    @allure.story("导出全部")
    @allure.title("导出全部-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_validity_manager_list)
    def test_export_validity_manager(self, res, token, data):
        # 获取测试参数
        query_data = {
            "excelHead": [{"Header": "序号", "accessor": "key", "width": 50},
                          {"Header": "样本编号", "accessor": "zcatalo", "width": 130},
                          {"Header": "样例编号", "accessor": "zsample", "width": 120},
                          {"Header": "客户名称", "accessor": "name1", "width": 120},
                          {"Header": "产品组合描述", "accessor": "zmatnr_ty_text", "width": 120},
                          {"Header": "产品编号", "accessor": "matnr", "width": 120},
                          {"Header": "产品描述", "accessor": "maktx", "width": 120},
                          {"Header": "样本类型", "accessor": "zyblx", "width": 120},
                          {"Header": "项目名称", "accessor": "zxmmc", "width": 120},
                          {"Header": "到样日期", "accessor": "zreceiveddate", "width": 120},
                          {"Header": "默认存储时间(天)", "accessor": "zday", "width": 120},
                          {"Header": "浮动天数", "accessor": "zfloat", "width": 120},
                          {"Header": "浮动原因", "accessor": "zreason", "width": 120},
                          {"Header": "预计销毁日期", "accessor": "zyjxhdate", "width": 120},
                          {"Header": "库存状态", "accessor": "zkc_status", "width": 120},
                          {"Header": "容器编码", "accessor": "zplate_num", "width": 120},
                          {"Header": "孔位", "accessor": "zpoint", "width": 120},
                          {"Header": "库存位置", "accessor": "zfrgid", "width": 120},
                          {"Header": "箱子编号", "accessor": "zbox", "width": 120}],
            "pageNumber": "1",
            "pageSize": "200000",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_ValidityManager",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=export_validity_manager", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and '详情' in response.json()["msg"], \
            f"导出失败！response：{response.json()}"

    @allure.story("导出本页")
    @allure.title("导出本页")
    def test_export_sample_detail(self, res, token):
        # 获取测试参数
        query_data = {
            "datas": [
                ["序号", "样本编号", "样例编号", "客户名称", "产品组合描述", "产品编号", "产品描述", "样本类型", "项目名称", "到样日期", "默认存储时间(天)", "浮动天数",
                 "浮动原因", "预计销毁日期", "库存状态", "容器编码", "孔位", "库存位置", "箱子编号"],
                [1, "10B00100104", "10B00100104", "Centre for DNA Fingerprinting", "单基因", "HW0040",
                 "NIFTY sinlge-gene screening test Bundle", "全血", "", "2020-10-13 10:39:53", "0000", "32", "3123",
                 "20201114", "入库定位", "20SZYCQX02-2046", "A04", "", ""],
                [2, "10B00100102", "10B00100102", "Centre for DNA Fingerprinting", "单基因", "HW0040",
                 "NIFTY sinlge-gene screening test Bundle", "全血", "", "2020-10-13 10:39:53", "0000", "366", "飞人\n",
                 "20211014", "入库定位", "20SZYCQX02-2046", "A02", "", ""],
                [3, "10B00100103", "10B00100103", "Centre for DNA Fingerprinting", "单基因", "HW0040",
                 "NIFTY sinlge-gene screening test Bundle", "全血", "", "2020-10-13 10:39:53", "0000", "366", "123",
                 "20211014", "入库定位", "20SZYCQX02-2046", "A03", "", ""]],
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_ValidityManager",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/exportSampleDetail.do?", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["status"] == "success" \
               and '详情' in response.json()["filePath"], f"导出失败！response：{response.json()}"

    @allure.story("新增浮动")
    @allure.title("新增浮动")
    def test_add_float(self, res, token):
        # 获取测试参数
        query_data = {
            "task": {"zybzx":"X","zreceiveddatenew":"","zyjxhdate":"","zmatnr_ty":"T001,T002,T003","zsfxhfy":"否"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_ValidityManager",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_validity_manager", data=urlencode(query_data))
        sample = query_response.json()["data"][0]["zcatalo"]
        add_data = {
            "datas": [{"ZCATALO": sample,
                       "ZFLOAT": 2000,
                       "ZREASON": f"autotest,reason_{int(time.time())}"}],
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_ValidityManager",
            "zsjd_type": "YX"
        }
        add_response = res.post_request("/ybzx/webintf.do?method=save_validity_manager_add_float", data=urlencode(add_data))
        # print(response.json())
        assert add_response.status_code == 200 and add_response.json()["code"] == "200" \
               and add_response.json()["msg"] == "success", f"新增浮动失败！response：{add_response.json()}"


if __name__ == '__main__':
    pytest.main()
