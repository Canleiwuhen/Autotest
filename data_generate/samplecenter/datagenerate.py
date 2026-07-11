import codecs
import copy
import os
from datetime import datetime, timedelta
import time
from typing import final

import openpyxl
from cryptography.x509 import random_serial_number
import pandas as pd
from openpyxl.styles import numbers

from utils.tools import sep, get_project_path, rsa_encrpt, data_to_image, replace_none, create_sample, create_expressnum
from utils.handle_yaml import GetConfig
from utils.request import Requests
from urllib.parse import urlencode
from utils.logger import logger_samplecenter_dg as logger


class DataGenerate:
    def __init__(self, token=None):
        self.token = token
        self.datafactory_res = Requests(configname='samplecenter_config.yaml', baseurl='data_factory_url')
        self.samplecenter_res = Requests(configname='samplecenter_config.yaml', baseurl='test_url',
                                         headers={"content-type": "application/x-www-form-urlencoded"})
        self.samplecenter_upload_res = Requests(configname='samplecenter_config.yaml', baseurl='test_url',
                                         headers={
                                             "Cookie": "JSESSIONID=76C17BACFDB50D386361E006A00D3EB0",
                                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
                                             "accept-encoding": "gzip, deflate",
                                             "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                                             "Accept": "*/*"
                                         })
        self.sample = []
        self.expressnum = ""
        self.container_prefix = f"{int(time.time())}"
        self.specifications = 96
        self.outbound_apply_order_number = None
        self.inbound_apply_order_number = None
        self.unpack_result = None
        self.arrvSerie = None
        self.container_num = ""
        self.container_id = ""

    def sumbit_sample(self):
        """
        造数工具提交送检单，返回已提交送检单的样本列表，目前一次调用只有一个样本
        :return:
        """
        response = self.datafactory_res.get_request("/api/samples?platform=frit&product=hills&end_step=1").json()
        if response['success'] and response['data']['samples']:
            logger.info(f"造数工具提交送检单成功，返回样本数据：{response['data']['samples']}")
            self.sample = response['data']['samples']
            return self.sample
        else:
            logger.error(f"造数工具提交送检单失败，返回结果：{response}")
            raise Exception

    def send_package(self, sample=None):
        """
        造数工具寄送包裹邮件，返回快递单号
        :return:
        """
        if sample:
            sampleid = sample
        else:
            sampleid = self.sample[0]
        data = {"sampleIds": sampleid}
        response = self.datafactory_res.post_request("/api/send-package", json=data).json()
        if response['success'] and response['data']['expressNum']:
            expressnum = response['data']['expressNum']
            self.expressnum = expressnum
            return self.expressnum
        else:
            logger.error(f"造数工具寄送包裹失败，返回结果：{response}")
            raise Exception

    def receive_package(self, expressnum=None):
        """
        样本中心包裹签收，可传快递单号进行签收
        :param expressnum: 快递单号
        :return:阶段处理成功返回到达序列号,处理失败返回False
        """
        if not expressnum:
            expressnum = self.expressnum
        # 先查询包裹信息
        query_datas = {"expressNumber": expressnum,
                       "bgjs": "X",
                       "token": self.token,
                       "menuId": "PackageRecive",
                       "zsjd_type": "YX"}
        query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_express_package_info",
                                                            data=query_datas).json()
        if query_response['code'] == '200' and query_response['data']:
            logger.info(f"查询包裹信息成功")
            tmp = {"expressNumber": query_response['data'][0]['expressNumber']}
        else:
            logger.error(f"查询包裹信息失败，返回结果{query_response}")
            raise Exception
        # 执行包裹签收
        datas = {"datas": [tmp],
                 "token": self.token,
                 "menuId": "PackageRecive",
                 "zsjd_type": "YX"}
        response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=update_express_package_info",
                                                      data=urlencode(datas)).json()
        if response['code'] == '200' and (expressnum in response['data'][0]['expressNumber']):
            arrvSerie = response['data'][0]['arrvSeries']  # 到达序列号
            logger.info(f"包裹签收成功，返回到达序列号{arrvSerie}")
            return {'arrvSeries': arrvSerie}
        else:
            logger.error(f"包裹签收失败，返回结果{response}")
            return False

    def replenish_record(self):
        """
        包裹接收的补录
        """
        expressnum = create_expressnum('WD')
        self.expressnum = expressnum
        if not self.sample:
            sample = create_sample()
            self.sample = sample
        # 先查询包裹信息
        query_datas = {"expressNumber": expressnum,
                       "bgjs": "X",
                       "token": self.token,
                       "menuId": "PackageRecive",
                       "zsjd_type": "YX"}
        query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_express_package_info",
                                                            data=query_datas).json()
        if query_response['code'] == '200':
            logger.info(f"进行补录操作")
        else:
            logger.error(f"查询包裹信息失败，返回结果{query_response}")
            raise Exception
        # 签收包裹
        tmp = {
            "expressNumber": expressnum,
            "_id": 1,
            "__kdgst": "顺丰速运",
            "kdgst": "顺丰速运",
            "__isUrgent": "否",
            "isUrgent": "否",
            "__sendHospital": "内蒙古工业大学",
            "sendHospital": "内蒙古工业大学",
            "__sendArea": "广东省深圳市盐田区盐田路605号",
            "sendArea": "广东省深圳市盐田区盐田路605号",
            "__sendName": "测试用户",
            "sendName": "测试用户",
            "__sendPhoneNum": "13530658357",
            "sendPhoneNum": "13530658357",
            "zwerks": "A020"}
        datas = {"expressInfo": [tmp],
                 "token": self.token,
                 "menuId": "PackageRecive",
                 "zsjd_type": "YX"}
        response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=save_express_package_info",
                                                      data=urlencode(datas)).json()
        if response['code'] == '200' and (expressnum in response['data'][0]['expressNumber']):
            arrvSerie = response['data'][0]['arrvSeries']  # 到达序列号
            self.arrvSerie = arrvSerie
            result = {'expressnum': expressnum, 'arrvSeries': arrvSerie}
            logger.info(f"包裹补录成功，返回{result}")
            return result
        else:
            logger.error(f"包裹补录失败，返回结果{response}")
            return False

    def unpack(self, expressnum=None):
        """
        样本中心医学拆包，可传快递单号进行拆包
        :param expressnum: 快递单号
        :return:阶段处理成功返回Ture,处理失败返回False
        """
        if not expressnum:
            expressnum = self.expressnum
        # 先查询获取pkid
        query_datas = {"expressNumber": expressnum,
                       "token": self.token,
                       "menuId": "YxUnpack",
                       "zsjd_type": "YX"
                       }
        query_response = self.samplecenter_res.post_request(
            "/ybzx/webintf.do?method=query_packageinfo_by_expressnumber_unpack",
            data=query_datas).json()
        if query_response['code'] == '200' and query_response['data']:
            logger.info(f"查询拆包信息成功")
            tmp = {"pkid": query_response['data'][0]['pkid'],
                   "sum_zcatalo": "1",
                   "sum_zsjdid": "1",
                   "sum_wlxp": "1"}
            datas = {"datas": tmp,
                     "token": self.token,
                     "menuId": "YxUnpack",
                     "zsjd_type": "YX"}
        else:
            logger.error(f"查询拆包信息失败，返回结果{query_response}")
            raise Exception
        # 执行拆包
        response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=save_package_info",
                                                      data=urlencode(datas)).json()
        if response['code'] == '200' and ('拆包成功' in response['msg']):
            logger.info(f"快递单号{expressnum}，包裹拆包成功")
            logger.info(f"拆包结果{response}")
            self.unpack_result = {'sample': self.sample, 'expressnum': self.expressnum, 'arrvSerie': self.arrvSerie}
            return self.unpack_result
        else:
            logger.info(f"拆包失败，返回结果：{response}")
            return False

    def locate_position(self, samples=None, container_num=None, container_id=None):
        """
        医学定位（新）
        :param samples: 样本列表，示例：["24X091300000", "24X091300001"]
        :param container_num: 容器编号：前缀+自动生成的4位数序号，示例：autotest-0001
        :param container_id: 容器id：新增容骑时自动生成的容器id，示例：POP000000000051160
        """
        if not samples:
            samples = self.sample
        if not container_num:
            container_num = self.container_num
        if not container_id:
            # container_id = self.query_container_by_container_num(container_num)['container_id']
            container_id = self.container_id
        if isinstance(samples, list):
            if len(samples) > 96:
                print("最大仅支持96个样本同时定位")
            else:
                req = []
                temp = {
                    "use_scene": "00",
                    "zcwbh": "24X091200019",  # 样本编号
                    "zcwlx": "干血片",
                    "zctrid": container_num,
                    "zplate_num": container_num,  # 容器编号
                    "zplate": container_id,  # 容器id
                    "zcontainer_id": container_id,  # 容器id
                    "zpoint": "A01",  # 孔位
                    "zkc_status": "RKDW",
                    "zsc_sutatus": "",
                    "zpbr": "",
                    "zrkr": "",
                    "zsfpcr": "",
                    "ztprt": "常温",
                    "zreceiveddate": "00000000",
                    "zfrgid": "",
                    "lgort": "",
                    "lgobe": "",
                    "zroomnum": "",
                    "zxxwz": "",
                    "ztype": ""
                }
                # 根据样本数量按A-H，1-12的顺序拼接后生成孔位，最多可支持生成96个孔位，例如：A01,B02...
                points = [f"{chr(65 + i // 12)}{str(i % 12 + 1).zfill(2)}" for i in range(len(samples))]
                tmp_dict = dict(zip(samples, points))
                for sample, point in tmp_dict.items():
                    temp["zcwbh"] = sample
                    temp["zpoint"] = point
                    req.append(copy.deepcopy(temp))
                data = {
                    "req": req,
                    "dev": "false",
                    "token": self.token
                }
                response_json = self.samplecenter_res.post_request("/ybzx/pos/position/save.do",
                                                                   data=urlencode(data)).json()
                assert response_json['code'] == '200'
                return True
        else:
            print("参数类型错误！")
            return False

    def query_sample_cycle(self, sample: str):
        """
        样本生命周期查询，目前仅支持按样本编号查询，传字符串，多个样本编号查询英文逗号分隔，如“24X091100012,24X091100011”
        :param sample:
        :return:
        """
        if isinstance(sample, str):
            result = {}
            task_tmp = {"zybzx": "X",
                        "zyjpcdate": "",
                        "zreceiveddate": "",
                        "zsampling_datum": "",
                        "zcatalo": sample,
                        "zsjdType": "YX",
                        "zsfxhfy": "否"}
            datas = {"task": task_tmp,
                     "token": self.token,
                     "menuId": "sampleCycle",
                     "zsjd_type": "YX"
                     }
            query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_all_samples",
                                                                data=urlencode(datas)).json()
            if query_response['code'] == '200' and query_response['data']:
                for i in query_response['data']:
                    result[i['zsample']] = {"zsjdid": i['zsjdid'],
                                            "matnr": i['matnr'],
                                            "zyblx": i['zyblx']}
                return result
            else:
                logger.error(f"查询不到数据，查询返回结果为{query_response}")
                raise Exception


        else:
            logger.error(f"sample入参类型错误，请传字符串类型！")
            raise Exception

    def create_container(self, container_prefix=None, specifications=None):
        """
        新增容器
        :param container_prefix: 容器编号前缀
        :param specifications: 容器规格，目前仅支持孔板类型的25, 50, 96, 100规格
        :return: container_num, container_id组成的tuple
        """
        if not container_prefix:
            container_prefix = self.container_prefix

        if not specifications:
            specifications = self.specifications
        elif specifications not in [25, 50, 96, 100]:
            print("规格错误！支持的规格：25或50或96或00，默认用96规格！")
            specifications = self.specifications

        req = [{"zcontainer_id": "", "zrqlx": "YCQX", "zcontainer_code": "YCQX", "zcontainer_num": "YCQX",
                "zplate_x": "12", "zplate_y": "8", "zplate_notes": "autotest", "zplate_status": "1",
                "c_temperature": "常温", "zcontainer_number": specifications, "zcontainer_type": "02", "zrqsl": "1",
                "zrqqz": container_prefix}]
        data = {
            "req": req,
            "token": self.token
        }
        response = self.samplecenter_res.post_request("/ybzx/pos/container/save.do", data=urlencode(data)).json()
        self.container_num = response['data'][0]['zcontainer_num']
        self.container_id = response['data'][0]['zcontainer_id']
        return self.container_num, self.container_id

    def query_container_by_container_num(self, container_num):
        """
        根据容器编号查询容器信息
        :param container_num: 容器编号：前缀+自动生成的4位数序号，示例：autotest-0001
        :return: container：返回容器编号、容器id和容器状态等信息
        """
        if not container_num:
            print("容器编号不能为空，格式：前缀-4位数字，示例：autotest-0001")
        else:

            req = [{"zplate_num": container_num}]
            data = {
                "req": req,
                "token": self.token
            }
            response = self.samplecenter_res.post_request("/ybzx/pos/query/plate/main.do", data=urlencode(data)).json()
            # print(response)
            assert response['code'] == '200'
            container = {
                'container_num': container_num,
                'container_id': response['data'][0]['zcontainer_id'],
                'container_status': response['data'][0]['zplate_status'],
                'point_count': response['data'][0]['zcontainer_number']
            }
            return container

    def outbound_apply(self, sample=None):
        """
        医学出库申请（样本出库）
        :param sample: 样本编号，对该样本进行申请出库操作
        :return:
        """
        if not sample:
            sample_id = self.sample[0]
        else:
            sample_id = sample
        # 查询待出库样本信息
        query_data = {
            "task": {"zybzx": "X", "zcatalo": sample_id, "zsjd_type": "YX"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": self.token,
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_wait_out_bound_samples",
                                                            data=urlencode(query_data))
        if query_response.status_code == 200 and query_response.json()["code"] == "200":
            logger.info(f"查询待出库样本信息成功！样本编号：{sample_id}")
        else:
            logger.error(f"查询待出库样本信息失败！样本编号：{sample_id}，响应：{query_response.json()}")
            raise Exception(f"查询待出库样本信息失败！样本编号：{sample_id}，响应：{query_response.json()}")
        # 申请出库，创建出库申请单
        outbound_data = {
            "params": {"zzzbm": "BC01", "zreson": "生产出库", "zyqyrq": "", "zghyrq": "", "lgort_t": "BC01",
                       "lgort_f": "XB39", "zydate": "", "zcmode": "0", "zccksq":"","zckyblxvalue":"新到样样本","zckyblx":"01","zsjd_type": "YX"},
            "samples": query_response.json()["data"],
            "token": self.token,
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        for i in range(len(outbound_data["samples"])):
            outbound_data["samples"][i]["_key"] = i + 1
            outbound_data["samples"][i]["_id"] = i + 1
        outbound_data = replace_none(outbound_data)  # 替换data中的None为""
        create_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=create_out_bound_apply",
                                                             data=urlencode(outbound_data))
        if create_response.status_code == 200 and create_response.json()["code"] == "200" and "已成功保存" in \
                create_response.json()["msg"]:
            logger.info(f"创建出库申请单成功！出库申请单号：{create_response.json()['msg'][5:-5]}")
        else:
            logger.error(f"创建出库申请单失败！样本编号：{sample_id}，响应：{create_response.json()}")
            raise Exception(f"创建出库申请单失败！样本编号：{sample_id}，响应：{create_response.json()}")
        # 返回出库申请单
        outbound_apply = create_response.json()["msg"][5:-5]
        self.outbound_apply_order_number = outbound_apply
        return outbound_apply

    def outbound_audit(self, outbound_apply=None):
        """
        出库审核
        :param outbound_apply: 出库申请单号，审核后创建出库单
        :return:
        """
        if not outbound_apply:
            outbound_apply_id = self.outbound_apply_order_number
        else:
            outbound_apply_id = outbound_apply
        # 查询出库申请单号内样本信息
        query_data = {
            "zscdh": outbound_apply_id,
            "token": self.token,
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_sample_by_sqdh",
                                                            data=urlencode(query_data))
        if query_response.status_code == 200 and query_response.json()["code"] == "200":
            logger.info(f"查询出库申请单内样本信息成功！出库申请单号：{outbound_apply_id}")
        else:
            logger.error(f"查询出库申请单内样本信息失败！出库申请单号：{outbound_apply_id}，响应：{query_response.json()}")
            raise Exception(
                f"查询出库申请单内样本信息失败！出库申请单号：{outbound_apply_id}，响应：{query_response.json()}")
        # 审核并创建出库单号
        create_data = {
            "datas": query_response.json()["data"],
            "token": self.token,
            "menuId": "outBound",
            "zsjd_type": "YX"
        }
        for i in range(len(create_data["datas"])):
            create_data["datas"][i]["zshdat"] = ""
            create_data["datas"][i]["_id"] = i + 1
        create_data = replace_none(create_data)  # 替换data中的None为""
        create_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=create_chuku_bill",
                                                             data=urlencode(create_data))
        if create_response.status_code == 200 and create_response.json()["code"] == "200" and "成功创建出库单" in \
                create_response.json()["msg"]:
            logger.info("审核并创建出库单成功！")
        else:
            logger.error(f"审核并创建出库单失败！出库申请单号：{outbound_apply_id}，响应：{create_response.json()}")
            raise Exception(f"审核并创建出库单失败！出库申请单号：{outbound_apply_id}，响应：{create_response.json()}")

    def lims_inbound_apply(self,sample=None):
        """
        LIMS产物入库申请
        :param sample: 样本编号，对该样本进行申请入库操作
        :return:
        """
        if sample:
            sampleid = sample.split(',')
        else:
            sampleid = self.sample
        sample_num = [num for num in sampleid for _ in range(2)]
        chanwu_num, sample_type,ruku_type,kongban = [], [],[],[]
        for i in range(len(sampleid)):
            a = sampleid[i].replace("B","P") +"-4"
            b = sampleid[i].replace("B", "P") + "-5"
            chanwu_num.append(a)
            chanwu_num.append(b)
            sample_type.append("S052")
            sample_type.append("S052")
            ruku_type.append("单管")
            ruku_type.append("单管")
            kongban.append("")
            kongban.append("")
        excel_data = {
            "样本编号*": sample_num,
            "产物编号*": chanwu_num,
            "孔板": kongban,
            "孔位": kongban,
            "样本类型*": sample_type,
            "入库类型*": ruku_type,
            "申请人*": kongban,
            "huxiaofeng_A020": kongban
        }
        file_path = 'excel_temp/chanwu.xlsx'
        df = pd.DataFrame(excel_data)
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='导入数据')
            workbook = writer.book
            worksheet = writer.sheets['导入数据']
            text_format = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'align': 'left', 'border': 1})
            worksheet.set_column('A:A', None, text_format)
            worksheet.set_column('B:B', None, text_format)
            worksheet.set_column('C:C', None, text_format)
            worksheet.set_column('D:D', None, text_format)
            worksheet.set_column('E:E', None, text_format)
            worksheet.set_column('F:F', None, text_format)
            worksheet.set_column('G:G', None, text_format)
            worksheet.set_column('H:H', None, text_format)
        absolute_path = os.path.abspath(file_path)
        now_date = datetime.now()
        date_str = now_date.strftime('%Y%m%d')
        future_date = now_date + timedelta(days=3)
        future_date_str = future_date.strftime('%Y%m%d')
        req = {
            "zzzbm": "深圳样本组",
            "zreson": "生产归还",
            "zyqyrq": date_str,
            "zghyrq": future_date_str,
            "lgort_f": "XB39",
            "lgort_t": "XB39",
            "lgore_f": "深圳样本组",
            "lgore_t": "深圳样本组",
            "ztprt": "常温",
            "token": "",
            "path": "",
            "mode": 0
        }
        data = {
            "req": (None,str(req), None),
            "methodName": (None,"importInboundData",None),
            "token": (None,self.token,None),

        }
        query_response = self.samplecenter_upload_res.post_request("/ybzx/excelFile/import.do", data=data ,file_path=absolute_path)
        batchId = query_response.json()["data"]["batchId"]
        data = {
            "id":batchId,
            "token": self.token
        }
        query_response = self.samplecenter_res.post_request("/ybzx/l2p/samplecenter/inbound/request.do",
                                                            data=urlencode(data))
        if query_response.json()["code"] == "200":
            logger.info(query_response.json()["msg"])
            self.inbound_apply_order_number = query_response.json()["data"]
            return query_response.json()["data"]
        else:
            logger.error(f"产物入库失败！返回结果：{query_response.json()}")
            raise Exception(f"产物入库失败！返回结果：{query_response.json()}")

    def inbound_apply(self, sample=None):
        """
        医学入库申请（样本入库）
        :param sample: 样本编号，对该样本进行申请入库操作
        :return:
        """
        if not sample:
            sample_id = self.sample[0]
        else:
            sample_id = sample
        # 查询待入库样本信息
        query_data = {
            "task": {"zybzx": "X", "zcatalo": sample_id, "zsjd_type": "YX"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": self.token,
            "menuId": "OutBoundApply",
            "zsjd_type": "YX"
        }
        query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_wait_in_bound_samples",
                                                            data=urlencode(query_data))
        if query_response.status_code == 200 and query_response.json()["code"] == "200" and query_response.json()[
            "msg"] == "success":
            logger.info(f"查询待入库样本信息成功！样本编号：{sample_id}")
        else:
            logger.error(f"查询待入库样本信息失败！样本编号：{sample_id}，响应：{query_response.json()}")
            raise Exception(f"查询待入库样本信息失败！样本编号：{sample_id}，响应：{query_response.json()}")
        # 申请入库，创建入库申请单
        inbound_data = {
            "params": {"zzzbm": "BC01", "zreson": "生产归还", "zyqyrq": "20240919", "lgort_t": "XB39",
                       "lgort_f": "BC01",
                       "ztprt": "-4℃"},
            "samples": query_response.json()["data"],
            "token": self.token,
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        for i in range(len(inbound_data["samples"])):
            inbound_data["samples"][i]["_key"] = i + 1
            inbound_data["samples"][i]["_id"] = i + 1
        inbound_data = replace_none(inbound_data)  # 替换data中的None为""
        create_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=create_in_bound_apply",
                                                             data=urlencode(inbound_data))
        if create_response.status_code == 200 and create_response.json()["code"] == "200" and "已成功保存" in \
                create_response.json()["msg"]:
            logger.info(f"创建入库申请单成功！入库申请单号：{create_response.json()['msg'][5:-5]}")
        else:
            logger.error(f"创建入库申请单失败！样本编号：{sample_id}，响应：{create_response.json()}")
            raise Exception(f"创建入库申请单失败！样本编号：{sample_id}，响应：{create_response.json()}")
        # 返回入库申请单
        inbound_apply = create_response.json()["msg"][5:-5]
        data = {
            "task": {
                "zybzx": "X",
                "zscdh": inbound_apply
            },
            "pageNumber": "1",
            "pageSize": "50",
            "token": self.token,
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_in_bound_apply_bill",
                                                      data=urlencode(data))
        if len(response.json()["data"])>0 and response.json()["code"] == "200":
            logger.info(f"查询入库申请单成功！")
        else:
            logger.error(f"查询入库申请单失败！响应：{response.json()}")
            raise Exception(f"查询入库申请单失败！响应：{response.json()}")
        data = {
            "datas":[{"zscdh":inbound_apply}],
            "token": self.token,
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=save_inapply_confirmation",
                                                      data=urlencode(data))
        if "success" in response.json()["msg"] and response.json()["code"] == "200":
            logger.info(f"交接确认成功！")
        else:
            logger.error(f"交接确认失败！响应：{response.json()}")
            raise Exception(f"交接确认失败！响应：{response.json()}")
        self.inbound_apply_order_number = inbound_apply
        return inbound_apply

    def inbound_audit(self, inbound_apply_order_number=None):
        """
        入库审核
        :param inbound_apply_order_numbe:
        :return:
        """

        if not inbound_apply_order_number:
            inbound_apply_order_number = self.inbound_apply_order_number
        # 查询入库申请单样本信息
        query_data = {
            "zscdh": inbound_apply_order_number,  # 入库申请单号
            "ziszbcrk": "",
            "dev": "false",
            "token": self.token
        }
        count = 0
        while True:
            time.sleep(5)
            count += 1
            query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_samples_by_sqdh_of_in_bound_apply",
                                          data=urlencode(query_data))
            if query_response.json()["code"] == "200" and len(query_response.json()['data']) > 0 :
                logger.info("查询入库申请单样本信息成功！")
                break
            if count >= 3:
                break
        # 新增容器，获取容器编号和id
        container_num, container_id = self.create_container()
        # 获取样本的数据源
        ybsource_data = {
            "req": [{"zcatalo": query_response.json()["data"][0]["zcatalo"], "ztype": "RKSH", "page_flag": ""}],
            "token": self.token
        }
        ybsource_response = self.samplecenter_res.post_request("/ybzx/pos/query/ybsource.do", data=urlencode(ybsource_data))
        if ybsource_response.status_code == 200 and ybsource_response.json()["code"] == "200" and \
               ybsource_response.json()["msg"] == "success":
            logger.info("获取样本数据源成功！")
        else:
            logger.error(f"获取样本数据源失败！response：{ybsource_response.json()}")
            raise Exception(f"获取样本数据源失败！response：{ybsource_response.json()}")
        # 根据样本数据源查询送检单信息
        reqform_data = {
            "req": [{"zcatalo": query_response.json()["data"][0]["zcatalo"],
                     "zdatasource": ybsource_response.json()["data"][0]["zdatasource"]}],
            "token": self.token
        }
        reqform_response = self.samplecenter_res.post_request("/ybzx/pos/query/reqform2.do", data=urlencode(reqform_data))
        if reqform_response.status_code == 200 and reqform_response.json()["code"] == "200" and \
               reqform_response.json()["msg"] == "success":
            logger.info("查询送检单信息成功！")
        else:
            logger.error(f"查询送检单信息失败！response：{reqform_response.json()}")
            raise Exception(f"查询送检单信息失败！response：{reqform_response.json()}")
        # 保存当前孔板信息
        save_data = {
            "req": [{"use_scene": "01",
                     "zcwbh": query_response.json()["data"][i]["zcatalo"],  # 样本编号
                     "zcwlx": query_response.json()["data"][i]["zyblx"],  # 样本类型
                     "zctrid":container_num,  # 孔板编号
                     "zplate_num": container_num,
                     "zplate": container_id,  # 孔板id
                     "zcontainer_id": container_id,
                     "zpoint": "A01",  # 孔位号
                     "zkc_status": "RKDW",
                     "zsc_sutatus": "",
                     "zpbr": "",
                     "zrkr": "",
                     "zsfpcr": "",
                     "ztprt": "4℃",
                     "zreceiveddate": query_response.json()["data"][i]["zreceiveddate"],  # 到样日期
                     "zfrgid": "",
                     "lgort": "",
                     "lgobe": "",
                     "zroomnum": "",
                     "zxxwz": "",
                     "ztype": "",
                     "zscdh": query_response.json()["data"][i]["zscdh"],  # 入库申请单号
                     "zscdh_item": query_response.json()["data"][i]["zscdh_item"]}
                    for i in range(len(query_response.json()["data"]))
                    ],
            "dev": "false",
            "token": self.token
        }
        save_response = self.samplecenter_res.post_request("/ybzx/pos/checkin_visual/post.do", data=urlencode(save_data))
        if save_response.status_code == 200 and save_response.json()["code"] == "200" and \
               save_response.json()["msg"] == "保存成功":
            logger.info("保存孔板信息成功！")
        else:
            logger.error(f"保存孔板信息失败！response：{save_response.json()}")
            raise Exception(f"保存孔板信息失败！response：{save_response.json()}")
        # 完成审核，创建入库单号
        create_data = {
            "zscdh": query_response.json()["data"][0]["zscdh"],  # 入库申请单号
            "dev": "false",
            "token": self.token
        }
        create_response = self.samplecenter_res.post_request("/ybzx/pos/checkin_visual/create_rkd.do", data=urlencode(create_data))
        if create_response.status_code == 200 and create_response.json()["code"] == "200" and \
               "成功创建入库单" in create_response.json()["msg"]:
            logger.info("入库审核成功！")
        else:
            logger.error(f"入库审核失败！response：{create_response.json()}")

    def medical_info_audit(self, sample=None):
        """
         医学信息审核（单个审核）
         :param sample: 样本编号，对该样本进行信息审核操作
         :return:
        """
        if not sample:
            sample = self.sample[0]
        # 查询待审核样本，获取样本查询结果，审核状态：未审核
        query_data = {
            "task": {"zybzx": "X", "zsample": sample, "chkstatus": "W", "zybyc": "0"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": self.token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas",
                                                            data=urlencode(query_data))
        if query_response.status_code == 200 and query_response.json()["code"] == "200" and query_response.json()[
            "msg"] == "success":
            logger.info("查询未审核样本成功！")
        else:
            logger.error(f"查询未审核样本失败！response：{query_response.json()}")
            raise Exception(f"查询未审核样本失败！response：{query_response.json()}")

        # 锁定当前样本
        lock_data = {
            "datas": query_response.json()["data"],
            "token": self.token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        lock_data["datas"][0]["chkstatus"] = "未审核"
        lock_data["datas"][0]["_key"] = 1
        lock_data["datas"][0]["_id"] = 1
        lock_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=lock_more_sjd",
                                                           data=urlencode(lock_data))
        if lock_response.status_code == 200 and lock_response.json()["code"] == "200" and lock_response.json()[
            "msg"] == "锁定成功":
            logger.info("锁定样本成功！")
        else:
            logger.error(f"锁定样本失败！response：{lock_response.json()}")
            raise Exception(f"锁定样本失败！response：{lock_response.json()}")

        # 当前样本信息审核
        audit_data = lock_data
        audit_data["datas"][0]["zrecordno"] = "autotest"  # 设置档案盒号
        audit_data["datas"][0]["chkstatus"] = "锁定"
        audit_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=audit_new_more_sjd",
                                                            data=urlencode(audit_data))
        if audit_response.status_code == 200 and audit_response.json()["code"] == "200" and audit_response.json()[
            "msg"] == "审核成功":
            logger.info("样本信息审核成功！")
        else:
            logger.error(f"样本信息审核失败！response：{audit_response.json()}")
            raise Exception(f"样本信息审核失败！response：{audit_response.json()}")

    def medical_info_audit_batch(self, sample=None):
        """
         批量医学信息审核
         :param sample: 样本编号，对该样本进行信息审核操作
         :return:
        """
        if sample:
            sampleid = sample
        else:
            sampleid = self.sample
        sampleid = ','.join(sampleid)
        data = {
            "task": {"zybzx": "X", "zsample": sampleid, "chkstatus": "wait", "zybyc": "0"},
            "pageNumber": "1",
            "pageSize": "1000",
            "token": self.token,
            "menuId": "informationAudit",
            "zsjd_type": "YX"
        }
        response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_new_xxsh_datas",
                                                            data=urlencode(data))
        if response.status_code == 200 and response.json()["code"] == "200" and response.json()[
            "msg"] == "success":
            logger.info("查询未审核样本成功！")
            response_data = (response.json()["data"])
            datas = []
            for i in range(len(response_data)):
                data_dic = {k: "" if v is None else v for k, v in response_data[i].items()}
                data_dic["_id"] = i + 1
                data_dic["_key"] = i + 1
                data_dic["zrecordno"] = self.container_prefix
                datas.append(data_dic)
            data = {
                "datas": datas,
                "token": self.token,
                "menuId": "informationAudit",
                "zsjd_type": "YX"
            }
            response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=audit_new_more_sjd",
                                                          data=urlencode(data))
            if response.json()["code"] == "200" and response.json()["msg"] == "审核成功":
                logger.info("医学信息批量审核成功")
            else:
                logger.error(f"医学信息批量审核失败！response：{response.json()}")
                raise Exception(f"医学信息批量审核失败！response：{response.json()}")
        else:
            logger.error(f"查询未审核样本失败！response：{response.json()}")
            raise Exception(f"查询未审核样本失败！response：{response.json()}")
    def receipt_confirmation(self, outbound_apply_order_number=None):
        """
         接收确认
         :param outbound_apply_order_number: 出库申请单号
         :return:
        """
        if not outbound_apply_order_number:
            outbound_apply_order_number = self.outbound_apply_order_number
        # 查询出库申请单内样本信息
        query_data = {
            "zscdh": outbound_apply_order_number,
            "token": self.token,
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        query_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=query_sample_by_sqdh", data=urlencode(query_data))
        if query_response.status_code == 200 and query_response.json()[
            "code"] == "200":
            logger.info("查询出库申请单内样本信息成功！")
        else:
            logger.error(f"查询出库申请单内样本信息失败！response：{query_response.json()}")
            raise Exception(f"查询出库申请单内样本信息失败！response：{query_response.json()}")
        query_response_data = query_response.json()["data"]
        # 基于查询的样本提交接收确认
        confirm_data = {
            "datas": [
                {
                    "zscdh": query_response_data[i]["zscdh"],
                    "zscdh_item": query_response_data[i]["zscdh_item"],
                    "zstatus": "20",
                    "zexc_text": "",
                    "zkeep_site": query_response_data[i]["zkeep_site"]
                }
                for i in range(len(query_response_data))
            ],
            "token": self.token,
            "menuId": "OutBoundAffirm",
            "zsjd_type": "YX"
        }
        confirm_data = replace_none(confirm_data)  # 替换data中的None为""
        confirm_response = self.samplecenter_res.post_request("/ybzx/webintf.do?method=submit_chuku", data=urlencode(confirm_data))
        if confirm_response.status_code == 200 and confirm_response.json()["code"] == "200" and \
               confirm_response.json()["msg"] == "success":
            logger.info(f"接收确认成功！")
        else:
            logger.error(f"接收确认失败！response：{confirm_response.json()}")
            raise Exception(f"接收确认失败！response：{confirm_response.json()}")

    def sample_batch_receive(self, samples=None, expressnumber=None,arrvseries=None):
        """
        样本批量接收
        @param samples: 样本编号列表
        @param expressnumber: 物流单号
        @param arrvseries: 到达序列号
        @return:
        """
        if not samples:
            samples = self.sample
        if expressnumber:
            logger.info(f"通过物流单号批量接收，物流单号：{expressnumber}")
            param = {"zexpressnumber": expressnumber}
        elif arrvseries:
            logger.info(f"通过到达序列号批量接收，到达序列号：{arrvseries}")
            param = {"zarrvseries": arrvseries}
        else:
            logger.info(f"默认使用物流单号批量接收，默认物流单号：9001")
            param = {"zexpressnumber": "9001"}

        headInfoDetail = {"zcontainer_type": "02",  # 容器类型 收纳盒
                          "zrqlx": "YCQX",  # 容器小类 SZ-病原
                          "c_temperature": "-4℃",  # 温度
                          "zplate_x": 99,  # 排版X
                          "zplate_y": 26,  # 排版Y
                          "flag_rq": "NEW",
                          "zzkpyls": "",
                          "zrqqz": ""}
        # 将物流单号或到达序列号合入headInfoDetail中
        headInfoDetail.update(param)
        # 将传入的样本编号格式化式，示例：[{"zcatalo":"sample1"},{"zcatalo":"sample2"}]
        zcataloInfo =  [{"zcatalo": x} for x in samples]
        data = {"zcataloInfo": zcataloInfo,
            "headInfo": [headInfoDetail],
            "token": self.token,
            "menuId": "XgBatchSampleConfirm",
            "zsjd_type": "YX"
        }
        response = self.samplecenter_res.post_request(url="/ybzx/webintf.do?method=save_xg_sample", data=urlencode(data))
        if response.status_code == 200 and response.json()["code"] == "200" and \
                "success" in response.json()["msg"]:
            logger.info("样本批量接收成功！")
        else:
            logger.error(f"样本批量接收失败！response：{response.json()}")
            raise Exception(f"样本批量接收失败！response：{response.json()}")

if __name__ == '__main__':
    test = DataGenerate(token="f511e606-523e-42ce-9aeb-092988b15f7b")
    # t = test.create_container()
    # t= test.medical_info_audit("24X120200001")
    # t = test.receipt_confirmation("OBR241100000477")
    # t = test.inbound_audit("IBR241200002989")
    samples = "25B01209453"
    test.lims_inbound_apply(samples)

    # print(t)

    # test.sumbit_sample()
    # test.send_package()
    # test.receive_package()
    # samples = ["24X091300000", "24X091300001"]
    # test.locate_position(samples=samples, container_num="mytest-0003", container_id="POP000000000051160")
    # test.query_container_by_container_num("mytest-0001")
