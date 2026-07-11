import pytest
import allure
from urllib.parse import urlencode


@allure.feature("样例查询")
@pytest.mark.usefixtures("res")
class TestSampleQuery:
    query_sample_data_list = [
        {
            "case_name": "输入填单日期",
            "data": {
                "task": {"zybzx": "X", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入样例编号+填单日期",
            "data": {
                "task": {"zybzx": "X", "zsample": "1047712147", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入样本编号+填单日期",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "1047712147", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入简编号查询+填单日期",
            "data": {
                "task": {"zybzx": "X", "zsample_s": "1047712147", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入样本编号模糊查询+填单日期",
            "data": {
                "task": {"zybzx": "X", "zcatalo1": "1047745", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入是否到样+填单日期",
            "data": {
                "task": {"zybzx": "X", "zsfdy": "是", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入送检单位+填单日期",
            "data": {
                "task": {"zybzx": "X", "kunnr": "1000000004", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入产品组合+填单日期",
            "data": {
                "task": {"zybzx": "X", "zmatnr_ty": "T002,T003", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入产品+填单日期",
            "data": {
                "task": {"zybzx": "X", "matnr": "DX1616", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入是否到样+身份证号+填单日期",
            "data": {
                "task": {"zybzx": "X", "zidcard": "15000019971001740X", "zsfdy": "是", "zcdate": "20240916",
                         "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入是否到样+姓名+填单日期",
            "data": {
                "task": {"zybzx": "X", "zsamplename": "涂彬", "zsfdy": "是", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入到样日期+填单日期",
            "data": {
                "task": {"zybzx": "X", "received_date": "20240916", "received_dateend": "20241116",
                         "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入样例编号+样本编号+简编号查询+样本编号模糊查询+是否到样+送检单位+产品组合+产品+身份证号+姓名+到样日期+填单日期",
            "data": {
                "task": {"zybzx": "X", "received_date": "20240916", "received_dateend": "20241116", "zsamplename": "涂彬",
                         "zidcard": "15000019971001740X", "zsfdy": "是", "zmatnr_ty": "T014", "matnr": "DX1676",
                         "zsample": "24B09190042", "zcatalo": "24B09190042", "zsample_s": "24B09190042",
                         "zcatalo1": "24B091900", "kunnr": "1000027045", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
    ]

    query_sample_data_list_fail = [
        {
            "case_name": "输入填单日期内无数据，筛选条件没有查询到数据！",
            "msg": "筛选条件没有查询到数据！",
            "data": {
                "task": {"zybzx": "X", "zcdate": "20241001", "zcdateend": "20241001"}
            }
        },
        {
            "case_name": "输入身份证号+填单日期，未输入是否到样，通过身份证号\\姓名查询时，是否到样必须选择是",
            "msg": "通过身份证号\\姓名查询时，是否到样必须选择是",
            "data": {
                "task": {"zybzx": "X", "zidcard": "15000019971001740X", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        },
        {
            "case_name": "输入姓名+填单日期，未输入是否到样，通过身份证号\\姓名查询时，是否到样必须选择是",
            "msg": "通过身份证号\\姓名查询时，是否到样必须选择是",
            "data": {
                "task": {"zybzx": "X", "zsamplename": "涂彬", "zcdate": "20240916", "zcdateend": "20241016"}
            }
        }
    ]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("搜索")
    @allure.title("搜索-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_sample_data_list)
    def test_query_sample(self, res, token, data):
        """
        测试样例查询
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
            "menuId": "YbzxReport_SampleQueryIndex",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_sample_list", data=urlencode(query_data))
        assert response.status_code == 200 and response.json()[
            "code"] == "200", f"查询样本信息失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("搜索")
    @allure.title("搜索-异常场景-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_sample_data_list_fail)
    def test_query_sample_fail(self, res, token, data):
        """
        测试样例查询-异常场景
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
            "menuId": "YbzxReport_SampleQueryIndex",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_sample_list", data=urlencode(query_data))
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data[
            "msg"], f"查询样本信息失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("样本编号导出")
    @allure.title("样本编号导出-用例名称：样本编号导出主流程")
    def test_sample_number_export(self, res, token):
        """
        测试样本编号导出主流程
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 查询样本信息
        query_data = {
            "task": {"zybzx": "X", "zsample": "24X101600006", "zcdate": "20240916", "zcdateend": "20241016"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token,
            "menuId": "YbzxReport_SampleQueryIndex",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_sample_list", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()[
            "code"] == "200", f"查询样本信息失败！response：{query_response.json()}"
        # 基于查询的样本提交样本编号导出
        export_data = {
            "excelHead": [
                {"Header": "样例编号", "accessor": "zsample"},
                {"Header": "样本编号", "accessor": "zcatalo"},
                {"Header": "样本类型", "accessor": "zyblx_code"}
            ],
            "excelName": "样本编号导出",
            "fileType": "xlsx",
            "datas": [{"zsample": i["zsample"], "zsjdid": i["zsjdid"]} for i in query_response.json()["data"]],
            "pageNumber": "1",
            "pageSize": "200000",
            "token": token,
            "menuId": "YbzxReport_SampleQueryIndex",
            "zsjd_type": "YX"
        }
        export_response = res.post_request("/ybzx/webintf.do?method=export_sample_query", data=urlencode(export_data))
        assert export_response.status_code == 200 and export_response.json()["code"] == "200" and "样本编号导出_" in \
               export_response.json()["msg"], f"样本编号导出失败！response：{export_response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("导出")
    @allure.title("导出-用例名称：导出主流程")
    def test_export(self, res, token):
        """
        测试导出主流程
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 查询样本信息
        query_data = {
            "task": {"zybzx": "X", "zsample": "24X101600006", "zcdate": "20240916", "zcdateend": "20241016"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token,
            "menuId": "YbzxReport_SampleQueryIndex",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_sample_list", data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()[
            "code"] == "200", f"查询样本信息失败！response：{query_response.json()}"
        query_response = query_response.json()
        # 遍历拼接导出样本信息
        datas = [
            [
                i + 1,
                query_response["data"][i]["zsample"],
                query_response["data"][i]["zmatnr_ty_text"],
                query_response["data"][i]["matnr"],
                query_response["data"][i]["maktx"],
                query_response["data"][i]["sum"],
                query_response["data"][i]["yblx"],
                query_response["data"][i]["name1"],
                query_response["data"][i]["zsamplename"],
                query_response["data"][i]["zcdate"],
                query_response["data"][i]["zcreator"],
                query_response["data"][i]["zsalesrep"] if query_response["data"][i]["zsalesrep"] else "null",
                "null",
                "null",
                "null",
                "null",
                query_response["data"][i]["received_date"],
                query_response["data"][i]["received_uname"],
                query_response["data"][i]["zzqty"],
                query_response["data"][i]["zsjdid"],
                query_response["data"][i]["zsjdlx"],
            ] for i in range(len(query_response["data"]))
        ]
        # 基于查询的样本提交导出
        export_data = {
            "datas": [
                [
                    "序号", "样例编号", "产品组合", "产品编号", "产品名称", "样本数量", "样本类型与数量", "送检单位", "受检者姓名",
                    "填单日期", "填单人", "销售", "主样本编号", "主样本类型", "对照样本编号", "对照样本类型", "到样日期", "到样人",
                    "是否捐献", "送检单号", "送检单类型"
                ]
            ],
            "token": token,
            "menuId": "YbzxReport_SampleQueryIndex",
            "zsjd_type": "YX"
        }
        export_data["datas"].extend(datas)
        export_response = res.post_request("/ybzx/exportSampleDetail.do", data=urlencode(export_data))
        assert export_response.status_code == 200 and export_response.json()["status"] == "success" and "详情.xlsx" in \
               export_response.json()["filePath"], f"样例查询-导出失败！response：{export_response.json()}"
