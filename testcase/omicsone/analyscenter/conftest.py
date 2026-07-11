import os
from time import sleep

import pytest


@pytest.fixture(scope="class")
def pre_analysis(res, res_file):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(parent_dir, 'import_files')
    file_path = os.path.join(base_path, 'sequence_import.xlsx')
    json_data = {"sequencingTechType": "HighThroughput"}
    upload_response = res_file.post_request("/api/sequencing/import", data=json_data, file_path=file_path)
    # 导入测序任务成功之后查出分析中心第一条待分析的数据
    if upload_response.json()['retInfo'] == 'success':
        query_task = res.post_request("/api/sequencing/page", json={"page": 1, "pageNum": 1, "limit": 100, "pageSize": 100})
        task_code = query_task.json()['result']['records'][0]['seqTaskCode']
        json_data = {
            "page": 1,
            "pageNum": 1,
            "limit": 100,
            "pageSize": 100,
            "taskCode": [task_code]
        }
        query_response = res.post_request("/api/analysis/taskManager/list", json=json_data)
        if len(query_response.json()['result']['records']) == 0:
            return {"task_status": '任务启动分析失败'}
        task_id = query_response.json()['result']['records'][0]['taskId']
        # 等60s，等任务状态从待分析更新为分析中
        for i in range(12):
            tmp = res.post_request("/api/analysis/taskManager/list", json={"taskCode": [task_code]})
            task_status = tmp.json()['result']['records'][0]['taskStatus']
            if task_status == 'Pending':
                sleep(5)
            elif task_status == 'Running':
                break
            else:
                return {"task_status": task_status}
        return {"task_id": task_id, "task_code": task_code, "task_status": 'Running'}
    else:
        pytest.fail("测序任务导入失败")
