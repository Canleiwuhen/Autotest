# -*- coding: utf-8 -*-
import pytest
import allure
from testcase.halos.oseq.interpretationcenter.interpretation_data import DataList


@pytest.mark.usefixtures("res")
class TestInterpretation:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-查询")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search(self, res, data):
        tmp = data['search_items']
        json_data = {
            "page": 1,
            "size": 200
        }
        json_data.update(tmp)
        response = res.post_request("/prod-api/api/oseq/reads/batch/page", json=json_data)
        assert response.status_code == 200
        assert response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-查看解读详情")
    @allure.title("查看解读详情")
    def test_query_interpretation_detail(self, res):
        query_response = res.post_request("/prod-api/api/oseq/reads/batch/page", json={"page": 1, "size": 100})
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        batch_no = query_response.json()['result']['rows'][0]['batchNo']
        detail_response = res.post_request("/prod-api/api/oseq/reads/page/sampleByBatchNo", json={"batchNo": batch_no})
        assert detail_response.status_code == 200
        assert detail_response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-重解读")
    @allure.title("重解读")
    def test_interpretation_reread(self, res):
        batch_response = res.post_request("/prod-api/api/oseq/reads/batch/page", json={"page": 1, "size": 100})
        assert batch_response.status_code == 200
        assert batch_response.json().get('success') == True

        for batch_item in batch_response.json()['result']['rows']:
            detail_response = res.post_request("/prod-api/api/oseq/reads/page/sampleByBatchNo",
                                               json={"batchNo": batch_item['batchNo']})
            assert detail_response.status_code == 200
            assert detail_response.json().get('success') == True

            for row in detail_response.json()['result']['rows']:
                if row.get('readStatus') == 2:
                    task_id = row.get('taskId')
                    reread_response = res.post_request("/prod-api/api/oseq/reads/reread", json={"taskId": task_id})
                    assert reread_response.status_code == 200
                    assert reread_response.json().get('success') == True
                    return

        assert False, "未找到 readStatus 为 2 的任务"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-生成报告")
    @allure.title("生成报告")
    def test_interpretation_generatereport(self, res):
        batch_response = res.post_request("/prod-api/api/oseq/reads/batch/page", json={"page": 1, "size": 100})
        assert batch_response.status_code == 200
        assert batch_response.json().get('success') == True

        for batch_item in batch_response.json()['result']['rows']:
            detail_response = res.post_request("/prod-api/api/oseq/reads/page/sampleByBatchNo",
                                               json={"batchNo": batch_item['batchNo']})
            assert detail_response.status_code == 200
            assert detail_response.json().get('success') == True

            for row in detail_response.json()['result']['rows']:
                if row.get('readStatus') == 4:
                    generate_data = {
                        "batchNo": batch_item['batchNo'],
                        "exProgramDtoList": [{
                            "batchSubNo": row.get('batchSubNo'),
                            "sampleId": row.get('sampleId'),
                            "inputFlag": 0
                        }]
                    }
                    generate_response = res.post_request("/prod-api/api/oseq/reads/generateReport", json=generate_data)
                    assert generate_response.status_code == 200
                    assert generate_response.json().get('success') == True
                    return

        assert False, "未找到 readStatus 为 4 的任务"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-结果导出")
    @allure.title("结果导出")
    def test_interpretation_resultexport(self, res):
        batch_response = res.post_request("/prod-api/api/oseq/reads/batch/page", json={"page": 1, "size": 100})
        assert batch_response.status_code == 200
        assert batch_response.json().get('success') == True

        for batch_item in batch_response.json()['result']['rows']:
            detail_response = res.post_request("/prod-api/api/oseq/reads/page/sampleByBatchNo",
                                               json={"batchNo": batch_item['batchNo']})
            assert detail_response.status_code == 200
            assert detail_response.json().get('success') == True

            for row in detail_response.json()['result']['rows']:
                if row.get('readStatus') == 4:
                    export_data = {
                        "batchNo": batch_item['batchNo'],
                        "readExportDtoList": [{
                            "batchSubNo": row.get('batchSubNo'),
                            "sampleId": row.get('sampleId')
                        }]
                    }
                    export_response = res.post_request("/prod-api/api/oseq/reads/resultExport", json=export_data)
                    assert export_response.status_code == 200
                    assert len(export_response.content) > 0
                    return

        assert False, "未找到 readStatus 为 4 的任务"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-让步解读")
    @allure.title("让步解读")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("解读中心-让步解读")
    @allure.title("让步解读")
    def test_interpretation_concessionread(self, res):
        batch_response = res.post_request("/prod-api/api/oseq/reads/batch/page", json={"page": 1, "size": 100})
        assert batch_response.status_code == 200
        assert batch_response.json().get('success') == True

        for batch_item in batch_response.json()['result']['rows']:
            detail_response = res.post_request("/prod-api/api/oseq/reads/page/sampleByBatchNo",
                                               json={"batchNo": batch_item['batchNo']})
            assert detail_response.status_code == 200
            assert detail_response.json().get('success') == True

            for row in detail_response.json()['result']['rows']:
                if row.get('sampleQcResult') == 1:
                    library_type_response = res.post_request("/prod-api/api/oseq/reads/reread/libraryType",
                                                             json={"batchNo": batch_item['batchNo'],
                                                                   "sampleIds": [row.get('sampleId')]})
                    assert library_type_response.status_code == 200
                    assert library_type_response.json().get('success') == True

                    venus_reread_sub2_list = [
                        {"batchSubNo": lib.get('batchSubNo'), "taskId": lib.get('taskId'),
                         "libraryType": lib.get('libraryType')}
                        for item in library_type_response.json().get('result', [])
                        for lib in item.get('libraryTypeBaseList', [])
                    ]
                    if len(venus_reread_sub2_list) == 0:
                        continue

                    concession_response = res.post_request("/prod-api/api/oseq/reads/reread", json={
                        "batchNo": batch_item['batchNo'],
                        "rereadFlag": 1,
                        "rereadSubs": [{"sampleId": row.get('sampleId'), "venusRereadSub2List": venus_reread_sub2_list}]
                    })
                    assert concession_response.status_code == 200
                    if concession_response.json().get('success') == True:
                        return

        assert False, "未找到可进行让步解读的样本"