import pytest
import allure
from urllib.parse import urlencode
from utils.handle_excel import OperationExcel
from utils.tools import get_project_path, sep


@allure.feature("入库审核")
@pytest.mark.usefixtures("res")
class TestInboundAudit:
    query_new_in_bound_apply_form_data_list = [
        {
            "case_name": "输入入库申请单号",
            "data": {
                "task": {"zybzx": "X", "zscdh": "IBR240900001891"}
            }
        },
        {
            "case_name": "输入申请人",
            "data": {
                "task": {"zybzx": "X", "zcjnam": "huxiaofeng_A020"}
            }
        },
        {
            "case_name": "输入申请日期起",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "20240901"}
            }
        },
        {
            "case_name": "输入申请日期止",
            "data": {
                "task": {"zybzx": "X", "zcjdatend": "20240912"}
            }
        },
        {
            "case_name": "输入状态",
            "data": {
                "task": {"zybzx": "X", "zreqstat_code": "00"}
            }
        },
        {
            "case_name": "输入入库申请单号+申请人+申请日期起+申请日期止+状态",
            "data": {
                "task": {"zybzx": "X", "zscdh": "IBR240900001891", "zreqstat_code": "20", "zcjnam": "huxiaofeng_A020",
                         "zcjdat": "20240905", "zcjdatend": "20240912"}
            }
        }
    ]
    query_new_in_bound_apply_form_data_list_fail = [
        {
            "case_name": "全部查询条件为空，查询条件不能为空!",
            "msg": "查询条件不能为空!",
            "data": {
                "task": {"zybzx": "X"}
            }
        },
        {
            "case_name": "输入不存在的入库申请单号，该查询无值.",
            "msg": "该查询无值.",
            "data": {
                "task": {"zybzx": "X", "zscdh": "111"}
            }
        }
    ]
    query_audited_in_bound_apply_form_data_list = [
        {
            "case_name": "空搜，所有条件未输入",
            "data": {
                "task": {"zybzx": "X"}
            }
        },
        {
            "case_name": "输入入库申请单号",
            "data": {
                "task": {"zybzx": "X", "zscdh": "IBR240900001891"}
            }
        },
        {
            "case_name": "输入入库单号",
            "data": {
                "task": {"zybzx": "X", "zckdid": "RKD240900000148"}
            }
        },
        {
            "case_name": "输入入库日期起",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "20240902"}
            }
        },
        {
            "case_name": "输入入库日期止",
            "data": {
                "task": {"zybzx": "X", "zcjnam": "huxiaofeng_A020"}
            }
        },
        {
            "case_name": "输入入库申请单号+入库单号+入库日期起+入库日期止+申请人",
            "data": {
                "task": {"zybzx": "X", "zscdh": "IBR240900001891", "zckdid": "RKD240900000148", "zdlvdate": "20240912",
                         "zdlvdateend": "20240912", "zcjnam": "huxiaofeng_A020"}
            }
        }
    ]
    query_audited_in_bound_apply_form_data_list_fail = [
        {
            "case_name": "输入不存在的入库申请单号，该查询无值.",
            "data": {
                "task": {"zybzx": "X", "zscdh": "IBR2409000018911"}
            }
        }
    ]

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("新增")
    @allure.title("搜索-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_new_in_bound_apply_form_data_list)
    def test_query_new_in_bound_apply_form(self, res, token, data):
        """
        测试查询新增入库申请单
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
            "menuId": "inBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_in_bound_apply_bill", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()[
            "code"] == "200", f"查询未审核的入库申请单失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("新增")
    @allure.title("搜索-异常场景-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_new_in_bound_apply_form_data_list_fail)
    def test_query_new_in_bound_apply_form_fail(self, res, token, data):
        """
        测试查询新增入库申请单-异常场景
        :param res:
        :param token:
        :param data:
        :return:
        """
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "inBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_in_bound_apply_bill", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()["msg"] == data[
            "msg"], f"查询审核的入库申请单失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询")
    @allure.title("搜索-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_audited_in_bound_apply_form_data_list)
    def test_query_audited_in_bound_apply_form(self, res, token, data):
        """
        测试查询已审核入库申请单
        :param res:
        :param token:
        :param data:
        :return:
        """
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "inBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_in_bound_bill", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()[
            "code"] == "200", f"查询已审核入库申请单失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询")
    @allure.title("搜索-异常场景-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_audited_in_bound_apply_form_data_list_fail)
    def test_query_audited_in_bound_apply_form_fail(self, res, token, data):
        """
        测试查询已审核入库申请单-异常场景
        :param res:
        :param token:
        :param data:
        :return:
        """
        # 获取测试参数和token
        query_data = {
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "inBound",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_in_bound_bill", data=urlencode(query_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()["code"] == "400" and response.json()[
            "msg"] == "该查询无值.", f"查询已审核入库申请单失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("新增")
    @allure.title("逐样审核-用例名称：逐样审核主流程")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 8, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_single_audit(self, res, token, generate_steps):
        """
        测试逐样审核
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        inbound_apply = generate_steps[0]["inbound_apply_order_number"]  # 拿到入库申请单号
        # 查询入库申请单样本信息
        query_data = {
            "zscdh": inbound_apply,  # 入库申请单号
            "ziszbcrk": "",
            "dev": "false",
            "token": token
        }
        query_response = res.post_request("/ybzx/webintf.do?method=query_samples_by_sqdh_of_in_bound_apply",
                                          data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()[
            "code"] == "200", f"查询入库申请单样本信息失败！response：{query_response.json()}"
        # 新增容器/孔板，生成孔板编号
        add_zplate_data = {
            "req": [{"zcontainer_id": "",
                     "zrqlx": "DNA",  # 容器类型
                     "zcontainer_code": "DNA",
                     "zcontainer_num": "DNA",
                     "zplate_x": "12",
                     "zplate_y": "8",
                     "zplate_notes": "",  # 容器备注
                     "zplate_status": "1",
                     "c_temperature": "4℃",  # 温度
                     "zcontainer_number": 96,  # 容器规格
                     "zcontainer_type": "02",  # 容器类型
                     "zrqsl": "1",  # 容器数量
                     "zrqqz": ""}],
            "token": token
        }
        add_zplate_response = res.post_request("/ybzx/pos/container/save.do", data=urlencode(add_zplate_data))
        assert add_zplate_response.status_code == 200 and add_zplate_response.json()["code"] == "200" and "成功生成编码" in \
               add_zplate_response.json()["msg"], f"生成孔板编号失败！response：{add_zplate_response.json()}"
        # 一个不知道做什么的接口
        unknown_data = {
            "req": [{"zplate_num": add_zplate_response.json()["data"][0]["zcontainer_num"]}],
            "token": token
        }
        unknown_response = res.post_request("/ybzx/pos/query/plate/xxwz.do", data=urlencode(unknown_data))
        assert unknown_response.status_code == 200 and unknown_response.json()[
            "code"] == "200", f"不知道做什么的接口调用失败！response：{unknown_response.json()}"
        # 获取样本的datasource？
        ybsource_data = {
            "req": [{"zcatalo": query_response.json()["data"][0]["zcatalo"], "ztype": "RKSH", "page_flag": ""}],
            "token": token
        }
        ybsource_response = res.post_request("/ybzx/pos/query/ybsource.do", data=urlencode(ybsource_data))
        assert ybsource_response.status_code == 200 and ybsource_response.json()["code"] == "200" and \
               ybsource_response.json()["msg"] == "success", f"获取样本datasource失败！response：{ybsource_response.json()}"
        # 保存datasource？
        reqform_data = {
            "req": [{"zcatalo": query_response.json()["data"][0]["zcatalo"],
                     "zdatasource": ybsource_response.json()["data"][0]["zdatasource"]}],
            "token": token
        }
        reqform_response = res.post_request("/ybzx/pos/query/reqform2.do", data=urlencode(reqform_data))
        assert reqform_response.status_code == 200 and reqform_response.json()["code"] == "200" and \
               reqform_response.json()["msg"] == "success", f"保存样本datasource失败！response：{reqform_response.json()}"
        # 保存当前孔板信息
        save_data = {
            "req": [{"use_scene": "01",
                     "zcwbh": query_response.json()["data"][0]["zcatalo"],  # 样本编号
                     "zcwlx": query_response.json()["data"][0]["zyblx"],  # 样本类型
                     "zctrid": add_zplate_response.json()["data"][0]["zcontainer_num"],  # 孔板编号
                     "zplate_num": add_zplate_response.json()["data"][0]["zcontainer_num"],
                     "zplate": add_zplate_response.json()["data"][0]["zcontainer_id"],  # 孔板id
                     "zcontainer_id": add_zplate_response.json()["data"][0]["zcontainer_id"],
                     "zpoint": "A01",  # 孔位号
                     "zkc_status": "RKDW",
                     "zsc_sutatus": "",
                     "zpbr": "",
                     "zrkr": "",
                     "zsfpcr": "",
                     "ztprt": "4℃",
                     "zreceiveddate": query_response.json()["data"][0]["zreceiveddate"],  # 到样日期
                     "zfrgid": "",
                     "lgort": "",
                     "lgobe": "",
                     "zroomnum": "",
                     "zxxwz": "",
                     "ztype": "",
                     "zscdh": query_response.json()["data"][0]["zscdh"],  # 入库申请单号
                     "zscdh_item": query_response.json()["data"][0]["zscdh_item"]}],
            "dev": "false",
            "token": token
        }
        save_response = res.post_request("/ybzx/pos/checkin_visual/post.do", data=urlencode(save_data))
        assert save_response.status_code == 200 and save_response.json()["code"] == "200" and \
               save_response.json()["msg"] == "保存成功", f"保存孔板信息失败！response：{save_response.json()}"
        # 完成审核，创建入库单号
        create_data = {
            "zscdh": query_response.json()["data"][0]["zscdh"],  # 入库申请单号
            "dev": "false",
            "token": token
        }
        create_response = res.post_request("/ybzx/pos/checkin_visual/create_rkd.do", data=urlencode(create_data))
        assert create_response.status_code == 200 and create_response.json()["code"] == "200" and \
               "成功创建入库单" in create_response.json()["msg"], f"创建入库单号失败！response：{create_response.json()}"

    # @pytest.mark.skip("编辑文件后接口报解析不到数据")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("新增")
    @allure.title("批量审核-用例名称：批量审核主流程")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path1', 'last_step': 8, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_batch_audit(self, res, token, generate_steps):
        """
        测试批量审核
        :param res:
        :param token:
        :return:
        """
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        sample = generate_steps[0]["sample"]  # 拿到样例编号
        # 获取项目路径，拼接文件相对路径，得到上传文件的绝对路径
        project_path = get_project_path()
        file_path = sep([project_path, "testcase/samplecenter/samplecenter/入库审核_批量审核.xlsx"])
        # 新增容器/孔板，生成孔板编号
        add_zplate_data = {
            "req": [{"zcontainer_id": "",
                     "zrqlx": "DNA",  # 容器类型
                     "zcontainer_code": "DNA",
                     "zcontainer_num": "DNA",
                     "zplate_x": "12",
                     "zplate_y": "8",
                     "zplate_notes": "",  # 容器备注
                     "zplate_status": "1",
                     "c_temperature": "4℃",  # 温度
                     "zcontainer_number": 96,  # 容器规格
                     "zcontainer_type": "02",  # 容器类型
                     "zrqsl": "1",  # 容器数量
                     "zrqqz": ""}],
            "token": token
        }
        add_zplate_response = res.post_request("/ybzx/pos/container/save.do", data=urlencode(add_zplate_data))
        assert add_zplate_response.status_code == 200 and add_zplate_response.json()["code"] == "200" and "成功生成编码" in \
               add_zplate_response.json()["msg"], f"保存生成孔板编号失败！response：{add_zplate_response.json()}"
        # 一个不知道做什么的接口
        unknown_data = {
            "req": [{"zplate_num": add_zplate_response.json()["data"][0]["zcontainer_num"]}],
            "token": token
        }
        unknown_response = res.post_request("/ybzx/pos/query/plate/xxwz.do", data=urlencode(unknown_data))
        assert unknown_response.status_code == 200 and unknown_response.json()[
            "code"] == "200", f"不知道做什么的接口调用失败！response：{unknown_response.json()}"
        # 实例化文件操作类，修改样本编号
        oe = OperationExcel(file_name=file_path, sheet_name="Sheet1")
        oe.write_value(1, 0, sample[0])  # 修改样本/产物编号
        oe.write_value(1, 1, add_zplate_response.json()["data"][0]["zcontainer_num"])  # 修改孔板/容器编号
        # oe.open_excel_by_win32()
        # 批量审核-上传文件
        res.s.headers = {"multipart/form-data; boundary=----WebKitFormBoundaryQiszW40ZiQ16bZAp"}
        print(f"请求头：{res.s.headers}")
        print(f"文件路径：{file_path}")
        upload_response = res.post_request(
            f"/ybzx/excelFile/import.do?methodName=importInboundAuditData&token={token}",
            file_path=file_path, )
        print(upload_response.text)
        assert upload_response.status_code == 200 and upload_response.json()["code"] == "200" and \
               upload_response.json()["data"][0]["message"] == "通过", f"批量审核上传文件失败！response：{upload_response.json()}"
        # 提交审核，创建入库单号
        create_data = {
            "datas": [
                {"ZCATALO_IN": sample[0], "ZPLATE_NUM_IN": add_zplate_response.json()["data"][0]["zcontainer_num"],
                 "ZPOINT_IN": "A01"}],
            "token": token,
            "menuId": "inBound",
            "zsjd_type": "YX",
        }
        res.s.headers = {"content-type": "application/x-www-form-urlencoded"}
        create_response = res.post_request("/ybzx/webintf.do?method=save_inbound_audit_data",
                                           data=urlencode(create_data))
        assert create_response.status_code == 200 and create_response.json()["code"] == "200" and "成功创建入库单" in \
               create_response.json()["msg"], f"创建入库单号失败！response：{create_response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询")
    @allure.title("入库单预览-用例名称：入库单预览主流程")
    def test_in_bound_form_preview(self, res, token):
        """
        测试入库单预览
        :param res:
        :param token:
        :return:
        """
        preview_data = {
            "zckdid": "RKD240900000146",
            "token": token("testuser1")["token"],
            "menuId": "inBound",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/webintf.do?method=query_samples_by_sqdh_of_in_bound_bill",
                                    data=urlencode(preview_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()[
            "code"] == "200", f"入库单预览失败！response：{response.json()}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("查询")
    @allure.title("入库单预览-用例名称：入库单预览->导出Excel到桌面")
    def test_in_bound_form_preview_export(self, res, token):
        """
        测试入库单预览->导出Excel到桌面
        :param res:
        :param token:
        :return:
        """
        export_data = {
            "zscdh": "IBR240800001832",
            "token": token("testuser1")["token"],
            "menuId": "inBound",
            "zsjd_type": "YX"
        }
        response = res.post_request("/ybzx/exportRuKuShenQingSample.do?", data=urlencode(export_data))
        # print(response.json())
        assert response.status_code == 200 and response.json()[
            "status"] == "success", f"导出Excel到桌面失败！response：{response.json()}"
