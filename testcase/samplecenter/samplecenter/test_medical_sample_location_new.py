from urllib.parse import urlencode

import allure
from data_generate.samplecenter.datagenerate import DataGenerate
from utils.logger import logger_samplecenter_dg as logger


@allure.feature("医学到样定位（新）")
class TestMedicalSampleLocationNew:
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("医学到样定位（新）")
    @allure.title("正常医学到样定位")
    def test_medical_sample_location(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        # 调用物流寄件方法对物流寄件
        express_num = data_gen.send_package(sample)
        # 调用包裹接收方法对包裹签收
        if data_gen.receive_package(express_num):
            # 调用包裹拆包方法对包裹拆包
            if data_gen.unpack(express_num):
                # 创建容器，方便后面医学定位
                container_num, container_id = data_gen.create_container("autotest", 96)
                # 调用医学定位方法进行医学定位
                assert data_gen.locate_position(sample_list, container_num, container_id) is True, f"医学定位失败!"
            else:
                logger.error("包裹拆包异常，请检查！")
        else:
            logger.error("包裹接收异常，请检查！")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("医学到样定位（新）")
    @allure.title("正常新增容器")
    def test_add_container(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        result = data_gen.create_container("create_container")
        assert result is not None, "新增容器失败！"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("医学到样定位（新）")
    @allure.title("标记异常")
    def test_mark_exception(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        # 调用物流寄件方法对物流寄件
        express_num = data_gen.send_package(sample)
        # 调用包裹接收方法对包裹签收
        if data_gen.receive_package(express_num):
            # 调用包裹拆包方法对包裹拆包
            if data_gen.unpack(express_num):
                # 创建容器，方便后面医学定位
                container_num, container_id = data_gen.create_container("autotest", 96)
                # 调用医学定位方法进行医学定位
                if data_gen.locate_position(sample_list, container_num, container_id):
                    # 构造异常邮件查询的请求参数，调用异常邮件查询接口查询异常邮件
                    query_data = {
                        "zcatalo": sample,
                        "token": token
                    }
                    query_response = res.post_request("/ybzx/webintf.do?method=query_yc_email",
                                                      data=urlencode(query_data))
                    assert query_response.status_code == 200 and query_response.json()["code"] == "200" and \
                           query_response.json()["msg"] == "success", f"查询异常邮件异常：{query_response.json()}"
                    # 构造标记异常的请求参数
                    data = {
                        "datas": {"zsjdid": inspection_form, "zcatalo": sample,
                                  "zexpressnumber": express_num, "zenote": "autotest-save-exception", "qdclr": "",
                                  "zycdmse": "se004", "zycdm": "se004", "zefilepath": "", "zycdmse_txt": "样本量不足",
                                  "zycdmie_txt": "", "zsjd_type": "YX", "znum": "1", "zsfyc": "X", "zsign": "X",
                                  "freezeCheck": "X", "testingCheck": "", "zyjlx": "01", "zsjemail": ""},
                        "token": token,
                        "menuId": "sampleCycle",
                        "zsjd_type": "YX"
                    }
                    # 标记异常
                    response = res.post_request("/ybzx/webintf.do?method=save_sample_exception", data=urlencode(data))
                    assert response.status_code == 200 and response.json()["code"] == "200" and "样本异常保存成功" in \
                           response.json()["msg"], f"样本标记异常失败：{response.json()}"
                else:
                    logger.error("医学定位异常，请检查！")
            else:
                logger.error("拆包异常，请检查！")
        else:
            logger.error("包裹接收异常，请检查！")
