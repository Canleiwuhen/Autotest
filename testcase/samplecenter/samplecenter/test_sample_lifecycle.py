import copy
import json
from urllib.parse import urlencode

import allure
import pytest
import requests

from data_generate.samplecenter.datagenerate import DataGenerate
from testcase.samplecenter.samplecenter.sample_lifecycle_data import DataList
from utils.request import Requests


@allure.feature("样本生命周期")
class TestSampleLifecycle:
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询所有样本")
    @allure.title("查询所有样本：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_samples_data_list)
    def test_query_all_samples(self, res, token, data):
        # 获取测试参数和token
        query_data = data["data"]
        query_token = token("testuser1")["token"]
        query_data["token"] = query_token
        response = res.post_request("/ybzx/webintf.do?method=query_all_samples", data=urlencode(query_data))
        response_json = response.json()
        assert response.status_code == 200 and response_json["code"] == "200"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("导出全部样本")
    @allure.title("导出全部样本:导出根据筛选条件过滤后的全部样本信息")
    def test_export_all_sample_info(self, res, token):
        # 需要导出的列,即Excel的表头
        excel_header = [{"Header": "序号", "accessor": "key", "width": 50},
                        {"Header": "样例", "accessor": "zsample", "width": 130},
                        {"Header": "样本编号", "accessor": "zcatalo", "width": 130},
                        {"Header": "自动化编码", "accessor": "zqrcode", "width": 130},
                        {"Header": "样例状态", "accessor": "zylzt", "width": 80},
                        {"Header": "产品编码", "accessor": "matnr", "width": 100},
                        {"Header": "产品描述", "accessor": "maktx", "width": 350},
                        {"Header": "原样本编号", "accessor": "zoldsamplenum", "width": 130},
                        {"Header": "样本类型", "accessor": "zyblx", "width": 150},
                        {"Header": "设备来源", "accessor": "ybsource", "width": 150},
                        {"Header": "模板标识", "accessor": "ztempbs", "width": 150},
                        {"Header": "采血管类型", "accessor": "ztubetype", "width": 130},
                        {"Header": "采样日期", "accessor": "zsampling_datum", "width": 100},
                        {"Header": "定位信息", "accessor": "zdwxx", "width": 100},
                        {"Header": "到样定位时间", "accessor": "zreceiveddate", "width": 150},
                        {"Header": "预计排产日期", "accessor": "zyjpcdate", "width": 100},
                        {"Header": "到样接收人", "accessor": "zdyr", "width": 130},
                        {"Header": "孔板", "accessor": "zplate_num", "width": 150},
                        {"Header": "孔位", "accessor": "zpoint", "width": 60},
                        {"Header": "冰箱/冷库（冰箱/冷库-层-架子-抽屉）", "accessor": "zfrgid", "width": 300},
                        {"Header": "箱子编号", "accessor": "zbox", "width": 80},
                        {"Header": "库存状态", "accessor": "zkc_status", "width": 100},
                        {"Header": "是否销毁返样", "accessor": "zsfxhfy", "width": 150},
                        {"Header": "销毁人", "accessor": "zxhr", "width": 150},
                        {"Header": "销毁时间", "accessor": "zxhdate", "width": 150},
                        {"Header": "冻结出库", "accessor": "pausestatus", "width": 150},
                        {"Header": "停测", "accessor": "stopTestStatus", "width": 150},
                        {"Header": "物流信息", "accessor": "zexpressnumber", "width": 150},
                        {"Header": "到达确认信息", "accessor": "zarrvseries", "width": 150},
                        {"Header": "包裹接收时间", "accessor": "zsigndate", "width": 150},
                        {"Header": "出入库日志", "accessor": "zcrkrz", "width": 100},
                        {"Header": "审核状态", "accessor": "chkstatus", "width": 100},
                        {"Header": "审核前置条件", "accessor": "chkcondition", "width": 130},
                        {"Header": "档案盒号", "accessor": "zrecordno", "width": 150},
                        {"Header": "送检单", "accessor": "zsjdid", "width": 210},
                        {"Header": "客户编码", "accessor": "kunnr", "width": 100},
                        {"Header": "客户名称", "accessor": "name1", "width": 200, "more": True},
                        {"Header": "产品组合描述", "accessor": "zmatnr_ty_text", "width": 230},
                        {"Header": "项目地区", "accessor": "projadesc", "width": 150},
                        {"Header": "项目名称", "accessor": "zxmmc", "width": 230},
                        {"Header": "样本来源省份", "accessor": "bezei", "width": 130},
                        {"Header": "名称", "accessor": "zsamplename1", "width": 80},
                        {"Header": "混样标识", "accessor": "flag_hy", "width": 80}]
        data = {"excelHead": excel_header,
                "task": {"zyjpcdate": "", "zreceiveddate": "20240901", "zsampling_datum": "",
                         "zreceiveddateend": "20240908", "zsjdType": "YX", "zsfxhfy": "否"},
                "pageNumber": 1,
                "pageSize": 200000,
                "token": token("testuser1")["token"],
                "menuId": "sampleCycle",
                "zsjd_type": "YX"
                }
        response = res.post_request("/ybzx/webintf.do?method=export_all_samplecycle", data=urlencode(data))
        response_json = response.json()
        print(response_json)
        assert response.status_code == 200 and response_json["code"] == "200" and response_json["msg"].endswith(
            "zip"), f"导出异常：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("导出本页样本")
    @allure.title("导出本页样本：导出根据筛选条件过滤后的当前页样本信息")
    def test_export_current_page_sample_info(self, res, token):
        # 当前页所有行记录,为测试方便，仅导出两行记录
        datas = [["序号", "样例", "样本编号", "自动化编码", "样例状态", "产品编码", "产品描述", "原样本编号", "样本类型", "设备来源", "模板标识", "采血管类型", "采样日期",
                  "定位信息", "到样定位时间", "预计排产日期", "到样接收人", "孔板", "孔位", "冰箱/冷库（冰箱/冷库-层-架子-抽屉）", "箱子编号", "库存状态", "是否销毁返样",
                  "销毁人", "销毁时间", "冻结出库", "停测", "物流信息", "到达确认信息", "包裹接收时间", "审核状态", "审核前置条件", "档案盒号", "送检单", "客户编码",
                  "客户名称", "产品组合描述", "项目地区", "项目名称", "样本来源省份", "名称", "混样标识"],
                 [51, "24S06983009", "24S06983009", "", "", "DX1515", "临床全外显子组检测-Trio", "", "羊水", "", "", "",
                  "20240801", "已定位", "2024-08-29 21:01:42", "20240829", "huxiaofeng_A020", "24SZYCQX02-0296", "B03", "",
                  "", "入库定位", "", "", "", "未冻结", "未停测", "TEST20220", "SZ2408290002", "2024-08-29 17:53:42", "已审核",
                  "信息审核已完成", "123", "INSP240000115201", "1000023786", "深圳市宝安区妇幼保健院", "临床全外", "", "", "", "***之胎", ""],
                 [52, "24B08289020", "24B08289020", "", "", "DX1515", "临床全外显子组检测-Trio", "", "全血", "", "", "",
                  "20240801", "已定位", "2024-08-29 21:01:42", "20240829", "huxiaofeng_A020", "24SZYCQX02-0296", "A11", "",
                  "", "入库定位", "", "", "", "未冻结", "未停测", "TEST20220", "SZ2408290002", "2024-08-29 17:53:42", "已审核",
                  "信息审核已完成", "123", "INSP240000115201", "1000023786", "深圳市宝安区妇幼保健院", "临床全外", "", "", "", "***", ""]]
        data = {"datas": datas,
                "token": token("testuser1")["token"],
                "menuId": "sampleCycle",
                "zsjd_type": "YX"
                }
        response = res.post_request("/ybzx/exportSampleDetail.do?", data=urlencode(data))
        response_json = response.json()
        print(response_json)
        assert response.status_code == 200 and response_json["status"] == "success" and response_json[
            "filePath"].endswith(".xlsx"), f"导出异常：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("分配档案盒号")
    @allure.title("分配档案盒号：样本未分配过档案盒号，首次分配档案盒号")
    def test_assign_archives_box_number(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample = data_gen.sumbit_sample()[0]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]['zsjdid']

        data = {"datas": [{"ZSJDID": inspection_form, "ZRECORDNO": "123"}],
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"
                }
        response = res.post_request("/ybzx/webintf.do?method=save_zrecordno", data=urlencode(data))
        response_json = response.json()
        print(response_json)
        assert response.status_code == 200 and response_json["code"] == "200" and response_json[
            "msg"] == "success", f"分配档案盒号异常：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("分配档案盒号")
    @allure.title("分配档案盒号：样本已分配过档案盒号，重复分配档案盒号")
    def test_repeat_assign_archives_box_number(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample = data_gen.sumbit_sample()[0]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]['zsjdid']

        data = {"datas": [{"ZSJDID": inspection_form, "ZRECORDNO": "123"}],
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"
                }
        for i in range(2):
            response = res.post_request("/ybzx/webintf.do?method=save_zrecordno", data=urlencode(data))
        response_json = response.json()
        print(response_json)
        assert response.status_code == 200 and response_json["code"] == "200" and response_json[
            "msg"] == "success", f"分配档案盒号异常：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("冻结出库")
    @allure.title("冻结出库：正常冻结出库")
    def test_freeze_outbound(self, res, token):
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
                    # 构造查询是否满足冻结条件接口的数据
                    query_data = {
                        "datas": [{"ZSJDID": inspection_form, "ZCATALO": sample}],
                        "action": 1,
                        "token": token,
                        "menuId": "sampleCycle",
                        "zsjd_type": "YX"
                    }
                    # 查询样本是否满足冻结条件
                    query_response_json = res.post_request("/ybzx/webintf.do?method=query_samples_matnrlist",
                                                           data=urlencode(query_data)).json()
                    if query_response_json["code"] == "200" and query_response_json["msg"] == "success":
                        product_no = query_response_json['data'][0]['matnr']
                        data = {
                            "datas": [{"ZSJDID": inspection_form, "PAUSEREASON": "autotest-冻结出库", "ACTION": 1,
                                       "ZCATALO": sample,
                                       "MATNR": product_no}],
                            "token": token,
                            "menuId": "sampleCycle",
                            "zsjd_type": "YX"
                        }
                        # 冻结出库
                        response = res.post_request("/ybzx/webintf.do?method=save_dongjie_chuku", data=urlencode(data))
                        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
                            "msg"] == "success", f"冻结出库异常：{response.json()}"
                    else:
                        print(f"查询结果异常：{query_response_json['msg']}")
                else:
                    print("医学定位异常，请检查！")
            else:
                print("拆包异常，请检查！")
        else:
            print("包裹接收异常，请检查！")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("冻结出库")
    @allure.title("冻结出库：样本状态不满足条件，冻结出库失败")
    def test_freeze_outbound_fail(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        # 构造查询是否满足冻结条件接口的数据
        query_data = {
            "datas": [{"ZSJDID": inspection_form, "ZCATALO": sample}],
            "action": 1,
            "token": token,
            "menuId": "sampleCycle",
            "zsjd_type": "YX"
        }
        # 查询样本是否满足冻结条件
        response = res.post_request("/ybzx/webintf.do?method=query_samples_matnrlist",
                                    data=urlencode(query_data))
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == f"样本{sample}当前状态不允许冻结出库!", f"冻结出库异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("取消冻结出库")
    @allure.title("取消冻结出库：正常取消冻结出库")
    def test_unfreeze_outbound(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
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
                    data = {
                        "datas": [{"ZSJDID": inspection_form, "PAUSEREASON": "autotest-冻结出库", "ACTION": 1,
                                   "ZCATALO": sample,
                                   "MATNR": product_no}],
                        "token": token,
                        "menuId": "sampleCycle",
                        "zsjd_type": "YX"
                    }
                    # 冻结出库
                    freeze_response = res.post_request("/ybzx/webintf.do?method=save_dongjie_chuku",
                                                       data=urlencode(data))
                    if freeze_response.status_code == 200 and freeze_response.json()["code"] == "200" and \
                            freeze_response.json()["msg"] == "success":
                        # 取消冻结出库
                        data["datas"][0]["ACTION"] = 2
                        data["datas"][0]["PAUSEREASON"] = "autotest-取消冻结出库"
                        unfreeze_response = res.post_request("/ybzx/webintf.do?method=save_dongjie_chuku",
                                                             data=urlencode(data))
                        assert unfreeze_response.status_code == 200 and unfreeze_response.json()["code"] == "200" and \
                               unfreeze_response.json()["msg"] == "success", f"取消冻结出库异常：{unfreeze_response.json()}"
                    else:
                        print("冻结出库异常，请检查！")
                else:
                    print("医学定位异常，请检查！")
            else:
                print("拆包异常，请检查！")
        else:
            print("包裹接收异常，请检查！")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("取消冻结出库")
    @allure.title("取消冻结出库：样本状态不满足条件，取消冻结出库失败")
    def test_unfreeze_outbound_fail(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]['zsjdid']
        # 构造查询是否满足取消冻结出库条件接口的数据
        query_data = {
            "datas": [{"ZSJDID": inspection_form, "ZCATALO": sample}],
            "action": 2,
            "token": token,
            "menuId": "sampleCycle",
            "zsjd_type": "YX"
        }
        # 查询样本是否满足取消冻结出库条件
        response = res.post_request("/ybzx/webintf.do?method=query_samples_matnrlist",
                                    data=urlencode(query_data))
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == f"样本{sample}当前状态不允许冻结出库!选中的样本均不允许取消冻结出库!", f"取消冻结出库异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询冻结日志")
    @allure.title("查询冻结日志：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_freeze_log_data_list)
    def test_query_freeze_log(self, res, token, data):
        # 获取测试参数和token
        query_data = data["data"]
        query_token = token("testuser1")["token"]
        query_data["token"] = query_token
        response = res.post_request("/ybzx/webintf.do?method=query_djck_log", data=urlencode(query_data))
        print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
            "msg"] == "success", f"查询冻结日志异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急：正常停测")
    def test_stop_testing(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
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
                    data = {
                        "datas": [
                            {"TCREASON": "autotest-停测", "ACTION": "10", "ZSAMPLE": sample, "MATNR": product_no,
                             "ZSJDID": inspection_form}],
                        "token": token,
                        "menuId": "sampleCycle",
                        "zsjd_type": "YX"}
                    # 停测
                    response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
                    assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
                        "msg"] == "success", f"停测异常：{response.json()}"
                else:
                    print(f"样本{sample}医学定位异常，请检查！")
            else:
                print(f"样本{sample}拆包异常，请检查！")
        else:
            print(f"样本{sample}包裹接收异常，请检查！")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急：样本状态不满足条件，停测失败")
    def test_stop_testing_fail(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")['token']
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        data = {
            "datas": [{"TCREASON": "autotest-停测", "ACTION": "10", "ZSAMPLE": sample, "MATNR": product_no,
                       "ZSJDID": inspection_form}],
            "token": token,
            "menuId": "sampleCycle",
            "zsjd_type": "YX"}
        # 停测
        response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == f"样例{sample}未到样，不允许停测!", f"停测异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急：正常取消停测")
    def test_cancel_stop_testing(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
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
                    data = {
                        "datas": [
                            {"TCREASON": "autotest-停测", "ACTION": "10", "ZSAMPLE": sample, "MATNR": product_no,
                             "ZSJDID": inspection_form}],
                        "token": token,
                        "menuId": "sampleCycle",
                        "zsjd_type": "YX"}
                    # 停测
                    response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
                    if response.status_code == 200 and response.json()["code"] == "200" and response.json()[
                        "msg"] == "success":
                        data = {"datas": [
                            {"TCREASON": "autotest-取消停测", "ACTION": "20", "ZSAMPLE": sample, "MATNR": product_no,
                             "ZSJDID": inspection_form}],
                            "token": token,
                            "menuId": "sampleCycle",
                            "zsjd_type": "YX"}
                        # 取消停测
                        response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
                        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
                            "msg"] == "success", f"取消停测异常：{response.json()}"
                    else:
                        print(f"样本{sample}停测异常，请检查！{response.json()}")
                else:
                    print(f"样本{sample}医学定位异常，请检查！")
            else:
                print(f"样本{sample}拆包异常，请检查！")
        else:
            print(f"样本{sample}包裹接收异常，请检查！")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急：样本状态不满足条件，取消停测失败")
    def test_cancel_stop_testing_fail(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        data = {"datas": [{"TCREASON": "autotest-取消停测", "ACTION": "20", "ZSAMPLE": sample, "MATNR": product_no,
                           "ZSJDID": inspection_form}],
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"}
        response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            'msg'] == f'样例{sample}产品{product_no}已取消停测,请勿重复操作!', f"取消停测异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急：正常加急")
    def test_urgent(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        data = data_gen.query_sample_cycle(sample)
        product_no = data[sample]["matnr"]
        inspection_form = data[sample]["zsjdid"]
        data = {"datas": [{"TCREASON": "autotest-加急", "ACTION": "30", "ZSAMPLE": sample, "MATNR": product_no,
                           "ZSJDID": inspection_form}],
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"}
        response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
            "msg"] == "success", f"加急异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急：样本已加急，加急失败")
    def test_urgent_fail(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        data = {"datas": [{"TCREASON": "autotest-加急", "ACTION": "30", "ZSAMPLE": sample, "MATNR": product_no,
                           "ZSJDID": inspection_form}],
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"}
        # 加急
        response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
        if response.status_code == 200 and response.json()["code"] == "200" and response.json()["msg"] == "success":
            # 重复加急
            response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
            assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
                "msg"] == f"样例{sample}产品{product_no}已加急,请勿重复操作!", f"加急异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急:取消加急")
    def test_cancel_urgent(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        # print(sample)
        data = {"datas": [{"TCREASON": "autotest-加急", "ACTION": "30", "ZSAMPLE": sample, "MATNR": product_no,
                           "ZSJDID": inspection_form}],
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"}
        # 加急
        response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
        if response.status_code == 200 and response.json()['code'] == "200" and response.json()[
            "msg"] == "success":
            data = {"datas": [{"TCREASON": "autotest-取消加急", "ACTION": "40", "ZSAMPLE": sample, "MATNR": product_no,
                               "ZSJDID": inspection_form}],
                    "token": token,
                    "menuId": "sampleCycle",
                    "zsjd_type": "YX"}
            # 取消加急
            response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
            assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
                "msg"] == "success", f"取消加急异常：{response.json()}"
        else:
            print(f"加急异常，异常如下：{response.json()}")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("停测与加急")
    @allure.title("停测与加急:样本状态不满足条件，取消加急失败")
    def test_cancel_urgent_fail(self, res, token):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        product_no = data_gen.query_sample_cycle(sample)[sample]["matnr"]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        # print(sample)
        data = {"datas": [{"TCREASON": "autotest-取消加急", "ACTION": "40", "ZSAMPLE": sample, "MATNR": product_no,
                           "ZSJDID": inspection_form}],
                "token": token,
                "menuId": "sampleCycle",
                "zsjd_type": "YX"}
        # 取消加急
        response = res.post_request("/ybzx/webintf.do?method=save_tc_matnr", data=urlencode(data))
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == f"样例{sample}产品{product_no}未加急,不允许取消加急!", f"取消加急异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询停测与加急日志")
    @allure.title("查询停测与加急日志：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_stop_testing_and_urgent_log_data_list)
    def test_query_stop_testing_and_urgent_log(self, res, token, data):
        # 获取测试参数和token
        query_data = data["data"]
        query_token = token("testuser1")["token"]
        query_data["token"] = query_token
        response = res.post_request("/ybzx/webintf.do?method=query_tc_log", data=urlencode(query_data))
        print(response.json())
        assert response.status_code == 200 and response.json()[
            "code"] == "200" and response.json()[
                   "msg"] == "success", f"查询停测与加急日志异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("转产")
    @allure.title("正常转产：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.production_conversion_success_data_list)
    def test_production_conversion(self, res, token, data):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        inspection_form = data_gen.query_sample_cycle(sample)[sample]["zsjdid"]
        # print(sample)
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
                    # 获取测试参数和token
                    req_data = data["data"]
                    req_data["token"] = token
                    for i in range(len(req_data["datas"])):
                        if "zcatalo" in req_data["datas"][i]:
                            req_data["datas"][i]["zcatalo"] = sample
                        req_data["datas"][i]["zsample"] = sample
                        if "zsjdid" in req_data["datas"][i]:
                            req_data["datas"][i]["zsjdid"] = inspection_form
                    # 转产
                    response = res.post_request("/ybzx/webintf.do?method=save_transfer_info", data=urlencode(req_data))
                    assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
                        "msg"] == "success", f"转产异常：{response.json()}"
                else:
                    print(f"样本{sample}医学定位异常，请检查！")
            else:
                print(f"样本{sample}拆包异常，请检查！")
        else:
            print(f"样本{sample}包裹接收异常，请检查！")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("转产")
    @allure.title("异常转产：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.production_conversion_fail_data_list)
    def test_production_conversion_fail(self, res, token, data):
        # 获取token保存在变量中，方便造数据时使用
        token = token("testuser1")["token"]
        # 引用造数据工具，创建送检单并得到样本编号和送检单号
        data_gen = DataGenerate(token=token)
        sample_list = data_gen.sumbit_sample()
        sample = sample_list[0]
        print(sample)
        req_data = data["data"]
        expected_results = data["expected_results"]
        if expected_results["msg"] == "样本xxx未到样,不能转产!":
            expected_results["msg"] = f"样本{sample}未到样,不能转产!"
        req_data["token"] = token
        req_data["datas"][0]["zcatalo"] = sample
        req_data["datas"][0]["zsample"] = sample
        # 转产
        response = res.post_request("/ybzx/webintf.do?method=save_transfer_info", data=urlencode(req_data))
        assert response.status_code == 200 and response.json()["code"] == expected_results["code"] and response.json()[
            "msg"] == expected_results["msg"], f"转产异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询转产记录")
    @allure.title("查询转产记录：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.production_conversion_records_data_list)
    def test_query_production_conversion_records(self, res, token, data):
        # 获取测试参数和token
        query_data = data["data"]
        query_token = token("testuser1")["token"]
        query_data["token"] = query_token
        response = res.post_request("/ybzx/webintf.do?method=query_transfer_log", data=urlencode(query_data))
        print(response.json())
        assert response.status_code == 200 and response.json()[
            "code"] == "200" and response.json()[
                   "msg"] == "success", f"查询转产记录异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询物流信息")
    @allure.title("查询物流信息")
    def test_query_logistics_info(self, res, token):
        # 获取测试参数和token
        query_data = {
            "datas": [{"zcatalo": "24X091800060", "werks_old": "A020"}],
            "token": token("testuser1")["token"],
            "menuId": "sampleCycle",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/webintf.do?method=query_transfer_logistics_log", data=urlencode(query_data))
        print(response.json())
        assert response.status_code == 200 and response.json()[
            "code"] == "200" and response.json()[
                   "msg"] == "success", f"查询物流信息异常：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询样例产品信息")
    @allure.title("查询样例产品信息：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.sample_product_info_data_list)
    def test_sample_product_info(self, res, token, data):
        # 获取测试参数和token
        query_data = data["data"]
        query_token = token("testuser1")["token"]
        query_data["token"] = query_token
        response = res.post_request("/ybzx/webintf.do?method=query_sample_product_info", data=urlencode(query_data))
        print(response.json())
        assert response.status_code == 200 and response.json()[
            "code"] == "200" and response.json()[
                   "msg"] == "success", f"查询样例产品信息失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("导出样例产品信息")
    @allure.title("导出查询出的样例产品信息")
    def test_export_sample_product_info(self, res, token):
        # 获取测试参数和token
        query_data = {
            "task": {"zybzx": "X", "zcjdat": "20240901", "zreceiveddate1": "20240901", "zsample": "", "matnr": "DX1616",
                     "zcjdatend": "20240930", "zreceiveddate1end": "20240930"},
            "token": None,
            "pageNumber": 1,
            "pageSize": 50,
            "menuId": "sampleCycle",
            "zsjd_type": "YX"
        }
        query_token = token("testuser1")["token"]
        query_data["token"] = query_token
        # 先查出9月份到样定位且转产的产品DX1616的样例产品信息记录，提供给下面的导出接口使用
        response = res.post_request("/ybzx/webintf.do?method=query_sample_product_info", data=urlencode(query_data))
        # print(response.json())
        if response.status_code == 200 and response.json()["code"] == "200" and response.json()["msg"] == "success":
            res_data = response.json()["data"]
            task = []
            for i in range(len(res_data)):
                tmp = {
                    "maktx": res_data[i]["maktx"],
                    "matnr": res_data[i]["matnr"],
                    "received_date": res_data[i]["received_date"],
                    "received_uname": res_data[i]["received_uname"],
                    "sjwerks": res_data[i]["sjwerks"],
                    "zsample": res_data[i]["zsample"],
                    "zsjdid": res_data[i]["zsjdid"],
                    "_id": i + 1,
                    "_key": i + 1,
                    "_zcrkrz":
                        {"key": "", "ref": "", "_owner": "", "props": {
                            "children": "查看日志",
                            "className": "cycle-btn-crk",
                            "ghost": False,
                            "loading": False,
                            "prefixCls": "ant-btn",
                            "style": {"width": "88%"}}
                         }
                }
                task.append(copy.deepcopy(tmp))
            data = {
                "task": task,
                "token": query_token
            }
            # 导出查询出的样例产品信息记录，这里要注意下，该接口支持的文本类型为json，与其他接口不同（form-data），需另外实例化Requests对象
            # res2 = Requests(configname="samplecenter_config.yaml", baseurl="test_url", headers={'Content-Type': 'application/json'})
            # response = res2.post_request("/ybzx/exportSampleProductInfoData.do", json=json.dumps(data))
            url = "https://sample-test.bgi.com/ybzx/exportSampleProductInfoData.do"
            # 公共组件中的requests实例对象有问题，暂时先使用原生的requests实例对象的requests方法请求接口
            response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, json=data)
            assert response.status_code == 200

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询产品信息")
    @allure.title("查询所有产品信息")
    def test_query_all_products(self, res, token):
        token = token("testuser1")["token"]
        params = '&token=' + token + '&menuId=sampleCycle&zsjd_type=YX'
        response = res.get_request("/ybzx/webintf.do?method=query_allcp_options", params=params)
        response_json = response.json()
        assert response.status_code == 200 and response_json["code"] == "200" and response_json[
            "msg"] == "success", f"查询产品信息异常：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询客户信息")
    @allure.title("查询所有客户信息")
    def test_query_all_customers(self, res, token):
        token = token("testuser1")["token"]
        params = '&token=' + token + '&menuId=sampleCycle&zsjd_type=YX'
        response = res.get_request("/ybzx/webintf.do?method=query_sjdw_options", params=params)
        response_json = response.json()
        assert response.status_code == 200 and response_json["code"] == "200" and response_json[
            "msg"] == "success", f"查询客户信息异常：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询项目地区")
    @allure.title("查询所有项目地区")
    def test_query_all_customers(self, res, token):
        token = token("testuser1")["token"]
        data = {
            "token": token,
            "menuId": "sampleCycle",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/webintf.do?method=query_project_area_new", data=urlencode(data))
        response_json = response.json()
        assert response.status_code == 200 and response_json["code"] == "200" and response_json[
            "msg"] == "success", f"查询项目地区异常：{response_json}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询样本类型")
    @allure.title("查询所有样本类型")
    def test_query_all_customers(self, res, token):
        token = token("testuser1")["token"]
        data = {
            "token": token,
            "menuId": "sampleCycle",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/webintf.do?method=query_zsamplelx_datas", data=urlencode(data))
        response_json = response.json()
        assert response.status_code == 200 and response_json["code"] == "200" and response_json[
            "msg"] == "success", f"查询样本类型异常：{response_json}"
