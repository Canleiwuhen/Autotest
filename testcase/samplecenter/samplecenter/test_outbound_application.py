import pytest
import allure
from urllib.parse import urlencode
from data_generate.samplecenter.datagenerate import DataGenerate
from utils.logger import logger_samplecenter_dg as logger
from utils.tools import replace_none
from testcase.samplecenter.samplecenter.outbound_data import DataList


@allure.feature("出库申请")
@pytest.mark.usefixtures("res", "token")
class TestOutboundApplication:
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("出库申请（样本出库）")
    @allure.title("样本出库-搜索-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_wait_outbound_list)
    def test_query_wait_outbound_list(self, res, token, data):
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_wait_out_bound_samples", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()["msg"] == "success",\
            f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("出库申请（样本出库）")
    @allure.title("样本出库-搜索-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_wait_outbound_fail_list)
    def test_query_wait_outbound_list_fail(self, res, token, data):
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_wait_out_bound_samples", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data["msg"],\
            f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-搜索-正向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_apply_uncheck_outbound_list)
    def test_query_apply_uncheck_outbound_list(self, res, token, data):
        # 获取测试参数
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()["msg"] == "success", \
            f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-搜索-反向用例-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_apply_uncheck_outbound_fail_list)
    def test_query_apply_uncheck_outbound_list_fail(self, res, token, data):
        # 获取测试参数和tokens
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data["msg"],\
            f"查询失败！response：{response.json()}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("出库申请（样本出库）")
    @allure.title("样本出库-样本详情导出")
    def test_export_sample_detail(self, res, token):
        data = [["序号","样本编号","产品组合描述","产品编码","产品描述","是否捐献","样本类型名称","孔板","孔位","详细位置","库存位置","放置楼层","放置房间","冰箱名称","推送设备","箱子号","采血管类型"],[1,"20B101500001","单基因","HW0040","NIFTY sinlge-gene screening test Bundle","","全血","20SZSZBY01-0010","A01","","","","","","","","Geneseek tube"],[2,"20B101500008","单基因","HW0040","NIFTY sinlge-gene screening test Bundle","","全血","20SZSZBY01-0010","A08","","","","","","","","Geneseek tube"],[3,"20B101500013","单基因","HW0040","NIFTY sinlge-gene screening test Bundle","","全血","20SZSZBY01-0010","B03","","","","","","","","Geneseek tube"]]
        export_data = {
            "datas": data,
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/exportSampleDetail.do?", data=urlencode(export_data))
        assert response.status_code == 200 and response.json()["status"] == "success" \
               and "详情" in response.json()["filePath"], f'导出详情失败：{response.json()}'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("出库申请（样本出库）")
    @allure.title("样本出库-申请出库-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.apply_outbound_list)
    def test_apply_outbound(self, res, token, data):
        samples = self.generate_data(res, token)
        # 申请出库，创建出库申请单
        outbound_data = {
            "samples": samples,
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        for i in range(len(outbound_data["samples"])):
            outbound_data["samples"][i]["_key"] = i + 1
            outbound_data["samples"][i]["_id"] = i + 1
        outbound_data.update(data["data"])
        outbound_data = replace_none(outbound_data)  # 替换data中的None为""
        create_response = res.post_request("/ybzx/webintf.do?method=create_out_bound_apply",
                                           data=urlencode(outbound_data))
        assert create_response.status_code == 200 and create_response.json()["code"] == "200" \
               and "已成功保存" in create_response.json()["msg"], f"创建出库申请单失败！响应：{create_response.json()}"
        # 申请出库后会自动导出出库申请单
        outbound_apply = create_response.json()["msg"][5:-5]
        export_data = {
            "zscdh": outbound_apply,
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/exportExcelChuKuShenQingSample.do?", data=urlencode(export_data))
        assert response.status_code == 200 and response.json()["status"] == "success" \
               and "出库申请单" in response.json()["filePath"], f'导出出库申请单失败：{response.json()}'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-详情预览")
    def test_preview_sample_detail(self, res, token):
        query_tmp = {"zybzx":"X","zdlvdate":"","syncdate":"","zreqstat_t":"已申请","zcjnam":"huxiaofeng_A020"}
        query_data = {
            "task": query_tmp,
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound",
                                          data=urlencode(query_data)).json()
        zscdh = query_response["data"][0]["zscdh"]
        review_data = {
            "zscdh": zscdh,
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        review_response = res.post_request("/ybzx/webintf.do?method=query_sample_by_sqdh",
                                           data=urlencode(review_data))
        assert review_response.status_code == 200 and review_response.json()["code"] == "200" \
               and len(review_response.json()["data"]) > 0, f'预览详情失败：{review_response.json()}'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("查询")
    @allure.title("查询-详情导出")
    def test_export_sample_detail(self, res, token):
        query_tmp = {"zybzx": "X", "zdlvdate": "", "syncdate": "", "zreqstat_t": "已申请", "zcjnam": "huxiaofeng_A020"}
        query_data = {
            "task": query_tmp,
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_un_check_out_bound",
                                          data=urlencode(query_data)).json()
        zscdh = query_response["data"][0]["zscdh"]
        data = {
            "zscdh": zscdh,
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/exportExcelChuKuShenQingSample.do?", data=urlencode(data))
        assert response.status_code == 200 and response.json()["status"] == "success" \
               and "出库申请单" in response.json()["filePath"], f'导出详情失败：{response.json()}'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("查询")
    @allure.title("查询-删除出入库申请单-正向用例")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 6, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_delete_order_success(self, res, token, generate_steps):
        token = token("testuser1")['token']
        zscdh = generate_steps[0]["outbound_apply_order_number"]
        tmp = [{"zscdh": zscdh}]
        data = {
            "datas": tmp,
            "token": token,
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/webintf.do?method=save_delete_out_apply", data=urlencode(data))
        assert response.status_code == 200 and response.json()["msg"] == "成功删除1条数据!", f"删除失败！response：{response.json()}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("查询")
    @allure.title("查询-删除出入库申请单-反向用例")
    @pytest.mark.parametrize("data", DataList.delete_order_fail_list)
    def test_delete_order_fail(self, res, token, data):
        delete_data = {
            "token": token("testuser1")["token"],
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        delete_data.update(data["data"])
        delete_response = res.post_request("/ybzx/webintf.do?method=save_delete_out_apply", data=urlencode(delete_data))
        assert delete_response.status_code == 200 and delete_response.json()["msg"] == data["msg"],\
            f"删除失败！response：{delete_response.json()}"

    def generate_data(self, res, token):
        dg = DataGenerate(token=token("testuser1")["token"])
        sampleid = dg.sumbit_sample()
        expressnum = dg.send_package(sampleid[0])
        dg.receive_package(expressnum)
        dg.unpack(expressnum)
        containernum, containerid = dg.create_container()
        locate = dg.locate_position(sampleid, containernum, containerid)
        if locate:
            # 查询待出库样本信息
            query_data = {
                "task": {"zybzx": "X", "zcatalo": sampleid[0], "zsjd_type": "YX"},
                "pageNumber": "1",
                "pageSize": "50",
                "token": token("testuser1")["token"],
                "menuId": "OutBoundApply",
                "zsjd_type": "YX"
            }
            query_response = res.post_request("/ybzx/webintf.do?method=query_wait_out_bound_samples",
                                              data=urlencode(query_data))
            if query_response.status_code == 200 and query_response.json()["code"] == "200":
                logger.info(f"查询待出库样本信息成功！样本编号：{sampleid}")
                return query_response.json()["data"]
            else:
                logger.error(f"查询待出库样本信息失败！样本编号：{sampleid}，响应：{query_response.json()}")
                raise Exception(f"查询待出库样本信息失败！样本编号：{sampleid}，响应：{query_response.json()}")
        else:
            print("样本定位失败")
        return []


if __name__ == '__main__':
    pytest.main()
