import pytest

from testcase.omicsone.conftest import mysql_connect


@pytest.fixture(scope="function")
def handle_task(res):
    query_data = {
        "status": ["ReadyForInterpret"],
        "manualServiceStatus": ["IsNull"],
        "page": 1,
        "pageNum": 1,
        "limit": 200,
        "pageSize": 200
    }
    query = res.post_request("/api/interpretation/cnv-seq/task/list", json=query_data)
    task_id = query.json()['result']['records'][0]['taskId']
    instance_no = query.json()['result']['records'][0]['instanceNo']
    interpreter = mysql_connect().select(f"select it.interpreter,it.interpreter_name from "
                                         f"interpretation_task it where it.task_id = '{task_id}'")
    if interpreter:
        # 把解读人置空，避免被权限校验住
        mysql_connect().execute(f"update interpretation_task set interpreter = null,interpreter_name = null "
                                f"where task_id = '{task_id}'")
        yield {"task_id": task_id, "instance_no": instance_no}
        # 执行完用例后，把数据恢复
        interpreter_org = interpreter[0]['interpreter'] if interpreter[0]['interpreter'] else ''
        interpreter_name_org = interpreter[0]['interpreter_name'] if interpreter[0]['interpreter_name'] else ''
        mysql_connect().execute(f"update interpretation_task set interpreter = '{interpreter_org}',"
                                f"interpreter_name = '{interpreter_name_org}',status = 'ReadyForInterpret',"
                                f"doctor_opinion = 'Pass' where task_id = '{task_id}'")
        mysql_connect().close_database()
    else:
        yield {"task_id": task_id, "instance_no": instance_no}
        mysql_connect().execute(f"update interpretation_task set interpreter = '',interpreter_name = '',"
                                f"status = 'ReadyForInterpret',doctor_opinion = 'Pass' "
                                f"where task_id = '{task_id}'")
        mysql_connect().close_database()
