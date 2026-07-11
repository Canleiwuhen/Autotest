import pytest
import allure
from data_generate.samplecenter.datagenerate import DataGenerate
from urllib.parse import urlencode
from testcase.samplecenter.anomalycenter.handle_exception_data import DataList
from utils.tools import replace_none
import requests


@pytest.mark.usefixtures("res", "token")
class TestHandleExcept:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本异常处理-查询")
    @allure.title("搜索数据：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_except_data)
    def test_query_except_data(self, res, token, data):
        token = token("testuser1")['token']
        tmp = data['task']
        data = {'task': tmp,
                'pageNumber': 1,
                'pageSize': 50,
                'token': token,
                'menuId': 'Exception_SampleException',
                'zsjd_type': 'YX'
                }
        response = res.post_request("/ybzx/webintf.do?method=query_expresscenter_data",
                                    data=urlencode(data))
        response_json = response.json()
        assert response.status_code == 200
        # assert response_json['code'] == '200'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本异常处理-查看送检单修改记录")
    def test_query_update_log(self, res, token):
        token = token("testuser1")['token']
        data = {'zsjdid': 'INSP190000502267',
                'posnr': '000001',
                'token': token,
                'menuId': 'Exception_SampleException',
                'zsjd_type': 'YX'
                }
        response = res.post_request("/ybzx/webintf.do?method=query_sjd_update_log",
                                    data=urlencode(data))
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == '200'
        assert response_json['msg'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本异常处理-导出")
    @pytest.mark.parametrize("data", DataList.file_data)
    def test_download_file(self, res, token, data):
        token = token("testuser1")['token']
        datas = {'datas': data,
                'token': token,
                'menuId': 'Exception_SampleException',
                'zsjd_type': 'YX'
                }
        response = res.post_request("/ybzx/exportSampleDetail.do?",
                                    data=urlencode(datas))
        response_json = response.json()
        assert response.status_code == 200
        assert '详情' in response_json['filePath']
        assert response_json['status'] == 'success'

    # @allure.feature("新增异常样本数据")
    # @pytest.mark.parametrize('generate_steps',
    #                          [{'route_path': 'path1', 'last_step': 1, 'run_time': 1, 'user_name': 'testuser1'}],
    #                          indirect=True)
    # def test_save_none_inspection_info(self, res, token, generate_steps):
    #     token = token("testuser1")['token']
    #     expressnum = generate_steps[0]['expressnum']
    #     sample = generate_steps[0]['sample']
    #     arrvSerie = generate_steps[0]['arrvSerie']
