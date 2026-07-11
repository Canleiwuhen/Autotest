import json

import pytest
import allure


@pytest.mark.usefixtures("res")
class TestConfig:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-检测项目管理")
    @allure.title("配置中心-检测项目管理-查询")
    def test_items_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_data_res = res.post_request("/api/base/projects/page", json=search_data)
        assert search_data_res.status_code == 200
        list_tem = []
        for i in search_data_res.json()['result']['records']:
            list_tem.append(i['projectCode'])
        assert ['CNV-seq', 'NIFTY', 'NBS', 'CS'] <= list_tem

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-导入规则配置")
    @allure.title("配置中心-导入规则配置-查询")
    def test_import_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100, "status": 1}
        search_data_res = res.post_request("/api/base/forms/page", json=search_data)
        assert search_data_res.status_code == 200
        list_tmp = []
        for i in search_data_res.json()['result']['records']:
            list_tmp.append(i['projectCode'])
        assert list_tmp >= ['CNV-seq', 'CS', 'NBS', 'NIFTY']

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-导出内容配置")
    @allure.title("配置中心-导出内容配置-查询")
    def test_export_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_data_res = res.post_request("/api/base/export/templates/page", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['result']['total'] > 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-质控品配置")
    @allure.title("配置中心-质控品配置-质控品查询")
    def test_control_search(self, res):
        search_data = {}
        search_data_res = res.post_request("/api/base/kits/page", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['result']['total'] >= 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-质控品配置")
    @allure.title("配置中心-质控品配置-添加质控品")
    def test_add_control(self, res):
        add_data = {"projectCode": "NIFTY", "kitNo": "test_api_forward", "qcSamples": [
            {"qcSampleType": "Positive", "sampleTypeCode": "S216", "qcSampleNo": "api_forward1", "productNo": "DX0558"},
            {"qcSampleType": "Negative", "sampleTypeCode": "L003", "qcSampleNo": "api_forward2", "productNo": "DX0558"},
            {"qcSampleType": "Empty", "sampleTypeCode": "S094", "qcSampleNo": "api_forward3", "productNo": "DX0558"}]}
        add_data_res = res.post_request("/api/base/kits/qcSample/add", json=add_data)
        assert add_data_res.status_code == 200
        assert add_data_res.json()['retInfo'] == 'success'
        search_data = {}
        search_data_res = res.post_request("/api/base/kits/page", json=search_data)
        list_tmp = search_data_res.json()['result']['records']
        target_kitId = ''
        for i in list_tmp:
            if i['kitNo'] == 'test_api_forward':
                target_kitId = i['kitId']
        # 再删除新增的数据
        delete_url = '/api/base/kits/delete/' + target_kitId
        delete_url_res = res.post_request(url=delete_url)
        assert delete_url_res.status_code == 200
        assert delete_url_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-质控品配置")
    @allure.title("配置中心-质控品配置-标准品查询")
    def test_standard_search(self, res):
        search_data = {}
        search_data_res = res.post_request("/api/base/standardSamples/page", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['result']['total'] >= 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-质控品配置")
    @allure.title("配置中心-质控品配置-添加标准品")
    def test_add_standard(self, res):
        add_data = {"standardSampleType": "StandardNegative", "standardBatchNo": "forward_test1", "standardGoodsNo": "forward_test2",
                       "standardSampleNo": "forward_test3", "sampleTypeCode": "S216", "productNo": "DX0558",
                       "projectCode": "NIFTY"}
        add_data_res = res.post_request("/api/base/standardSamples", json=add_data)
        assert add_data_res.status_code == 200
        assert add_data_res.json()['retInfo'] == 'success'
        # 查询验证已新增的数据
        search_data = {"projectCodes": ["NIFTY"]}
        search_data_res = res.post_request("/api/base/standardSamples/project/page", json=search_data)
        target_data = search_data_res.json()['result']['records']
        index = len(target_data)-1
        assert target_data[index]['standardBatchNo'] == add_data['standardBatchNo']
        assert target_data[index]['standardGoodsNo'] == add_data['standardGoodsNo']
        assert target_data[index]['standardSampleNo'] == add_data['standardSampleNo']
        assert target_data[index]['standardSampleType'] == add_data['standardSampleType']
        assert target_data[index]['sampleTypeCode'] == add_data['sampleTypeCode']
        standardSampleId = target_data[index]['standardSampleId']
        # 再删除新增数据
        delete_url = '/api/base/standardSamples/' + standardSampleId
        res.post_request(url=delete_url)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-验证配置")
    @allure.title("配置中心-验证配置-查询{data}验证配置")
    @pytest.mark.parametrize("data", ["CNV-seq", "CS", "NBS", "NIFTY"])
    def test_validation_search(self, res, data):
        search_data = {"projectCode": data, "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_data_res = res.post_request("/api/base/products/page", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['result']['total'] >= 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-验证配置")
    @allure.title("配置中心-验证配置-编辑{data}验证配置")
    @pytest.mark.parametrize("data", ["CNV-seq", "CS", "NBS", "NIFTY"])
    def test_validation_edit(self, res, data):
        search_data = {"projectCode": data, "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_data_res = res.post_request("/api/base/products/page", json=search_data)
        product_id = search_data_res.json()['result']['records'][0]['productId']
        product_name = search_data_res.json()['result']['records'][0]['productName']
        product_no = search_data_res.json()['result']['records'][0]['productNo']
        project_code = search_data_res.json()['result']['records'][0]['projectCode']
        validation_param = search_data_res.json()['result']['records'][0]['validationParam']
        if validation_param != "":
            edit_data = {"projectCode": project_code, "productId": product_id, "productNo": product_no,
                         "productName": product_name}
            edit_data.update(json.loads(validation_param))
            edit_data_res = res.post_request(f"/api/base/products/validationEdit/{product_id}", json=edit_data)
            assert edit_data_res.status_code == 200
            assert edit_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-解读分配配置")
    @allure.title("配置中心-解读分配配置-查询{data}配置")
    @pytest.mark.parametrize("data", ["bgiCenterDelivery", "bgiExpertServices", "siteInterpretationLib"])
    def test_interpretation_search(self, res, data):
        search_data_res = res.get_request(f"/api/base/project/interpretation/list/{data}")
        assert search_data_res.status_code == 200
        assert len(search_data_res.json()['result']) >= 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-解读分配配置")
    @allure.title("配置中心-解读分配配置-查询{data}-{data1}配置")
    @pytest.mark.parametrize("data", ["bgiCenterDelivery", "bgiExpertServices", "siteInterpretationLib"])
    @pytest.mark.parametrize("data1", ["CNV-seq", "CS", "NBS", "NIFTY"])
    def test_interpretation_search(self, res, data, data1):
        search_data_res = res.get_request(f"/api/base/project/interpretation/userDistribute/{data}/{data1}")
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-解读分配配置")
    @allure.title("配置中心-解读分配配置-更新{data}-{data1}人员投入比例配置")
    @pytest.mark.parametrize("data", ["bgiCenterDelivery", "bgiExpertServices", "siteInterpretationLib"])
    @pytest.mark.parametrize("data1", ["CNV-seq", "CS", "NBS", "NIFTY"])
    def test_interpretation_search(self, res, data, data1):
        search_data_res = res.get_request(f"/api/base/project/interpretation/userDistribute/{data}/{data1}")
        update_data = search_data_res.json()['result']
        update_res = res.post_request("/api/base/project/interpretation/updateUserDistribute", json=update_data)
        assert update_res.status_code == 200
        assert update_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-解读分配配置")
    @allure.title("配置中心-解读分配配置-更新{data}-{data1}产品分类配置")
    @pytest.mark.parametrize("data", ["bgiCenterDelivery", "bgiExpertServices", "siteInterpretationLib"])
    @pytest.mark.parametrize("data1", ["CNV-seq", "CS", "NBS", "NIFTY"])
    def test_interpretation_search(self, res, data, data1):
        search_data_res = res.get_request(f"/api/base/project/interpretation/list/{data}")
        result_data = search_data_res.json()['result']
        for item in result_data:
            inter_distribute_id = item['interpretationDistributeId']
            project_code = item['projectCode']
            project_name = item['projectName']
            user_business = item['userBusiness']
            if item['projectCode'] == data1:
                prod_classify = item['prodClassify']
                if prod_classify:
                    update_data = {"projectCode": project_code, "interpretationDistributeId": inter_distribute_id,
                                   "projectName": project_name, "userBusiness": user_business,
                                   "prodClassifyList": json.loads(prod_classify)}
                    update_res = res.post_request("/api/base/project/interpretation/updateProdClassify",
                                                  json=update_data)
                    assert update_res.status_code == 200
                    assert update_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-邮件配置")
    @allure.title("配置中心-邮件配置-查询{data}验证配置")
    @pytest.mark.parametrize("data", ["CNV-seq", "CS", "NBS", "NIFTY"])
    def test_mail_search(self, res, data):
        search_data_res = res.post_request(f"/api/base/mail/template/page/{data}", json={})
        assert search_data_res.status_code == 200
        assert search_data_res.json()['result']['total'] >= 0

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-邮件配置")
    @allure.title("配置中心-邮件配置-新增邮件配置")
    def test_mail_add(self, res_file, mysql_connect):
        form_data = {
            'mailId': '',
            'mailType': 'ReportList',
            'sendPeriod': 'Once',
            'title': 'test',
            'receiver': 'test',
            'copyer': 'test',
            'addOperationFlag': 0,
            'attachmentName': '',
            'file': '',
            'content': 'test',
            'remark': 'test',
            'fileName': '',
            'projectCode': 'NIFTY'
        }
        search_data_res = res_file.post_request("/api/base/mail/template", data=form_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'
        # 把新增的邮件配置删除
        mysql_connect.execute("delete from base_mail_template where title = 'test' and project_code = 'NIFTY'")
