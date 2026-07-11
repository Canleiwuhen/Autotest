import pytest


@pytest.fixture(scope="function")
def handle_task(res, mysql_connect, request):
    """
    event:
    1、query: 查询;
    2、operate: 需要修改解读人/审核人以便后续操作;
    3、reparse: 重解析;
    4、terminate: 解读终止;
    5、finish: 完成服务;
    6、urgent: 加急;
    7、submit_review: 提交审核;
    8、allocate: 手动分配;
    9、couple_merge: 配对分析;
    10、recomplete: 流转失败报告重新推送;
    11、fallback: 退回解读;
    12、variant_detail: 查看变异详情;
    """
    # 入参：解读状态，操作事件，返回数据条数
    status, event, count = request.param
    operator = []
    if status == "review":
        search_item = {"status": ["ReadyForReview", "Reviewing"]}
        operator = ["reviewer", "reviewer_name"]
    elif status == "fallback-positive":
        search_item = {
            "status": ["ReadyForReview", "Reviewing"],
            "checkoutTips": ["Positive"]
        }
        operator = ["reviewer", "reviewer_name"]
    elif status == "fallback-negative":
        search_item = {
            "status": ["ReadyForReview", "Reviewing"],
            "checkoutTips": ["Negative"],
            "spouseCheckoutTips": ["Negative"]
        }
        operator = ["reviewer", "reviewer_name"]
    elif status == "allocate-positive":  # 检出提示、配偶检出其中一个为阳性就是阳性样本
        search_item = {
            "status": ["ReadyForAllocate"],
            "checkoutTips": ["Positive"]
        }
    elif status == "allocate-negative":  # 检出提示、配偶检出均为阴性是阴性样本
        search_item = {
            "status": ["ReadyForAllocate"],
            "checkoutTips": ["Negative"]
            # "spouseCheckoutTips": ["Negative"]  # 新生儿没有配偶检出字段
        }
    elif status == "allocate":
        search_item = {"status": ["ReadyForAllocate"]}
    elif status == "finish" and event == "recomplete":
        search_item = {"status": ["Finished"], "reportStatus": ["Fail"]}
    else:
        search_item = {"status": ["ReadyForInterpret", "Interpreting"]}
        operator = ["interpreter", "interpreter_name"]
    query_data = {
        "page": 1,
        "pageNum": 1,
        "limit": 200,
        "pageSize": 200,
        "doctorOpinion": ["Pass"]
    }
    query_data.update(search_item)
    query = res.post_request("/api/interpretation/nbs/task/list", json=query_data)
    result = []
    for i in range(count):
        tmp = {
            "status": status,
            "sample_data_tag": query.json()['result']['records'][i]['sampleTestResult'],
            "task_id": query.json()['result']['records'][i]['taskId'],
            "operator_org": query.json()['result']['records'][i][operator[0]] if len(operator) > 0 else '',
            "operator_name_org": query.json()['result']['records'][i][operator[1].replace("_n", "N")]
            if len(operator) > 0 else ''
        }
        result.append(tmp)

    if event in ["query", "recomplete"]:
        yield result

    elif event == "reparse":
        for item in result:
            mysql_connect.execute(f"update interpretation_task set status='ReceiveError' "
                                  f"where task_id = '{item['task_id']}' ")
        yield result

    elif event == "allocate":
        yield result
        # 将状态重置回待分配
        for item in result:
            mysql_connect.execute(f"update interpretation_task set status='ReadyForAllocate' "
                                  f"where task_id = '{item['task_id']}' ")

    elif event == "couple_merge":
        if status in ["interpret", "review"]:
            # 查找符合配对分析校验的任务
            task_ids = mysql_connect.select(f"select a.sample_no, a.task_id, a.{operator[0]}, a.{operator[1]} from "
                                            f"interpretation_task a inner join (select sample_no,product_no,"
                                            f"task_info ->>'$.spouseSampleNo' as spouse_no from interpretation_task "
                                            f"where task_info->>'$.spouseSampleNo' is not null and project_code = 'CS' "
                                            f"and task_source = 'Centre' and status not in ('ReceiveError','Receiving')"
                                            f") b on a.sample_no = b.spouse_no and a.product_no = b.product_no where "
                                            f"a.status in ('{search_item['status'][0]}', '{search_item['status'][1]}') "
                                            f"and a.project_code = 'CS' and a.task_source = 'Centre'")
            # 将当前任务的解读人/审核人设置为自动化测试账号
            for i in range(count):
                mysql_connect.execute(f"update interpretation_task set {operator[0]} = 562663278568931328,"
                                      f"{operator[1]} = '自动化测试_中心交付' where task_id = '{task_ids[i]['task_id']}'")
                print(f"任务：{task_ids[i]['task_id']} 已分配给自动化测试账号")
            yield task_ids[:count]
            # 执行完用例后，把数据恢复回原始的解读人/审核人
            for i in range(count):
                mysql_connect.execute(f"update interpretation_task set {operator[0]} = '{task_ids[i][f'{operator[0]}']}',"
                                      f"{operator[1]} = '{task_ids[i][f'{operator[1]}']}' "
                                      f"where task_id = '{task_ids[i]['task_id']}'")
        else:
            pytest.fail("配对分析请选择解读状态或审核状态的任务")

    elif event == "variant_detail":
        task_ids = [item["task_id"] for item in result if len(result) > 0]
        search_data = {
            "page": 1, "pageNum": 1, "limit": 50, "pageSize": 50, "taskIds": task_ids
        }
        response = res.post_request(url="/api/interpretation/nbs/exoncnvandsnv/list", json=search_data)
        variant_id = response.json()["result"]["records"][0]["variantId"]
        yield [{"variant_id": variant_id}]

    else:
        # 将任务的解读人/审核人设置为自动化测试账号
        for item in result:
            mysql_connect.execute(f"update interpretation_task set {operator[0]} = 562663278568931328,"
                                  f"{operator[1]} = '自动化测试_中心交付' where task_id = '{item['task_id']}'")
            # 去除原本有的加急标签
            if event == "urgent":
                # 去除原本有的加急标签
                mysql_connect.execute(f"delete from interpretation_task_tag where tag_name = 'UrgentSample' and "
                                      f"task_id = '{item['task_id']}'")
        yield result
        # 执行完用例后，把数据恢复回原始的解读人/审核人
        for item in result:
            mysql_connect.execute(f"update interpretation_task set {operator[0]} = '{item['operator_org']}',"
                                  f"{operator[1]} = '{item['operator_name_org']}' "
                                  f"where task_id = '{item['task_id']}'")
            # 提交审核用例执行之后把状态重置回解读中
            if event == "submit_review":
                mysql_connect.execute(f"update interpretation_task set status = 'Interpreting' where "
                                      f"task_id = '{item['task_id']}'")
            # 退回解读用例执行之后把状态重置回审核中
            if event == "fallback":
                mysql_connect.execute(f"update interpretation_task set status = 'Reviewing' where "
                                      f"task_id = '{item['task_id']}'")

@pytest.fixture(scope="function")
def pre_validate_task(res, mysql_connect, request):
    types = request.param
    result = mysql_connect.select(f"select iv.variant_id, iv.task_id, iv.sample_no, iva.validation_primer, "
                                  f"iti.task_item_id, it.interpreter, it.interpreter_name from interpretation_variant iv"
                                  f" inner join interpretation_task it on it.task_id = iv.task_id inner join "
                                  f"interpretation_variant_aggregation iva on iva.variant_id = iv.variant_id inner join"
                                  f" interpretation_task_item iti on iti.task_id = it.task_id and iti.sample_no = "
                                  f"it.sample_no where it.project_code = 'NBS' and it.task_source = 'Centre' "
                                  f"and it.status in ('Interpreting', 'ReadyForInterpret') "
                                  f"and iv.variant_type = '{types}'")
    task_id = result[0]['task_id']
    # 将任务的解读人设置为自动化测试账号
    mysql_connect.execute(f"update interpretation_task set interpreter = 562663278568931328,"
                          f"interpreter_name = '自动化测试_中心交付' where task_id = '{task_id}'")
    validate_json = {
        "taskId": task_id,
        "sampleNo": result[0]['sample_no'],
        "validationType": types if types != "SNV" else "Snv",
        "variationId": result[0]['variant_id'],
        "validationObj": result[0]['validation_primer'],
        "taskItemId": result[0]['task_item_id'],
        "validationSuggestion": "needValidate",
        "applyRemark": "自动化测试提交" + types + "验证"
    }
    # 清空validation表验证中、验证完成、验证取消的数据
    mysql_connect.execute(f"delete from interpretation_validation where task_id = '{task_id}' and "
                          f"validation_type = '{types}' and variant_id = '{result[0]['variant_id']}'")
    mysql_connect.execute(f"delete from validation_task where task_id = '{task_id}' and "
                          f"validation_type = '{types}' and validation_obj = '{result[0]['validation_primer']}'")
    yield validate_json
    # 执行完用例后，把数据恢复回原始的解读人/审核人
    mysql_connect.execute(f"update interpretation_task set interpreter = '{result[0]['interpreter']}',"
                          f"interpreter_name = '{result[0]['interpreter_name']}' where task_id = '{task_id}'")

