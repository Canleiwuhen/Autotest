# -*- coding: utf-8 -*-
class DataList:
    search_data = [
        {
            "case_name": "样本编号精准搜索",
            "search_items": {"sampleIdFuzzy": "25B0115001"}
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items":  {"sampleIdFuzzy": "B"}
        },
        {
            "case_name": "病理号",
            "search_items": {"pathologyNum": "222"
                             }
        },
        {
            "case_name": "姓名模糊搜索",
            "search_items": {"pathologyNum": "222"
                             }
        }
    ]
    field_base_data = [{'sampleNo': '样本编号', 'productNo': '产品套餐', 'sampleTypeCode': '样本类型',
                        'hospitalSampleNo': '医院样本编号', 'hospitalId': '送检医院', 'departmentId': '送检科室', 'doctorId': '送检医生',
                        'patientName': '姓名', 'patientGender': '性别', 'patientAge': '年龄', 'patientBirthday': '出生日期',
                        'patientIdCard': '证件号', 'patientMobile': '联系电话', 'collectDate': '采样日期', 'receivedDate': '到样日期',
                        'createTime': '创建时间', 'projectCode': '检测项目'}]
    field_project_data = [{
        'OSEQ': {'patientNation': '民族', 'patientNativePlace': '籍贯', 'patientEmail': '电子邮箱', 'medicalRecordNo': '病历号',
                'barNumber': '条码号', 'healthInsuranceCard': '医保卡号', 'guardianName': '监护人姓名', 'birthWeight': '出生时体重(kg)',
                'birthtHeight': '出生时体长(cm)', 'apgarScore': 'Apgar评分', 'medicationHistory': '用药史',
                'clinicalSymptoms': '临床症状', 'otherClinicalInfo': '其他补充临床信息', 'focusGenes': '重点关注基因',
                'donateStatus': '是否同意捐献'}}]