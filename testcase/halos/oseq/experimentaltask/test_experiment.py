# -*- coding: utf-8 -*-
import json

import pytest
import allure
import os

from testcase.omicsone.conftest import pre_field_config
from utils.tools import calculate_file_buffer
from testcase.halos.oseq.experimentaltask.experiment_data import DataList
from testcase.omicsone.experimentaltask.conftest import handle_upload_file


@pytest.mark.usefixtures("res", "res_file")
class TestExperiment:
    """
    制作了样本编号和板号的查询，OSEQ实验中心没环境
    """

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("自动化实验任务-查询")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search(self, res, data):
        tmp = data['search_items']
        json_data = {
            "page": 1,
            "size": 100,
        }
        json_data.update(tmp)
        response = res.post_request("/prod-api/api/oseq/experimental/task/page", json=json_data)
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert response.json()['retCode'] == 0



    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.feature("自动化实验任务-创建实验任务")
    # @allure.title("{data[case_name]}")
    # @pytest.mark.parametrize("data", DataList.experiment_data)
    # def test_create_task(self, res, handle_experiment_task, data):
    #     status_code = handle_experiment_task["status_code"]
    #     json = handle_experiment_task["json"]
    #     assert status_code == 200
    #     assert json['retInfo'] == 'success'
