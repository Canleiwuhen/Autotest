# -*- coding: utf-8 -*-
class DataList:
    search_data = [
        {
            "case_name": "任务编号精准搜索",
            "search_items": {"batchNoFuzzy": "R250915000001"}
        },
        {
            "case_name": "任务编号模糊搜索",
            "search_items": {"batchNoFuzzy": "R2509"}
        },
        {
            "case_name": "样本编号搜索",
            "search_items": {"sampleIdFuzzy": "25B06200009"
                             }
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleIdFuzzy": "25B062"
                             }
        },
        {
            "case_name": "芯片号搜索",
            "search_items": {"slideNoFuzzy": "V350284050"
                             }
        },
        {
            "case_name": "芯片号模糊搜索",
            "search_items": {"slideNoFuzzy": "V350"
                             }
        },
        {
            "case_name": "产品套餐编号搜索",
            "search_items": {"productNo": "DX18331"
                             }
        },
        {
            "case_name": "肿瘤类型搜索",
            "search_items": {"tumorType": "100"
                             }
        },
        {
            "case_name": "原样本编号",
            "search_items": {"oldSampleNumFuzzy": "2323"
                             }
        }
    ]

    field_config = [
        {
            "page": "AnalysisList",
            "field_base_data": {'projectCode': '检测项目', 'anaTaskCode': '任务编号', 'flowCellId': '芯片ID', 'taskStatus': '分析状态',
                                'analysisProgress': '分析进度', 'dimension': '分析维度', 'sampleNum': '样本/样例数量',
                                'analysisStartDate': '分析开始时间', 'analysisEndDate': '分析结束时间', 'analysisRemark': '备注',
                                'pipelineName': '分析流程', 'failCause': '分析失败原因'},
            "field_project_data": {'projectCode': '检测项目', 'anaTaskCode': '任务编号', 'flowCellId': '芯片ID',
                                   'taskStatus': '分析状态', 'analysisProgress': '分析进度', 'dimension': '分析维度',
                                   'sampleNum': '样本/样例数量', 'analysisStartDate': '分析开始时间', 'analysisEndDate': '分析结束时间',
                                   'analysisRemark': '备注', 'pipelineName': '分析流程', 'failCause': '分析失败原因',
                                   'analysisError': '分析失败详情'}
        }
    ]
