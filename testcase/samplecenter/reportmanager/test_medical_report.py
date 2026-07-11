import pytest
import allure
from urllib.parse import urlencode


@allure.severity(allure.severity_level.NORMAL)
@allure.feature("医学报表")
@pytest.mark.usefixtures("res", "token")
class TestMedicalReport:
    query_bgcrk_report_list = [
        {
            "case_name": "输入操作日期",
            "data": {
                "task": {"zybzx":"X","zdate":"20240601","zdateend":"20241101"}
            }
        },
        {
            "case_name": "输入操作日期、操作人账号",
            "data": {
                "task": {"zybzx":"X","zuser":"autotest1","zdate":"20240301","zdateend":"20241107"}
            }
        }
    ]

    query_bgcrk_report_fail_list = [
        {
            "case_name": "全部查询条件为空，请输入：操作日期",
            "msg": "请输入：操作日期",
            "data": {
                "task": {"zybzx": "X", "zuser": ""}
            }
        },
        {
            "case_name": "仅输入操作人账号，请输入：操作日期",
            "msg": "请输入：操作日期",
            "data": {
                "task": {"zybzx": "X", "zuser": "auto"}
            }
        }
    ]

    query_dysh_report_list = [
        {
            "case_name": "输入操作日期",
            "data": {
                "task": {"zybzx":"X","zdate":"20240801","zdateend":"20241101"}
            }
        },
        {
            "case_name": "输入操作日期、产品",
            "data": {
                "task": {"zybzx":"X","matnr":"DX0511,DX0510","zdate":"20240801","zdateend":"20241101"}
            }
        },
        {
            "case_name": "输入操作日期、产品类",
            "data": {
                "task": {"zybzx":"X","zmatnr_ty":"T019","zdate":"20240801","zdateend":"20241101"}
            }
        },
        {
            "case_name": "输入操作日期、操作人账号",
            "data": {
                "task": {"zybzx":"X","zuser":"huxiaofeng_A020,zhongyingying","zdate":"20240801","zdateend":"20241101"}
            }
        },
        {
            "case_name": "输入操作日期、操作人账号、产品类、产品",
            "data": {
                "task": {"zybzx":"X","zuser":"huxiaofeng_A020,zhongyingying","zmatnr_ty":"T019","matnr":"DX1356,DX1355,DX1352,DX1351,DX1259,DX1258,DX1257","zdate":"20240801","zdateend":"20241101"}
            }
        }
    ]

    query_dysh_report_fail_list = [
        {
            "case_name": "全部查询条件为空，请输入：操作日期",
            "msg": "请输入：操作日期",
            "data": {
                "task": {"zybzx":"X"}
            }
        },
        {
            "case_name": "仅输入操作人账号，请输入：操作日期",
            "msg": "请输入：操作日期",
            "data": {
                "task": {"zybzx": "X", "zuser": "auto"}
            }
        }
    ]

    @allure.story("包裹与出入库")
    @allure.title("搜索-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_bgcrk_report_list)
    def test_query_bgcrk_report_list(self, res, token, data):
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_bgcrk_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200", f"查询失败！response：{response.json()}"

    @allure.story("包裹与出入库")
    @allure.title("搜索-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_bgcrk_report_fail_list)
    def test_query_bgcrk_report_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_bgcrk_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data["msg"],\
            f"查询失败！response：{response.json()}"

    @allure.story("包裹与出入库")
    @allure.title("导出全部-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_bgcrk_report_list)
    def test_export_bgcrk_report(self, res, token, data):
        # 获取测试参数
        query_data = {
            "excelHead": [{"Header": "序号", "accessor": "key", "width": 50},
                          {"Header": "操作人账号", "accessor": "zuser", "width": 130},
                          {"Header": "包裹接收(个)", "accessor": "cnt_bgjs", "width": 120},
                          {"Header": "拆包(个)", "accessor": "cnt_cb", "width": 120},
                          {"Header": "出库(样本数)", "accessor": "cnt_out", "width": 130},
                          {"Header": "样本入库", "accessor": "cnt_in", "width": 130},
                          {"Header": "整版入库", "accessor": "cnt_in_zb", "width": 130},
                          {"Header": "逐样入库", "accessor": "cnt_in_zysh", "width": 130},
                          {"Header": "批量入库", "accessor": "cnt_in_plsh", "width": 130},
                          {"Header": "操作日期起", "accessor": "zdate_f", "width": 110},
                          {"Header": "操作日期止", "accessor": "zdate_t", "width": 110}],
            "pageNumber": "1",
            "pageSize": "200000",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=export_bgcrk_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and '详情' in response.json()["msg"], \
            f"导出失败！response：{response.json()}"

    @allure.story("包裹与出入库")
    @allure.title("导出全部-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_bgcrk_report_fail_list)
    def test_export_bgcrk_report_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "excelHead": [{"Header": "序号", "accessor": "key", "width": 50},
                          {"Header": "操作人账号", "accessor": "zuser", "width": 130},
                          {"Header": "包裹接收(个)", "accessor": "cnt_bgjs", "width": 120},
                          {"Header": "拆包(个)", "accessor": "cnt_cb", "width": 120},
                          {"Header": "出库(样本数)", "accessor": "cnt_out", "width": 130},
                          {"Header": "样本入库", "accessor": "cnt_in", "width": 130},
                          {"Header": "整版入库", "accessor": "cnt_in_zb", "width": 130},
                          {"Header": "逐样入库", "accessor": "cnt_in_zysh", "width": 130},
                          {"Header": "批量入库", "accessor": "cnt_in_plsh", "width": 130},
                          {"Header": "操作日期起", "accessor": "zdate_f", "width": 110},
                          {"Header": "操作日期止", "accessor": "zdate_t", "width": 110}],
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=export_bgcrk_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data[
            "msg"], f"导出失败！response：{response.json()}"

    @allure.story("样本与样例")
    @allure.title("搜索-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_dysh_report_list)
    def test_query_dysh_report_list(self, res, token, data):
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_dysh_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200", f"查询失败！response：{response.json()}"

    @allure.story("样本与样例")
    @allure.title("搜索-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_dysh_report_fail_list)
    def test_query_dysh_report_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_dysh_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data["msg"],\
            f"查询失败！response：{response.json()}"

    @allure.story("样本与样例")
    @allure.title("导出全部-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_dysh_report_list)
    def test_export_dysh_report(self, res, token, data):
        # 获取测试参数
        query_data = {
            "excelHead": [{"Header": "序号", "accessor": "key", "width": 50},
                          {"Header": "产品编号", "accessor": "matnr", "width": 100},
                          {"Header": "产品名称", "accessor": "maktx", "width": 230},
                          {"Header": "产品类", "accessor": "ewbez", "width": 130},
                          {"Header": "操作人账号", "accessor": "zuser", "width": 130},
                          {"Header": "到样数(样例/个)", "accessor": "cnt_yl", "width": 120},
                          {"Header": "到样数(样本/个)", "accessor": "cnt_yb", "width": 120},
                          {"Header": "转出样例数", "accessor": "cnt_zcyl", "width": 120},
                          {"Header": "转出样本数", "accessor": "cnt_zcyb", "width": 120},
                          {"Header": "销毁数", "accessor": "cnt_xhyb", "width": 120},
                          {"Header": "信息审核(送检单/份)", "accessor": "cnt_sjd", "width": 150},
                          {"Header": "操作日期起", "accessor": "zdate_f", "width": 110},
                          {"Header": "操作日期止", "accessor": "zdate_t", "width": 110}],
            "pageNumber": "1",
            "pageSize": "200000",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=export_dysh_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and '详情' in response.json()["msg"], \
            f"导出失败！response：{response.json()}"

    @allure.story("样本与样例")
    @allure.title("导出全部-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_dysh_report_fail_list)
    def test_export_dysh_report_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "excelHead": [{"Header": "序号", "accessor": "key", "width": 50},
                          {"Header": "产品编号", "accessor": "matnr", "width": 100},
                          {"Header": "产品名称", "accessor": "maktx", "width": 230},
                          {"Header": "产品类", "accessor": "ewbez", "width": 130},
                          {"Header": "操作人账号", "accessor": "zuser", "width": 130},
                          {"Header": "到样数(样例/个)", "accessor": "cnt_yl", "width": 120},
                          {"Header": "到样数(样本/个)", "accessor": "cnt_yb", "width": 120},
                          {"Header": "转出样例数", "accessor": "cnt_zcyl", "width": 120},
                          {"Header": "转出样本数", "accessor": "cnt_zcyb", "width": 120},
                          {"Header": "销毁数", "accessor": "cnt_xhyb", "width": 120},
                          {"Header": "信息审核(送检单/份)", "accessor": "cnt_sjd", "width": 150},
                          {"Header": "操作日期起", "accessor": "zdate_f", "width": 110},
                          {"Header": "操作日期止", "accessor": "zdate_t", "width": 110}],
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "YbzxReport_YxIndexReport",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=export_dysh_report", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data[
            "msg"], f"导出失败！response：{response.json()}"


if __name__ == '__main__':
    pytest.main()
