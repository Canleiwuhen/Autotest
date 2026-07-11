# -*-coding:utf-8 -*-
# @Time:2024/8/8 21:21
# @Author:CQR
# @File:request.py
# @Software:PyCharm

import requests
# 导入adapters，处理接口重试
from requests.adapters import HTTPAdapter
from utils.handle_yaml import GetConfig
from utils.handle_allure import deal_with_res
from utils.tools import safe_str
from utils.logger import logger_t as logger


class Requests:
    # 构造函数，初始化session，封装requests
    def __init__(self, configname, baseurl, headers=None, timeout=None):
        """
        封装requests方法
        :param headers:接口的header
        :param timeout:如果需要设置设置超时时间就传，默认None
        """
        self.config = configname
        self.baseurl = baseurl
        self.s = requests.Session()
        # 在session实例上挂载adapter实例，目的就是请求异常时，自动重试
        self.s.mount("http://", HTTPAdapter(max_retries=3))
        self.s.mount("https://", HTTPAdapter(max_retries=3))

        # 公共请求头设置，把对应的值设置好
        self.s.headers = headers
        self.timeout = timeout
        # 调用获取yaml里的url，把测试域名拿出来，下面做拼接接口用
        self.url = GetConfig(self.config, self.baseurl).get_url()

    def get_request(self, url, params=None):
        """
        GET方法封装
        :param url: 接口地址
        :param params: 一般GET的参数都是放在URL里面
        :return:
        """
        # 可以看到用yaml里的self.url加上接口路径，就是完整的接口了
        res = self.s.get(self.url + url, params=params, timeout=self.timeout)
        if res.status_code == 200:
            logger.info(f"get接口请求成功，url:{self.url + url}")
            logger.info(f"get接口入参params:{params}")
            logger.info(f"接口返回结果:{res}")
            # 调用处理报文的方法，把接口信息加入到测试报告
            deal_with_res(params, res)
            return res
        else:
            logger.error(f"get接口请求失败，url:{self.url + url}")
            logger.error(f"get接口入参params:{params}")
            raise Exception

    def put_request(self, url, params=None, data=None, json=None):
        """
        PUT方法封装
        :param url: 接口地址
        :param params: 一般PUT的参数都是放在URL里面
        :param data: 参数放在表单中
        :param json: 参数放在请求体中，一般是json
        :return:
        """
        # 如果传入的是表单，那接口就传data，适用一些接口是form-data格式的
        if data:
            res = self.s.put(self.url + url, params=params, data=data, timeout=self.timeout)
            if res.status_code == 200 or res.status_code // 100 == 3 or res.status_code == 400:  # 判断状态码为200、400和3打头
                logger.info(f"put接口请求成功，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.info(f"put接口入参data:{data}")
                try:
                    logger.info(f"接口返回结果:{safe_str(res.json())}")
                except:
                    logger.info(f"接口返回结果:无法解析为JSON")
                # 调用处理报文的方法，把接口信息加入到测试报告
                deal_with_res(data, res)
                return res
            else:
                logger.error(f"put接口请求失败，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.error(f"put接口入参data:{data}")
                raise Exception

        # 如果传入的json，就传入json，适用大部分接口
        if json:
            res = self.s.put(self.url + url, params=params, json=json, timeout=self.timeout)
            if res.status_code == 200 or res.status_code // 100 == 3 or res.status_code == 400:  # 判断状态码为200、400和3打头
                logger.info(f"put接口请求成功，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.info(f"put接口入参json:{json}")
                content = res.headers.get('Content-Type', '')
                if content.find('octet-stream') == -1 and content.find('zip') == -1 and content.find('pdf') == -1:
                    try:
                        logger.info(f"接口返回结果:{safe_str(res.json())}")
                    except:
                        logger.info(f"接口返回结果:无法解析为JSON")
                # 调用处理报文的方法，把接口信息加入到测试报告
                deal_with_res(json, res)
                return res
            else:
                logger.error(f"put接口请求失败，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.error(f"put接口入参json:{json}")
                content = res.headers.get('Content-Type', '')
                if content.find('octet-stream') == -1 and content.find('zip') == -1 and content.find('pdf') == -1:
                    try:
                        logger.error(f"接口响应信息:{safe_str(res.json())}")
                    except:
                        logger.error(f"接口响应信息:无法解析为JSON")
                raise Exception

    def delete_request(self, url, params=None):
        """
        DELETE方法封装
        :param url: 接口地址
        :param params: 一般DELETE的参数都是放在URL里面
        :return:
        """
        # 使用yaml里的self.url加上接口路径，就是完整的接口了
        res = self.s.delete(self.url + url, params=params, timeout=self.timeout)
        if res.status_code == 200:
            logger.info(f"delete接口请求成功，url:{self.url + url}")
            logger.info(f"delete接口入参params:{params}")
            logger.info(f"接口返回结果:{res}")
            # 调用处理报文的方法，把接口信息加入到测试报告
            deal_with_res(params, res)
            return res
        else:
            logger.error(f"delete接口请求失败，url:{self.url + url}")
            logger.error(f"delete接口入参params:{params}")
            raise Exception

    def post_request(self, url, params=None, data=None, json=None, file_path=None):
        """
        POST方法封装
        :param url: 接口地址
        :param data: 参数放在表单中
        :param json: 参数放在请求体中，一般是json
        :param file_path: 上传文件路径,上传接口上其他参数传data
        :return:
        """
        # 如果传入的是表单，那接口就传data，适用一些接口是form-data格式的
        if data and (not file_path):
            res = self.s.post(self.url + url, params=params, data=data, timeout=self.timeout)
            if res.status_code == 200 or res.status_code // 100 == 3 or res.status_code == 400:  # 判断状态码为200、400和3打头
                logger.info(f"post接口请求成功，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.info(f"post接口入参data:{data}")
                try:
                    logger.info(f"接口返回结果:{safe_str(res.json())}")
                except:
                    logger.info(f"接口返回结果:无法解析为JSON")
                # 调用处理报文的方法，把接口信息加入到测试报告
                deal_with_res(data, res)
                return res
            else:
                logger.error(f"post接口请求失败，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.error(f"post接口入参data:{data}")
                raise Exception

        # 如果传入的json，就传入json，适用大部分接口
        if json:
            res = self.s.post(self.url + url, params=params, json=json, timeout=self.timeout)
            if res.status_code == 200 or res.status_code // 100 == 3 or res.status_code == 400:  # 判断状态码为200、400和3打头
                logger.info(f"post接口请求成功，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.info(f"post接口入参json:{json}")
                content = res.headers.get('Content-Type', '').lower()
                # 检测是否为文件下载接口（URL包含download等关键字）
                is_file_download = any(keyword in url.lower() for keyword in ['download', 'export', 'file'])

                # 只有当Content-Type明确是JSON时才尝试解析JSON
                if 'application/json' in content:
                    try:
                        result = res.json()
                        logger.info(f"接口返回结果:{safe_str(result)}")
                    except:
                        logger.info(f"接口返回结果:非JSON格式响应")
                elif is_file_download or 'octet-stream' in content or 'zip' in content or 'pdf' in content or 'multipart' in content:
                    # 文件下载接口，跳过JSON解析
                    logger.info(f"接口返回结果:文件流响应，文件大小: {len(res.content)} 字节")
                else:
                    # 尝试解析，如果失败则跳过
                    try:
                        result = res.json()
                        logger.info(f"接口返回结果:{safe_str(result)}")
                    except:
                        logger.info(f"接口返回结果:无法解析为JSON")
                # 调用处理报文的方法，把接口信息加入到测试报告
                deal_with_res(json, res)
                return res
            else:
                logger.error(f"post接口请求失败，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.error(f"post接口入参json:{json}")
                content = res.headers.get('Content-Type', '').lower()
                is_file_download = any(keyword in url.lower() for keyword in ['download', 'export', 'file'])

                # 只有当Content-Type明确是JSON时才尝试解析JSON
                if 'application/json' in content:
                    try:
                        result = res.json()
                        logger.error(f"接口响应信息:{safe_str(result)}")
                    except:
                        logger.error(f"接口响应信息:非JSON格式响应")
                elif is_file_download or 'octet-stream' in content or 'zip' in content or 'pdf' in content or 'multipart' in content:
                    logger.error(f"接口响应信息:文件流响应，文件大小: {len(res.content)} 字节")
                else:
                    try:
                        result = res.json()
                        logger.error(f"接口响应信息:{safe_str(result)}")
                    except:
                        logger.error(f"接口响应信息:无法解析为JSON")
                raise Exception

        # 上传文件接口，传文件绝对路径，接口上其他参数在data
        if file_path:
            file = {
                'file': open(file_path, 'rb'),
                "Content-Disposition": "form-data",
                "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
            res = self.s.post(self.url + url, params=params, data=data, files=file, timeout=self.timeout)
            if res.status_code == 200 or res.status_code // 100 == 3:
                logger.info(f"post接口请求成功，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.info(f"接口入参data:{data},文件路径file_path：{file_path}")
                try:
                    logger.info(f"接口返回结果:{safe_str(res.json())}")
                except:
                    logger.info(f"接口返回结果:无法解析为JSON")
                deal_with_res(file, res)
                return res
            else:
                logger.error(f"post接口请求失败，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                logger.error(f"接口入参data:{data},文件路径file_path：{file_path}")
                try:
                    logger.error(f"接口响应信息:{safe_str(res.json())}")
                except:
                    logger.error(f"接口响应信息:无法解析为JSON")
                raise Exception

        # post接口什么也不传的，兼容这种情况
        if not data and not json and not file_path:
            res = self.s.post(self.url + url, data=data, json=json, timeout=self.timeout)
            if res.status_code == 200 or res.status_code // 100 == 3:
                logger.info(f"post接口请求成功，接口无其他入参，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                try:
                    logger.info(f"接口返回结果:{safe_str(res.json())}")
                except:
                    logger.info(f"接口返回结果:无法解析为JSON")
                deal_with_res(json, res)
                return res
            else:
                logger.error(f"post接口请求失败，url:{self.url + url}")
                logger.info(f"状态码为{res.status_code}")
                raise Exception

    # 魔法函数
    def __del__(self):
        """
        当实例被销毁时，释放掉session所持有的连接
        :return:
        """
        if self.s:
            self.s.close()


# 测试一下下
if __name__ == '__main__':
    # 这里域名设置的是http://httpbin.org
    get_res = Requests("samplecenter_config.yaml").get_request("/get")
    post_res = Requests("samplecenter_config.yaml").post_request("/post")
    print(get_res.text, "\n", post_res.text, "\n")