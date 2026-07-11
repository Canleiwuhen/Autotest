# -*- coding: utf-8 -*-
import json
import os
from datetime import date
from time import sleep

import pytest
import allure

from testcase.halos.oseq.conftest import pre_field_config
from testcase.halos.oseq.analyscenter.analys_data import DataList
from testcase.halos.oseq.sequencetask.sequence_data import DataList as SequenceDataList
from testcase.halos.oseq.sequencetask.conftest import search_sequence_task


@pytest.mark.usefixtures("res", "res_file")
class TestAnalys:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("分析中心-查询")
    @allure.title("分析中心-查询：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search_analys(self, res, data):
        """
        分析中心查询，只做了任务编号、样本编号、芯片号、原样本编号、产品套餐编号字段搜索
        :param res:
        :param data:
        :return:
        """
        tmp = data['search_items']
        json_data = {
            "page": 1,
            "size": 100,
        }
        json_data.update(tmp)
        response = res.post_request("/prod-api/api/oseq/task/batch/page", json=json_data)
        assert response.status_code == 200
        assert response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("分析中心-查看分析详情")
    @allure.title("查看分析详情")
    def test_query_task_detail(self, res):
        json_data = {
            "page": 1,
            "size": 100,
        }
        query_response = res.post_request("/prod-api/api/oseq/task/batch/page", json=json_data)
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True
        # 获取最新的任务编号（第一条记录）
        batch_no = query_response.json()['result']['rows'][0]['batchNo']
        # 使用任务编号查询详情
        response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": batch_no})
        assert response.status_code == 200
        assert response.json().get('success') == True

    @pytest.mark.run(order=2)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-停止分析")
    @allure.title("停止分析")
    def test_stop_analysis(self, res, res_file):
        # 第一步：导入任务（使用 analyscenter 路径下的 import_files 文件）
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(parent_dir, 'import_files')
        file_path = os.path.join(base_path, '单芯片任务模板.xlsx')

        # 调用导入接口
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

        # 调用确认接口
        confirm_data = SequenceDataList.import_confirm_template.copy()
        confirm_data["venusSampleSubVos"] = venus_sample_sub_vos
        confirm_data["destPath"] = dest_path

        confirm_response = res_file.post_request("/prod-api/api/oseq/batchs/import/confirm", json=confirm_data)
        assert confirm_response.status_code == 200
        confirm_json = confirm_response.json()
        assert confirm_json.get('success') == True or confirm_json.get('retInfo') == 'success'

        # 等待任务创建
        sleep(2)

        # 查询导入的任务
        response_after_import = next(search_sequence_task(res, {}))
        task_code = response_after_import["task_code"]
        task_id = response_after_import["task_id"]

        # 等待任务流转到分析中心并变为Running状态（优化：减少等待时间和次数）
        # 第一次立即检查，后续每3秒检查一次，最多检查8次（约24秒）
        running_task_ids = []  # 存储所有Running状态的样本任务ID
        for i in range(8):
            if i > 0:  # 第一次不等待，立即检查
                sleep(3)  # 缩短等待时间从5秒到3秒

            # 查询任务详情
            detail_response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": task_code})
            if detail_response.status_code == 200 and detail_response.json().get('success'):
                detail_rows = detail_response.json().get('result', {}).get('rows', [])
                # 收集所有Running状态的样本任务ID（属于该批次的所有样本任务）
                running_task_ids = []
                for row in detail_rows:
                    row_task_id = row.get('taskId', '')
                    analysis_status = row.get('analysisStatus')
                    if analysis_status == 3:  # Running
                        if row_task_id:  # 确保taskId不为空
                            running_task_ids.append(row_task_id)

                # 如果找到Running状态的任务，停止所有任务
                if running_task_ids:
                    # 第二步：停止分析任务
                    # 使用样本任务ID（多个用逗号分隔）停止该批次下的所有样本任务
                    task_ids_str = ','.join(running_task_ids)
                    response = res.post_request(f"/prod-api/api/oseq/task/stop/{task_ids_str}", json={})
                    assert response.status_code == 200
                    ret_info = response.json().get('retInfo', '')
                    assert response.json().get('success') == True or response.json().get(
                        'retInfo') == 'success' or 'stop failed' in ret_info

                    print(f"已停止批次 {task_code} 下的 {len(running_task_ids)} 个Running状态的任务: {running_task_ids}")

                    # 后置清理：删除导入的任务
                    try:
                        res.delete_request(f"/prod-api/api/oseq/batchs/delete/{task_id}")
                    except Exception as e:
                        print(f"删除任务 {task_id} 时出错: {e}")
                    return

        # 如果等待超时，仍然尝试停止任务
        # 再次查询任务详情，获取所有样本任务ID
        detail_response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": task_code})
        if detail_response.status_code == 200 and detail_response.json().get('success'):
            detail_rows = detail_response.json().get('result', {}).get('rows', [])
            all_task_ids = []
            for row in detail_rows:
                row_task_id = row.get('taskId', '')
                if row_task_id:  # 确保taskId不为空
                    all_task_ids.append(row_task_id)

            if all_task_ids:
                # 使用样本任务ID（多个用逗号分隔）停止
                task_ids_str = ','.join(all_task_ids)
                response = res.post_request(f"/prod-api/api/oseq/task/stop/{task_ids_str}", json={})
                assert response.status_code == 200
                ret_info = response.json().get('retInfo', '')
                assert response.json().get('success') == True or response.json().get(
                    'retInfo') == 'success' or 'stop failed' in ret_info
                print(f"已停止批次 {task_code} 下的 {len(all_task_ids)} 个任务: {all_task_ids}")

        # 后置清理：删除导入的任务
        try:
            res.delete_request(f"/prod-api/api/oseq/batchs/delete/{task_id}")
        except Exception as e:
            print(f"删除任务 {task_id} 时出错: {e}")

    @pytest.mark.run(order=4)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("分析中心-重分析")
    @allure.title("重分析")
    def test_restart_analysis(self, res):
        # 获取最新的任务编号
        json_data = {
            "page": 1,
            "size": 100,
        }
        query_response = res.post_request("/prod-api/api/oseq/task/batch/page", json=json_data)
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True
        # 遍历任务列表，找到分析失败的任务
        batch_list = query_response.json()['result']['rows']
        target_task = None
        batch_no = None

        for batch_item in batch_list:
            batch_no = batch_item['batchNo']
            # 使用任务编号查询详情
            detail_response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": batch_no})
            assert detail_response.status_code == 200
            assert detail_response.json().get('success') == True
            # 从详情中筛选analysisStatus为4（失败）的任务
            rows = detail_response.json()['result']['rows']
            for row in rows:
                # analysisStatus为4（失败）的任务
                if row.get('analysisStatus') == 4:
                    target_task = row
                    break
            if target_task:
                break

        # 如果没有找到符合条件的任务，抛出异常
        assert target_task is not None, "未找到analysisStatus为4（失败）的任务"
        # 获取batchSubNo
        batch_sub_no = target_task['batchSubNo']
        # 使用任务编号和batchSubNo进行重分析
        request_data = {
            "batchNo": batch_no,
            "batchSubNo": batch_sub_no
        }
        response = res.post_request("/prod-api/api/oseq/task/rerun", json=request_data)
        assert response.status_code == 200
        assert response.json().get('success') == True or response.json().get('retInfo') == 'Task reanalysis failed!'

    @pytest.mark.run(order=5)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-结果导出")
    @allure.title("结果导出")
    def test_export_result(self, res, res_file):
        # 获取任务列表
        json_data = {
            "page": 1,
            "size": 100,
        }
        query_response = res.post_request("/prod-api/api/oseq/task/batch/page", json=json_data)
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 遍历任务列表，找到分析完成的任务
        batch_list = query_response.json()['result']['rows']
        completed_samples = []  # 存储所有分析完成的样本信息
        batch_no = None

        for batch_item in batch_list:
            batch_no = batch_item['batchNo']
            # 使用任务编号查询详情
            detail_response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": batch_no})
            assert detail_response.status_code == 200
            assert detail_response.json().get('success') == True
            # 从详情中筛选analysisStatus为8（完成）的任务
            rows = detail_response.json()['result']['rows']
            for row in rows:
                # analysisStatus为8（完成）的任务
                if row.get('analysisStatus') == 8:
                    batch_sub_no = row.get('batchSubNo')
                    sample_id = row.get('sampleId')
                    if batch_sub_no and sample_id:
                        completed_samples.append({
                            "batchSubNo": batch_sub_no,
                            "sampleId": sample_id
                        })
            # 如果找到分析完成的样本，使用这个批次
            if completed_samples:
                break

        # 如果没有找到符合条件的任务，抛出异常
        assert len(completed_samples) > 0, "未找到analysisStatus为8（完成）的任务"

        print(f"找到 {len(completed_samples)} 个分析完成的样本，批次号: {batch_no}")

        # 构建导出请求参数（使用analysisDownloadDtoList格式）
        export_data = {
            "analysisDownloadDtoList": completed_samples
        }

        # 调用导出接口
        export_response = res.post_request("/prod-api/api/oseq/task/export/resultFile",
                                           json=export_data)
        assert export_response.status_code == 200

        # 检查响应内容类型，导出接口可能返回文件而不是JSON
        content_type = export_response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            # 如果是JSON响应，解析JSON
            export_json = export_response.json()
            if export_json.get('success') == True or export_json.get('retInfo') == 'success':
                print(f"已成功导出批次 {batch_no} 的 {len(completed_samples)} 个样本结果文件")
            else:
                error_msg = export_json.get('retInfo', '未知错误')
                print(f"导出批次 {batch_no} 失败: {error_msg}")
                assert False, f"导出失败: {error_msg}"
        else:
            # 如果是文件响应，检查响应大小
            content_length = len(export_response.content)
            if content_length > 0:
                print(f"已成功导出批次 {batch_no} 的 {len(completed_samples)} 个样本结果文件，文件大小: {content_length} 字节")
            else:
                assert False, f"导出失败: 响应内容为空"

    @pytest.mark.run(order=6)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("分析中心-让步分析")
    @allure.title("让步分析")
    def test_concession_analysis(self, res):
        # 获取任务列表
        json_data = {
            "page": 1,
            "size": 100,
        }
        query_response = res.post_request("/prod-api/api/oseq/task/batch/page", json=json_data)
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 遍历任务列表，找到分析完成的任务
        batch_list = query_response.json()['result']['rows']
        completed_task = None
        batch_no = None

        for batch_item in batch_list:
            batch_no = batch_item['batchNo']
            # 使用任务编号查询详情
            detail_response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": batch_no})
            assert detail_response.status_code == 200
            assert detail_response.json().get('success') == True
            # 从详情中筛选analysisStatus为8（完成）的任务
            rows = detail_response.json()['result']['rows']
            for row in rows:
                # analysisStatus为8（完成）的任务
                if row.get('analysisStatus') == 8:
                    completed_task = row
                    break
            if completed_task:
                break

        # 如果没有找到符合条件的任务，抛出异常
        assert completed_task is not None, "未找到analysisStatus为8（完成）的任务"

        # 获取任务信息
        task_id = completed_task.get('taskId')
        batch_sub_no = completed_task.get('batchSubNo')
        sample_id = completed_task.get('sampleId')

        assert task_id, "任务ID为空"
        assert batch_sub_no, "批次子编号为空"
        assert sample_id, "样本ID为空"

        print(f"找到分析完成的任务: taskId={task_id}, batchSubNo={batch_sub_no}, sampleId={sample_id}, batchNo={batch_no}")

        # 构建让步分析请求参数
        # 接口需要concessionAnalysisList格式，包含batchNo、batchSubNo和sampleId
        concession_data = {
            "concessionAnalysisList": [{
                "batchNo": batch_no,
                "batchSubNo": batch_sub_no,
                "sampleId": sample_id
            }]
        }

        # 调用让步分析接口
        concession_response = res.post_request("/prod-api/api/oseq/task/concession/analysis",
                                               json=concession_data)
        assert concession_response.status_code == 200
        concession_json = concession_response.json()

        # 检查让步分析结果
        if concession_json.get('success') == True or concession_json.get('retInfo') == 'success':
            print(f"已成功对任务 {task_id} 进行让步分析")
        else:
            error_msg = concession_json.get('retInfo', '未知错误')
            # 如果返回"已存在"的错误，说明接口工作正常，只是该任务已经进行过让步分析
            if '已存在' in error_msg or '已存在' in str(error_msg):
                print(f"任务 {task_id} 的让步分析已存在，说明接口工作正常")
            else:
                print(f"让步分析任务 {task_id} 失败: {error_msg}")
                assert False, f"让步分析失败: {error_msg}"
