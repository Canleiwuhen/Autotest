import pytest
import allure
from urllib.parse import urlencode
from utils.tools import replace_none


@allure.feature("医学信息审核")
@pytest.mark.usefixtures("res")
class TestMedicalInfoAudit:
    query_unaudited_sample_data_list = [
        {
            "case_name": "输入样例编号+样本编号+审核状态",
            "data": {
                "task": {"zybzx": "X", "zsample": "24X090200001", "zcatalo": "24X090200001", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入样本编号+到样人+审核状态",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "24X090200001", "zsampling_per": "lupengtao-sz",
                         "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入到样人+送检单号+审核状态",
            "data": {
                "task": {"zybzx": "X", "zsjdid": "INSP240000115271", "zsampling_per": "lupengtao-sz",
                         "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入送检单号+审核状态+样本是否异常",
            "data": {
                "task": {"zybzx": "X", "zsjdid": "INSP240000115271", "chkstatus": "wait", "zybyc": "0"}
            }
        },
        {
            "case_name": "输入审核状态+样本是否异常+到样日期",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "20240904", "zreceiveddateend": "20240905",
                         "chkstatus": "wait",
                         "zybyc": "0"}
            }
        },
        {
            "case_name": "输入审核状态+产品类+产品",
            "data": {
                "task": {"zybzx": "X", "zmatnr_ty": "T040", "matnr": "DX1616", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+产品+送检单类型",
            "data": {
                "task": {"zybzx": "X", "zsjdlx": "全外", "matnr": "DX1616", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+送检单类型+送检单位",
            "data": {
                "task": {"zybzx": "X", "zsjdlx": "全外", "kunnr": "1000000004", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+送检单位+样本类型",
            "data": {
                "task": {"zybzx": "X", "kunnr": "1000000004", "zyblx": "S052", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+样本类型+项目名称",
            "data": {
                "task": {"zybzx": "X", "zxmbh": "P17Z11900N0426", "zyblx": "S051", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+项目名称+来源",
            "data": {
                "task": {"zybzx": "X", "zxmbh": "P17Z11900N0426", "zdatasource": "java_null", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+来源+存疑说明",
            "data": {
                "task": {"zybzx": "X", "zdatasource": "bisp_hpv", "zsfcy": "-", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+存疑说明+采样日期",
            "data": {
                "task": {"zybzx": "X", "zsfcy": "0", "zsampling_datum": "20240904",
                         "zsampling_datumend": "20240904",
                         "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+采样日期+录单人",
            "data": {
                "task": {"zybzx": "X", "zsampling_datum": "20240904", "zsampling_datumend": "20240904",
                         "zcreator": "guozhitao", "chkstatus": "wait"}
            }
        },
        {
            "case_name": "输入审核状态+样本是否异常+到样日期，未查询到数据！",
            "data": {
                "task": {"zybzx": "X", "zybyc": "1", "chkstatus": "wait", "zreceiveddate": "20240831",
                         "zreceiveddateend": "20240906"}
            }
        },
        {
            "case_name": "输入样例编号+样本编号+到样人+送检单号+审核状态+样本是否异常+到样日期+产品类+产品+送检单类型+送检单位+样本类型+"
                         "来源+存疑说明+采样日期+录单人",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "20240901", "zsampling_datum": "20240901",
                         "zreceiveddateend": "20240907", "zsample": "24X090200001", "zcatalo": "24X090200001",
                         "zsampling_per": "lupengtao-sz", "zsjdid": "INSP240000115271", "zmatnr_ty": "T040",
                         "matnr": "DX1616", "zsjdlx": "全外", "kunnr": "1000000004", "zyblx": "S080",
                         "zdatasource": "java_null", "zsfcy": "0", "zsampling_datumend": "20240907",
                         "zcreator": "lupengtao-sz", "chkstatus": "wait", "zybyc": "0"}
            }
        }
    ]
    query_unaudited_sample_data_list_fail = [
        {
            "case_name": "输入审核状态+来源+存疑说明，没有查询到数据！",
            "data": {
                "task": {"zybzx": "X", "zdatasource": "bisp_pahys", "zsfcy": "1", "chkstatus": "wait"}
            }
        }
    ]
    query_audited_sample_data_list = [
        {
            "case_name": "输入样例编号",
            "data": {
                "task": {"zybzx": "X", "zsample": "24B09060012", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入样本编号",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "24B09060012", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入到样人",
            "data": {
                "task": {"zybzx": "X", "zsampling_per": "huxiaofeng_A020", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入送检单号",
            "data": {
                "task": {"zybzx": "X", "zsjdid": "INSP240000115454", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入审核人",
            "data": {
                "task": {"zybzx": "X", "chkper": "huxiaofeng_A020", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入审核日期",
            "data": {
                "task": {"zybzx": "X", "chkdate": "20240903", "chkdateend": "20240909", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入到样日期",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "20240903", "zreceiveddateend": "20240909",
                         "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入产品类",
            "data": {
                "task": {"zybzx": "X", "zmatnr_ty": "T040", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入产品",
            "data": {
                "task": {"zybzx": "X", "matnr": "DX1616", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入送检单类型",
            "data": {
                "task": {"zybzx": "X", "zsjdlx": "全外", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入送检单位",
            "data": {
                "task": {"zybzx": "X", "kunnr": "1000000004", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入样本类型",
            "data": {
                "task": {"zybzx": "X", "zyblx": "S051", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入项目名称",
            "data": {
                "task": {"zybzx": "X", "zxmbh": "P17Z11900N0201", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入来源",
            "data": {
                "task": {"zybzx": "X", "zdatasource": "java_null", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入存疑说明",
            "data": {
                "task": {"zybzx": "X", "zsfcy": "1", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入采样日期",
            "data": {
                "task": {"zybzx": "X", "zsampling_datum": "20240901", "zsampling_datumend": "20240907",
                         "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入录单人",
            "data": {
                "task": {"zybzx": "X", "zcreator": "guozhitao", "chkstatus": "X"}
            }
        },
        {
            "case_name": "输入样例编号+样本编号+到样人+送检单号+审核人+审核日期+到样日期+产品类+产品+送检单类型+送检单位+样本类型+来源+"
                         "存疑说明+采样日期+录单人",
            "data": {
                "task": {"zybzx": "X", "chkdate": "20240906", "zreceiveddate": "20240906",
                         "zsampling_datum": "20240906", "zreceiveddateend": "20240912", "zsample": "24X091200018",
                         "zcatalo": "24X091200018", "zsampling_per": "whxg", "zsjdid": "INSP240000115544",
                         "chkper": "whxg", "chkdateend": "20240912", "zmatnr_ty": "T050", "matnr": "DX2352",
                         "zsjdlx": "全外", "kunnr": "1000000004", "zyblx": "S051", "zdatasource": "java_null",
                         "zsfcy": "0", "zsampling_datumend": "20240912", "zcreator": "lupengtao-sz", "chkstatus": "X"}
            }
        }
    ]
    query_audited_sample_data_list_fail = [
        {
            "case_name": "输入不存在的样例编号，没有查询到数据！",
            "data": {
                "task": {"zybzx": "X", "zsample": "123456789", "chkstatus": "X"}
            }
        }
    ]

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("未审核")
    @allure.title("搜索-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_unaudited_sample_data_list)
    def test_query_unaudited_sample(self, res, token, data):
        """
        测试未审核-查询未审核的样本
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
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
            "msg"] == "success", f"查询未审核的样本失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("未审核")
    @allure.title("搜索-异常场景-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_unaudited_sample_data_list_fail)
    def test_query_unaudited_sample_fail(self, res, token, data):
        """
        测试未审核-查询未审核的样本-异常场景
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
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == "没有查询到数据！", f"查询未审核的样本-异常场景失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("已审核")
    @allure.title("搜索-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_audited_sample_data_list)
    def test_query_audited_sample(self, res, token, data):
        """
        测试已审核-查询已审核的样本
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
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
            "msg"] == "success", f"查询已审核的样本失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("已审核")
    @allure.title("搜索-异常场景_用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_audited_sample_data_list_fail)
    def test_query_audited_sample_fail(self, res, token, data):
        """
        测试已审核-查询已审核的样本-异常场景
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
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == "没有查询到数据！", f"查询已审核的样本失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("未审核")
    @allure.title("信息审核-用例名称：信息审核->审核")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 5, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_info_audit_to_audit(self, res, token, generate_steps):
        """
        测试未审核-信息审核-审核
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        sample = generate_steps[0]["sample"]  # 拿到样例编号
        # 查询待审核样本，获取样本查询结果，审核状态：未审核
        query_data = {
            "task": {"zybzx": "X", "zsample": sample[0], "chkstatus": "W", "zybyc": "0"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()["code"] == "200" and query_response.json()[
            "msg"] == "success", f"查询未审核样本失败！response：{query_response.json()}"
        # 锁定当前样本
        lock_data = {
            "datas": query_response.json()["data"],
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        lock_data["datas"][0]["chkstatus"] = "未审核"
        lock_data["datas"][0]["_key"] = 1
        lock_data["datas"][0]["_id"] = 1
        lock_response = res.post_request("/ybzx/webintf.do?method=lock_more_sjd", data=urlencode(lock_data))
        assert lock_response.status_code == 200 and lock_response.json()["code"] == "200" and lock_response.json()[
            "msg"] == "锁定成功", f"锁定样本失败！response：{lock_response.json()}"
        # 当前样本信息审核
        audit_data = lock_data
        audit_data["datas"][0]["zrecordno"] = "autotest"  # 设置档案盒号
        audit_data["datas"][0]["chkstatus"] = "锁定"
        audit_response = res.post_request("/ybzx/webintf.do?method=audit_new_more_sjd", data=urlencode(audit_data))
        assert audit_response.status_code == 200 and audit_response.json()["code"] == "200" and audit_response.json()[
            "msg"] == "审核成功", f"样本信息审核失败！response：{audit_response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("未审核")
    @allure.title("信息审核-用例名称：信息审核->存疑")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 5, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_info_audit_to_doubt(self, res, token, generate_steps):
        """
        测试未审核-信息审核-存疑
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        sample = generate_steps[0]["sample"]  # 拿到样例编号
        # 查询待审核样本，获取样本查询结果，审核状态：未审核
        query_data = {
            "task": {"zybzx": "X", "zsample": sample[0], "chkstatus": "W", "zybyc": "0"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()["code"] == "200" and query_response.json()[
            "msg"] == "success", f"查询未审核样本失败！response：{query_response.json()}"
        # 锁定当前样本
        lock_data = {
            "datas": query_response.json()["data"],
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        lock_data["datas"][0]["chkstatus"] = "未审核"
        lock_data["datas"][0]["_key"] = 1
        lock_data["datas"][0]["_id"] = 1
        lock_response = res.post_request("/ybzx/webintf.do?method=lock_more_sjd", data=urlencode(lock_data))
        assert lock_response.status_code == 200 and lock_response.json()["code"] == "200" and lock_response.json()[
            "msg"] == "锁定成功", f"锁定样本失败！response：{lock_response.json()}"
        # 查询当前样本送检单详细信息
        query_details_data = {
            "method": "query_new_xxsh_details",
            "sampleInfo": {
                "ZSJDID": query_response.json()["data"][0]["zsjdid"],
                "ZTEMPBS": query_response.json()["data"][0]["ztempbs"]
            },
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        details_response = res.get_request("/ybzx/webintf.do", params=urlencode(query_details_data))
        assert details_response.status_code == 200 and details_response.json()["code"] == "200" and \
               details_response.json()["msg"] == "success", f"查询样本送检单详细信息失败！response：{details_response.json()}"
        # 输入存疑说明和档案盒号后点击存疑
        doubt_data = {
            "sampleInfo": {
                "yl": [details_response.json()["data"][1]],
                "yb": [details_response.json()["data"][2]],
                "produc": [details_response.json()["data"][3]],
                "info": details_response.json()["data"][0],
                "sampleSite": []
            },
            "xinxi": "qwxz",
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        doubt_data["sampleInfo"]["yl"][0]["ZDETECTTYPE"] = "ZSUSPECTEDPATIENTS"
        doubt_data["sampleInfo"]["yb"][0]["ZITEMYB"] = "1"
        doubt_data["sampleInfo"]["info"]["ZCONFIRM"] = "是"
        doubt_data["sampleInfo"]["info"]["ZSFCY"] = "X"  # 是否存疑
        doubt_data["sampleInfo"]["info"]["ZCY_DES"] = "接口自动化测试"  # 存疑说明
        doubt_data["sampleInfo"]["info"]["ZRECORDNO"] = "110"  # 档案盒号
        doubt_data = replace_none(doubt_data)  # 替换data中的None为""
        doubt_response = res.post_request("/ybzx/webintf.do?method=new_doubt_sjd", data=urlencode(doubt_data))
        assert doubt_response.status_code == 200 and doubt_response.json()["code"] == "200" and \
               "保存成功" in doubt_response.json()["msg"], f"医学信息审核创建存疑失败！response：{doubt_response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("未审核")
    @allure.title("批量审核-用例名称：批量审核主流程")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 5, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_batch_audit(self, res, token, generate_steps):
        """
        测试未审核-批量审核
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        sample = generate_steps[0]["sample"]  # 拿到样例编号
        # 查询待审核样本（一个或多个），获取样本查询结果，审核状态：未审核
        query_data = {
            "task": {"zybzx": "X", "zsample": sample[0], "chkstatus": "W", "zybyc": "0"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()["code"] == "200" and query_response.json()[
            "msg"] == "success", f"查询未审核样本失败！response：{query_response.json()}"
        # 样本批量信息审核
        audit_data = {
            "datas": query_response.json()["data"],
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        for i in range(len(audit_data["datas"])):
            audit_data["datas"][i]["zrecordno"] = "autotest"
            audit_data["datas"][i]["chkstatus"] = "未审核"
            audit_data["datas"][i]["_key"] = i + 1
            audit_data["datas"][i]["_id"] = i + 1
        audit_response = res.post_request("/ybzx/webintf.do?method=audit_new_more_sjd", data=urlencode(audit_data))
        assert audit_response.status_code == 200 and audit_response.json()["code"] == "200" and audit_response.json()[
            "msg"] == "审核成功", f"样本批量审核失败！response：{audit_response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("未审核")
    @allure.title("解锁-用例名称：解锁主流程")
    def test_unlock(self, res, token):
        """
        测试未审核-解锁
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 查询待审核样本，获取样本查询结果，审核状态：锁定
        query_data = {
            "task": {"zybzx": "X", "chkstatus": "L", "zybyc": "0", "zsampling_per": "huxiaofeng_A020"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()["code"] == "200" and query_response.json()[
            "msg"] == "success", f"查询锁定样本失败！response：{query_response.json()}"
        # 解锁
        unlock_data = {
            "datas": [query_response.json()["data"][0]],
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        unlock_data["datas"][0]["chkstatus"] = "锁定"
        unlock_data["datas"][0]["_key"] = 1
        unlock_data["datas"][0]["_id"] = 1
        unlock_response = res.post_request("/ybzx/webintf.do?method=unlock_more_sjd", data=urlencode(unlock_data))
        print(unlock_response.json())
        print(unlock_data["datas"][0]["zsample"])
        assert unlock_response.status_code == 200 and unlock_response.json()["code"] == "200" and \
               unlock_response.json()[
                   "msg"] == "解锁成功", f"样本解锁失败！response：{unlock_response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("未审核")
    @allure.title("解锁-用例名称：批量解锁主流程")
    def test_batch_unlock(self, res, token):
        """
        测试未审核-批量解锁
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 查询待审核样本（一个或多个），获取样本查询结果，审核状态：锁定
        query_data = {
            "task": {"zybzx": "X", "chkstatus": "L", "zybyc": "0", "zsampling_per": "huxiaofeng_A020"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()["code"] == "200" and query_response.json()[
            "msg"] == "success", f"查询锁定样本失败！response：{query_response.json()}"
        # 解锁
        unlock_data = {
            "datas": [query_response.json()["data"][0], query_response.json()["data"][1]],
            "token": token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        for i in range(len(unlock_data["datas"])):
            unlock_data["datas"][i]["chkstatus"] = "锁定"
            unlock_data["datas"][i]["_key"] = i + 1
            unlock_data["datas"][i]["_id"] = i + 1
        unlock_response = res.post_request("/ybzx/webintf.do?method=unlock_more_sjd", data=urlencode(unlock_data))
        print(unlock_response.json())
        print(f"{[i['zsample'] for i in unlock_data['datas']]}")
        assert unlock_response.status_code == 200 and unlock_response.json()["code"] == "200" and \
               unlock_response.json()[
                   "msg"] == "解锁成功", f"样本批量解锁失败！response：{unlock_response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("已审核")
    @allure.title("详情-用例名称：详情主流程")
    def test_doubt(self, res, token):
        """
        测试已审核-详情
        :param res:
        :param token:
        :return:
        """
        details_params = {
            "sampleInfo": {"ZSJDID": "INSP240000115544", "ZTEMPBS": "qwxz"},
            "method": "query_new_xxsh_details",
            "token": token("testuser1")["token"],
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        details_response = res.get_request("/ybzx/webintf.do", params=urlencode(details_params))
        assert details_response.status_code == 200 and details_response.json()["code"] == "200" and \
               details_response.json()["msg"] == "success", f"查询样本详情失败！response：{details_response.json()}"