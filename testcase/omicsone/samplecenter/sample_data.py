class DataList:
    search_data = [
        {
            "case_name": "样本编号精准搜索",
            "search_items": {"sampleNo": "25B0115001"}
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleNo": "25B0115"}
        },
        {
            "case_name": "样本编号批量搜索",
            "search_items": {"sampleNo": ["25B07286185", "25B07280998"]
                             }
        },
        {
            "case_name": "姓名搜索",
            "search_items": {"patientName": "AutoTest394001"
                             }
        },
        {
            "case_name": "姓名模糊搜索",
            "search_items": {"patientName": "AutoTest39"
                             }
        },
        {
            "case_name": "姓名批量搜索",
            "search_items": {"patientName": ["AutoTest394001", "AutoTest398136"]
                             }
        },
        {
            "case_name": "证件号搜索",
            "search_items": {"patientIdCard": "421127200207150063"
                             }
        },
        {
            "case_name": "证件号模糊搜索",
            "search_items": {"patientIdCard": "42112720020715006"
                             }
        },
        {
            "case_name": "证件号模糊搜索",
            "search_items": {"patientIdCard": ["421127200207150063", "421127200102010088"]
                             }
        },
        {
            "case_name": "产品套餐搜索",
            "search_items": {"productNo": "DX0006"
                             }
        },
        {
            "case_name": "样本类型搜索",
            "search_items": {"sampleTypeCode":"S370"
                             }
        },
        {
            "case_name": "医院编号搜索",
            "search_items": {"hospitalSampleNo":"23S04210012"
                             }
        },
        {
            "case_name": "送检医院搜索",
            "search_items": {"hospitalId":"528160617853489152"
                             }
        },
        {
            "case_name": "送检医院搜索",
            "search_items": {"hospitalId":"528160617853489152"
                             }
        },
        {
            "case_name": "送检科室搜索",
            "search_items": {"departmentId":"494538674420187136"
                             }
        },
        {
            "case_name": "送检医生搜索",
            "search_items": {"doctorId":"494538674462130176"
                             }
        },
        {
            "case_name": "姓名搜索",
            "search_items": {"patientGender": ["Female", "Male"]
                             }
        },
        {
            "case_name": "年龄搜索",
            "search_items": {"patientAge": "25"
                             }
        },
        {
            "case_name": "出生日期搜索",
            "search_items": {"patientBirthday": {"startDate": "2025-01-01", "endDate": "2026-01-01"}
                             }
        },
        {
            "case_name": "联系电话搜索",
            "search_items": {"patientMobile": "	1+-2312"
                              }
        },
        {
            "case_name": "采样日期搜索",
            "search_items": {"collectDate": {"startDate": "2025-01-01", "endDate": "2026-01-01"}
                             }
        },
        {
            "case_name": "到样日期搜索",
            "search_items": {"receivedDate": {"startDate": "2025-01-01", "endDate": "2026-01-01"}
                             }
        },
        {
            "case_name": "门诊号搜索",
            "search_items": {"outpatientNo": "123123123"
                             }
        },
        {
            "case_name": "住院号搜索",
            "search_items": {"inpatientNo": "123"
                             }
        },
        {
            "case_name": "备注搜索",
            "search_items": {"remark": "备注"
                             }
        },
        {
            "case_name": "先证者编号搜索",
            "search_items": {"probandSampleNo": "25B0108002"
                             }
        },
        {
            "case_name": "送检原因搜索",
            "search_items": {"reasonForInspection": "送检"
                             }
        },
        {
            "case_name": "创建人搜索",
            "search_items": {"creator": "autotest_omics1"
                             }
        },
        {
            "case_name": "送检项目搜索",
            "search_items": {"projectCode": ["CNV-seq", "NIFTY"]
                             }
        },
        {
            "case_name": "运输条件搜索",
            "search_items": {"shipmentCondition": ["1", "2"]
                             }
        },
        {
            "case_name": "胎儿类型搜索",
            "search_items": {"fetusType": ["Single", "Twins"]
                             }
        },
        {
            "case_name": "管道类型搜索",
            "search_items": {"tubeType": ["STRECK", "EDTA"]
                             }
        },
        {
            "case_name": "附加报告搜索",
            "search_items": {"additionalReportFlag": ["Yes"]
                             }
        },
        {
            "case_name": "家庭电话搜索",
            "search_items": {"patientTel": "123"
                             }
        },
        {
            "case_name": "电子邮箱搜索",
            "search_items": {"createTime": "123123123@qq.com"
                             }
        },
        {
            "case_name": "病历号搜索",
            "search_items": {"createTime": "123"
                             }
        },
        {
            "case_name": "条码号搜索",
            "search_items": {"barNumber": "123"
                             }
        },
        {
            "case_name": "医保卡号搜索",
            "search_items": {"healthInsuranceCard": "123"
                             }
        },
        {
            "case_name": "监护人搜索",
            "search_items": {"guardianName": "监护人"
                             }
        },
        {
            "case_name": "家庭编号搜索",
            "search_items": {"familyNumber": "F0001"
                             }
        },
        {
            "case_name": "报告模式搜索",
            "search_items": {"reportMode": ["DoubleReport"]
                             }
        },
        {
            "case_name": "配偶编号搜索",
            "search_items": {"spouseSampleNo": "25S06160001"
                             }
        },
        {
            "case_name": "配偶姓名搜索",
            "search_items": {"spouseName": "样本A"
                             }
        },
        {
            "case_name": "配偶证件号搜索",
            "search_items": {"spouseIdCard": "123123"
                             }
        },
        {
            "case_name": "IVF号搜索",
            "search_items": {"ivfNo": "IVF"
                             }
        },
        {
            "case_name": "试管编号搜索",
            "search_items": {"testTubeNo": "sg1231233123"
                             }
        }
    ]

    field_base_data = [{'sampleNo': '样本编号', 'productNo': '产品套餐', 'sampleTypeCode': '样本类型',
                        'hospitalSampleNo': '医院样本编号', 'hospitalId': '送检医院', 'departmentId': '送检科室',
                        'doctorId': '送检医生',
                        'patientName': '姓名', 'patientGender': '性别', 'patientAge': '年龄',
                        'patientBirthday': '出生日期',
                        'patientIdCard': '证件号', 'patientMobile': '联系电话', 'collectDate': '采样日期',
                        'receivedDate': '到样日期',
                        'createTime': '创建时间', 'projectCode': '检测项目'}]

    field_project_data = [{
        'CS': {'familyNumber': '家庭编号', 'reportMode': '报告模式', 'spouseSampleNo': '配偶样本编号',
               'spouseName': '配偶姓名',
               'spouseIdCard': '配偶证件号', 'pregnancyCondition': '妊娠情况', 'adversePregnancyHistory': '不良孕产史',
               'matingSituation': '近亲婚配情况', 'spouseClinical': '配偶临床信息（临床表型/遗传家族史/不良孕产史等）',
               'ivfNo': 'IVF号',
               'testTubeNo': '试管编号'},
        'NIFTY': {'shipmentCondition': '运输条件', 'fetusType': '胎儿类型', 'tubeType': '管道类型',
                  'additionalReportFlag': '附加报告',
                  'patientHeight': '身高(cm)', 'patientWeight': '体重(kg)', 'patientAddress': '联系地址',
                  'patientTel': '家庭电话',
                  'emergentName': '紧急联系人', 'emergentRelation': '关系', 'emergentTel': '联系人电话',
                  'childbirthExpectedDate': '预产期', 'chorion': '绒毛膜', 'downScreening': '唐筛结果',
                  'typeBultrasonic': 'B超检查结果', 'ivfFlag': '是否IVF', 'conceptionMethod': '受孕方式',
                  'bhGravidity': '分娩史孕次',
                  'bhParity': '分娩史产次', 'bhOther': '分娩史其他', 'amniocentesis': '羊水穿刺',
                  'illnessHistoryPast': '既往史',
                  'illnessHistoryPresent': '现病史', 'illnessHistoryAllergy': '过敏史'},
        'CNV-seq': {'sampleNo': '样本编号', 'productNo': '产品套餐', 'sampleTypeCode': '样本类型',
                    'hospitalSampleNo': '医院样本编号',
                    'hospitalId': '送检医院', 'departmentId': '送检科室', 'doctorId': '送检医生', 'patientName': '姓名',
                    'patientGender': '性别', 'patientAge': '年龄', 'patientBirthday': '出生日期',
                    'patientIdCard': '证件号',
                    'patientMobile': '联系电话', 'collectDate': '采样日期', 'receivedDate': '到样日期',
                    'outpatientNo': '门诊号',
                    'inpatientNo': '住院号', 'remark': '备注', 'enterPedigreeFlag': '是否录入家系',
                    'probandSampleNo': '先证者样本编号',
                    'knownFamilyRelation': '已知家系关系信息', 'reasonForInspection': '送检原因',
                    'patientType': '受检者类型',
                    'familyHistory': '家族遗传病史', 'gestationalAge': '孕周', 'donorEggFlag': '是否借卵',
                    'lastMenstruation': '末次月经', 'pregnancyDetectionFlag': '是否单胎双胎检测',
                    'ultrasonographyFlag': '是否做过超声检查',
                    'ultrasoundDate': '超声检测日期', 'abnormalUltrasonographyFlag': '超声检查是否异常',
                    'maleChromosomeDetection': '男方染色体检测', 'maleDetectionMethod': '男方检测方法',
                    'maleDetectionResult': '男方结果', 'femaleChromosomeDetection': '女方染色体检测',
                    'femaleDetectionMethod': '女方检测方法', 'femaleDetectionResult': '女方结果',
                    'childChromosomeDetection': '子女染色体检测', 'childDetectionMethod': '子女检测方法',
                    'childDetectionResult': '子女结果', 'maleMedicalHistory': '男方疾病既往史',
                    'femaleMedicalHistory': '女方疾病既往史',
                    'createTime': '创建时间', 'creator': '创建人', 'projectCode': '检测项目'},
        'NBS': {'patientNation': '民族', 'patientNativePlace': '籍贯', 'patientEmail': '电子邮箱',
                'medicalRecordNo': '病历号',
                'barNumber': '条码号', 'healthInsuranceCard': '医保卡号', 'guardianName': '监护人姓名',
                'birthWeight': '出生时体重(kg)',
                'birthtHeight': '出生时体长(cm)', 'apgarScore': 'Apgar评分', 'medicationHistory': '用药史',
                'clinicalSymptoms': '临床症状', 'otherClinicalInfo': '其他补充临床信息', 'focusGenes': '重点关注基因',
                'donateStatus': '是否同意捐献'}}]

    field_project_all_data = [{
        'CS': {'productNo': '产品套餐', 'hospitalSampleNo': '医院样本编号', 'hospitalId': '送检医院',
               'departmentId': '送检科室', 'doctorId': '送检医生', 'patientName': '姓名', 'patientGender': '性别',
               'patientAge': '年龄', 'patientBirthday': '出生日期', 'patientIdCard': '证件号',
               'patientMobile': '联系电话', 'collectDate': '采样日期', 'receivedDate': '到样日期',
               'outpatientNo': '门诊号', 'inpatientNo': '住院号', 'remark': '备注', 'sampleTypeCode': '样本类型',
               'projectCode': '检测项目', 'sampleNo': '样本编号', 'familyHistory': '家族遗传病史', 'creator': '创建人',
               'createTime': '创建时间', 'patientAddress': '联系地址', 'patientNation': '民族',
               'patientNativePlace': '籍贯', 'patientEmail': '电子邮箱', 'medicalRecordNo': '病历号',
               'barNumber': '条码号', 'healthInsuranceCard': '医保卡号', 'familyNumber': '家庭编号',
               'reportMode': '报告模式', 'spouseSampleNo': '配偶样本编号', 'spouseName': '配偶姓名',
               'spouseIdCard': '配偶证件号', 'gestationalAge': '孕周', 'pregnancyCondition': '妊娠情况',
               'clinicalSymptoms': '临床症状', 'adversePregnancyHistory': '不良孕产史',
               'matingSituation': '近亲婚配情况', 'otherClinicalInfo': '其他补充临床信息',
               'spouseClinical': '配偶临床信息（临床表型/遗传家族史/不良孕产史等）', 'focusGenes': '重点关注基因',
               'donateStatus': '是否同意捐献', 'ivfNo': 'IVF号', 'testTubeNo': '试管编号'},

        'NIFTY': {'sampleNo': '样本编号', 'productNo': '产品套餐', 'sampleTypeCode': '样本类型',
                  'hospitalSampleNo': '医院样本编号', 'hospitalId': '送检医院', 'departmentId': '送检科室',
                  'doctorId': '送检医生',
                  'patientName': '姓名', 'patientAge': '年龄',
                  'patientBirthday': '出生日期',
                  'patientIdCard': '证件号', 'patientMobile': '联系电话', 'collectDate': '采样日期',
                  'receivedDate': '到样日期',
                  'createTime': '创建时间', 'projectCode': '检测项目', 'creator': '创建人',
                  'shipmentCondition': '运输条件', 'fetusType': '胎儿类型', 'tubeType': '管道类型',
                  'additionalReportFlag': '附加报告',
                  'patientHeight': '身高(cm)', 'patientWeight': '体重(kg)', 'patientAddress': '联系地址',
                  'patientTel': '家庭电话',
                  'emergentName': '紧急联系人', 'emergentRelation': '关系', 'emergentTel': '联系人电话',
                  'childbirthExpectedDate': '预产期', 'chorion': '绒毛膜', 'downScreening': '唐筛结果',
                  'typeBultrasonic': 'B超检查结果', 'ivfFlag': '是否IVF', 'conceptionMethod': '受孕方式',
                  'bhGravidity': '分娩史孕次',
                  'bhParity': '分娩史产次', 'bhOther': '分娩史其他', 'amniocentesis': '羊水穿刺',
                  'illnessHistoryPast': '既往史',
                  'illnessHistoryPresent': '现病史', 'illnessHistoryAllergy': '过敏史'},

        'CNV-seq': {'sampleNo': '样本编号','productNo': '产品套餐', 'sampleTypeCode': '样本类型',
                    'hospitalSampleNo': '医院样本编号',
                    'hospitalId': '送检医院', 'departmentId': '送检科室', 'doctorId': '送检医生', 'patientName': '姓名',
                    'patientGender': '性别', 'patientAge': '年龄', 'patientBirthday': '出生日期',
                    'patientIdCard': '证件号',
                    'patientMobile': '联系电话', 'collectDate': '采样日期', 'receivedDate': '到样日期',
                    'outpatientNo': '门诊号',
                    'inpatientNo': '住院号', 'remark': '备注', 'enterPedigreeFlag': '是否录入家系',
                    'probandSampleNo': '先证者样本编号',
                    'knownFamilyRelation': '已知家系关系信息', 'reasonForInspection': '送检原因',
                    'patientType': '受检者类型',
                    'familyHistory': '家族遗传病史', 'gestationalAge': '孕周', 'donorEggFlag': '是否借卵',
                    'lastMenstruation': '末次月经', 'pregnancyDetectionFlag': '是否单胎双胎检测',
                    'ultrasonographyFlag': '是否做过超声检查',
                    'ultrasoundDate': '超声检测日期', 'abnormalUltrasonographyFlag': '超声检查是否异常',
                    'maleChromosomeDetection': '男方染色体检测', 'maleDetectionMethod': '男方检测方法',
                    'maleDetectionResult': '男方结果', 'femaleChromosomeDetection': '女方染色体检测',
                    'femaleDetectionMethod': '女方检测方法', 'femaleDetectionResult': '女方结果',
                    'childChromosomeDetection': '子女染色体检测', 'childDetectionMethod': '子女检测方法',
                    'childDetectionResult': '子女结果', 'maleMedicalHistory': '男方疾病既往史',
                    'femaleMedicalHistory': '女方疾病既往史',
                    'createTime': '创建时间', 'creator': '创建人', 'projectCode': '检测项目'},

        'NBS': {'productNo': '产品套餐', 'hospitalSampleNo': '医院样本编号', 'hospitalId': '送检医院',
                'departmentId': '送检科室', 'doctorId': '送检医生', 'patientName': '姓名', 'patientGender': '性别',
                'patientAge': '年龄', 'patientBirthday': '出生日期', 'patientIdCard': '证件号',
                'patientMobile': '联系电话', 'collectDate': '采样日期', 'receivedDate': '到样日期',
                'outpatientNo': '门诊号', 'inpatientNo': '住院号', 'remark': '备注', 'sampleTypeCode': '样本类型',
                'projectCode': '检测项目', 'sampleNo': '样本编号', 'familyHistory': '家族遗传病史', 'creator': '创建人',
                'createTime': '创建时间', 'patientAddress': '联系地址', 'patientNation': '民族',
                'patientNativePlace': '籍贯', 'patientEmail': '电子邮箱', 'medicalRecordNo': '病历号',
                'barNumber': '条码号', 'healthInsuranceCard': '医保卡号', 'guardianName': '监护人姓名',
                'birthWeight': '出生时体重(kg)', 'birthtHeight': '出生时体长(cm)', 'apgarScore': 'Apgar评分',
                'medicationHistory': '用药史', 'clinicalSymptoms': '临床症状', 'otherClinicalInfo': '其他补充临床信息',
                'focusGenes': '重点关注基因', 'donateStatus': '是否同意捐献'}}]



