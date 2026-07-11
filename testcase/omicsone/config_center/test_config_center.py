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
        # 查询已新增的质控品数据
        search_data_kit = {"pageSize": 100, "pageNum": 1, "kitId": target_kitId}
        search_data_kit_res = res.post_request("/api/base/kits/qcSample/page", json=search_data_kit)
        assert search_data_kit_res.status_code == 200
        qcSamples_tmp = []
        for i in search_data_kit_res.json()['result']['records']:
            qcSamples_tmp.append({"qcSampleType": i['qcSampleType'], "sampleTypeCode": i['sampleTypeCode'], "qcSampleNo": i['qcSampleNo'], "productNo": i['productNo']})
        assert qcSamples_tmp == add_data['qcSamples']
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
    @allure.feature("配置中心-报告配置")
    @allure.title("配置中心-报告配置-查询")
    def test_report_conf(self, res):
        project_code = ['CNV-seq', 'NIFTY', 'NBS', 'CS']
        for code in project_code:
            search_data = {"projectCode": code}
            search_data_res = res.post_request("/api/base/report/templateCategory/page", json=search_data)
            assert search_data_res.status_code == 200
            list_tmp = []
            for i in search_data_res.json()['result']['records']:
                list_tmp.append(i['category'])
            if code == 'CNV-seq':
                assert list_tmp == ['失败报告', '正式报告', '阴性报告']
            if code == 'NIFTY':
                assert list_tmp == ['单胎报告', '双胎报告', '退费报告', '重取样报告']
            if code == 'NBS' or code == 'CS':
                assert list_tmp == ['失败报告', '正式报告']

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-报告配置")
    @allure.title("配置中心-报告配置-报告命名")
    def test_report_conf(self, res):
        project_code = ['CNV-seq', 'NIFTY', 'NBS', 'CS']
        for code in project_code:
            search_url = '/api/base/reportNameRules/query/' + code
            search_data_res = res.get_request(url=search_url)
            assert search_data_res.status_code == 200
            assert search_data_res.json()['result']['projectCode'] == code

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("配置中心-报告配置")
    @allure.title("配置中心-报告配置-报告周期设置")
    def test_reportcycle_conf(self, res):
        project_code = ['CNV-seq', 'NIFTY', 'NBS', 'CS']
        for code in project_code:
            search_url = '/api/base/reportPeriodRules/query/' + code
            search_data_res = res.get_request(url=search_url)
            assert search_data_res.status_code == 200
            assert search_data_res.json()['result']['projectCode'] == code












