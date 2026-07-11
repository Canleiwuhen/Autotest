class DataList:
    search_data = [
        {
            "case_name": "样本编号精准搜索",
            "search_items": {"sampleNo": "25B0115001"}
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleNo": "11"}
        },
        {
            "case_name": "样本编号批量搜索",
            "search_items": {"sampleNo": ["25B0115004", "25B0115008"]}
        },
        {
            "case_name": "产品套餐搜索",
            "search_items": {"productNo": ["DX0006"]}
        },
        {
            "case_name": "样本类型搜索",
            "search_items": {"sampleTypeCode": ["S094", "S402", "S370"]}
        },
        {
            "case_name": "医院样本编号精准搜索",
            "search_items": {"hospitalSampleNo": "25B0115001"}
        },
        {
            "case_name": "医院样本编号模糊搜索",
            "search_items": {"hospitalSampleNo": "11"}
        },
        {
            "case_name": "医院样本编号批量搜索",
            "search_items": {"hospitalSampleNo": ["25B0115004", "25B0115008"]}
        },
        {
            "case_name": "送检医院搜索",
            "search_items": {"hospitalId": ["528160617853489152", "545190430782918656"]}
        },
        {
            "case_name": "姓名精准搜索",
            "search_items": {"patientName": "AutoTest455719"}
        },
        {
            "case_name": "姓名模糊搜索",
            "search_items": {"patientName": "AutoTest"}
        },
        {
            "case_name": "姓名批量搜索",
            "search_items": {"patientName": ["AutoTest455719", "测试1"]}
        },
        {
            "case_name": "性别搜索",
            "search_items": {"patientGender": ["Female", "Unknown"]}
        },
        {
            "case_name": "采样日期搜索",
            "search_items": {"collectDate": {"startDate": "2024-12-03", "endDate": "2025-01-15"}}
        },
        {
            "case_name": "到样日期搜索",
            "search_items": {"receivedDate": {"startDate": "2024-11-24", "endDate": "2025-01-15"}}
        },
        {
            "case_name": "备注搜索",
            "search_items": {"remark": "1111"}
        },
        {
            "case_name": "解读状态搜索",
            "search_items": {"status": ["ReadyForInterpret", "Interpreting"]}
        },
        {
            "case_name": "服务状态搜索",
            "search_items": {"manualServiceStatus": ["InService", "ServiceCompleted"]}
        },
        {
            "case_name": "质控搜索",
            "search_items": {"qcResult": ["Pass", "Warn"]}
        },
        {
            "case_name": "操作建议搜索",
            "search_items": {"qcAdvice": ["ReSequence", "ReBuild"]}
        },
        {
            "case_name": "医生意见搜索",
            "search_items": {"doctorOpinion": ["ReSequence", "Refund"]}
        },
        {
            "case_name": "NGS-异倍体/母源污染搜索",
            "search_items": {"mccTriploidSeqResult": ["haploid-pollution", "triploid-pollution"]}
        },
        {
            "case_name": "异倍体-验证搜索",
            "search_items": {"aneuploidyResult": ["XNN", "Haploid", "Fail", "XY"]}
        },
        {
            "case_name": "母源污染-验证搜索",
            "search_items": {"maternalPollutionResult": ["NoPollution", "Ge30", "Fail"]}
        },
        {
            "case_name": "LOH搜索",
            "search_items": {"roh": ["R", "N"]}
        },
        {
            "case_name": "LOH-验证搜索",
            "search_items": {"rohValidationResult": ["Positive", "Fail"]}
        },
        {
            "case_name": "病原搜索",
            "search_items": {"pathogen": ["Y"]}
        },
        {
            "case_name": "病原-验证搜索",
            "search_items": {"pathogenValidationResult": ["Fail", "Negative"]}
        },
        {
            "case_name": "芯片ID搜索",
            "search_items": {"chipCode": "V350298394"}
        },
        {
            "case_name": "解读人搜索",
            "search_items": {"interpreterName": "黄雁"}
        },
        {
            "case_name": "项目类型搜索",
            "search_items": {"projectType": ["1", "2"]}
        },
        {
            "case_name": "样例编号搜索",
            "search_items": {"instanceNo": "25X01200002-1"}
        },
        {
            "case_name": "测序开始时间搜索",
            "search_items": {"sequenceStartTime": {"startDate": "2025-12-09", "endDate": "2025-12-10"}}
        },
        {
            "case_name": "测序结束时间搜索",
            "search_items": {"sequenceEndTime": {"startDate": "2025-12-09", "endDate": "2025-12-10"}}
        },
        {
            "case_name": "分析批次搜索",
            "search_items": {"analysisTaskCode": "R25112800"}
        },
        {
            "case_name": "分析开始时间搜索",
            "search_items": {"analysisStartTime": {"startDate": "2024-11-26", "endDate": "2025-01-09"}}
        },
        {
            "case_name": "分析结束时间搜索",
            "search_items": {"analysisFinishTime": {"startDate": "2024-11-26", "endDate": "2025-01-09"}}
        },
        {
            "case_name": "解析开始时间搜索",
            "search_items": {"receiveStartTime": {"startDate": "2024-11-26", "endDate": "2025-01-09"}}
        },
        {
            "case_name": "解析完成时间搜索",
            "search_items": {"receiveFinishTime": {"startDate": "2024-11-26", "endDate": "2025-01-09"}}
        },
        {
            "case_name": "解读开始时间搜索",
            "search_items": {"interpretStartTime": {"startDate": "2024-12-04", "endDate": "2025-10-07"}}
        },
        {
            "case_name": "解读完成时间搜索",
            "search_items": {"interpretTime": {"startDate": "2024-12-04", "endDate": "2025-10-07"}}
        },
        {
            "case_name": "服务提交时间搜索",
            "search_items": {"manualServiceSubmitTime": {"startDate": "2024-12-04", "endDate": "2025-10-07"}}
        },
        {
            "case_name": "服务结束时间搜索",
            "search_items": {"manualServiceFinishTime": {"startDate": "2024-12-04", "endDate": "2025-10-07"}}
        },
        {
            "case_name": "审核开始时间搜索",
            "search_items": {"reviewStartTime": {"startDate": "2024-12-04", "endDate": "2025-10-07"}}
        },
        {
            "case_name": "审核完成时间搜索",
            "search_items": {"reviewTime": {"startDate": "2024-12-04", "endDate": "2025-10-07"}}
        },
        {
            "case_name": "审核人搜索",
            "search_items": {"reviewerName": "黄雁"}
        },
        {
            "case_name": "报告到期日期搜索",
            "search_items": {"reportExpireTime": {"startDate": "2024-12-02", "endDate": "2025-11-04"}}
        },
        {
            "case_name": "样本标签搜索",
            "search_items": {"sampleTags": ["ReviewFallback", "AnalysisAbnormal", "UrgentSample"]}
        },
        {
            "case_name": "CNV数据标签搜索",
            "search_items": {"cnvDataTag": ["Negative"]}
        },
        {
            "case_name": "CNV-是否报告搜索",
            "search_items": {"cnvReportFlag": ["Y"]}
        },
        {
            "case_name": "组合搜索",
            "search_items": {"mccTriploidSeqResult": ["diploid"], "productNo": ["DX0007"], "sampleTypeCode": ["L001", "S100"],
                             "qcResult": ["Pass"], "roh": ["R"], "interpreterName": "黄雁", "projectType": ["0"],
                             "analysisStartTime": {"startDate": "2024-12-02", "endDate": "2025-11-04"},
                             "interpretStartTime": {"startDate": "2024-12-02", "endDate": "2025-11-12"},
                             "cnvReportFlag": ["Y"]}
        }
    ]
