import pytest
import allure



@pytest.mark.usefixtures("res")
class TestLogin:
    comdata = {
        "userName": "test_login_user",
        "userRealName": "测试123123",
        "projectCodeList": [
            "CNV-seq",
            "NIFTY",
            "NBS",
            "CS"
        ],
        "rolesIdList": [
            "444516187007746048"
        ],
        "password": "test123123@123",
        "passwordConfirm": "test123123@123",
        "userMobile": "15361476671",
        "userEmail": "15361476671@163.com",
        "userId": ""
    }

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("登录")
    @allure.title("登录-错误密码登录")
    def test_login_ero(self, res, res_cus):
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        # 错误的账号密码登录
        username = "test_login_user"
        pwd = "test123123@555"
        login_res = res_cus(username, pwd)
        assert login_res.status_code == 200
        assert login_res.json()["retInfo"] == '用户名或密码错误'
        # 测试后删除数据
        search_data = {"userName": "test_login_user", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("登录")
    @allure.title("登录-登录用户不存在")
    def test_login_erouser(self, res, res_cus):
        data = self.comdata
        # 新增用户操作
        res.post_request("/api/base/user/add", json=data)
        # 不存在的登录用户
        username = "test_login_user1"
        pwd = "test123123@123"
        login_res = res_cus(username, pwd)
        assert login_res.status_code == 200
        assert login_res.json()["retInfo"] == '用户名或密码错误'
        # 测试后删除数据
        search_data = {"userName": "test_login_user", "page": 1, "pageNum": 1, "limit": 100, "pageSize": 100}
        search_res = res.post_request("/api/base/user/list", json=search_data).json()
        userid = search_res['result']['records'][0]['userId']
        delete_data = {"userId": userid}
        res.post_request("/api/base/user/delete", json=delete_data)

