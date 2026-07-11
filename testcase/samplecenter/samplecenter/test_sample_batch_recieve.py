# -*-coding:utf-8-*-
import json

from data_generate.samplecenter.datagenerate import DataGenerate
from urllib.parse import urlencode
import pytest
import allure


ContainerClass = {
    "AA00": "CQ20C",
    "A020": "SZBY",
    "A230": "DCH",
    "A440": "BLOOD",
    "A080": "BAG1"
}

user = "testuser2"


@allure.feature("样本批量接收")
@pytest.mark.usefixtures("res", "token")
class TestSampleBatchReceive:
    list_sample_batch_receive = [
        ["通过物流单号批量接收", {"zexpressnumber": "091102"}, {"code": "200", "msg": "success"}],
        ["通过物流单号批量接收物流单号不存在", {"zexpressnumber": "091102bucunzai"}, {"code": "400", "msg": "不存在"}],
        ["通过到达序列号批量接收", {"zarrvseries": "SZ2409110003"}, {"code": "200", "msg": "success"}],
        ["通过到达序列号批量接收序列号不存在", {"zarrvseries": "SZ2409110003bucunzai"}, {"code": "400", "msg": "不存在"}]
    ]

    @allure.story("样本批量接收")
    @allure.title("样本批量接收")
    @pytest.mark.parametrize("param", list_sample_batch_receive)
    @allure.severity(allure.severity_level.BLOCKER)
    def test_sample_batch_receive(self, res, token, param):
        allure.step(param[0])
        dg = DataGenerate(token(user)["token"])
        dg.sumbit_sample()
        if param[0] == "通过物流单号批量接收":
            param[1]["zexpressnumber"] = dg.send_package()
            dg.receive_package(dg.expressnum)
            dg.unpack()
        elif param[0] == "通过到达序列号批量接收":
            dg.send_package()
            param[1]["zarrvseries"] = dg.receive_package(dg.expressnum)["arrvSeries"]
            dg.unpack()
        batch_receive_path = "/ybzx/webintf.do"
        batch_receive_param = {"method": "save_xg_sample"}
        headInfoDetail = {"zcontainer_type": "01",  # 容器类型 收纳盒
                              "zrqlx": "SZBY",  # 容器小类 SZ-病原
                              "c_temperature": "-4℃",  # 温度
                              "zplate_x": 12,  # 排版X
                              "zplate_y": 8,  # 排版Y
                              "flag_rq": "NEW",
                              "zzkpyls": "",
                              "zrqqz": ""}
        headInfoDetail.update(param[1])
        batch_receive_data = {"zcataloInfo": [
            {"zcatalo": dg.sample[0]}
        ],
                "headInfo": [ headInfoDetail ],
                "token": token(user)["token"],
                "menuId": "XgBatchSampleConfirm",
                "zsjd_type": "YX"
                }
        if token(user)["userWerks"] in ContainerClass.keys():
            headInfoDetail["zrqlx"] = ContainerClass[token(user)["userWerks"]]
        else:
            raise Exception("当前片区未配置对应的容器小类")
        print("请求参数:", batch_receive_data)
        batch_receive_resp = res.post_request(url=batch_receive_path, params=batch_receive_param, data=urlencode(batch_receive_data))
        print("响应结果:", batch_receive_resp.json())
        assert batch_receive_resp.json()["code"] == param[2]["code"]
        assert param[2]["msg"] in batch_receive_resp.json()["msg"]


if __name__ == '__main__':
    pytest.main()