import yaml
from utils.tools import get_project_path, sep


class GetConfig:
    def __init__(self, configname, baseurl=None):
        self.config = configname
        self.baseurl = baseurl
        project_path = get_project_path()
        target_path = project_path + sep(["config", self.config], add_sep_before=1)
        with open(target_path, "r", encoding="utf-8") as env_file:
            self.env = yaml.load(env_file, Loader=yaml.FullLoader)

    def get_username_password(self, user):
        """
        读取配置文件里账号密码
        :param user: 需要取哪一个账号的就输入对应的名称
        :return:
        """
        try:
            # return对应的账号密码
            return self.env["user"][f"{user}"]["username"], self.env["user"][f"{user}"]["password"]
        except Exception as e:
            raise Exception(f"用户名{user}不存在，请检查! 错误原因：{e}")

    def get_url(self):
        """
        测试地址
        :return:
        """
        try:
            # return对应的测试url
            return self.env[self.baseurl]
        except Exception as e:
            raise Exception(f"baseurl为{self.baseurl}对应的测试url在配置文件上不存在，请检查！ 错误原因：{e}")

    def get_mysql_config(self):
        """
        获取数据库配置
        :return:
        """
        try:
            # return对应数据库参数，输出字典
            return self.env["mysql"]
        except Exception as e:
            raise Exception(f"mysql配置信息在配置文件上不存在，请检查！ 错误原因：{e}")

    def get_chihiro_db_config(self):
        """
        获取数据库配置
        :return:
        """
        try:
            # return对应数据库参数，输出字典
            return self.env["chihiro_db"]
        except Exception as e:
            raise Exception(f"chihiro_db配置信息在配置文件上不存在，请检查！ 错误原因：{e}")


    def get_key(self, key):
        try:
            return self.env[key]
        except Exception as e:
            raise Exception(f"配置文件未找到key为{key}的信息，请检查！ 错误原因：{e}")



if __name__ == '__main__':
    getConfig = GetConfig("samplecenter_config.yaml")
    print(getConfig.get_key(key='log_path'))

