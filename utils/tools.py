# -*-coding:utf-8 -*-
# @Time:2024/8/8 21:21
# @Author:CQR
# @File:tools.py
# @Software:PyCharm

import os
import io
import random
import time
from PIL import Image as im
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
import base64
import hashlib
import inspect
import json


# from utils.logger import logger_t as logger


def get_project_path():
    """
    获取项目根目录
    :return:
    """
    # 获取当前目录
    file_path = os.path.dirname(__file__)
    # 返回项目根目录
    return os.path.dirname(file_path)


def sep(path, add_sep_before=False, add_sep_after=False):
    """
    拼接文件路径，添加系统分隔符
    :param path: 路径列表，类型为数组  ["config","environment.yaml"]
    :param add_sep_before: 是否需要在拼接的路径前加一个分隔符
    :param add_sep_after: 是否需要再拼接的路径后加一个分隔符
    :return:
    """
    # 拼接传入的数组
    all_path = os.sep.join(path)
    # 如果before为TRUE，那就在路径前面加“/”
    if add_sep_before:
        all_path = os.sep + all_path
    # 如果after为TRUE，那就在路径后面加“/”
    if add_sep_after:
        all_path = all_path + os.sep
    # logger.info(f"传入路径为{path}，拼接的最终路径为：{all_path}")
    return all_path


def data_to_image(content, path):
    '''
    二进制数据流转换为图片
    :param content:
    :return:
    '''
    byte_stream = io.BytesIO(content)  # 请求数据转化字节流
    roiImg = im.open(byte_stream)  # Image打开二进制流Byte字节流数据
    imgByteArr = io.BytesIO()  # 创建一个空的Bytes对象
    roiImg.save(imgByteArr, format='PNG')  # PNG就是图片格式
    imgByteArr = imgByteArr.getvalue()  # 保存的二进制流
    # 创建图片
    with open(path, "wb+") as f:
        f.write(imgByteArr)


# RSA加密方法
def rsa_encrpt(key, password):
    """
    :param key: 公钥key
    :param password: 明文密码
    :return:
    """
    public_key = "-----BEGIN PUBLIC KEY-----\n" + key + "\n-----END PUBLIC KEY-----"
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()


def page_rsa_encrpt(menu_id, method):
    """
    pageId的RSA加密方法
    :param menu_id: 原菜单id
    :param method:
    :return:
    """
    page_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArXxw7ZpF7So5E8eZpVfqWdqNOfmKUiS9wlAKh0o1BVLMZr6PkOyILAc51BVtNn3I1veCIzXw/Ik8vHfxRBmHvqTegNSDsfWtmLG2CQ29ijdMcbWJBnH1vz3VgMx5gGnL1E6s+P4QpHtWROs09LXkKG53SFfRAaAM7z67wM/tg4JCqvbymfIP2UpHzw8WWxiRYJCPA2PYa0bTQ2TabDmQx+oNHQgkCPLjryrDR3JYZMWvzMLKtIuCFp4UIaWZ9jngzMnU7hY6Q84TFg0LghHpO6+hiP08kw5mPL7vJWwtjWw49NMTfBTMep0+BRTezoaUTAJ4ydGrnKRYA3EpjJYdGQIDAQAB"
    page_public_key = "-----BEGIN PUBLIC KEY-----\n" + page_key + "\n-----END PUBLIC KEY-----"
    rsa_key = RSA.importKey(page_public_key)
    cipher = Cipher_pksc1_v1_5.new(rsa_key)
    # 拼接待加密的pageId，格式：menuId##method##随机数
    wait_encrpt_page_id = f"{menu_id}##{method}##{random.randint(0, 9)}"
    cipher_text = base64.b64encode(cipher.encrypt(wait_encrpt_page_id.encode()))
    return cipher_text.decode()


# MD5加密 16进制 字母转大写
def md5_encrpt(password):
    """
    :param password: 明文密码
    :return:
    """
    return hashlib.md5(bytes(password, encoding='utf-8')).hexdigest().upper()


def replace_none(data):
    if isinstance(data, dict):
        return {k: replace_none(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_none(i) for i in data]
    elif data is None:
        return ""
    else:
        return data


def create_sample(mark=None):
    """
    生成样本编号，格式：2位年份+B+mmdd+4位流水
    """
    cur_time = time.localtime()
    cur_year = str(cur_time.tm_year)[-2:].zfill(2)
    cur_mon = str(cur_time.tm_mon).zfill(2)
    cur_day = str(cur_time.tm_mday).zfill(2)
    time.sleep(0.02)
    random_number = str(int(round(time.time() * 1000)))[-4:]
    if mark:
        sample_id = cur_year + mark + cur_mon + cur_day + random_number
    else:
        sample_id = cur_year + 'B' + cur_mon + cur_day + random_number
    return sample_id


def create_expressnum(mark=None):
    """
    生成快递单号，格式：两位前缀+yyyymmdd+5位流水
    """
    cur_time = time.strftime("%Y%m%d", time.localtime())
    random_number = str(int(round(time.time() * 1000)))[-5:]
    if mark:
        expressnum = mark + cur_time + random_number
    else:
        expressnum = 'SF' + cur_time + random_number
    return expressnum


def calculate_file_buffer(filestream):
    """
    :param filestream: 接口响应的文件流
    :return: 返回文件流字节大小
    """
    with io.BytesIO() as file_buffer:
        for chunk in filestream.iter_content(chunk_size=8192):  # 8192是默认的chunk大小，可以根据需要调整
            file_buffer.write(chunk)
        # 现在file_buffer包含了完整的文件内容，我们可以计算大小
        file_size = file_buffer.tell()  # tell()方法返回当前位置指针的值，即已写入的数据量
    return file_size


def safe_str(obj, max_length=5000):
    """
    安全地将对象转换为字符串，处理编码问题
    :param obj: 要转换的对象
    :param max_length: 最大长度，超过则截断
    :return: 安全的字符串
    """
    try:
        if obj is None:
            return "None"
        if isinstance(obj, bytes):
            # 如果是字节，尝试解码
            try:
                s = obj.decode('utf-8', errors='replace')
            except:
                s = obj.decode('latin-1', errors='replace')
        else:
            s = str(obj)

        # 移除或替换无法编码的字符
        # 使用 errors='replace' 确保所有字符都能被处理
        s = s.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

        # 截断过长的字符串
        if len(s) > max_length:
            s = s[:max_length] + f"... (已截断，总长度: {len(s)})"

        return s
    except Exception as e:
        return f"<无法转换为字符串: {type(obj).__name__}>"


if __name__ == '__main__':
    # path = get_project_path()
    # print("目录是：" + path)
    # path1 = ["config", "samplecenter_config.yaml"]
    # print(sep(path1))
    # path1 = [get_project_path(), "img/sample_center_code.png"]
    # print(sep(path1))
    print(create_sample())
    print(create_sample())
