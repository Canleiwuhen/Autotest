import pytest
import allure
from urllib.parse import urlencode
from data_generate.samplecenter.datagenerate import DataGenerate
from utils.tools import replace_none
from testcase.samplecenter.samplecenter.outbound_data import DataList


@allure.feature("出库审核")
@pytest.mark.usefixtures("res", "token")
class TestOutboundAudit:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("新增")
    @allure.title("新增-搜索-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_uncheck_outbound_list)
    def test_query_uncheck_outbound_list(self, res, token, data):
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()["msg"] == "success",\
            f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("新增")
    @allure.title("新增-搜索-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_uncheck_outbound_fail_list)
    def test_query_uncheck_outbound_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data[
            "msg"], f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-搜索-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_outbound_bill_list)
    def test_query_outbound_bill_list(self, res, token, data):
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_out_bound_bill", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200", f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-搜索-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_outbound_bill_fail_list)
    def test_query_outbound_bill_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_out_bound_bill", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data[
            "msg"], f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("新增")
    @allure.title("新增-创建出库单")
    def test_create_outbound_order(self, res, token):
        dg = DataGenerate(token=token("testuser1")["token"])
        sampleid = dg.sumbit_sample()
        expressnum = dg.send_package(sampleid[0])
        receive = dg.receive_package(expressnum)
        if receive:
            unpack = dg.unpack(expressnum)
            if unpack:
                containernum, containerid = dg.create_container()
                locate = dg.locate_position(sampleid, containernum, containerid)
                if locate:
                    outbound_num = dg.outbound_apply(sampleid[0])
                    query_data = {"zscdh": outbound_num,
                                  "token": token("testuser1")["token"],
                                  "menuId": "outBound",
                                  "zsjd_type": "YX"
                                  }
                    query_response = res.post_request("/ybzx/webintf.do?method=query_sample_by_sqdh",
                                                      data=urlencode(query_data)).json()
                    audit_data = {
                        "datas": query_response['data'],
                        "token": token("testuser1")["token"],
                        "menuId": "outBound",
                        "zsjd_type": "YX"
                    }
                    for i in range(len(audit_data["datas"])):
                        audit_data["datas"][i]["zshdat"] = ''
                        audit_data["datas"][i]["_id"] = i + 1
                    audit_data = replace_none(audit_data)
                    audit_response = res.post_request("/ybzx/webintf.do?method=create_chuku_bill",
                                                      data=urlencode(audit_data))
                else:
                    print("样本定位失败")
                    audit_response = None
            else:
                print("拆包失败")
                audit_response = None
        else:
            print("包裹签收失败")
            audit_response = None
        assert audit_response.status_code == 200 and audit_response.json()["code"] == "200" \
               and "成功创建出库单" in audit_response.json()["msg"], f'创建出库单失败：{audit_response.json()}'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-出库单预览")
    def test_preview_outbound_order(self, res, token):
        query_tmp = {"zybzx":"X"}
        query_data = {
            "task": query_tmp,
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_out_bound_bill",
                                          data=urlencode(query_data)).json()
        zckdid = query_response["data"][0]["zckdid"]
        review_data = {
            "zckdid": zckdid,
            "token": token("testuser1")["token"],
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        review_response = res.post_request("/ybzx/webintf.do?method=query_samples_by_sqdh_of_out_bound_bill",
                                           data=urlencode(review_data))
        assert review_response.status_code == 200 and review_response.json()["code"] == "200" \
               and len(review_response.json()["data"]) > 0, f'预览出库单失败：{review_response.json()}'
        zscdh = query_response["data"][0]["zscdh"]
        return zscdh

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-出库审核单导出")
    def test_export_outbound_order(self, res, token):
        zscdh = self.test_preview_outbound_order(res, token)
        data = {
            "zscdh": zscdh,
            "token": token("testuser1")["token"],
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/exportExcelChuKusShenHeSample.do?", data=urlencode(data))
        assert response.status_code == 200 and response.json()["status"] == "success" \
               and "出库申请单" in response.json()["filePath"], f'导出出库单失败：{response.json()}'


if __name__ == '__main__':
    pytest.main()
