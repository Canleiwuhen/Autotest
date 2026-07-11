class InterpretationData:
    search_data = [
        {
            "case_name": "样本编号-精确搜索",
            "search_item": {"sampleNo": "23B11221404"}
        },
        {
            "case_name": "样本编号-模糊搜索",
            "search_item": {"sampleNo": "23B"}
        },
        {
            "case_name": "样本类型-全血",
            "search_item": {"sampleTypeCode": ["S051"]}
        },
        {
            "case_name": "解读状态查询",
            "search_item": {"status": ["ReceiveError", "ReadyForInterpret", "Interpreting"]}
        },
        {
            "case_name": "质控-通过",
            "search_item": {"qcResult": ["Pass"]}
        },
        {
            "case_name": "医生意见-重上机",
            "search_item": {"doctorOpinion": ["ReSequence"]}
        },
        {
            "case_name": "姓名-精确搜索",
            "search_item": {"patientName": "test9"}
        },
        {
            "case_name": "姓名-模糊搜索",
            "search_item": {"patientName": "test"}
        },
        {
            "case_name": "到样日期-2025/11/20",
            "search_item": {"receivedDate": {"startDate": "2025-11-20", "endDate": "2025-11-20"}}
        },
        {
            "case_name": "分析批次-精确搜索",
            "search_item": {"analysisTaskCode": "R251017000003"}
        },
        {
            "case_name": "分析批次-模糊搜索",
            "search_item": {"analysisTaskCode": "R251017"}
        }
    ]
