import pytest
import allure
from urllib.parse import urlencode


@allure.feature("样本推送SIMS")
@pytest.mark.usefixtures("res")
class TestSamplePushSims:
    query_sample_push_sims_data_list = [
        {
            "case_name": "输入样本编号",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "24X110800003"}
            }
        },
        {
            "case_name": "输入不存在的样本编号",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "24X110899999"}
            }
        }
    ]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("搜索")
    @allure.title("搜索-用例名称：{data[case_name]}")
    @pytest.mark.parametrize("data", query_sample_push_sims_data_list)
    def test_query_sample_push_sims(self, res, token, data):
        """
        样本推送SIMS查询
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
            "menuId": "SamplesToSims",
            "zsjd_type": "YX"
        }
        query_data.update(data["data"])  # 合并查询参数到通用参数
        response = res.post_request("/ybzx/webintf.do?method=query_ybzx_to_sims_list", data=urlencode(query_data))
        assert response.status_code == 200 and response.json()["code"] == "200" and response.json()[
            "msg"] == "success", f"查询样本推送SIMS失败！response：{response.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("样本推送SIMS")
    @allure.title("样本推送SIMS-用例名称：样本推送SIMS主流程")
    def test_sample_push_sims(self, res, token):
        """
        测试样本推送SIMS主流程
        :param res:
        :param token:
        :return:
        """
        # 输入样本编号后提交即可
        push_data = {
            "datas": [{"zcatalo": "24X110800003"}],
            "token": token("testuser1")["token"],
            "menuId": "SamplesToSims",
            "zsjd_type": "YX"
        }
        push_response = res.post_request("/ybzx/webintf.do?method=ybzx_push_sims", data=urlencode(push_data))
        assert push_response.status_code == 200 and push_response.json()["code"] == "200" and push_response.json()[
            "msg"] == "success", f"样本推送SIMS失败！response：{push_response.json()}"

