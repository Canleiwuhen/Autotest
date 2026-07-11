import pytest
import allure
from utils.handle_yaml import GetConfig
from utils.tools import calculate_file_buffer



@pytest.mark.usefixtures("res")
class TestDatamanage:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-测序文件-查询")
    def test_sequence_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 500, "pageSize": 500, "moduleCode": "Sequencing"}
        search_data_res = res.post_request("/api/dataManage/fileSearch", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-分析文件-查询")
    def test_analysis_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 500, "pageSize": 500, "moduleCode": "Analysis"}
        search_data_res = res.post_request("/api/dataManage/fileSearch", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-解读文件-查询")
    def test_interpre_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 500, "pageSize": 500, "moduleCode": "Interpretation"}
        search_data_res = res.post_request("/api/dataManage/fileSearch", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-报告文件-查询")
    def test_report_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 500, "pageSize": 500, "moduleCode": "Report"}
        search_data_res = res.post_request("/api/dataManage/reportFileSearch", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-删除记录-查询")
    def test_soperationslog_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 500, "pageSize": 500}
        search_data_res = res.post_request("/api/dataManage/operationsLogSearch", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-备份设置-查询")
    def test_backupconfig_search(self, res):
        items = ['Sequencing', 'Analysis', 'Interpretation', 'Report']
        for item in items:
            param_data = {"moduleCode": item}
            search_data_res = res.get_request("/api/dataManage/getAutoBackupConfig", params=param_data)
            assert search_data_res.status_code == 200
            assert search_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-测序文件-子集文件夹查询")
    def test_sequence_subfile_search(self, res):
        search_sequence_data = {"page": 1, "pageNum": 1, "limit": 500, "pageSize": 500, "moduleCode": "Sequencing"}
        search_sequence_data_res = res.post_request("/api/dataManage/fileSearch", json=search_sequence_data)
        tmp_data = search_sequence_data_res.json()['result']['records'][0]
        search_sequence_subfile_data = {"batchId": tmp_data['batchId'],
                                        "folderPath": tmp_data['folderPath'],
                                        "moduleCode": "Sequencing"}
        search_sequence_subfile_data_res = res.post_request("/api/dataManage/subFileFolder", json=search_sequence_subfile_data)
        assert search_sequence_subfile_data_res.status_code == 200
        assert search_sequence_subfile_data_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("数据管理")
    @allure.title("数据管理-报告文件-下载文件")
    def test_report_downLoad(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 500, "pageSize": 500, "moduleCode": "Report"}
        search_data_res = res.post_request("/api/dataManage/reportFileSearch", json=search_data)
        tmp_data = search_data_res.json()['result']['records'][0]
        url = GetConfig(configname="omicsone_config.yaml", baseurl="test_url").get_url()
        download_data = {"moduleCode": "Report", "hostUrl": url, "downFileList": [tmp_data]}
        download_data_res = res.post_request("/api/dataManage/downLoad/getDownLoadFileMode", json=download_data)
        if download_data_res.status_code == 200:
            file_size = calculate_file_buffer(download_data_res)
            assert file_size > 0  # 判断文件非空文件
