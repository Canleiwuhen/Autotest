import pytest


@pytest.fixture(scope="function")
def handle_task(res_cloud, mysql_connect, request):
    """
    event:
    1、query: 查询;
    2、reparse: 重解析;
    3、terminate: 解读终止;
    4、finish: 完成服务;
    5、reset: 重置解读结果;
    """
    event = request.param
    # 查找解读中的任务
    query_data = {
        "page": 1,
        "pageNum": 1,
        "limit": 200,
        "pageSize": 200,
        "status": ["Interpreting"]
    }
    operator = ["interpreter", "interpreter_name"]
    query = res_cloud.post_request("/api/interpretation/nifty/task/list", json=query_data)
    task_id = query.json()['result']['records'][0]['taskId']
    operator_org = query.json()['result']['records'][0][operator[0]]
    operator_name_org = query.json()['result']['records'][0][operator[1].replace("_n", "N")]

    if event == "query":
        yield {'task_id': task_id}

    elif event == "reparse":
        mysql_connect.execute(f"update interpretation_task set status='ReceiveError' where task_id = '{task_id}' ")
        yield {'task_id': task_id}

    elif event in ["terminate", "forward", "finish", "reset"]:
        # 将任务的解读人设置为自动化测试账号
        mysql_connect.execute(f"update interpretation_task set {operator[0]} = 567289559516319744,"
                              f"{operator[1]} = '自动化测试-专家云' where task_id = '{task_id}'")
        # 在完成服务步骤中，更新专家意见确保值不为空
        if event == "finish":
            json_data = {"taskId": task_id, "manualServiceOpinion": "PassNegative"}
            res_cloud.post_request("api/interpretation/nifty/task/taskInfo/update", json=json_data)

        yield {'task_id': task_id}
        # 执行完用例后，把数据恢复回原始的解读人
        mysql_connect.execute(f"update interpretation_task set {operator[0]} = '{operator_org}',"
                              f"{operator[1]} = '{operator_name_org}' where task_id = '{task_id}'")
