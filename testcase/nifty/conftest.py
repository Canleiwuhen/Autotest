import os
import json
from urllib.parse import urlencode

import pytest
import shutil
import time
import ddddocr
import requests

from data_generate.nifty.datagenerate import NiftydataGenerate
from utils.tools import sep, get_project_path, rsa_encrpt, data_to_image
from utils.handle_yaml import GetConfig
from utils.request import Requests
from data_generate.samplecenter.datagenerate import DataGenerate
from data_generate.nifty.data_route import ROUTE

# RSA加密公钥
key = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMmRhnJLei0SR/d6UkdpCgJHvF+3ygzhVh0CfPtJpSAX4SFPt75eXGw0VVKPrGQ1+FIsJF3dCHi/dq4SSHrI2fsCAwEAAQ=="
record_id = os.environ.get('LAST_RECORD_ID')
data = {
    "id": record_id
}
url = "http://127.0.0.1:8087/get_data"
response = requests.get(url, params=urlencode(data))
var_list = response.json()["message"]
if var_list[12]=="HK":
    configname = "niftyHK_config.yaml"
else:
    configname = "nifty_config.yaml"
getconf = GetConfig(configname=configname)


def login(user):
    """
    封装登录接口
    :param user: yaml文件里账号密码的用户名称
    :return: 返回登录token和用户所属片区编码，字典返回
    """
    res = Requests(configname=configname, baseurl="test_url")
    # 获取验证码
    time_13 = int(time.time() * 1000)
    uuid = str(time_13) + "_5010064645373613100053736131000"
    param = {"uuid": uuid}
    content = res.get_request("/presap/code/vcode.do", params=param).content
    cur_path = get_project_path()
    path_tmp = [cur_path, "img/nifty_code.png"]
    img_path = sep(path_tmp)
    data_to_image(content, img_path)
    # 识别图片中的验证码
    ocr = ddddocr.DdddOcr()
    with open(img_path, 'rb') as f:
        img_bytes = f.read()
    code = ocr.classification(img_bytes)

    # 取出账号密码
    username, password = getconf.get_username_password(user)
    # 构造登录接口入参
    data = {"userName": username,
            "passWord": rsa_encrpt(key, password),
            "vcode": code,
            "uuid": uuid,
            "token": "",
            "menuId": "",
            "systemSource": "frit-nifty"
            }
    # 执行接口请求
    login_res = res.post_request("/presap/user/login.do", data=data)
    if login_res.status_code == 200 and login_res.json()["code"] == "200" and login_res.json()["msg"] == "success":
        new_token = login_res.json()["data"]["token"]
        userWerks = login_res.json()["data"]["userWerks"]
        return {'token': new_token, 'userWerks': userWerks}
    elif login_res.json()["code"] == "10010":  # 验证码错误重试登录
        return login(user)

# 用例执行前的前置操作和后置操作处理，前置获取接口所需的token，后置清理类用例执行后的token信息避免失效
@pytest.fixture(scope="class")
def token():
    def _token(user):
        # 前置操作
        # 判断存放token文件的文件夹是否存在，不存在则自动创建
        token_json_dir = sep([get_project_path(), "tokendir"])
        if not os.path.exists(token_json_dir):
            os.mkdir(token_json_dir)
        # 生成用户user对应token的json文件
        token_json_path = sep([token_json_dir, "nifty_"+user + "_token.json"])
        # 若文件不存在，调用登录接口，把token写入json文件
        if not os.path.exists(token_json_path):
            print(f"{user}对应的token的json文件不存在，调用登录接口")
            # 调用登录方法，拿到token
            token = login(user)
            print(f"写入{user}对应token的json文件{token}")
            # 拿到token后，开始生成token文件，并写入token
            with open(token_json_path, "w+") as write_token:
                # 键值对的形式，方便拿取
                write_token.write(json.dumps({"token": token}))
            return token
        else:
            # 文件存在，直接取出文件里面的token
            print(f"{user}对应的token_json文件存在，直接取文件token")
            with open(token_json_path, "r") as token_info:
                token = json.loads(token_info.read())
                return token["token"]

    yield _token
    # 后置操作，测试用例类执行后清除token的json文件
    token_json_dir = sep([get_project_path(), "tokendir"])
    for filename in os.listdir(token_json_dir):
        file_path = os.path.join(token_json_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# 涉及读取参数文件的配置，前置操作返回requests实例化对象，避免多处维护
@pytest.fixture
def res():
    res = Requests(configname=configname, baseurl="test_url", headers={"content-type": "application/x-www-form-urlencoded"})
    return res

@pytest.fixture
def send_file():
    send_file = Requests(configname=configname, baseurl="test_url", headers={"multipart/form-data; boundary=----WebKitFormBoundary7TPD6gp0EuUeDAqr"})
    return send_file

@pytest.fixture
def res_json():
    res_json = Requests(configname=configname, baseurl="test_url", headers={"content-type": "application/json;charset=UTF-8"})
    return res_json

@pytest.fixture
def generate_steps(request):
    """
    :param request:
      route_path 要执行的技术路线
      last_step 执行技术路线的最终步骤编号
      run_time 传次数，执行几次，造几遍数据
      user_name 执行造数所登录的用户
    :return: 返回造数过程中所有产物，对应造数据类DataGenerate下的所有类变量，返回数据类型为列表中多个字典值[{'sample': ['24X101600015'], 'expressnum': 'SF20241016165713', 'container_prefix': 'autotest_1729069044'.....},{}......]
    """
    route_path = request.param['route_path']
    last_step = request.param['last_step']
    run_times = request.param['run_time']
    user = request.param['user_name']
    istest = request.param['istest']
    login_result = login(user)
    token = login_result['token']
    area_code = login_result['userWerks']
    tmp = NiftydataGenerate(token, area_code, istest)
    # token = login(user)['token']
    # area_code = login(user)['userWerks']
    # tmp = NiftydataGenerate(area_code,token)
    # 获取对应的技术路线信息
    switch_step = ROUTE[route_path]
    result = []
    for n in range(run_times):
        for i in range(last_step + 1):
            funname = switch_step.get(i)
            getattr(tmp, funname)()
        # 获取实例化对象的所有类变量
        varlist = vars(tmp)
        # 剔除不需要的类变量
        remove_key = ['token','configname','area_code','chr_info','sample_excel_list','lane_index_info','config_info', 'datafactory_res', 'samplecenter_res', 'nifty_res', 'nifty_api_res','date_str','time_str','datatime_str','container_prefix','specifications','abnormal_input']
        new_dict = {k: v for k, v in varlist.items() if k not in remove_key}
        result.append(new_dict)
    return result

