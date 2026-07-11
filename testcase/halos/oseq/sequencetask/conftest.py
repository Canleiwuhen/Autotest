import pytest


def search_sequence_task(res, data):
    json_data = {
        "page": 1,
        "pageNum": 1,
        "limit": 100,
        "pageSize": 100
    }
    json_data.update(data)
    response = res.post_request("/prod-api/api/oseq/batchs/page", json=json_data)
    json_result = response.json()
    task_id = json_result["result"]["rows"][0]["id"]
    task_code = json_result["result"]["rows"][0]["batchNo"]
    response_result = {"status_code": response.status_code, "json": json_result, "task_id": task_id,
                       "task_code": task_code}
    yield response_result


@pytest.fixture(scope="function")
def handle_sequence_task(res, data):
    opt = data['option']
    json_data = data['task_items']
    tmp1 = {}
    response = res.post_request("/prod-api/api/oseq/batchs/create", json=json_data)
    # 创建完后把 task_id 查出来用于后续操作
    search_result = next(search_sequence_task(res, tmp1))
    task_id = search_result["task_id"]
    task_code = search_result["task_code"]
    response_result = {"status_code": response.status_code, "json": response.json(), "task_id": task_id,
                       "task_code": task_code}
    yield response_result
    # 后置删除任务
    if task_id and opt == "clear":
        try:
            res.delete_request(f"/prod-api/api/oseq/batchs/delete/{task_id}")
        except Exception as e:
            print(f"Teardown: 删除任务 {task_id} 时出错: {e}")
