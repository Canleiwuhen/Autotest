import pytest

import sys

sys.path.append("Z:\\auto_test\\apiforward")

from utils.handle_db import HandleDB
from utils.tools import sep, get_project_path, rsa_encrpt, data_to_image
from utils.handle_yaml import GetConfig
from utils.request import Requests

# RSA加密公钥
key = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMVlSrnimCsDHMNIcAtDEJMJBKSgsyitizolJIV1rzInvAwDNhaX5TBohzVY/hqkKgbAwMiysfoJ5TaD14slzIsCAwEAAQ=="
getconf = GetConfig(configname="omicscloud_config.yaml")


def login(user):
    """
    封装登录接口
    :param user: yaml文件里账号密码的用户名称
    :return: 返回登录token和用户所属片区编码，字典返回
    """
    res = Requests(configname="omicscloud_config.yaml", baseurl="test_url")
    # 取出账号密码
    username, password = getconf.get_username_password(user)
    # 构造登录接口入参
    data = {"userName": rsa_encrpt(key, username),
            "passWord": rsa_encrpt(key, password)
            }
    # 执行接口请求
    login_res = res.post_request(url="/api/base/system/login", json=data)
    if login_res.status_code == 200:
        new_token = login_res.json()["result"]["token"]
        return new_token


# 涉及读取参数文件的配置，前置操作返回requests实例化对象，避免多处维护
@pytest.fixture(scope="class")
def res():
    token = login('sitest')
    header = {"content-type": "application/json", "omics-vtk": token}
    res = Requests(configname="omicscloud_config.yaml", baseurl="test_url", headers=header)
    return res


@pytest.fixture(scope="class")
def res_1():
    token = login('sitest1')
    header = {"content-type": "application/json", "omics-vtk": token}
    res_1 = Requests(configname="omicscloud_config.yaml", baseurl="test_url", headers=header)
    return res_1


@pytest.fixture(scope="class")
def res_cloud():
    token = login('sitest2')
    header = {"content-type": "application/json", "omics-vtk": token}
    res_cloud = Requests(configname="omicscloud_config.yaml", baseurl="test_url", headers=header)
    return res_cloud


@pytest.fixture(scope="class")
def res_file():
    token1 = login('sitest1')
    header = {"omics-vtk": token1}  # 请求头不加content-type，不理解
    res_file = Requests(configname="omicscloud_config.yaml", baseurl="test_url", headers=header)
    return res_file


@pytest.fixture(scope="class")
def res_cus():
    """
    夹具工厂，自定义登录的账号，可传入对应的账号和密码，明文
    :param request:
    :return:
    """
    def _longin(username, pwd):
        data = {"userName": rsa_encrpt(key, username),
                "passWord": rsa_encrpt(key, pwd)
                }
        res = Requests(configname="omicscloud_config.yaml", baseurl="test_url")
        # 执行接口请求
        login_res = res.post_request(url="/api/base/system/login", json=data)
        return login_res
    return _longin
#
#
# def res_change(product):
#     # 该账号用于更换检测项目权限，仅适用于配置单个检测项目的账号
#     sql = f"update base_user_project set project_code = '{product}' where user_id = 540947205813571584"
#     mysql_connect().execute(sql)
#     token = login('sitest2')
#     header = {"content-type": "application/json", "omics-vtk": token}
#     res = Requests(configname="omicsone_config.yaml", baseurl="test_url", headers=header)
#     return res
#
#
@pytest.fixture(scope="function")
def mysql_connect():
    mysql_config = getconf.get_mysql_config()
    mysql_conn = HandleDB(mysql_config['host'], mysql_config['port'], mysql_config['user'], mysql_config['password'],
                          mysql_config['db'])
    yield mysql_conn
    try:
        mysql_conn.close_database()
    except Exception as e:
        print(f"关闭数据库连接失败: {e}")


#
#
# def pre_field_config(product, page):
#     new_base_fields = dict()
#     new_project_fields = dict()
#     data = {"configModule": page}
#     res = res_change(product)
#     response = res.post_request("/api/base/searchconfig/config/fields", json=data)
#     if response.status_code == 200:
#         project_fields = response.json()['result']['projectFields']  # 全量字段
#         base_fields = response.json()['result']['baseFields']  # 常用字段
#         for i in base_fields:
#             new_base_fields.update({i["fieldCode"]: i["fieldName"]})
#         print(f"{project_fields[0]['projectCode']} 项目 new_base_fields 值为:{new_base_fields}")
#
#         for i in project_fields:
#             new_project_fields.update({i["fieldCode"]: i["fieldName"]})
#         print(f"{project_fields[0]['projectCode']} 项目 new_project_fields 值为:{new_project_fields}")
#     yield new_base_fields, new_project_fields


if __name__ == '__main__':
    login('sitest')
