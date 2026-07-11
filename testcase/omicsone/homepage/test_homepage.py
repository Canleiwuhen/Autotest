import pytest
import allure


@pytest.mark.usefixtures("res")
class TestHomepage:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("首页")
    @allure.title("首页-查询")
    def test_home_search(self, res):
        # 待处理样本数据
        search_data = {"dateType": "collectDate", "dateTime": ["2025-09-24", "2025-12-24"],
                       "collectDate": "2025-09-24,2025-12-24"}
        search_data_res = res.post_request("/api/homepage/sample/list", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'
        # 样本量增长趋势
        search_data_growth_res = res.post_request("/api/homepage/sample/growth", json=search_data)
        assert search_data_growth_res.status_code == 200
        assert search_data_growth_res.json()['retInfo'] == 'success'
        # 资源监控
        search_data_resource_res = res.get_request(url='/api/homepage/resource')
        assert search_data_resource_res.status_code == 200
        assert search_data_resource_res.json()['retInfo'] == 'success'
        # 样本进度查询
        search_data_progress = {"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100, "dateType": "collectDate",
                                    "dateTime": ["2025-09-24", "2025-12-24"], "collectDate": "2025-09-24,2025-12-24"}
        search_data_progress_res = res.post_request("/api/homepage/progress", json=search_data_progress)
        assert search_data_progress_res.status_code == 200
        assert search_data_progress_res.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("首页")
    @allure.title("首页-版本信息查询")
    def test_systeminfo_search(self, res):
        search_data_res = res.post_request("/api/base/system/systemInfo")
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'
        assert search_data_res.json()['result']['version'] is not None




