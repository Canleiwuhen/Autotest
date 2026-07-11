import pytest

from testcase.omicscloud.interpretationcenter_cnvseq.interpretation_cnvseq_data import InterpretationData


def query_detect_data(res, mysql_connect, task_id, param):
    if param == "cnv":
        cnv_info = res.get_request(url=f"/api/interpretation/cnv-seq/largecnv/list?taskId={task_id}")
        variant_id = cnv_info.json()['result'][0]['largeCnvId']
        validation_obj = 'F8;NM001;EX1-EX2;Deletion;-;EX1-EX2'
        if cnv_info.json()['result'][0]['validationStatus'] != 'ToBeValidate':
            # 修改对应的cnv验证状态为待验证
            mysql_connect.execute(f"update interpretation_large_cnv set validation_status = 'ToBeValidate' "
                                  f"where large_cnv_id = '{variant_id}'")
            # 清空validation表验证中、验证完成、验证取消的数据
            mysql_connect.execute(f"delete from validation_task where task_id = '{task_id}' and "
                                  f"validation_type = 'LargeCnvGene' and validation_obj = '{validation_obj}'")
            mysql_connect.execute(f"delete from interpretation_validation where task_id = '{task_id}' and "
                                  f"validation_type = 'LargeCnvGene' and variant_id = '{variant_id}'")
        return {"validation_type": "基因验证", "variation_id": variant_id, "validation_obj": validation_obj,
                "svType": cnv_info.json()['result'][0]['svType'], "part_result": cnv_info.json()['result'][0]}
    elif param == "roh":
        roh_info = res.get_request(url=f"/api/interpretation/cnv-seq/roh/rohInfo?taskId={task_id}")
        for item in roh_info.json()['result']:
            # 取印记区域ROH
            if item['imprintFlag'] == 'Y':
                validation_obj = item['chrStartEnd'] + ',' + item['diseaseName'] + ',' + item['expressedAllele']
                # 如果ROH验证状态不是待验证，需要先改成待验证
                if item['validationStatus'] != 'ToBeValidate':
                    # 修改对应的roh验证状态为待验证
                    mysql_connect.execute(f"update interpretation_roh set validation_status = 'ToBeValidate',"
                                          f"validation_no = '',validation_result = '' where roh_id = '{item['rohId']}'")
                    # 清空validation表验证中、验证完成、验证取消的数据
                    mysql_connect.execute(f"delete from validation_task where task_id = '{task_id}' and "
                                          f"validation_type = 'ROH' and validation_obj = '{validation_obj}'")
                return {"validation_type": "ROH", "variation_id": item['rohId'], "validation_obj": validation_obj,
                        "part_result": item}
            else:
                continue
    elif param == "pathogen":
        pathogen_info = res.get_request(url=f"/api/interpretation/cnv-seq/pathogen/pathogenInfo?taskId={task_id}")
        for item in pathogen_info.json()['result']:
            if item['mappedReads'] > 0:
                validation_obj = item['pathogenNameZh'] + ',' + item['pathogenNameEn'] + ',' + str(item['mappedReads'])\
                                 + '/' + str(item['totalReads']) + ',' + str(item['fraction'])
                # 如果病原验证状态不是待验证，需要先改成待验证
                if item['validationStatus'] != 'ToBeValidate':
                    # 修改对应的pathogen验证状态为待验证
                    mysql_connect.execute(f"update interpretation_pathogen set validation_status = 'ToBeValidate',"
                                          f"validation_no = '',validation_result = '' "
                                          f"where pathogen_id = '{item['pathogenId']}'")
                    # 清空validation表验证中、验证完成、验证取消的数据
                    mysql_connect.execute(f"delete from validation_task where task_id = '{task_id}' and "
                                          f"validation_type = 'Pathogen' and validation_obj = '{validation_obj}'")
                return {"validation_type": "病原", "variation_id": item['pathogenId'], "validation_obj": validation_obj,
                        "part_result": item}
            else:
                continue
    else:
        ploidy_info = res.get_request(url=f"/api/interpretation/cnv-seq/ploidy/ploidyInfo?taskId={task_id}")
        ploidy_mapping = InterpretationData.ploidy_mapping
        validation_obj = ploidy_mapping[ploidy_info.json()['result']['mccTriploidSeqResult']]
        if ploidy_info.json()['result']['validationStatus'] != 'ToBeValidate':
            # 修改对应的ploidy验证状态为待验证
            mysql_connect.execute(f"update interpretation_ploidy set validation_status = 'ToBeValidate',"
                                  f"validation_no = '',maternal_pollution_result = '',aneuploidy_result =  '' "
                                  f"where ploidy_id = '{ploidy_info.json()['result']['ploidyId']}'")
            # 清空validation表验证中、验证完成、验证取消的数据
            mysql_connect.execute(f"delete from validation_task where task_id = '{task_id}' and "
                                  f"validation_type = 'Ploidy' and validation_obj = '{validation_obj}'")
        return {"validation_type": "异倍体/母源污染", "variation_id": ploidy_info.json()['result']['ploidyId'],
                "validation_obj": validation_obj, "part_result": ploidy_info.json()['result']}


@pytest.fixture(scope="function")
def search_test_data(res, mysql_connect, request):
    """
    查询测试数据
    :param res: 请求对象
    :param mysql_connect: 数据库连接对象
    :param request: 数据对象类型，如下:
        interpretation: 解读/待解读
        interpretation-RT: 解读/待解读
        review: 审核/待审核
        review-RT: 审核/待审核
        allocate: 待分配
        allocate-Positive: 待分配阳性
        allocate-Negative: 待分配阴性
        all: 所有解读任务
    :return:
    """
    param = request.param
    search_data = {
        "page": 1,
        "pageNum": 1,
        "limit": 200,
        "pageSize": 200
    }
    search_item = {}
    operator = []
    if param == "interpretation" or param == "interpretation-RT":
        # 查找解读人为当前用户的待解读、解读中的任务
        search_item = {
            "status": ["ReadyForInterpret", "Interpreting"]
        }
        operator = ["interpreter", "interpreterName", "interpreter_name"]
    elif param == "review" or param == "review-RT":
        # 查找审核人为当前用户的待审核、审核中的任务
        search_item = {
            "status": ["ReadyForReview", "Reviewing"]
        }
        operator = ["reviewer", "reviewerName", "reviewer_name"]
    elif param == "allocate-Positive":
        # 查找状态为待分配的阳性任务
        search_item = {
            "status": ["ReadyForAllocate"],
            "cnvDataTag": ["Positive"]
        }
    elif param == "allocate-Negative":
        # 查找状态为待分配的阴性任务
        search_item = {
            "status": ["ReadyForAllocate"],
            "cnvDataTag": ["Negative"]
        }
    elif param == "allocate":
        # 查找状态为待分配的任务
        search_item = {
            "status": ["ReadyForAllocate"]
        }
    search_data.update(search_item)
    response = res.post_request(url="/api/interpretation/cnv-seq/task/list", json=search_data)
    task_id = response.json()["result"]["records"][0]["taskId"]  # 取第一个任务的task_id返回即可
    cnv_data_tag = response.json()["result"]["records"][0]["cnvDataTag"]  # 阴/阳性样本标签
    is_interpreter = True if "interpreter" in response.json()["result"]["records"][0].keys() else False  # 是否存在解读人
    if param in ("interpretation", "interpretation-RT", "review", "review-RT"):
        # 获取原解读/审核人
        operator_id = response.json()["result"]["records"][0][operator[0]]  # 获取解读/审核人id
        operator_name = response.json()["result"]["records"][0][operator[1]]  # 获取解读/审核人姓名
        # 修改任务解读/审核人为自动化用户
        mysql_connect.execute(f"update interpretation_task set {operator[0]}=562663278568931328, "
                              f"{operator[2]}='自动化测试_中心交付' where task_id='{task_id}';")
        # 重置数据sql
        reset_sql = f"update interpretation_task set {operator[0]}='{operator_id}', {operator[2]}='{operator_name}' where task_id='{task_id}';"
    elif param in ("allocate-Positive", "allocate-Negative"):
        # 手动分配的任务重置数据sql
        reset_sql = (f"update interpretation_task set status='ReadyForAllocate', interpreter=null, interpreter_name=null, "
                      f"reviewer=null, reviewer_name=null where task_id='{task_id}';")
    elif param == "allocate":
        # 修改待分配的数据为解析失败，用于重解析
        update_sql = f"update interpretation_task set status='ReceiveError' where task_id = '{task_id}';"
        mysql_connect.execute(update_sql)
    yield task_id, cnv_data_tag, param, is_interpreter
    if param in ("interpretation", "interpretation-RT", "review", "review-RT", "allocate-Positive", "allocate-Negative"):
        # 如果是转发任务需要恢复数据
        mysql_connect.execute(reset_sql)


@pytest.fixture(scope="function")
def handle_task(res, mysql_connect, request):
    """
    将要做的操作及检出类型传进来以查找符合相关条件的数据并将外层接口需要的参数查出来一并返回
    1、event
    validate: 提交验证;
    reset: 重置解读;
    exception: 其他异常处理;
    get_sample: 获取样本信息;
    redraw: 重新生成核型图;
    scatter: 查看全局图;
    urgent: 加急;
    terminate: 解读终止;
    recomplete: 报告重新推送;
    update_result: 详情页面更新检出结果;

    2、param
    cnv: cnv检出;
    roh: 印记区域检出;
    pathogen: 病原检出;
    fail: 报告流转失败;
    """
    # 入参：解读状态，操作事件，额外查询条件
    status, event, param = request.param
    if status == "review":
        query_status = ["ReadyForReview", "Reviewing"]
        operator = ["reviewer", "reviewer_name"]
    elif status == "finish":
        query_status = ["Finished"]
        operator = ["interpreter", "interpreter_name"]
    else:
        query_status = ["ReadyForInterpret", "Interpreting"]
        operator = ["interpreter", "interpreter_name"]
    query_data = {
        "status": query_status,
        "page": 1,
        "pageNum": 1,
        "limit": 200,
        "pageSize": 200
    }
    search_item = {}
    if param == "cnv":
        # 查找cnv为阳性的任务
        search_item = {"cnvDataTag": ["Positive"]}
    elif param == "roh":
        # 查找印记区域有检出的任务
        search_item = {"roh": ["RI"]}
    elif param == "pathogen":
        # 查找病原为阳性的任务
        search_item = {"pathogen": ["Y"]}
    elif param == "push_fail":
        # 查找报告状态为流转失败的任务
        search_item = {"reportStatus": ["Fail"]}
    query_data.update(search_item)
    query = res.post_request("/api/interpretation/cnv-seq/task/list", json=query_data)
    task_id = query.json()['result']['records'][0]['taskId']
    sample_no = query.json()['result']['records'][0]['sampleNo']
    instance_no = query.json()['result']['records'][0]['instanceNo']
    operator_org = query.json()['result']['records'][0][operator[0]]
    operator_name_org = query.json()['result']['records'][0][operator[1].replace("_n", "N")]

    if event in ["validate", "update_result"]:
        # 将任务的解读人/审核人设置为自动化测试-中心交付账号
        mysql_connect.execute(f"update interpretation_task set {operator[0]} = 562663278568931328,"
                              f"{operator[1]} = '自动化测试_中心交付' where task_id = '{task_id}'")
        # 调用解读详情接口获取当前样本的三个id并返回
        detail = res.get_request(f"/api/interpretation/cnv-seq/task/detail/baseInfo?taskId={task_id}")
        sample_product_id = detail.json()["result"]["sampleInfo"]["sampleProductId"]
        sample_patient_id = detail.json()["result"]["sampleInfo"]["samplePatientId"]
        sample_inspection_id = detail.json()["result"]["sampleInfo"]["sampleInspectionId"]
        # 调用检出变异查询接口获取提交验证需要的传参并返回
        query_detect_result = query_detect_data(res, mysql_connect, task_id, param)
        validation_type = query_detect_result.get("validation_type", "")
        variation_id = query_detect_result.get("variation_id", "")
        validation_obj = query_detect_result.get("validation_obj", "")
        sv_type = query_detect_result.get("sv_type", "")
        part_result = query_detect_result.get("part_result", {})
        yield {"task_id": task_id, "instanceNo": instance_no, "sampleNo": sample_no, "variationId": variation_id,
               "validationType": validation_type, "validationObj": validation_obj, "sampleProductId": sample_product_id,
               "samplePatientId": sample_patient_id, "sampleInspectionId": sample_inspection_id, "svType": sv_type,
               "part_result": part_result,
               "update_url": f"{param}/{param}Update" if param != "cnv" else "largecnv/update"}
        # 执行完用例后，把数据恢复回原始的解读人/审核人
        mysql_connect.execute(f"update interpretation_task set {operator[0]} = '{operator_org}',"
                              f"{operator[1]} = '{operator_name_org}' where task_id = '{task_id}'")

    elif event in ["redraw", "scatter", "recomplete"]:
        yield {"task_id": task_id}

    else:
        variant_id = ''
        # 将任务的解读人/审核人设置为自动化测试账号
        mysql_connect.execute(f"update interpretation_task set {operator[0]} = 562663278568931328,"
                              f"{operator[1]} = '自动化测试_中心交付' where task_id = '{task_id}'")
        if event == "urgent":
            # 去除原本有的加急标签
            mysql_connect.execute(f"delete from interpretation_task_tag where tag_name = 'UrgentSample' and "
                                  f"task_id = '{task_id}'")
        if event == "reset":
            cnv_info = res.get_request(url=f"/api/interpretation/cnv-seq/largecnv/list?taskId={task_id}")
            variant_id = cnv_info.json()['result'][0]['largeCnvId']

        yield {"variationId": variant_id, "task_id": task_id}
        # 执行完用例后，把数据恢复回原始的解读人/审核人
        mysql_connect.execute(f"update interpretation_task set {operator[0]} = '{operator_org}',"
                              f"{operator[1]} = '{operator_name_org}' where task_id = '{task_id}'")
