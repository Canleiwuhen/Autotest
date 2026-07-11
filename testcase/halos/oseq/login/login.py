# -*- coding: utf-8 -*-
import pytest
import allure

@pytest.mark.usefixtures("res")
class TestLogin:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("登录")
    @allure.title("登录-登录失败")
    def test_login_ero(self,res,res_cus):
        user = "test_login"
        password = "1234565"
        login_res  = res_cus(user,password)
        login_json = login_res.json()
        ret_code = login_json['retCode']
        assert ret_code == 100510103

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("登录")
    @allure.title("登录-登录成功")
    def test_login_succeed(self,res,res_cus):
        username = ""
        pwd = ""
        login_res  = res_cus(username,pwd)
        assert login_res.status_code == 200
