# -*-coding:utf-8 -*-
# @Time:2024/8/8 21:23
# @Author:CQR
# @File:deal_allure.py
# @Software:PyCharm

import allure


def deal_with_res(data, res):
    # 主要用到了allure.attach，在接口请求时可以把必要的信息存放到报告里查看
    # 一一把需要显示的内容获取到，然后使用attach存放到报告
    # 方法里的res就是后面接口请求的内容，data就算是入参报文

    # 请求的url
    request_url = str(res.request.url)
    allure.attach(request_url, "请求的url")

    # 请求的方法
    request_method = str(res.request.method)
    allure.attach(request_method, "请求的方法")

    # 请求的headers
    request_headers = str(res.request.headers)
    allure.attach(request_headers, "请求的headers")

    # 入参报文
    request_data = str(data)
    allure.attach(request_data, "入参报文")

    # 响应时间
    response_time = str(res.elapsed.total_seconds() * 1000)
    allure.attach(response_time, "响应时间")

    # 状态码
    status_code = str(res.status_code)
    allure.attach(status_code, "状态码")

    # 响应报文
    content_type = res.headers.get('Content-Type', '').lower()
    # 检查是否为二进制文件（PDF、ZIP、图片等）
    if 'pdf' in content_type or 'octet-stream' in content_type or 'zip' in content_type or 'image' in content_type:
        # 对于二进制文件，只显示文件大小和类型信息
        file_size = len(res.content)
        response_text = f"二进制文件响应\nContent-Type: {content_type}\n文件大小: {file_size} 字节"
    else:
        # 对于文本响应，安全地处理编码
        try:
            response_text = res.text
        except UnicodeDecodeError:
            # 如果解码失败，尝试使用错误处理
            try:
                response_text = res.content.decode('utf-8', errors='replace')
            except:
                response_text = f"无法解码响应内容，Content-Type: {content_type}, 大小: {len(res.content)} 字节"
    allure.attach(str(response_text), "响应报文")