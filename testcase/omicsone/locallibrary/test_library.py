import pytest
import allure




@pytest.mark.usefixtures("res")
class TestLibrary:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("本地库")
    @allure.title("本地库-查询")
    def test_library_search(self, res):
        search_data = {"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_data_res = res.post_request("/api/knowledgebase/case/query", json=search_data)
        assert search_data_res.status_code == 200
        assert search_data_res.json()['retInfo'] == 'success'

