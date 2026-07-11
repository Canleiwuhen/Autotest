import json
import time

import pytest
import allure
import os
from datetime import datetime

from testcase.halos.oseq.sequencetask.conftest import search_sequence_task
from utils.tools import calculate_file_buffer, replace_none
from testcase.halos.oseq.sequencetask.sequence_data import DataList


@pytest.mark.usefixtures("res", "res_file")
class TestSequence:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-查询")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search(self, res, data):
        tmp = data['search_items']
        # 如果createTime是日期格式，转换为时间戳格式
        if 'createTime' in tmp and tmp['createTime']:
            create_time = tmp['createTime']
            # 判断是否为日期格式（包含"-"且不是纯数字）
            if isinstance(create_time, str) and '-' in create_time:
                try:
                    # 分割日期字符串，格式为 "YYYY-MM-DD,YYYY-MM-DD"
                    dates = create_time.split(',')
                    timestamps = []
                    for date_str in dates:
                        # 解析日期字符串为datetime对象
                        date_obj = datetime.strptime(date_str.strip(), '%Y-%m-%d')
                        # 转换为时间戳（毫秒）
                        # 优先使用 timestamp()，如果失败则使用 time.mktime() 作为备用方案
                        try:
                            timestamp = int(date_obj.timestamp() * 1000)
                        except (OSError, OverflowError):
                            # 在某些系统上 timestamp() 可能失败，使用 mktime 作为备用
                            timestamp = int(time.mktime(date_obj.timetuple()) * 1000)
                        timestamps.append(str(timestamp))
                    # 用逗号连接时间戳
                    tmp['createTime'] = ','.join(timestamps)
                except (ValueError, AttributeError, OSError, OverflowError) as e:
                    # 如果转换失败，保持原值
                    print(f"日期转换失败: {e}, 保持原值: {create_time}")
                    pass
        json_data = {
            "page": 1,
            "size": 1
        }
        json_data.update(tmp)
        response = res.post_request("/prod-api/api/oseq/batchs/page", json=json_data)
        assert response.status_code == 200
        assert response.json()['success'] == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("测序任务-创建任务")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.sequence_data)
    def test_create_task(self, res, handle_sequence_task, data):
        status_code = handle_sequence_task["status_code"]
        json = handle_sequence_task["json"]
        assert status_code == 200
        # 新 API 返回格式可能是 success 或 retInfo
        assert json.get('success') == True or json.get('retInfo') == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-复用任务")
    @allure.title("复用任务")
    def test_reuse_task(self, res):
        data = {}
        response_result_before = next(search_sequence_task(res, data))
        task_id = response_result_before["task_id"]
        json_result = response_result_before["json"]
        # 从查询结果中获取 batchId, slideNo, createUser
        batch_id = json_result["result"]["rows"][0]["id"]
        slide_no = json_result["result"]["rows"][0]["slideNo"]
        create_user = json_result["result"]["rows"][0]["createUser"]
        # 使用新的传参格式
        reuse_data = {
            "batchId": batch_id,
            "slideNo": slide_no,
            "createUser": create_user
        }
        response = res.post_request("/prod-api/api/oseq/batchs/reuse", json=reuse_data)
        assert response.status_code == 200
        # 新 API 返回格式可能是 success 或 retInfo
        assert response.json().get('success') == True or response.json().get('retInfo') == 'success'
        # 后置把复用的任务删掉
        response_result_after = next(search_sequence_task(res, data))
        task_id_after = response_result_after["task_id"]
        res.delete_request(f"/prod-api/api/oseq/batchs/delete/{task_id_after}")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-删除任务")
    @allure.title("删除任务")
    @pytest.mark.parametrize("data", DataList.delete_data)
    def test_delete_task(self, res, handle_sequence_task, data):
        task_id = handle_sequence_task["task_id"]
        if task_id:
            response = res.delete_request(f"/prod-api/api/oseq/batchs/delete/{task_id}")
            assert response.status_code == 200
            # 新 API 返回格式可能是 success 或 retInfo
            assert response.json().get('success') == True or response.json().get('retInfo') == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-查看任务详情")
    @allure.title("查看任务详情")
    def test_query_task_detail(self, res):
        data = {}
        response_result = next(search_sequence_task(res, data))
        task_code = response_result["task_code"]
        # 使用新的传参格式
        detail_data = {
            "page": 1,
            "size": 1000,
            "batchNo": task_code
        }
        response = res.post_request("/prod-api/api/oseq/batchs/page/detail", json=detail_data)
        assert response.status_code == 200
        # 新 API 返回格式可能是 success 或 retInfo
        assert response.json().get('success') == True or response.json().get('retInfo') == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-停止任务")
    @allure.title("停止任务")
    @pytest.mark.parametrize("data", DataList.sequence_data[0:1])
    def test_stop_task(self, res, handle_sequence_task, data):
        task_id = handle_sequence_task["task_id"]
        task_code = handle_sequence_task["task_code"]
        slide_no = data['task_items']['slideNo']
        # 使用新的传参格式
        stop_data = {
            "batchId": task_id,
            "batchNo": task_code,
            "slideNo": slide_no
        }
        response = res.post_request("/prod-api/api/oseq/batchs/stop", json=stop_data)
        assert response.status_code == 200
        # 新 API 返回格式可能是 success 或 retInfo
        assert response.json().get('success') == True or response.json().get('retInfo') == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-启动任务")
    @allure.title("启动任务")
    @pytest.mark.parametrize("data", DataList.sequence_data[1:2])
    def test_start_task(self, res, handle_sequence_task, data):
        task_id = handle_sequence_task["task_id"]
        task_code = handle_sequence_task["task_code"]
        slide_no = data['task_items']['slideNo']
        # 使用新的传参格式
        start_data = {
            "batchId": task_id,
            "batchNo": task_code,
            "slideNo": slide_no
        }
        response = res.post_request("/prod-api/api/oseq/batchs/start", json=start_data)
        assert response.status_code == 200
        # 新 API 返回格式可能是 success 或 retInfo
        assert response.json().get('success') == True or response.json().get('retInfo') == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-编辑任务")
    @allure.title("编辑任务")
    @pytest.mark.parametrize("data", DataList.sequence_data[0:1])
    def test_edit_task(self, res, handle_sequence_task, data):
        task_id, task_code = handle_sequence_task["task_id"], handle_sequence_task["task_code"]
        slide_no = data['task_items']['slideNo']

        # 先查询任务详情（在停止任务前）
        detail_response = res.post_request("/prod-api/api/oseq/batchs/page/detail",
                                           json={"page": 1, "size": 1000, "batchNo": task_code})
        rows = detail_response.json().get('result', {}).get('rows', [])

        # 如果查询不到详情，等待一下再重试
        if not rows:
            time.sleep(2)
            detail_response = res.post_request("/prod-api/api/oseq/batchs/page/detail",
                                               json={"page": 1, "size": 1000, "batchNo": task_code})
            rows = detail_response.json().get('result', {}).get('rows', [])

        # 如果仍然查询不到，使用创建任务时的数据
        if not rows:
            # 使用创建任务时的原始数据
            original_lane = data['task_items'].get('lane', [])
            assert len(original_lane) > 0, "无法获取任务详情且创建数据为空，无法编辑任务"
            # 停止任务
            res.post_request("/prod-api/api/oseq/batchs/stop",
                             json={"batchId": task_id, "batchNo": task_code, "slideNo": slide_no})
            time.sleep(1)
            # 使用原始数据构建编辑请求
            response = res.put_request("/prod-api/api/oseq/batchs/edit", json={
                "batchNo": task_code,
                "slideNo": slide_no,
                "projectType": data['task_items'].get('projectType', 0),
                "preparationRunner": data['task_items'].get('preparationRunner') or None,
                "sequenceRunner": data['task_items'].get('sequenceRunner') or None,
                "kitExtraction": data['task_items'].get('kitExtraction') or None,
                "kitPreparation": data['task_items'].get('kitPreparation') or None,
                "kitSequencing": data['task_items'].get('kitSequencing') or None,
                "lane": original_lane
            })
        else:
            # 停止任务并等待
            res.post_request("/prod-api/api/oseq/batchs/stop",
                             json={"batchId": task_id, "batchNo": task_code, "slideNo": slide_no})
            time.sleep(2)

            # 空值转换
            to_none = lambda v: None if (v is None or (isinstance(v, str) and not v.strip())) else v

            # 按 lane 和 dnbId 分组样本
            lanes_dict = {}
            for row in rows:
                lane_no, dnb_id = str(row.get('laneNo', 'L01')), str(row.get('dnbId', '1'))
                lane_key = f"{lane_no}_{dnb_id}"
                if lane_key not in lanes_dict:
                    lanes_dict[lane_key] = {
                        "laneId": int(lane_no[1:]) if lane_no.startswith('L') else 1,
                        "dnbId": dnb_id,
                        "samples": []
                    }
                lanes_dict[lane_key]["samples"].append({
                    "id": row.get('id'),
                    "sampleId": row.get('sampleId'),
                    "sampleType": row.get('sampleType'),
                    "barcode": row.get('barcode'),
                    "subId": to_none(row.get('subId')),
                    "umiCode": row.get('umiCode'),
                    "dnaQualityAssessment": row.get('dnaQualityAssessment'),
                    "libraryType": row.get('libraryType'),
                    "libraryQualityAssessment": to_none(row.get('libraryQualityAssessment')),
                    "dnaLevel": to_none(row.get('dnaLevel'))
                })

            # 构建并发送编辑请求
            first_row = rows[0]
            response = res.put_request("/prod-api/api/oseq/batchs/edit", json={
                "batchNo": task_code, "slideNo": slide_no, "projectType": first_row.get('projectType', 0),
                "preparationRunner": to_none(first_row.get('preparationRunner')),
                "sequenceRunner": to_none(first_row.get('sequenceRunner')),
                "kitExtraction": to_none(first_row.get('kitExtraction')),
                "kitPreparation": to_none(first_row.get('kitPreparation')),
                "kitSequencing": to_none(first_row.get('kitSequencing')),
                "lane": list(lanes_dict.values())
            })

        assert response.status_code == 200
        json_response = response.json()
        assert json_response.get('success') == True or json_response.get('retInfo') == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-获取待选样本")
    @allure.title("获取待选样本")
    def test_query_sample(self, res):
        json_data = {
            "page": 1,
            "size": 30,
        }
        response = res.post_request("/prod-api/api/oseq/samples/page", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-获取设备ID")
    @allure.title("获取设备ID")
    def test_query_device(self, res):
        response = res.post_request("/prod-api/api/sys/properties/allPage",
                                    json={"page": 1, "size": 100, "parentId": 1000000010})
        assert response.status_code == 200
        json_response = response.json()
        assert json_response.get('success') == True or json_response.get('retInfo') == 'success'

        # 提取所有 value 字段并做成列表
        result = json_response.get('result', {})
        rows = result.get('rows', [])
        value_list = [item.get('value') for item in rows if item.get('value') is not None]
        # 验证列表不为空
        assert len(value_list) > 0, "value列表为空"
        print(f"提取的value列表: {value_list}")
        print(f"value列表长度: {len(value_list)}")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-获取测序平台")
    @allure.title("获取测序平台")
    def test_query_platform(self, res):
        response = res.post_request("/prod-api/api/sys/properties/allPage",
                                    json={"page": 1, "size": 100, "parentId": 1000000009})
        assert response.status_code == 200
        json_response = response.json()
        assert json_response.get('success') == True or json_response.get('retInfo') == 'success'

        # 提取所有 value 字段并做成列表
        result = json_response.get('result', {})
        rows = result.get('rows', [])
        value_list = [item.get('value') for item in rows if item.get('value') is not None]
        # 验证列表不为空
        assert len(value_list) > 0, "value列表为空"
        print(f"提取的value列表: {value_list}")
        print(f"value列表长度: {len(value_list)}")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("测序任务-查询产品套餐")
    @allure.title("查询产品套餐")
    def test_query_product(self, res):
        response = res.get_request("/prod-api/api/oseq/samples/allSysComboEx/2")
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("测序任务-下载模板")
    @allure.title("下载模板")
    def test_export_template(self, res):
        """
        导出所有模板，校验导出非空文件
        :param res:
        :return:
        """
        response = res.get_request(
            "/prod-api/api/sys/common/downloadFile?fileName=OSEQ%E4%BB%BB%E5%8A%A1%E5%AF%BC%E5%85%A5%E6%A8%A1%E6%9D%BF.xlsx")
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("测序任务-导入单芯片测序任务")
    @allure.title("导入单芯片测序任务")
    def test_upload_task(self, res, res_file):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(parent_dir, 'import_files')
        file_path = os.path.join(base_path, '单芯片任务模板.xlsx')

        # 第一步：调用导入接口
        import_response = res_file.post_request("/prod-api/api/oseq/batchs/import", file_path=file_path)
        assert import_response.status_code == 200
        import_json = import_response.json()
        assert import_json.get('success') == True or import_json.get('retInfo') == 'success'

        # 从导入接口响应中获取必要信息
        result = import_json.get('result', {})
        dest_path = result.get('destPath', '')
        venus_sample_sub_vos = result.get('venusSampleSubVos', [])

        assert dest_path, "导入接口未返回destPath"
        assert len(venus_sample_sub_vos) > 0, "导入接口未返回样本数据"

        # 第二步：调用确认接口
        # 从 sequence_data.py 中获取模板数据，并填充动态数据
        confirm_data = DataList.import_confirm_template.copy()
        confirm_data["venusSampleSubVos"] = venus_sample_sub_vos
        confirm_data["destPath"] = dest_path

        confirm_response = res_file.post_request("/prod-api/api/oseq/batchs/import/confirm", json=confirm_data)
        assert confirm_response.status_code == 200
        confirm_json = confirm_response.json()
        assert confirm_json.get('success') == True or confirm_json.get('retInfo') == 'success'

        # 后置把导入的任务删掉
        response_after_import = next(search_sequence_task(res, {}))
        task_code = response_after_import["task_code"]
        task_id = response_after_import["task_id"]
        res.delete_request(f"/prod-api/api/oseq/batchs/delete/{task_id}")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("测序任务-导入多芯片测序任务")
    @allure.title("导入多芯片测序任务")
    def test_upload_multitask(self, res, res_file):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(parent_dir, 'import_files')
        file_path = os.path.join(base_path, '合并任务模板.xlsx')

        # 第一步：调用多芯片导入接口
        import_response = res_file.post_request("/prod-api/api/oseq/batchs/import/multiTask", file_path=file_path)
        assert import_response.status_code == 200
        import_json = import_response.json()
        assert import_json.get('success') == True or import_json.get('retInfo') == 'success'

        # 从导入接口响应中获取必要信息
        result = import_json.get('result', {})
        dest_path = result.get('destPath', '')
        venus_sample_sub_vos = result.get('venusSampleSubVos', [])

        assert dest_path, "导入接口未返回destPath"
        assert len(venus_sample_sub_vos) > 0, "导入接口未返回样本数据"

        # 第二步：调用多芯片确认接口
        # 从 sequence_data.py 中获取模板数据，并填充动态数据
        confirm_data = DataList.import_confirm_template.copy()
        confirm_data["venusSampleSubVos"] = venus_sample_sub_vos
        confirm_data["destPath"] = dest_path

        confirm_response = res_file.post_request("/prod-api/api/oseq/batchs/import/multiTask/confirm",
                                                 json=confirm_data)
        assert confirm_response.status_code == 200
        confirm_json = confirm_response.json()
        assert confirm_json.get('success') == True or confirm_json.get('retInfo') == 'success'

        # 后置把导入的任务删掉
        response_after_import = next(search_sequence_task(res, {}))
        task_code = response_after_import["task_code"]
        task_id = response_after_import["task_id"]
        res.delete_request(f"/prod-api/api/oseq/batchs/delete/{task_id}")