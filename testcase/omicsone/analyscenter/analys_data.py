class DataList:
    search_data = [
        {
            "case_name": "任务编号精准搜索",
            "search_items": {"taskCode": ["R250915000001"]}
        },
        {
            "case_name": "任务编号模糊搜索",
            "search_items": {"taskCode": ["R2509"]}
        },
        {
            "case_name": "任务编号批量搜索",
            "search_items": {"taskCode": ["R250915000001", "R250911000003"]
                             }
        },
        {
            "case_name": "样本编号搜索",
            "search_items": {"sampleNo": ["25B06200009"]
                             }
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleNo": ["25B062"]
                             }
        },
        {
            "case_name": "样本编号批量搜索",
            "search_items": {"sampleNo": ["25B06200009", "25B06200019"]
                             }
        },
        {
            "case_name": "芯片号搜索",
            "search_items": {"flowCellId": ["V350284050"]
                             }
        },
        {
            "case_name": "芯片号模糊搜索",
            "search_items": {"flowCellId": ["V350"]
                             }
        },
        {
            "case_name": "芯片号模糊搜索",
            "search_items": {"flowCellId": ["V350284050", "V352404121"]
                             }
        },
        {
            "case_name": "检测项目搜索",
            "search_items": {"projectCode": ["NIFTY", "NBS", "CS"]
                             }
        },
        {
            "case_name": "检测项目搜索",
            "search_items": {"projectCode": ["NIFTY", "NBS", "CS"]
                             }
        },
        {
            "case_name": "分析开始时间搜索",
            "search_items": {"analysisEndDate": "2025-09-01,2025-09-20"
                             }
        },
        {
            "case_name": "分析结束时间搜索",
            "search_items": {"analysisEndDate": "2025-09-01,2025-09-20"
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
