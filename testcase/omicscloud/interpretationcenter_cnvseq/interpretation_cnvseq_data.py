class InterpretationData:
    search_data = [
        {
            "case_name": "样本编号-精确搜索",
            "search_item": {"sampleNo": "25X112000004"}
        },
        {
            "case_name": "样本编号-模糊搜索",
            "search_item": {"sampleNo": "25X1120000"}
        },
        {
            "case_name": "样本类型-全血",
            "search_item": {"sampleTypeCode": ["S051"]}
        },
        {
            "case_name": "解读状态-解析失败",
            "search_item": {"status": ["ReceiveError"]}
        },
        {
            "case_name": "质控-警告",
            "search_item": {"qcResult": ["Warn"]}
        },
        {
            "case_name": "医生意见-重上机",
            "search_item": {"doctorOpinion": ["ReSequence"]}
        },
        {
            "case_name": "姓名-精确搜索",
            "search_item": {"patientName": "黄海波"}
        },
        {
            "case_name": "姓名-模糊搜索",
            "search_item": {"patientName": "测试受检者"}
        },
        {
            "case_name": "性别-未知",
            "search_item": {"patientGender": ["Unknown"]}
        },
        {
            "case_name": "到样日期-2025/11/20",
            "search_item": {"receivedDate": {"startDate": "2025-11-20", "endDate": "2025-11-20"}}
        },
        {
            "case_name": "芯片ID-精确搜索",
            "search_item": {"chipCode": "V350115474"}
        },
        {
            "case_name": "芯片ID-模糊搜索",
            "search_item": {"chipCode": "V3501154"}
        },
        {
            "case_name": "样本标签-报告回退",
            "search_item": {"sampleTags": ["ReportFallback"]}
        },
        {
            "case_name": "查询待办任务",
            "search_item": {"isTodoList": "Y"}
        },
    ]

    other_exception_data = [
        {
            "case_name": "实验数据异常-性别不一致",
            "reason_items": {"exceptionType": "ExperimentAbnormal", "reportExpireReason": "genderDiff"}
        },
        {
            "case_name": "实验数据异常-检测结果不一致",
            "reason_items": {"exceptionType": "ExperimentAbnormal", "reportExpireReason": "clinicalDiff"}
        },
        {
            "case_name": "实验数据异常-其他",
            "reason_items": {"exceptionType": "ExperimentAbnormal", "reportExpireReason": "Other",
                             "reportExpireRemark": "testtest"}
        },
        {
            "case_name": "分析数据异常-家系样本断点不一致",
            "reason_items": {"exceptionType": "AnalysisAbnormal", "reportExpireReason": "familyBreakpointDiff"}
        },
        {
            "case_name": "分析数据异常-外院检测断点不一致",
            "reason_items": {"exceptionType": "AnalysisAbnormal", "reportExpireReason": "outerTestDiff"}
        },
        {
            "case_name": "分析数据异常-其他",
            "reason_items": {"exceptionType": "AnalysisAbnormal", "reportExpireReason": "Other",
                             "reportExpireRemark": "testtest"}
        },
        {
            "case_name": "样本信息异常-风险告知-母源污染",
            "reason_items": {"exceptionType": "SampleAbnormal", "reportExpireReason": "riskMaternalPollution"}
        },
        {
            "case_name": "样本信息异常-信息核对-补充历史检测结果",
            "reason_items": {"exceptionType": "SampleAbnormal", "reportExpireReason": "checkHistoryResult"}
        },
        {
            "case_name": "延期预警-临床信息待确认",
            "reason_items": {"exceptionType": "Delay", "reportExpireReason": "clinicalToBeConfirm"}
        }
    ]

    ploidy_mapping = {
        "diploid": "二倍体",
        "haploid-pollution": "单倍体/母源污染",
        "triploid-pollution": "三倍体/母源污染"
    }

