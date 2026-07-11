# -*-coding:utf-8-*-
from data_generate.samplecenter.datagenerate import DataGenerate
from urllib.parse import urlencode
import datetime
import pytest
import allure
import json

user = "testuser2"


@allure.feature("包裹接收")
@pytest.mark.usefixtures("res", "token")
class TestPackageReceive:
    list_query_received_package = [
        {"expressNumber": "SF20240914173142"},
        {"arrvSeries": "SZ2409140018"},
        {"sendArea": "广东省深圳市盐田区盐田路605号"},
        {"sendHospital": "测试单位"},
        {"sendName": "测试用户"},
        {"sendPhoneNum": "13530658357"},
        {"sfycb": "no"},
        {"sfycb": "yes"},
        {"zsfzc": "X"},
        {"packageExterior": "0"},
        {"receiver": "autotest2"},
        {"signDate": "20240914"},
        {"signDateend": "20240914"},
    ]
    list_query_in_transit_package = [
        {"expressNumber": "SF20240926105907"},
        {"sendArea": "广东省深圳市盐田区盐田路605号"},
        {"sendHospital": "测试单位"},
        {"sendName": "测试用户"},
        {"zjsrq": "20220926"},
        {"yjddsj": "20220926"},
        {"yjddsjend": "20240911"},
        {"zjsrqend": "20240911"}
    ]

    @allure.story("包裹接收")
    @allure.title("包裹签收")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_package_receive(self, res, token):
        allure.step("查询待接收包裹")
        dg = DataGenerate(token)
        dg.sumbit_sample()
        express_number = dg.send_package()
        path = "/ybzx/webintf.do"
        param = {"method": "query_express_package_info"}
        data = {
            "expressNumber": express_number,
            "bgjs": "X",
            "token": token(user)["token"],
            "menuId": "PackageRecive",
            "zsjd_type": "YX"
        }
        resp = res.post_request(url=path, params=param, data=urlencode(data)).json()
        allure.step("包裹签收")
        receive_param = {"method": "update_express_package_info"}
        receive_data = {
            "datas": resp["data"],
            "token": token(user)["token"],
            "menuId": "PackageRecive",
            "zsjd_type": "YX"
        }
        print("请求参数:", receive_data)
        receive_resp = res.post_request(url=path, params=receive_param, data=urlencode(receive_data))
        print("响应结果:", receive_resp.json())
        assert receive_resp.json()["code"] == "200"
        assert len(receive_resp.json()["data"]) > 0

    @allure.story("包裹补录")
    @allure.title("包裹补录")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_package_record(self, res, token):
        allure.step("查询包裹")
        express_number = datetime.datetime.now().strftime("%Y%m%d")
        path = "/ybzx/webintf.do"
        param = {"method": "query_express_package_info"}
        data = {
            "expressNumber": express_number,
            "bgjs": "X",
            "token": token(user)["token"],
            "menuId": "PackageRecive",
            "zsjd_type": "YX"
        }
        res.post_request(url=path, params=param, data=urlencode(data))
        allure.step("包裹补录")
        record_param = {"method": "save_express_package_info"}
        record_data = {
            "expressInfo": [{"expressNumber": express_number,
                             "_id": 1,
                             "tsbjbtn": None,
                             "__kdgst": "顺丰速运",
                             "kdgst": "顺丰速运",
                             "__isUrgent": "",
                             "isUrgent": "",
                             "__sendHospital": "测试单位",
                             "sendHospital": "测试单位",
                             "__sendArea": "测试地址",
                             "sendArea": "测试地址",
                             "__sendName": "测试员",
                             "sendName": "测试员",
                             "__sendPhoneNum": "18988889999",
                             "sendPhoneNum": "18988889999",
                             "zwerks": token(user)["userWerks"]}],
            "token": token(user)["token"],
            "menuId": "PackageRecive",
            "zsjd_type": "YX"
        }
        print("请求参数:", record_data)
        record_resp = res.post_request(url=path, params=record_param, data=urlencode(record_data))
        print("响应结果:", record_resp.json())
        assert record_resp.json()["code"] == "200"
        assert record_resp.json()["msg"] == "操作成功"

    @allure.story("已接收")
    @allure.title("根据不同条件查询已接收包裹")
    @pytest.mark.parametrize("param", list_query_received_package)
    @allure.severity(allure.severity_level.BLOCKER)
    def test_query_received_package(self, res, token, param):
        allure.step("查询参数为:" + json.dumps(param))
        query_path = "/ybzx/webintf.do"
        query_param = {"method": "quer_recived_package"}
        query_data = {
            "token": token(user)["token"],
            "menuId": "PackageRecive",
            "zsjd_type": "YX",
            "pageNumber": 1,
            "pageSize": 50
        }
        query_data.update(param)
        print("请求参数:", query_data)
        resp = res.post_request(url=query_path, params=query_param, data=urlencode(query_data))
        print("响应结果:", resp.json())
        assert resp.json()["code"] == "200"
        assert resp.json()["msg"] == "success"
        assert resp.json()["total"] > 0

    @allure.story("已接收")
    @allure.title("导出已接收包裹")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_export_received_package(self, res, token):
        path = "/ybzx/exportSampleDetail.do"
        data = {
            "token": token(user)["token"],
            "menuId": "PackageRecive",
            "zsjd_type": "YX",
            "datas": [
                ["序号", "是否加急", "到达序列号", "快递单号", "快递公司", "签收时间", "寄件地址", "寄件单位", "寄件人", "寄件人电话", "寄件日期", "签收人", "包裹外观",
                 "异常备注", "是否暂存", "暂存位置", "拆包人", "拆包日期", "实收送检单数", "实收送样本数", "无单样本数", "到样样本数", "备注"],
                [1, "否", "SZ2409040001", "DD202409040003", "顺丰速运", "2024-09-04 10:19:32", "", "", "", "",
                 "20240904", "huxiaofeng_A020", "", "", "", "", "", "", "", "", "0 ", "0 ", ""]]
        }
        print("请求参数:", data)
        resp = res.post_request(url=path, data=urlencode(data))
        print("响应结果:", resp.json())
        assert resp.json()["status"] == "success"
        assert "详情.xlsx" in resp.json()["filePath"]

    @allure.story("预计在途")
    @allure.title("根据不同条件查询在途包裹")
    @pytest.mark.parametrize("param", list_query_in_transit_package)
    @allure.severity(allure.severity_level.BLOCKER)
    def test_query_in_transit_package(self, res, token, param):
        allure.step("查询参数为:" + json.dumps(param))
        query_path = "/ybzx/webintf.do"
        query_param = {"method": "quer_on_the_way_package"}
        query_data = {
            "token": token(user)["token"],
            "menuId": "PackageRecive",
            "zsjd_type": "YX",
            "pageNumber": 1,
            "pageSize": 50
        }
        query_data.update(param)
        print("请求参数:", query_data)
        resp = res.post_request(url=query_path, params=query_param, data=urlencode(query_data))
        print("响应结果:", resp.json())
        assert resp.json()["code"] == "200"
        assert resp.json()["msg"] == "success"
        assert resp.json()["total"] > 0


if __name__ == '__main__':
    pytest.main()
