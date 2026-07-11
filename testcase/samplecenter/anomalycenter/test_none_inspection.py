import pytest
import allure
from data_generate.samplecenter.datagenerate import DataGenerate
from urllib.parse import urlencode
from testcase.samplecenter.anomalycenter.none_inspection_data import DataList
from utils.tools import replace_none
import requests


@pytest.mark.usefixtures("res", "token")
class TestNoneInspection:
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.feature("添加无单信息样本")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 1, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_save_none_inspection_info(self, res, token, generate_steps):
        token = token("testuser1")['token']
        expressnum = generate_steps[0]['expressnum']
        sample = generate_steps[0]['sample']
        arrvSerie = generate_steps[0]['arrvSerie']
        test = DataGenerate(token=token)
        container_info = test.create_container(container_prefix='WDYB')
        tmp = [{"isNew": 'true',
                "zexpressnumber": expressnum,
                "zarrvseries": arrvSerie,
                "zplate_num": container_info[0],
                "zplate": container_info[1],
                "zpoint": "A01",
                "zcatalo": sample,
                "zewbez": "CESHI",
                "matnr": "DX1605",
                "bezei": "",
                "zkuname": "",
                "zsamplename1": "",
                "zyblx_name": "",
                "zsjemail": "",
                "zycdm": "01",
                "zenote": "",
                "znotes": "",
                "zname": "test1",
                "zyblx": "血浆",
                "status": "I"}]
        data = {'task': tmp,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'}
        response = res.post_request("/ybzx/webintf.do?method=save_or_update_none_inspection_info", data=urlencode(data))
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == '200'
        assert response_json['msg'] == '保存成功'
        assert 'WDYB' in response_json['invokeInfo']

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.feature("无单样本搜索数据")
    @allure.title("搜索数据：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.query_none_inspection_list)
    def test_query_none_inspection(self, res, token, data):
        token = token("testuser1")['token']
        tmp = data['task']
        data = {'task': tmp,
                'pageNumber': 1,
                'pageSize': 50,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'
        }
        response = res.post_request("/ybzx/webintf.do?method=query_none_inspection_list",
                                    data=urlencode(data))
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == '200'
        assert response_json['msg'] == None
        assert 'WDYB' in response_json['invokeInfo']

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.feature("无单样本编辑数据")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 1, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_update_none_inspection(self, res, token, generate_steps):
        token = token("testuser1")['token']
        expressnum = generate_steps[0]['expressnum']
        sample = generate_steps[0]['sample']
        arrvSerie = generate_steps[0]['arrvSerie']
        test = DataGenerate(token=token)
        container_info = test.create_container(container_prefix='WDYB')
        tmp = [{"isNew": 'true',
                "zexpressnumber": expressnum,
                "zarrvseries": arrvSerie,
                "zplate_num": container_info[0],
                "zplate": container_info[1],
                "zpoint": "A01",
                "zcatalo": sample,
                "zewbez": "CESHI",
                "matnr": "DX1605",
                "bezei": "",
                "zkuname": "",
                "zsamplename1": "",
                "zyblx_name": "",
                "zsjemail": "",
                "zycdm": "01",
                "zenote": "",
                "znotes": "",
                "zname": "test1",
                "zyblx": "血浆",
                "status": "I"}]
        data = {'task': tmp,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'}
        # 先新增无单样本
        res.post_request("/ybzx/webintf.do?method=save_or_update_none_inspection_info", data=urlencode(data))
        # 查询无单样本信息
        data = {'task': {"zybzx": "X", "zcatalo": sample},
                'pageNumber': 1,
                'pageSize': 50,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'
                }
        query_response = res.post_request("/ybzx/webintf.do?method=query_none_inspection_list",
                                    data=urlencode(data)).json()
        task = query_response['data'][0]
        task['bezei'] = '广东省'
        task['status'] = 'U'
        task = replace_none(task)
        # 锁定样本信息
        lock_data = {'task': [{"zcatalo": sample}],
                     'token': token,
                     'menuId': 'Exception_NoInspectionSampleException',
                     'zsjd_type': 'YX'}
        res.post_request("/ybzx/webintf.do?method=sample_lock",
                                    data=urlencode(lock_data)).json()

        # 更新无单样本信息
        edit_data = {'task': [task],
                     'token': token,
                     'menuId': 'Exception_NoInspectionSampleException',
                     'zsjd_type': 'YX'}
        edit_response = res.post_request("/ybzx/webintf.do?method=save_or_update_none_inspection_info",
                                    data=urlencode(edit_data))
        edit_response_json = edit_response.json()
        assert edit_response.status_code == 200
        assert edit_response_json['code'] == '200'
        assert edit_response_json['msg'] == '保存成功'

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.feature("无单样本异常邮件")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 1, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_send_email_none_inspection(self, res, token, generate_steps):
        token = token("testuser1")['token']
        expressnum = generate_steps[0]['expressnum']
        sample = generate_steps[0]['sample']
        arrvSerie = generate_steps[0]['arrvSerie']
        test = DataGenerate(token=token)
        container_info = test.create_container(container_prefix='WDYB')
        tmp = [{"isNew": 'true',
                "zexpressnumber": expressnum,
                "zarrvseries": arrvSerie,
                "zplate_num": container_info[0],
                "zplate": container_info[1],
                "zpoint": "A01",
                "zcatalo": sample,
                "zewbez": "CESHI",
                "matnr": "DX1605",
                "bezei": "",
                "zkuname": "",
                "zsamplename1": "",
                "zyblx_name": "",
                "zsjemail": "",
                "zycdm": "01",
                "zenote": "",
                "znotes": "",
                "zname": "test1",
                "zyblx": "血浆",
                "status": "I"}]
        data = {'task': tmp,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'}
        # 先新增无单样本
        res.post_request("/ybzx/webintf.do?method=save_or_update_none_inspection_info", data=urlencode(data))
        # 发送异常邮件
        email_data = {"zcatalo": sample,
                      "subject": "深圳样本中心反馈异常样本邮件",
                      "zsjemail": "chenqingrong@genomics.cn",
                      "ztext": "<p>各位好:</p><p></p><p>以下样本异常，请及时处理，确认后请回复到样本中心公邮：产前：P_sz_sample@genomics.cn+非产前：lc-b2c@genomics.cn，此邮件是系统发送，请勿直接回复。</p><p>"}
        data = {'task': email_data,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'}
        response = res.post_request("/ybzx/webintf.do?method=none_inspection_email_send",
                                    data=urlencode(data))
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == '200'
        assert response_json['msg'] == '发送成功'

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.feature("无单销毁")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 1, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_destroy_none_inspection(self, res, token, generate_steps):
        token = token("testuser1")['token']
        expressnum = generate_steps[0]['expressnum']
        sample = generate_steps[0]['sample']
        arrvSerie = generate_steps[0]['arrvSerie']
        test = DataGenerate(token=token)
        container_info = test.create_container(container_prefix='WDYB')
        tmp = [{"isNew": 'true',
                "zexpressnumber": expressnum,
                "zarrvseries": arrvSerie,
                "zplate_num": container_info[0],
                "zplate": container_info[1],
                "zpoint": "A01",
                "zcatalo": sample,
                "zewbez": "CESHI",
                "matnr": "DX1605",
                "bezei": "",
                "zkuname": "",
                "zsamplename1": "",
                "zyblx_name": "",
                "zsjemail": "",
                "zycdm": "01",
                "zenote": "",
                "znotes": "",
                "zname": "test1",
                "zyblx": "血浆",
                "status": "I"}]
        data = {'task': tmp,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'}
        # 先新增无单样本
        res.post_request("/ybzx/webintf.do?method=save_or_update_none_inspection_info", data=urlencode(data))
        # 销毁无单样本
        destroy_data = {'task': [{"zcatalo": sample}],
                        'token': token,
                        'menuId': 'Exception_NoInspectionSampleException',
                        'zsjd_type': 'YX'}
        response = res.post_request("/ybzx/webintf.do?method=none_inspection_destroy",
                                    data=urlencode(destroy_data))
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == '200'
        assert response_json['msg'] == '无单销毁成功！'

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.feature("无单样本转寄")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 1, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_forward_sample(self, res, token, generate_steps):
        token = token("testuser1")['token']
        expressnum = generate_steps[0]['expressnum']
        sample = generate_steps[0]['sample']
        arrvSerie = generate_steps[0]['arrvSerie']
        test = DataGenerate(token=token)
        container_info = test.create_container(container_prefix='WDYB')
        tmp = [{"isNew": 'true',
                "zexpressnumber": expressnum,
                "zarrvseries": arrvSerie,
                "zplate_num": container_info[0],
                "zplate": container_info[1],
                "zpoint": "A01",
                "zcatalo": sample,
                "zewbez": "CESHI",
                "matnr": "DX1605",
                "bezei": "",
                "zkuname": "",
                "zsamplename1": "",
                "zyblx_name": "",
                "zsjemail": "",
                "zycdm": "01",
                "zenote": "",
                "znotes": "",
                "zname": "test1",
                "zyblx": "血浆",
                "status": "I"}]
        data = {'task': tmp,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'}
        # 先新增无单样本
        res.post_request("/ybzx/webintf.do?method=save_or_update_none_inspection_info", data=urlencode(data))
        # 转寄样本
        forward_data = {'task': [{"zcatalo": sample, "znote":"测试转寄"}],
                        'token': token,
                        'menuId': 'Exception_NoInspectionSampleException',
                        'zsjd_type': 'YX'}
        response = res.post_request("/ybzx/webintf.do?method=forward_sample",
                                    data=urlencode(forward_data))
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == '200'
        assert response_json['msg'] == '无单转寄成功！'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("无单样本导出全部")
    def test_export_all_none_inspection(self, res_json, token):
        token1 = token("testuser1")['token']
        header = {"content-type": "application/json;charset=UTF-8"}
        data = {'pageNumber': 1,
                'pageSize': 50,
                'exportCurrentPage': False,
                'task': '{\"zcdate\":\"20241008\",\"zcdateend\":\"20241014\"}',
                'token': token1
                }
        url = "https://sample-test.bgi.com/ybzx/exportNoneInspectionData.do"
        # response = res_json.post_request("/ybzx/exportNoneInspectionData.do", json=data)
        response = requests.request("post", url, headers=header, json=data)
        print(response.headers)
        assert response.status_code == 200

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("无单样本导出本页")
    def test_export_all_none_inspection(self, res_json, token):
        token1 = token("testuser1")['token']
        header = {"content-type": "application/json;charset=UTF-8"}
        data = {'pageNumber': 1,
                'pageSize': 50,
                'exportCurrentPage': True,
                'task': '{\"zcdate\":\"20241008\",\"zcdateend\":\"20241014\"}',
                'token': token1
                }
        url = "https://sample-test.bgi.com/ybzx/exportNoneInspectionData.do"
        # response = res_json.post_request("/ybzx/exportNoneInspectionData.do", json=data)
        response = requests.request("post", url, headers=header, json=data)
        print(response.headers)
        assert response.status_code == 200

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.feature("无单样本自动到样")
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': 'path2', 'last_step': 1, 'run_time': 1, 'user_name': 'testuser1'}],
                             indirect=True)
    def test_auto_to_sample(self, res, token, generate_steps):
        token = token("testuser1")['token']
        expressnum = generate_steps[0]['expressnum']
        sample = generate_steps[0]['sample']
        arrvSerie = generate_steps[0]['arrvSerie']
        test = DataGenerate(token=token)
        container_info = test.create_container(container_prefix='WDYB')
        tmp = [{"isNew": 'true',
                "zexpressnumber": expressnum,
                "zarrvseries": arrvSerie,
                "zplate_num": container_info[0],
                "zplate": container_info[1],
                "zpoint": "A01",
                "zcatalo": sample,
                "zewbez": "CESHI",
                "matnr": "DX1605",
                "bezei": "",
                "zkuname": "",
                "zsamplename1": "",
                "zyblx_name": "",
                "zsjemail": "",
                "zycdm": "01",
                "zenote": "",
                "znotes": "",
                "zname": "test1",
                "zyblx": "血浆",
                "status": "I"}]
        data = {'task': tmp,
                'token': token,
                'menuId': 'Exception_NoInspectionSampleException',
                'zsjd_type': 'YX'}
        # 先新增无单样本
        res.post_request("/ybzx/webintf.do?method=save_or_update_none_inspection_info", data=urlencode(data))
        # 前端工作平台录入送检单
        new_sample = test.sumbit_sample()[0]
        # 修改无单样本编号为新录入送检单的样本编号
        modify_data = {'task': {"zcatalo_old": sample, "zcatalo_new": new_sample},
                       'token': token,
                       'menuId': 'Exception_NoInspectionSampleException',
                       'zsjd_type': 'YX'}
        res.post_request("/ybzx/webintf.do?method=modify_sample", data=urlencode(modify_data))
        # 执行查询
        query_data = {'task':{"zybzx": "X", "zcatalo": new_sample},
                      'pageNumber': 1,
                      'pageSize': 50,
                      'token': token,
                      'menuId': 'Exception_NoInspectionSampleException',
                      'zsjd_type': 'YX'}
        query_response = res.post_request("/ybzx/webintf.do?method=query_none_inspection_list",
                                    data=urlencode(query_data)).json()
        if query_response['data'][0]['zsign'] == '02':
            # 执行自动到样
            auto_data = {'task': [{"zcatalo": new_sample, "zplate_num": container_info[0], "zpoint": "A01",
                                   "zexpressnumber": expressnum}],
                         'token': token,
                         'menuId': 'Exception_NoInspectionSampleException',
                         'zsjd_type': 'YX'}
            response = res.post_request("/ybzx/webintf.do?method=none_inspection_auto_to_sample",
                                        data=urlencode(auto_data))
            response_json = response.json()
            assert response.status_code == 200
            assert response_json['code'] == '200'
            assert response_json['msg'] == '保存成功数据保存成功！'
        else:
            print('样本状态不满足！')















