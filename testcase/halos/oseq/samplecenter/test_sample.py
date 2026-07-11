import pytest
import allure
import os
import time
from datetime import datetime, timedelta
from utils.tools import create_sample, calculate_file_buffer
from testcase.halos.oseq.samplecenter.sample_data import DataList


@pytest.mark.usefixtures("res","res_file")
class TestSample:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-OSEQ_seq样本添加")
    @allure.title("样本中心-OSEQ_seq样本添加")
    def test_add_sample(self, res):
        # 使用固定的时间戳，与成功案例保持一致
        # 生成简单的数字序列号
        sampleno = "25SSS"+create_sample()
        data = {"sampleId": sampleno, "productNo": "LD01361", "sampleCurrentStatus": "2", "sampleTyping": "2",
                "sampleType": "2", "sampleSerialNumber": create_sample(), "controlSampleId": "", "collectDate": 1766592000000,
                "receivedDate": 1766592000000, "arrivalDate": 1766592000000, "tumorType": "100", "patientName": "test2",
                "patientGender": "1", "hospitalId": "", "departmentId": "", "doctorId": "", "patientIdCard": "",
                "smokingHistory": "", "personalCancerHistory": "", "familyCancerHistory": "", "clinicalStage": "",
                "tnmStage": "", "cancerThrombus": "", "nerveInvasion": "", "originOfLesion": "", "formId": 32,
                "createUser": "13aa71751c4f4c559064519c4357dae8"}
        response = res.post_request("/prod-api/api/oseq/samples/create", json=data)
        assert response.status_code == 200
        response_json = response.json()
        # 如果失败，打印详细信息以便调试
        if not response_json.get('success'):
            print(f"请求数据: {data}")
            print(f"响应结果: {response_json}")
        assert response_json['success'] == True, f"创建样本失败: {response_json}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-查询样本")
    @allure.title("样本中心-查询样本：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search_sample(self, res, data):
        """
        样本中心查询，只做了样本编号、病理号字段搜索
        :param res:
        :param data:
        :return:
        """
        tmp = data['search_items']
        json_data = {
            "page": 1,
            "size": 100,
            "controlSampleFlag":1
        }
        json_data.update(tmp)
        response = res.post_request("/prod-api/api/oseq/samples/page", json=json_data)
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert response.json()['retCode'] == 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-OSEQ_seq样本编辑")
    @allure.title("样本中心-OSEQ_seq样本编辑")
    def test_edit_sample(self, res):
        """
        当前只做了OSEQ的编辑
        :param res:
        :return:
        """
        sampleno = "25SSS"+create_sample()
        data1 = {"sampleId": sampleno, "productNo": "LD01361", "sampleCurrentStatus": "2", "sampleTyping": "2",
                "sampleType": "2", "sampleSerialNumber": create_sample(), "controlSampleId": "", "collectDate": 1766592000000,
                "receivedDate": 1766592000000, "arrivalDate": 1766592000000, "tumorType": "100", "patientName": "test2",
                "patientGender": "1", "hospitalId": "", "departmentId": "", "doctorId": "", "patientIdCard": "",
                "smokingHistory": "", "personalCancerHistory": "", "familyCancerHistory": "", "clinicalStage": "",
                "tnmStage": "", "cancerThrombus": "", "nerveInvasion": "", "originOfLesion": "", "formId": 32,
                "createUser": "13aa71751c4f4c559064519c4357dae8"}
        create_response = res.post_request("/prod-api/api/oseq/samples/create", json=data1)   # 先新增样本
        assert create_response.status_code == 200
        create_json = create_response.json()
        assert create_json['success'] == True, f"创建样本失败: {create_json}"
        detailurl = "/prod-api/api/oseq/samples/queryById/"+sampleno
        detairesp = res.get_request(url=detailurl)  # 获取样本详情
        assert detairesp.status_code == 200
        data2 = detairesp.json()['result']
        assert data2 is not None, "获取样本详情失败，result为None"
        # 根据日志，服务器端可以正常处理null值，所以保持数据原样
        # 去掉controlSampleType字段
        if 'controlSampleType' in data2:
            del data2['controlSampleType']
        data2['oldSampleNum'] = create_sample()  # 添加oldSampleNum字段
        response = res.put_request("/prod-api/api/oseq/samples/edit", json=data2)  # 执行编辑操作
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert response.json()['retCode'] == 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-OSEQ_seq样本删除")
    @allure.title("样本中心-OSEQ_seq样本删除")
    def test_delete_sample(self, res):
        """
        当前只做了OSEQ样本的删除
        :param res:
        :return:
        """
        sampleno = "25DPP2"+create_sample()
        data1 = {"sampleId": sampleno, "productNo": "DX18331", "sampleCurrentStatus": "2", "sampleTyping": "2",
                "sampleType": "2", "sampleSerialNumber": create_sample(), "controlSampleId": "", "collectDate": 1766592000000,
                "receivedDate": 1766592000000, "arrivalDate": 1766592000000, "tumorType": "100", "patientName": "test2",
                "patientGender": "1", "hospitalId": "", "departmentId": "", "doctorId": "", "patientIdCard": "",
                "smokingHistory": "", "personalCancerHistory": "", "familyCancerHistory": "", "clinicalStage": "",
                "tnmStage": "", "cancerThrombus": "", "nerveInvasion": "", "originOfLesion": "", "formId": 32,
                "createUser": "13aa71751c4f4c559064519c4357dae8"}
        res.post_request("/prod-api/api/oseq/samples/create", json=data1)   # 先新增样本
        response = res.delete_request("/prod-api/api/oseq/samples/delete/"+sampleno)  # 执行删除操作
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert response.json()['retCode'] == 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本导出")
    @allure.title("样本中心-样本导出")
    def test_export_sample(self, res):
        """
        当前只做了OSEQ样本的导出，判断导出文件非空文件
        :param res:
        :return:
        """
        sampleno1 = "25DPP2"+create_sample()
        sampleno2 = "25DPP2"+create_sample()
        data1 = {"sampleId": sampleno1, "productNo": "DX18331", "sampleCurrentStatus": "2", "sampleTyping": "2",
                "sampleType": "2", "sampleSerialNumber": create_sample(), "controlSampleId": "", "collectDate": 1766592000000,
                "receivedDate": 1766592000000, "arrivalDate": 1766592000000, "tumorType": "100", "patientName": "test2",
                "patientGender": "1", "hospitalId": "", "departmentId": "", "doctorId": "", "patientIdCard": "",
                "smokingHistory": "", "personalCancerHistory": "", "familyCancerHistory": "", "clinicalStage": "",
                "tnmStage": "", "cancerThrombus": "", "nerveInvasion": "", "originOfLesion": "", "formId": 32,
                "createUser": "13aa71751c4f4c559064519c4357dae8"}
        data2 = {"sampleId": sampleno2, "productNo": "DX18331", "sampleCurrentStatus": "2", "sampleTyping": "2",
                "sampleType": "2", "sampleSerialNumber": create_sample(), "controlSampleId": "", "collectDate": 1766592000000,
                "receivedDate": 1766592000000, "arrivalDate": 1766592000000, "tumorType": "100", "patientName": "test2",
                "patientGender": "1", "hospitalId": "", "departmentId": "", "doctorId": "", "patientIdCard": "",
                "smokingHistory": "", "personalCancerHistory": "", "familyCancerHistory": "", "clinicalStage": "",
                "tnmStage": "", "cancerThrombus": "", "nerveInvasion": "", "originOfLesion": "", "formId": 32,
                "createUser": "13aa71751c4f4c559064519c4357dae8"}
        res.post_request("/prod-api/api/oseq/samples/create", json=data1)  # 先新增样本
        res.post_request("/prod-api/api/oseq/samples/create", json=data2)
        # 样本编号用逗号分隔，放在URL路径中
        sample_ids = ",".join([sampleno1, sampleno2])
        export_url = "/prod-api/api/oseq/samples/export/" + sample_ids
        response = res.get_request(url=export_url)  # 执行导出操作
        assert response.status_code == 200
        file_size = calculate_file_buffer(response)
        assert file_size > 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-下载模板")
    @allure.title("样本中心-下载模板")
    def test_export_template(self, res):
        """
        下载样本信息导入模板，校验导出非空文件
        :param res:
        :return:
        """
        from urllib.parse import quote
        # 调用forms/page接口获取importFile字段
        forms_response = res.post_request("/prod-api/api/sys/forms/page", json={"page": 1, "size": 100})
        assert forms_response.status_code == 200
        assert forms_response.json()['success'] == True
        # 从rows中获取第一个有importFile的元素
        rows = forms_response.json()['result']['rows']
        assert len(rows) > 0, "表单列表为空"
        # 查找第一个有importFile且不为空的表单
        import_file = None
        for row in rows:
            if row.get('importFile') and row['importFile'].strip():
                import_file = row['importFile']
                break
        assert import_file is not None, "没有找到有效的importFile"
        # 下载模板文件
        download_url = f"/prod-api/api/sys/common/downloadFile?fileName={quote(import_file, safe='')}"
        response = res.get_request(url=download_url)
        assert response.status_code == 200
        assert calculate_file_buffer(response) > 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-送检单导入")
    @allure.title("样本中心-送检单导入")
    def test_import_sample(self, res_file):
        """
        导入所有检测项目的送检单，目前只做了oseq,导入文件数据非动态数据
        :param res_file:
        :return:
        """
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'import_files')
        # 获取导入表单列表
        forms_response = res_file.post_request("/prod-api/api/sys/forms/page", json={"page": 1, "size": 100})
        assert forms_response.status_code == 200
        forms_json = forms_response.json()
        assert forms_json['success'] == True
        formid_list = [row for row in forms_json['result']['rows'] if row.get('importFile')]
        assert len(formid_list) > 0, "没有找到可导入的表单"
        # 循环导入所有送检单
        for form in formid_list:
            project_code = form.get('productServiceName') or (form.get('formName', '').split('-')[0] if form.get('formName') else '')
            if not project_code:
                continue
            file_path = os.path.join(base_path, f"{project_code}.xlsx")
            if not os.path.exists(file_path):
                continue
            # 导入文件
            response = res_file.post_request("/prod-api/api/oseq/samples/excel/import", data={"formId": form['id']}, file_path=file_path)
            assert response.status_code == 200
            response_json = response.json()
            assert response_json['success'] == True and response_json['retCode'] == 0
            assert len(response_json['result']['success']) != 0 and len(response_json['result']['fail']) == 0
            # 删除导入的样本
            res_file.delete_request("/prod-api/api/oseq/samples/delete", json=[response_json['result']['success'][0]['sampleNo']])