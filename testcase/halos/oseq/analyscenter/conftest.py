# -*- coding: utf-8 -*-
from time import sleep

import pytest


@pytest.fixture(scope="class")
def pre_analysis(res):
    # 从分析中心查询任务列表，查找Running状态的任务
    json_data = {
        "page": 1,
        "size": 100,
    }
    query_response = res.post_request("/prod-api/api/oseq/task/batch/page", json=json_data)
    assert query_response.status_code == 200
    assert query_response.json().get('success') == True

    rows = query_response.json()['result']['rows']
    if len(rows) == 0:
        pytest.fail("分析中心没有可用任务")

    # 遍历任务列表，查找Running状态的任务
    # analysisStatus: 3=Running, 4=Failed, 8=Completed
    for batch_item in rows:
        batch_no = batch_item['batchNo']
        task_code = batch_no

        # 使用任务编号查询详情
        detail_response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": batch_no})
        assert detail_response.status_code == 200
        assert detail_response.json().get('success') == True

        detail_rows = detail_response.json()['result']['rows']
        if len(detail_rows) == 0:
            continue

        # 遍历任务详情，查找Running状态的任务
        for row in detail_rows:
            analysis_status = row.get('analysisStatus')
            if analysis_status == 3:  # Running
                task_id = row.get('taskId')
                return {"task_id": task_id, "task_code": task_code, "task_status": 'Running'}

        # 如果当前batch没有Running状态的任务，检查是否有Pending状态的任务（可能会变成Running）
        # 等待一段时间后重试
        for row in detail_rows:
            analysis_status = row.get('analysisStatus')
            # 如果状态是Pending或其他非完成状态，等待后重试
            if analysis_status not in [4, 8]:  # 不是Failed或Completed
                task_id = row.get('taskId')
                # 等待任务状态变为Running
                for i in range(12):
                    sleep(5)
                    current_detail = res.post_request("/prod-api/api/oseq/task/pageByBatchNo",
                                                      json={"batchNo": batch_no})
                    assert current_detail.status_code == 200
                    assert current_detail.json().get('success') == True

                    current_rows = current_detail.json()['result']['rows']
                    for current_row in current_rows:
                        if current_row.get('taskId') == task_id:
                            current_status = current_row.get('analysisStatus')
                            if current_status == 3:  # Running
                                return {"task_id": task_id, "task_code": task_code, "task_status": 'Running'}
                            elif current_status in [4, 8]:  # Failed或Completed，跳出内层循环
                                break
                    else:
                        continue
                    break

    # 如果遍历完所有任务都没有找到Running状态，返回第一个任务的状态
    batch_no = rows[0]['batchNo']
    task_code = batch_no
    detail_response = res.post_request("/prod-api/api/oseq/task/pageByBatchNo", json={"batchNo": batch_no})
    detail_rows = detail_response.json()['result']['rows']
    if len(detail_rows) > 0:
        task_id = detail_rows[0].get('taskId')
        analysis_status = detail_rows[0].get('analysisStatus')
        status_map = {3: 'Running', 4: 'Failed', 8: 'Completed'}
        status = status_map.get(analysis_status, f'Unknown({analysis_status})')
        return {"task_id": task_id, "task_code": task_code, "task_status": status}

    pytest.fail("未找到可用任务")