# -*- coding: utf-8 -*-
import pytest
from datetime import datetime

from testcase.omicsone.conftest import mysql_connect
from utils.handle_excel import OperationExcel


def search_experiment_task(res, data):
    json_data = {
        "page": 1,
        "pageNum": 1,
        "limit": 100,
        "pageSize": 100
    }
    json_data.update(data)
    response = res.post_request("/prod-api/api/oseq/experimental/task/page", json=json_data)
    json_result = response.json()
    task_id = json_result["result"]["records"][0]["taskId"]
    task_code = json_result["result"]["records"][0]["taskCode"]
    response_result = {"status_code": response.status_code, "json": json_result, "task_id": task_id,
                       "task_code": task_code}
    yield response_result


@pytest.fixture(scope="function")
def handle_experiment_task(res, data):
    opt = data['option']
    tmp = data['task_items']
    tmp1 = {}
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    json_data = {
        "createTime": current_time,
        "updateTime": current_time
    }
    json_data.update(tmp)
    response = res.post_request("/api/experiment/add", json=json_data)
    # 获取 task_id 用于后续清理操作
    search_result = next(search_experiment_task(res, tmp1))
    task_id = search_result["task_id"]
    task_code = search_result["task_code"]
    response_result = {"status_code": response.status_code, "json": response.json(), "task_id": task_id,
                       "task_code": task_code}
    yield response_result
    # 测试执行后关闭和删除
    if task_id and opt == "clear":
        try:
            res.post_request("/api/experiment/close", json={"taskId": task_id})
        except Exception as e:
            print(f"Teardown: 关闭任务 {task_id} 时出错: {e}")

        try:
            res.post_request("/api/experiment/delete", json={"taskId": task_id})
        except Exception as e:
            print(f"Teardown: 删除任务 {task_id} 时出错: {e}")
    # 只删除，不执行关闭，在case之后删除测试数据
    if task_id and opt == "delete":
        try:
            res.post_request("/api/experiment/delete", json={"taskId": task_id})
        except Exception as e:
            print(f"Teardown: 删除任务 {task_id} 时出错: {e}")


def handle_upload_file(product, filename):
    search_sample_sql = 'select sp.sample_no from sample_patient sp ' \
                        'inner join sample_inspection si on si.sample_inspection_id = sp.sample_inspection_id ' \
                        f"where si.project_code = '{product}' LIMIT 8"
    mysql_select = mysql_connect().select(search_sample_sql)
    operate_excel = OperationExcel(filename, "Sheet1")
    for i in range(8):
        sample_no = mysql_select[i]["sample_no"]
        operate_excel.write_value(i+1, 2, sample_no)
    mysql_connect().close_database()
    return True


if __name__ == '__main__':
    handle_upload_file('CS', '')
    # result = handle_upload_file('CS')
    # print(result[0])
