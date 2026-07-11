import pytest
import allure
from celery.bin.result import result

import app
from data_generate.nifty.datagenerate import NiftydataGenerate
from urllib.parse import urlencode
from testcase.samplecenter.anomalycenter.none_inspection_data import DataList
from utils.logger import logger_other as logger
from utils.tools import replace_none
import requests
import os

record_id = os.environ.get('LAST_RECORD_ID')
data = {
    "id": record_id
}
url = "http://127.0.0.1:8087/get_data"
response = requests.get(url, params=urlencode(data))
var_list = response.json()["message"]
# with open('var_dir/nifty/var.txt', 'r', encoding='utf-8') as file:
#     # 按行读取
#     var_list = []
#     for line in file:
#         # 处理每一行
#         var_list.append(line.strip())
# logger.info(f"输入参数：{str(var_list)}")


@pytest.mark.usefixtures("res", "token")
class TestApi:
    @pytest.mark.parametrize('generate_steps',
                             [{'route_path': var_list[1], 'last_step': int(var_list[2]), 'run_time': int(var_list[4]),
                               'user_name': var_list[5],'istest':False}],
                             indirect=True)
    def test_api_tools(self, token, generate_steps):
        try:
            # token = token(var_list[5])['token']
            # area_code = token(var_list[5])['userWerks']
            # NiftydataGenerate(area_code=area_code,token=token)
            # files = os.listdir('var_dir/nifty')
            # for i in files:
            #     if i.startswith('nifty'):
            #         os.remove('var_dir/nifty/'+i)
            # for i in range(int(var_list[4])):
            #     filename = f"nifty_var{i}.txt"
            #     with open('var_dir/nifty/'+filename, 'w', encoding='utf-8') as file:
            #         file.write("")
            #         file.write(str([generate_steps[i]]) + '\n')
            result_list = []
            for i in range(int(var_list[4])):
                result_data = str([generate_steps[i]])
                result_list.append(result_data)
            headers = {'Content-Type': 'application/json'}
            data = {
                "data": result_list,
            }
            requests.post("http://127.0.0.1:8087/update_data", json=data, headers=headers)
        except Exception as e:
            return str(e)














