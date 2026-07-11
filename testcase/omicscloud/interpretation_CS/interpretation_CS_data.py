class InterpretationData:
    search_data = [
        {
            "case_name": "样本编号-精确搜索",
            "search_item": {"sampleNo": "25D2512171006"}
        },
        {
            "case_name": "样本编号-模糊搜索",
            "search_item": {"sampleNo": "25D2512"}
        },
        {
            "case_name": "样本类型-脐带血",
            "search_item": {"sampleTypeCode": ["S053"]}
        },
        {
            "case_name": "解读状态查询",
            "search_item": {"status": ["ReadyForInterpret", "Terminated"]}
        },
        {
            "case_name": "质控-不通过、警告",
            "search_item": {"qcResult": ["Warn", "Fail"]}
        },
        {
            "case_name": "医生意见-合格、无需解读",
            "search_item": {"doctorOpinion": ["NoNeed", "Pass"]}
        },
        {
            "case_name": "姓名-精确搜索",
            "search_item": {"patientName": "赵金凤"}
        },
        {
            "case_name": "姓名-模糊搜索",
            "search_item": {"patientName": "赵"}
        },
        {
            "case_name": "性别",
            "search_item": {"patientGender": ["Female"]}
        },
        {
            "case_name": "到样日期-2025/11/20",
            "search_item": {"receivedDate": {"startDate": "2025-11-20", "endDate": "2025-11-20"}}
        },
        {
            "case_name": "芯片ID",
            "search_item": {"chipCode": "V350331010"}
        }
    ]

    other_exception_data = [
        {
            "case_name": "实验数据异常",
            "reason_items": {"exceptionType": "ExperimentAbnormal"}
        },
        {
            "case_name": "分析数据异常",
            "reason_items": {"exceptionType": "AnalysisAbnormal"}
        },
        {
            "case_name": "样本信息异常",
            "reason_items": {"exceptionType": "SampleAbnormal"}
        },
        {
            "case_name": "延期预警",
            "reason_items": {"exceptionType": "Delay"}
        }
    ]

    detail_search_data = [
        {
            "case_name": "查看全量疾病",
            "search_item": {"showDiseaseList": "Y"}
        },
        {
            "case_name": "致病性查询",
            "search_item": {"pathogenicity": ["4", "3"]}
        },
        {
            "case_name": "杂合性查询",
            "search_item": {"zygosity": ["Heteroplasmy", "Hom"]}
        },
        {
            "case_name": "报告类别查询",
            "search_item": {"reportType": ["Formal", "AdditionalLargeDeletion", "AdditionalXCA"]}
        },
        {
            "case_name": "过滤PreRep查询",
            "search_item": {"preRepFlag": ["N"]}
        },
        {
            "case_name": "基因名单个查询",
            "search_item": {"geneSymbol": "ACADM"}
        },
        {
            "case_name": "基因名批量查询",
            "search_item": {"geneSymbol": ["ACADM", "HBA1"]}
        },
        {
            "case_name": "疾病名称单个查询",
            "search_item": {"diseaseName": "产前表型异常"}
        },
        {
            "case_name": "疾病名称批量查询",
            "search_item": {"diseaseName": ["产前表型异常", "囊性纤维化"]}
        },
        {
            "case_name": "疾病系统查询",
            "search_item": {"diseases": ["2", "5", "7"]}
        },
        {
            "case_name": "位点类型查询",
            "search_item": {"siteType": ["SevereMutation", "SnvVariant", "PathogenicSite"]}
        },
        {
            "case_name": "共分离查询",
            "search_item": {"cosegregation": ["CompositeZygosity", "XLinked"]}
        },
        {
            "case_name": "NO标签查询",
            "search_item": {"noTag": ["N"]}
        },
        {
            "case_name": "验证建议查询",
            "search_item": {"validationSuggest": ["Y"]}
        }
    ]
