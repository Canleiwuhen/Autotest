class DataList:
    search_data = [
        {
            "case_name": "样本编号精准搜索",
            "search_items": {"sampleNo": "25S06160003"}
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleNo": "111"}
        },
        {
            "case_name": "芯片ID模糊搜索",
            "search_items": {"chipCode": "V3502"}
        },
        {
            "case_name": "任务编号模糊搜索",
            "search_items": {"batchNoFuzzy": "R2509"}
        },
        {
            "case_name": "创建日期搜索",
            "search_items": {"createTime": "2025-06-01,2025-07-31"}
        },
        {
            "case_name": "组合搜索",
            "search_items": {"sampleNo": "11", "chipCode": "V35", "batchNoFuzzy": "R2508",
                             "createTime": "2025-06-01,2025-10-30"}
        }
    ]

    sequence_data = [
        {
            "case_name": "创建单芯片任务(无法流转至分析中心)",
            "option": "clear",
            "task_items": {
                "seqMachineId": "测试",
                "platform": "MGISEQ-2000",
                "platformId": 1000001004,
                "slideNo": "232323",
                "lane": [
                    {
                        "laneId": 1,
                        "dnbId": "1",
                        "samples": [
                            {
                                "id": 10419,
                                "sampleId": "25DPP225B12260216",
                                "sampleType": 2,
                                "barcode": "1",
                                "umiCode": "2",
                                "libraryType": 3,
                                "dnaQualityAssessment": "1",
                                "laneNo": "L01",
                                "dnbId": "1",
                                "hospitalName": None,
                                "patientName": "test2"
                            },
                            {
                                "id": 10418,
                                "sampleId": "25DPP225B12260185",
                                "sampleType": 2,
                                "barcode": "2",
                                "umiCode": "2",
                                "libraryType": 3,
                                "dnaQualityAssessment": "2",
                                "laneNo": "L01",
                                "dnbId": "1",
                                "hospitalName": None,
                                "patientName": "test2"
                            },
                            {
                                "id": 10417,
                                "sampleId": "25DPP225B12264469",
                                "sampleType": 2,
                                "barcode": "3",
                                "umiCode": "2",
                                "libraryType": 3,
                                "dnaQualityAssessment": "3",
                                "laneNo": "L01",
                                "dnbId": "1",
                                "hospitalName": None,
                                "patientName": "test2"
                            }
                        ]
                    }
                ],
                "preparationRunner": "",
                "sequenceRunner": "",
                "kitExtraction": "",
                "kitPreparation": "",
                "kitSequencing": "",
                "projectType": "0",
                "projectTypeName": "临床",
                "createUser": "13aa71751c4f4c559064519c4357dae8"
            }
        },
        {
            "case_name": "创建多芯片任务(无法流转至分析中心)",
            "option": "clear",
            "task_items": {
                "seqMachineId": "测试",
                "platform": "MGISEQ-2000",
                "platformId": 1000001004,
                "slideNo": "232324",
                "lane": [
                    {
                        "laneId": 1,
                        "dnbId": "1",
                        "samples": [
                            {
                                "id": 10419,
                                "sampleId": "25DPP225B12260216",
                                "sampleType": 2,
                                "barcode": "1",
                                "umiCode": "2",
                                "libraryType": 3,
                                "dnaQualityAssessment": "1",
                                "laneNo": "L01",
                                "dnbId": "1",
                                "hospitalName": None,
                                "patientName": "test2"
                            }
                        ]
                    }
                ],
                "preparationRunner": "",
                "sequenceRunner": "",
                "kitExtraction": "",
                "kitPreparation": "",
                "kitSequencing": "",
                "projectType": "0",
                "projectTypeName": "临床",
                "createUser": "13aa71751c4f4c559064519c4357dae8"
            }
        }
    ]

    delete_data = [
        {
            "case_name": "创建单芯片任务(无法流转至分析中心)",
            "option": "",
            "task_items": {
                "seqMachineId": "测试",
                "platform": "MGISEQ-2000",
                "platformId": 1000001004,
                "slideNo": "232325",
                "lane": [
                    {
                        "laneId": 1,
                        "dnbId": "1",
                        "samples": [
                            {
                                "id": 10419,
                                "sampleId": "25DPP225B12260216",
                                "sampleType": 2,
                                "barcode": "1",
                                "umiCode": "2",
                                "libraryType": 3,
                                "dnaQualityAssessment": "1",
                                "laneNo": "L01",
                                "dnbId": "1",
                                "hospitalName": None,
                                "patientName": "test2"
                            }
                        ]
                    }
                ],
                "preparationRunner": "",
                "sequenceRunner": "",
                "kitExtraction": "",
                "kitPreparation": "",
                "kitSequencing": "",
                "projectType": "0",
                "projectTypeName": "临床",
                "createUser": "13aa71751c4f4c559064519c4357dae8"
            }
        }
    ]

    # 导入确认接口的模板数据
    import_confirm_template = {
        "seqMachineId": "MGISEQ-2000",
        "platform": "MGISEQ-2000",
        "platformId": 1000001004,
        "slideNo": "232",
        "preparationRunner": "",
        "sequenceRunner": "",
        "mitochondrialProbe": "",
        "sequenceType": 0,
        "kitExtraction": "",
        "kitPreparation": "",
        "kitSequencing": "",
        "projectType": "0",
        "projectTypeName": "",
        "labMethod": 0
    }

    field_config = [
        {
            "page": "SequencingList",
            "field_base_data": {'createTime': '创建时间', 'chipCode': '芯片ID', 'seqTaskCode': '任务编号', 'sequencerId': '测序仪ID',
                                'sequencePlatform': '测序平台', 'sequenceProgress': '测序进度', 'sequenceStatus': '测序状态',
                                'uploadStatus': '测序数据上传状态', 'seqTaskStatus': '任务状态', 'causeError': '失败原因',
                                'exampleTotal': '样例数量'},
            "field_project_data": {'createTime': '创建时间', 'creator': '创建人', 'chipCode': '芯片ID',
                                   'sequenceStartTime': '测序开始时间', 'sequenceEndTime': '测序结束时间', 'seqTaskCode': '任务编号',
                                   'sequencerId': '测序仪ID', 'sequencePlatform': '测序平台', 'sequenceProgress': '测序进度',
                                   'sequenceStatus': '测序状态', 'uploadStatus': '测序数据上传状态', 'seqTaskStatus': '任务状态',
                                   'causeError': '失败原因', 'exampleTotal': '样例数量'}
        }, {
            "page": "Sequencing",
            "field_base_data": {'productNo': '产品套餐', 'sampleTypeCode': '样本类型', 'barcode': 'Barcode ID', 'poolingId': 'Pooling ID',
                                'sampleSetting': '样本设定', 'instanceNo': '样例编号', 'panelType': '技术路线', 'lane': 'Lane ID',
                                'dnbId': 'DNB ID', 'dnaConcentration': '提取产物浓度', 'libraryConcentration': '建库产物浓度',
                                'dnbConcentration': 'DNB浓度'},
            "field_project_data": {'productNo': '产品套餐', 'sampleTypeCode': '样本类型', 'barcode': 'Barcode ID',
                                   'sampleIndex': 'Index ID', 'umi': 'UMI', 'poolingId': 'Pooling ID', 'sampleSetting': '样本设定',
                                   'projectType': '项目类型', 'instanceNo': '样例编号', 'panelType': '技术路线', 'lane': 'Lane ID',
                                   'dnbId': 'DNB ID', 'dnaConcentration': '提取产物浓度', 'libraryConcentration': '建库产物浓度',
                                   'dnbConcentration': 'DNB浓度'}
        }
    ]
