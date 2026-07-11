import datetime
from urllib.parse import urlencode

import allure
import pytest

from data_generate.samplecenter.datagenerate import DataGenerate
from testcase.samplecenter.conftest import *


@allure.feature("入库申请")
@pytest.mark.usefixtures("res", "token")
class TestInboundApply:
    list_sample_search = [
        {"zsjd_type": "KF"},  # 科服
        {"zmatnr_ty": "T099"},  # 产品组合
        {"matnr": "DX1712"},  # 产品编码
        {"zcatalo": "1037747022"},  # 样本编号
        {"zsample": "1037747022"},  # 样例编号
        {"zcdate": "20240901", "zcdateend": "20240929"},  # 出库日期
        {"zscdh": "OBR240900000285"},  # 出库申请单号，此数据需要依赖于前一步的出库审核
        {"zcwlx": "S051"},    # 样本类型
    ]
    inbound_apply_data = [
        {
            "params": {  # params入库申请信息
                "zzzbm": "BC01",  # 库存地点
                "zreson": "生产归还",  # 入库原因
                "zyqyrq": "20241012",  # 应取样日期
                "lgort_t": "XB39",  # 接收库存地点
                "lgort_f": "BC01",  # 发出库存地点
                "ztprt": "常温"  # 保存条件
            },
        }
    ]
    list_apply_bill_search = [
        {"zscdh": "IBR241000002275"},  # 入库申请单号
        {"zreqstat_code": "00"},  # 状态
        {"zreqstat_code": "05"},  # 状态
        {"zreqstat_code": "10"},  # 状态
        {"zreqstat_code": "20"},  # 状态
        {"zcatalo": "24X101400059"},  # 样本编号
        {"zcjnam": "autotest1"},  # 申请人
        {"zcjdat": "20240914", "zcjdatend": "20241014"},  # 申请日期
        # {"zjob_code": ""},  # 任务单号，没有数据有任务单号
    ]

    # @pytest.mark.skip('跳过')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('入库申请样本搜索')
    @pytest.mark.parametrize("data", list_sample_search)
    def test_inbound_apply_sample_search(self, res, token, data):
        query_data = {
            "task": '{"zybzx":"X","zcdate":"20240829","zcdateend":"20240929","zsjd_type":"YX"}',
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        query_data.update(data)
        ret = res.post_request(url='/ybzx/webintf.do?method=query_wait_in_bound_samples', data=urlencode(query_data))
        assert ret.status_code == 200 and ret.json()[
            "code"] == "200", f"查询入库申请单失败！response：{ret.json()}"

    # @pytest.mark.skip('跳过')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title('样本入库申请')
    def test_inbound_apply(self, res, token):
        # 出库审核后才能创建入库申请单，outbound_apply拿到出库申请单号
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        dg = DataGenerate(token)
        sample = dg.sumbit_sample()  # 提交送检单，生成样本编号
        expressnum = dg.send_package(sample[0])  # 寄送包裹，生成快递单号
        _ = dg.receive_package(expressnum)  # 包裹接收
        if dg.unpack(expressnum):  # 医学拆包
            container_num, container_id = dg.create_container("autotest", 96)  # 创建容器
            if dg.locate_position(sample, container_num, container_id):  # 医学到样定位（新）
                outbound_apply = dg.outbound_apply(sample[0])  # 出库申请
                dg.outbound_audit(outbound_apply)  # 出库审核
            else:
                raise Exception("医学到样定位异常！")
        else:
            raise Exception("医学拆包异常！")
        # 通过出库申请单号查询数据并获取样本信息
        query_data = {
            "task": {"zybzx":"X","zsjd_type":"YX","zscdh": outbound_apply},
            "pageNumber": "1",
            "pageSize": "50",
            "menuId": "InBoundApply",
            "zsjd_type": "YX",
            "token": token
        }
        query_response = res.post_request(url="/ybzx/webintf.do?method=query_wait_in_bound_samples",
                                          data=urlencode(query_data))
        assert query_response.status_code == 200 and query_response.json()[
            "code"] == "200", f"查询出库申请单样本信息失败！response：{query_response.json()}"

        # 拿到样本信息作为入库申请单入参
        collect_date = str(datetime.date.today()).replace('-', '')
        apply_data = {
            "params": {"zzzbm": "BC01", "zreson": "生产归还", "zyqyrq": collect_date, "lgort_t": "XB39",
                       "lgort_f": "BC01", "ztprt": "常温"},  # 应取样日期和保存条件可以为空
            "samples": [
                {"_key": 1, "_id": 1}
            ],
            "zsjd_type": "YX",
            "menuId": "InBoundApply",
            "token": token
        }
        # 更新样本信息
        apply_data['samples'][0].update(query_response.json()['data'][0])
        apply_response = res.post_request(url='/ybzx/webintf.do?method=create_in_bound_apply',
                                          data=urlencode(apply_data))
        assert apply_response.status_code == 200 and apply_response.json()[
            "code"] == "200", f"创建入库申请单失败！response：{apply_response.json()}"

    # @pytest.mark.skip('跳过')
    # def test_inbound_apply_total(self, res, token):
    #     data = DataGenerate()
    #     sampleid = data.sumbit_sample()
    #     print(sampleid)
    #     expressnum = data.send_package(sampleid[0])
    #     print(expressnum)
    #     data.receive_package(expressnum)
    #     data.unpack(expressnum)
    #     container_num = data.create_container()[0]
    #     container_id = data.create_container()[1]
    #     data.locate_position(sampleid, container_num)
    #     outboundnum = data.outbound_apply(sampleid)
    #     data.outbound_audit(outboundnum)


    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('查询&交接确认搜索')
    @pytest.mark.parametrize("data", list_apply_bill_search)
    def test_inbound_apply_bill_search(self, res, token, data):
        query_data = {
            "task": {"zybzx": "X"},
            "pageNumber": "1",
            "pageSize": "50",
            "token": token("testuser1")["token"],
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        query_data['task'].update(data)
        ret = res.post_request(url='/ybzx/webintf.do?method=query_in_bound_apply_bill', data=urlencode(query_data))
        assert ret.status_code == 200 and ret.json()[
            "code"] == "200", f"查询入库交接单失败！response：{ret.json()}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('查询&交接详情预览')
    def test_inbound_detail_preview(self, res, token, data):
        query_data = {
            "zscdh": "IBR241000002244",  # 暂时写死
            "token": token("testuser1")["token"],
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        ret = res.post_request(url='/ybzx/webintf.do?method=query_samples_by_sqdh_of_in_bound_apply',
                               data=urlencode(query_data))
        assert ret.status_code == 200 and ret.json()[
            "code"] == "200", f"查询样本详情预览失败！response：{ret.json()}"
        # 判断传入的多个申请单号的样本总数与实际返回是否能对应上？

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('交接确认')
    def test_inbound_confirmation(self, res, token):
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        dg = DataGenerate(token)
        sample = dg.sumbit_sample()  # 提交送检单，生成样本编号
        expressnum = dg.send_package(sample[0])  # 寄送包裹，生成快递单号
        _ = dg.receive_package(expressnum)  # 包裹接收
        if dg.unpack(expressnum):  # 医学拆包
            container_num, container_id = dg.create_container("autotest", 96)  # 创建容器
            if dg.locate_position(sample, container_num, container_id):  # 医学到样定位（新）
                outbound_apply = dg.outbound_apply(sample[0])  # 出库申请
                dg.outbound_audit(outbound_apply)  # 出库审核
                inbound_apply = dg.inbound_apply(sample[0])  # 入库申请，获取入库申请单号
            else:
                raise Exception("医学到样定位异常！")
        else:
            raise Exception("医学拆包异常！")

        confirmation_data = {
            "datas": [{"zscdh": inbound_apply}],
            "token": token,
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        ret = res.post_request(url='/ybzx/webintf.do?method=save_inapply_confirmation',
                               data=urlencode(confirmation_data))
        assert ret.status_code == 200 and ret.json()[
            "code"] == "200", f"交接确认失败！response：{ret.json()}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('删除出入库申请单')
    def test_inbound_delete(self, res, token):
        token = token("testuser1")["token"]
        # 通过数据生成工具类生成数据
        dg = DataGenerate(token)
        sample = dg.sumbit_sample()  # 提交送检单，生成样本编号
        expressnum = dg.send_package(sample[0])  # 寄送包裹，生成快递单号
        _ = dg.receive_package(expressnum)  # 包裹接收
        if dg.unpack(expressnum):  # 医学拆包
            container_num, container_id = dg.create_container("autotest", 96)  # 创建容器
            if dg.locate_position(sample, container_num, container_id):  # 医学到样定位（新）
                outbound_apply = dg.outbound_apply(sample[0])  # 出库申请
                dg.outbound_audit(outbound_apply)  # 出库审核
                inbound_apply = dg.inbound_apply(sample[0])  # 入库申请，获取入库申请单号
            else:
                raise Exception("医学到样定位异常！")
        else:
            raise Exception("医学拆包异常！")

        delete_data = {
            "datas": [],
            "token": token,
            "menuId": "InBoundApply",
            "zsjd_type": "YX"
        }
        # 遍历获取入库申请单下的所有样本
        for i in sample:
            delete_data['datas'].append({"zscdh": inbound_apply, "zcatalo": i})

        ret = res.post_request(url='/ybzx/webintf.do?method=save_delete_out_apply',
                               data=urlencode(delete_data))
        print(delete_data)
        assert ret.status_code == 200 and ret.json()[
            "code"] == "200", f"出入库申请单删除失败！response：{ret.json()}"

    # def test_inbound_


if __name__ == '__main__':
    data = DataGenerate()
    print(data.sumbit_sample())
