# -*-coding:utf-8-*-
from utils.tools import get_project_path, sep
from urllib.parse import urlencode
import allure
import pytest
import json


user = "testuser2"


@allure.feature("医学拆包")
@pytest.mark.usefixtures("res")
class TestYxUnpack:
    list_query_package_info_unpack = [
        {"expressNumber": "SF20240911172659"},
        {"zsjdid": "INSP240000115520"},
        {"arrvSeries": "SZ2409110006"}
    ]

    @allure.story("医学拆包")
    @allure.title("包裹信息查询")
    @pytest.mark.parametrize("params", list_query_package_info_unpack)
    @allure.severity(allure.severity_level.BLOCKER)
    def test_query_package_info_unpack(self, res, token, params):
        allure.step("查询参数:{}" + json.dumps(params))
        path = "/ybzx/webintf.do"
        param = {"method": "query_packageinfo_by_expressnumber_unpack"}
        data = {
            "token": token(user)["token"],
            "menuId": "YxUnpack",
            "zsjd_type": "YX"
        }
        data.update(params)
        print("请求参数:", data)
        resp = res.post_request(url=path, params=param, data=urlencode(data))
        print("响应结果:", resp.json())
        assert resp.json()["code"] == "200"
        assert len(resp.json()["data"]) == 1

    @allure.story("医学拆包")
    @allure.title("包裹样本信息查询")
    @pytest.mark.parametrize("params", list_query_package_info_unpack)
    @allure.severity(allure.severity_level.BLOCKER)
    def test_query_package_unpack(self, res, token, params):
        allure.step("查询参数:" + json.dumps(params))
        path = "/ybzx/webintf.do"
        param = {"method": "query_allsample_by_expressnumber_unpack"}
        data = {
            "token": token(user)["token"],
            "menuId": "YxUnpack",
            "zsjd_type": "YX",
            "pageNumber": 1,
            "pageSize": 50
        }
        data.update(params)
        print("请求参数:", data)
        resp = res.post_request(url=path, params=param, data=urlencode(data))
        print("响应结果:", resp.json())
        assert resp.json()["code"] == "200"
        assert resp.json()["msg"] == "success"
        assert resp.json()["total"] > 0

    @allure.story("医学拆包")
    @allure.title("拆包")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_unpack(self, res, token):
        allure.step("查询包裹")
        path = "/ybzx/webintf.do"
        query_param = {"method": "query_packageinfo_by_expressnumber_unpack"}
        query_data = {
            "expressNumber": "SF20240911172659",
            "token": token(user)["token"],
            "menuId": "YxUnpack",
            "zsjd_type": "YX"
        }
        query_resp = res.post_request(url=path, params=query_param, data=urlencode(query_data))
        allure.step("拆包")
        package_info = query_resp.json()["data"][0]
        unpakc_param = {"method": "save_package_info"}

        unpakc_data = {
            "datas": {"pkid": package_info["pkid"],
                      "sum_zcatalo": package_info["sum_zcatalo"],
                      "sum_zsjdid": package_info["sum_zsjdid"],
                      "sum_wlxp": package_info["sum_wlxp"],
                      "znote": package_info["znote"],
                      "zsfyc": package_info["zsfyc"],
                      "zycdm": package_info["zycdm"],
                      "zystj": package_info["zystj"],
                      "zsendarea": package_info["sendArea"],
                      "zsendname": package_info["sendName"],
                      "zsendphonenum": package_info["zsendphonenum"],
                      "zsendhospital": package_info["zsendhospital"]},
            "token": token(user)["token"],
            "menuId": "YxUnpack",
            "zsjd_type": "YX"
        }
        print("请求参数:", unpakc_data)
        unpakc_resp = res.post_request(url=path, params=unpakc_param, data=urlencode(unpakc_data))
        print("响应结果:", unpakc_resp.json())
        assert unpakc_resp.json()["code"] == "200"
        assert "拆包成功" in unpakc_resp.json()["msg"]

    @allure.story("医学拆包")
    @allure.title("批量拆包")
    @pytest.mark.usefixtures("send_file")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_bacth_unpack_exists(self, send_file, token):
        path = "/ybzx/excelFile/import.do"
        param = {"methodName": "importUnpackExcelData",
                 "token": token(user)["token"]}
        project_path = get_project_path()
        filepath = sep([project_path, "testcase/samplecenter/samplecenter/批量拆包_存在.xlsx"])
        print("请求参数:", filepath)
        resp = send_file.post_request(url=path, params=param, file_path=filepath)
        print("响应结果:", resp.json())
        assert resp.json()["code"] == "200"
        assert resp.json()["msg"] == "success"

    @allure.story("医学拆包")
    @allure.title("批量拆包(包裹不存在)")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_bacth_unpack_not_exists(self, send_file, token):
        path = "/ybzx/excelFile/import.do"
        param = {"methodName": "importUnpackExcelData",
                 "token": token(user)["token"]}
        project_path = get_project_path()
        filepath = sep([project_path, "testcase/samplecenter/samplecenter/批量拆包_不存在.xlsx"])
        resp = send_file.post_request(url=path, params=param, file_path=filepath)
        print("响应结果:", resp.json())
        assert resp.json()["code"] == "400"
        assert "不存在" in resp.json()["msg"]


if __name__ == '__main__':
    pytest.main()