import pytest

from testcase.omicsone.conftest import mysql_connect
from utils.handle_excel import OperationExcel


def search_sequence_task(res, data):
    json_data = {
        "page": 1,
        "pageNum": 1,
        "limit": 100,
        "pageSize": 100
    }
    json_data.update(data)
    response = res.post_request("/api/sequencing/page", json=json_data)
    json_result = response.json()
    task_id = json_result["result"]["records"][0]["seqTaskId"]
    task_code = json_result["result"]["records"][0]["seqTaskCode"]
    response_result = {"status_code": response.status_code, "json": json_result, "task_id": task_id,
                       "task_code": task_code}
    yield response_result


@pytest.fixture(scope="function")
def handle_sequence_task(res, data):
    opt = data['option']
    json_data = data['task_items']
    tmp1 = {}
    response = res.post_request("/api/sequencing/create", json=json_data)
    # 创建完后把 task_id 查出来用于后续操作
    search_result = next(search_sequence_task(res, tmp1))
    task_id = search_result["task_id"]
    task_code = search_result["task_code"]
    response_result = {"status_code": response.status_code, "json": response.json(), "task_id": task_id,
                       "task_code": task_code}
    yield response_result
    # 后置删除任务
    if task_code and opt == "clear":
        try:
            res.post_request(f"/api/sequencing/delete/{task_code}")
        except Exception as e:
            print(f"Teardown: 删除任务 {task_code} 时出错: {e}")


def handle_upload_file(filename):
    search_sample_sql = 'select sp.sample_no from sample_patient sp LIMIT 3'
    mysql_select = mysql_connect().select(search_sample_sql)
    operate_excel = OperationExcel(filename, "Sheet1")
    for i in range(3):
        sample_no = mysql_select[i]["sample_no"]
        operate_excel.write_value(i+1, 0, sample_no)
    mysql_connect().close_database()
    return True
