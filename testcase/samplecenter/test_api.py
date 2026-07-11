import pytest
import allure
from data_generate.samplecenter.datagenerate import DataGenerate
from urllib.parse import urlencode
from testcase.samplecenter.anomalycenter.none_inspection_data import DataList
from utils.logger import logger_other as logger
from utils.tools import replace_none
import requests
import os

with open('var_dir/sample/var.txt', 'r') as file:
    # 按行读取
    var_list = []
    for line in file:
        # 处理每一行
        var_list.append(line.strip())
# logger.info(f"输入参数：{str(var_list)}")


@pytest.mark.usefixtures("res", "token")
class TestApi:
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': var_list[0], 'last_step': int(var_list[1]), 'run_time': int(var_list[2]),
                               'user_name': var_list[3]}],
                             indirect=True)
    def test_api_tools(self, token, generate_steps):
        token = token(var_list[3])['token']
        DataGenerate(token=token)
        files = os.listdir('var_dir/sample')
        for i in files:
            if i.endswith('.txt'):
                os.remove('var_dir/sample/'+i)
        for i in range(int(var_list[2])):
            filename = f"var{i}.txt"
            with open('var_dir/sample/'+filename, 'w') as file:
                file.write("")
                file.write(str([generate_steps[i]]) + '\n')















