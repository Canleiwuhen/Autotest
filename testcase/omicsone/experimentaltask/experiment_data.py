import random

pre_plate_code = "P" + str(random.randint(10**12, 10**13 - 1))
lib_plate_code = "L" + str(random.randint(10**12, 10**13 - 1))
hybrid_plate_code = "H" + str(random.randint(10**12, 10**13 - 1))


class DataList:
    search_data = [
        {
            "case_name": "样本编号精准搜索",
            "search_items": {"sampleNo": ["25S06160003"]}
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleNo": ["111"]}
        },
        {
            "case_name": "样本编号批量搜索",
            "search_items": {"sampleNo": ["25S06160002", "25S06160003"]}
        },
        {
            "case_name": "Pooling ID模糊搜索",
            "search_items": {"poolingId": "P"}
        },
        {
            "case_name": "板号模糊搜索",
            "search_items": {"plateCode": "L2025"}
        },
        {
            "case_name": "检测项目批量搜索",
            "search_items": {"projectCode": ["CNV-seq", "CS"]}
        },
        {
            "case_name": "实验状态批量搜索",
            "search_items": {"experimentalState": ["InDelivery", "ExperimentCompletion"]}
        },
        {
            "case_name": "实验创建时间搜索",
            "search_items": {"createTime": "2025-07-29,2025-09-02"}
        },
        {
            "case_name": "组合搜索",
            "search_items": {"experimentalState": ["ExperimentCompletion", "InExperiment"],
                             "createTime": "2025-05-01,2025-09-16",
                             "plateCode": "S",
                             "poolingId": "SEQ",
                             "projectCode": ["CS", "NIFTY"],
                             "sampleNo": ["25"]}
        }
    ]

    experiment_data = [
        {
            "case_name": "创建携筛-全流程-预处理产物实验任务",
            "option": "clear",
            "task_items": {
                "schemeId": "532574949186080781",
                "instrumentId": "SIRO16_202409110001",
                "instrumentType": "SIRO-48",
                "automationScheme": "携筛001",
                "experimentalProcedure": "Full-process",
                "productClass": "PreprocessedProduct",
                "projectCode": "CS",
                "routingName": "CS",
                "sequencePlatform": "MGISEQ-2000",
                "chipType": "FCL",
                "status": 1,
                "createUser": "427868391118864384",
                "updateUser": "427868391118864384",
                "plateCodeList": pre_plate_code,
                "sampleList": [{
                    "barcode": 1, "hybridProductConcentration": "", "libProductConcentration": "", "sampleIndex": "",
                    "umi": "", "samplePatientId": "526782660492787713", "sampleInspectionId": "526782660492787712",
                    "sampleProductId": "526782660492787714", "sampleNo": "25B09010352",
                    "sampleTypeCode": "L001", "probandSampleNo": "", "hospitalSampleNo": "", "collectDate": "2025-05-01",
                    "receivedDate": "2025-05-02", "patientName": "test2352", "patientGender": "Female",
                    "patientAge": "", "patientBirthday": "", "patientWeight": "", "patientHeight": "",
                    "patientAddress": "", "patientIdCard": "", "patientMobile": "", "patientEmail": "",
                    "outpatientNo": "", "inpatientNo": "", "extInfo": "{}", "enterPedigreeFlag": "",
                    "knownFamilyRelation": "", "creator": "陈清荣", "createTime": "2025-09-01 15:26:13",
                    "updateUser": "", "updateTime": "", "hospitalId": "451794825952493568", "hospitalName": "罗湖中医院",
                    "doctorId": "", "doctorName": "", "departmentId": "", "departmentName": "", "remark": "",
                    "projectCode": "CS", "productClass": "0", "productNo": "DX2002", "sampleClinicalId": "",
                    "clinicalInfo": "{\"ivfNo\": \"\", \"bhOther\": \"\", \"chorion\": \"\", \"ivfFlag\": \"\", \"bhParity\": \"\", \"apgarScore\": \"\", \"focusGenes\": \"\", \"reportMode\": \"SingleReport\", \"spouseName\": \"\", \"testTubeNo\": \"\", \"bhGravidity\": \"\", \"birthWeight\": \"\", \"patientType\": \"\", \"birthtHeight\": \"\", \"donateStatus\": \"\", \"donorEggFlag\": \"\", \"guardianName\": \"\", \"spouseIdCard\": \"\", \"amniocentesis\": \"\", \"downScreening\": \"\", \"familyHistory\": \"无\", \"gestationalAge\": \"\", \"spouseClinical\": \"\", \"ultrasoundDate\": \"\", \"matingSituation\": \"\", \"typeBultrasonic\": \"\", \"clinicalSymptoms\": \"无\", \"conceptionMethod\": \"\", \"lastMenstruation\": \"\", \"medicationHistory\": \"\", \"otherClinicalInfo\": \"\", \"illnessHistoryPast\": \"\", \"maleMedicalHistory\": \"\", \"pregnancyCondition\": \"\", \"healthInsuranceCard\": \"\", \"maleDetectionMethod\": \"\", \"maleDetectionResult\": \"\", \"reasonForInspection\": \"\", \"ultrasonographyFlag\": \"\", \"childDetectionMethod\": \"\", \"childDetectionResult\": \"\", \"femaleMedicalHistory\": \"\", \"femaleDetectionMethod\": \"\", \"femaleDetectionResult\": \"\", \"illnessHistoryAllergy\": \"\", \"illnessHistoryPresent\": \"\", \"childbirthExpectedDate\": \"\", \"pregnancyDetectionFlag\": \"\", \"adversePregnancyHistory\": \"无\", \"maleChromosomeDetection\": \"\", \"childChromosomeDetection\": \"\", \"femaleChromosomeDetection\": \"\", \"abnormalUltrasonographyFlag\": \"\"}",
                    "experimentFlag": "", "formId": "", "flowId": "3261100", "status": "Sample", "operationCode": "",
                    "patientCountry": "", "patientNation": "", "patientNativePlace": "", "medicalRecordNo": "",
                    "barNumber": "", "familyNumber": "", "spouseSampleNo": "", "__index__": 95, "selectable": "false",
                    "sampleSetting": "Clinical", "sampleId": "526782660492787713", "inspectionType": "Sample",
                    "retestFlag": "No", "holeId": "A1", "pointCode": "A1", "plateCode": pre_plate_code}]
            }
        },
        {
            "case_name": "创建新筛-前处理建库-原始样本实验任务",
            "option": "clear",
            "task_items": {
                "schemeId": "532610305646268426",
                "instrumentId": "SIRO16_202409110001",
                "instrumentType": "SIRO-48",
                "automationScheme": "新筛006",
                "experimentalProcedure": "Pretreatment-LibraryPrep",
                "productClass": "RawSample",
                "projectCode": "NBS",
                "routingName": "NBS",
                "sequencePlatform": "MGISEQ-2000",
                "chipType": "FCL",
                "status": 1,
                "createUser": "427868391118864384",
                "updateUser": "427868391118864384",
                "plateCodeList": pre_plate_code,
                "sampleList": [{
                    "barcode": "", "hybridProductConcentration": "", "libProductConcentration": "", "sampleIndex": "",
                    "umi": "", "samplePatientId": "492734592600637449", "sampleInspectionId": "492734592600637448",
                    "sampleProductId": "492734592600637450", "sampleNo": "25B0530602", "sampleTypeCode": "L001",
                    "probandSampleNo": "", "hospitalSampleNo": "", "collectDate": "2025-05-01", "receivedDate": "2025-05-02",
                    "patientName": "test32", "patientGender": "Female", "patientAge": "",  "patientBirthday": "2025-03-20",
                    "patientWeight": "", "patientHeight": "", "patientAddress": "", "patientIdCard": "",
                    "patientMobile": "", "patientEmail": "", "outpatientNo": "", "inpatientNo": "", "extInfo": "{}",
                    "enterPedigreeFlag": "", "knownFamilyRelation": "", "creator": "陈清荣", "createTime": "2025-05-30 16:31:21",
                    "updateUser": "", "updateTime": "", "hospitalId": "451794825952493568", "hospitalName": "罗湖中医院",
                    "doctorId": "", "doctorName": "", "departmentId": "", "departmentName": "", "remark": "",
                    "projectCode": "NBS", "productClass": "0", "productNo": "DX1968", "sampleClinicalId": "",
                    "clinicalInfo": "{\"ivfNo\": \"\", \"bhOther\": \"\", \"chorion\": \"\", \"ivfFlag\": \"\", \"bhParity\": \"\", \"apgarScore\": \"\", \"focusGenes\": \"\", \"reportMode\": \"\", \"spouseName\": \"\", \"testTubeNo\": \"\", \"bhGravidity\": \"\", \"birthWeight\": \"\", \"patientType\": \"\", \"birthtHeight\": \"\", \"donateStatus\": \"\", \"donorEggFlag\": \"\", \"guardianName\": \"ftest\", \"spouseIdCard\": \"\", \"amniocentesis\": \"\", \"downScreening\": \"\", \"familyHistory\": \"无\", \"gestationalAge\": \"\", \"spouseClinical\": \"\", \"ultrasoundDate\": \"\", \"matingSituation\": \"\", \"typeBultrasonic\": \"\", \"clinicalSymptoms\": \"无\", \"conceptionMethod\": \"\", \"lastMenstruation\": \"\", \"medicationHistory\": \"\", \"otherClinicalInfo\": \"\", \"illnessHistoryPast\": \"\", \"maleMedicalHistory\": \"\", \"pregnancyCondition\": \"\", \"healthInsuranceCard\": \"\", \"maleDetectionMethod\": \"\", \"maleDetectionResult\": \"\", \"reasonForInspection\": \"\", \"ultrasonographyFlag\": \"\", \"childDetectionMethod\": \"\", \"childDetectionResult\": \"\", \"femaleMedicalHistory\": \"\", \"femaleDetectionMethod\": \"\", \"femaleDetectionResult\": \"\", \"illnessHistoryAllergy\": \"\", \"illnessHistoryPresent\": \"\", \"childbirthExpectedDate\": \"\", \"pregnancyDetectionFlag\": \"\", \"adversePregnancyHistory\": \"\", \"maleChromosomeDetection\": \"\", \"childChromosomeDetection\": \"\", \"femaleChromosomeDetection\": \"\", \"abnormalUltrasonographyFlag\": \"\"}",
                    "experimentFlag": "", "formId": "", "flowId": "2190929", "status": "Experiment", "operationCode": "",
                    "patientCountry": "", "patientNation": "", "patientNativePlace": "", "medicalRecordNo": "",
                    "barNumber": "", "familyNumber": "", "spouseSampleNo": "", "__index__": 0, "selectable": "false",
                    "sampleSetting": "Clinical", "sampleId": "492734592600637449", "inspectionType": "Sample",
                    "retestFlag": "No", "plateCode": pre_plate_code}]
            }
        },
        {
            "case_name": "创建新筛-杂交洗脱-预处理产物实验任务",
            "option": "clear",
            "task_items": {
                "schemeId": "532612174410027015",
                "instrumentId": "SIRO16_202409110001",
                "instrumentType": "SIRO-48",
                "automationScheme": "新筛003",
                "experimentalProcedure": "Hybridization",
                "productClass": "PreprocessedProduct",
                "projectCode": "NBS",
                "routingName": "NBS",
                "sequencePlatform": "MGISEQ-2000",
                "chipType": "FCL",
                "status": 1,
                "createUser": "427868391118864384",
                "updateUser": "427868391118864384",
                "sampleList": [{
                    "barcode": "1", "hybridProductConcentration": "", "libProductConcentration": "0", "sampleIndex": "1",
                    "umi": "1", "plateCode": lib_plate_code, "sampleNo": "25B06040185", "sampleId": "494531613363929095",
                    "inspectionType": "Sample", "sampleProductId": "494531613363929096", "productNo": "DX2427",
                    "sampleTypeCode": "S050", "sampleSetting": "Clinical", "projectCode": "NBS", "pointCode": "A01",
                    "libPointCode": "A01", "libPlateCode": lib_plate_code
                }, {"barcode": "1",
                    "hybridProductConcentration": "", "libProductConcentration": "0", "sampleIndex": "1", "umi": "1",
                    "plateCode": lib_plate_code, "sampleNo": "25B06040185", "sampleId": "494531613363929095",
                    "inspectionType": "Sample", "sampleProductId": "494531613363929096", "productNo": "DX2427",
                    "sampleTypeCode": "S050", "sampleSetting": "Clinical", "projectCode": "NBS", "pointCode": "A02",
                    "libPointCode": "A02", "libPlateCode": lib_plate_code}]
            }
        },
        {
            "case_name": "创建携筛-上机前准备-原始样本实验任务",
            "option": "clear",
            "task_items": {
                "schemeId": "532617542083153940",
                "instrumentId": "SIRO16_202409110001",
                "instrumentType": "SIRO-48",
                "automationScheme": "携筛008",
                "experimentalProcedure": "SequencingPrep",
                "productClass": "RawSample",
                "projectCode": "CS",
                "routingName": "CS",
                "sequencePlatform": "MGISEQ-2000",
                "chipType": "FCL",
                "status": 1,
                "createUser": "427868391118864384",
                "updateUser": "427868391118864384",
                "sampleList": [{
                    "barcode": "1", "hybridProductConcentration": "1", "libProductConcentration": "",
                    "sampleIndex": "1", "umi": "1", "plateCode": hybrid_plate_code, "sampleNo": "25A0000001",
                    "sampleId": "494168929636319232", "inspectionType": "Sample", "sampleProductId": "494168929640513536",
                    "productNo": "DX1412", "sampleTypeCode": "L001", "sampleSetting": "Clinical",
                    "projectCode": "CS", "pointCode": "A1", "hybridizationId": "ZXbh0001-1"}]
            }
        },
        {
            "case_name": "创建NIFTY-上机前准备实验任务",
            "option": "clear",
            "task_items": {
                "schemeId": "532622041912840195",
                "instrumentId": "SIRO16_202409110001",
                "instrumentType": "SIRO-48",
                "automationScheme": "NIFTY003",
                "experimentalProcedure": "SequencingPrep",
                "productClass": "NIFTY",
                "projectCode": "NIFTY",
                "routingName": "一步离心富集",
                "sequencePlatform": "MGISEQ-2000",
                "chipType": "FCL",
                "status": 1,
                "createUser": "427868391118864384",
                "updateUser": "427868391118864384",
                "sampleList": [{
                    "experimentSampleId": "", "oldExperimentSampleId": "461480293220614144", "flowId": "1585932",
                    "taskId": "461480293195448320", "taskCode": "F202503050001", "hisTaskCode": "F202503050001",
                    "retestFlag": "", "sampleId": "461466289697849345", "sampleNo": "25B0305073",
                    "deviceSampleNo": "", "autoFlag": "", "inspectionType": "Sample", "sampleProductId": "461466289702043648",
                    "productNo": "DX1975", "productName": "", "sampleTypeCode": "S051", "sampleTypeName": "",
                    "sampleSetting": "Clinical", "productClass": "", "routingName": "", "projectCode": "NIFTY",
                    "createTime": "2025-03-05 10:37:56", "createUser": "", "creator": "黄雁", "updateTime": "",
                    "updateUser": "", "updater": "", "planPlateCode": "", "planPointCode": "",
                    "plateCode": "L03050001-HY", "pointCode": "A01", "prepPlateCode": "P03050001-HY",
                    "prepPointCode": "A01", "libPlateCode": "L03050001-HY", "libPointCode": "A01",
                    "hybridPlateCode": "", "hybridPointCode": "", "seqPlateCode": "", "seqPointCode": "", "umi": "1",
                    "hasIndexId": "1", "sampleIndex": "1", "dnaSamlpingVolume": "4.23", "dnaReplenishmentVolume": "5.23",
                    "extractProductConcentration": "3.1", "extractionProductSignal": "3.22",
                    "libProductConcentration": "3.1", "libProductSignal": "3.22", "hybridProductConcentration": "",
                    "hybridProductSignal": "", "seqProductConcentration": "", "seqProductSignal": "",
                    "poolingId": "", "libraryVolume": "", "poolingReplenishmentVolume": "", "barcode": "1",
                    "hybridizationId": "", "extractConcentrationQualifiedFlag": "", "hybridizationPoolingSignal": "",
                    "hybridizationPoolingConcentration": "", "hybridizationPoolingConcentrationFlag": "",
                    "hybridConcentrationQualifiedFlag": "", "dnbConcentrationQualifiedFlag": "",
                    "libConcentrationQualifiedFlag": "", "hybridizationSamlpingVolume": "",
                    "hybridizationReplenishmentVolume": ""}]
            }
        }
    ]

    close_data = [
        {
            "option": "delete",
            "task_items": {
                "schemeId": "532574949186080781",
                "instrumentId": "SIRO16_202409110001",
                "instrumentType": "SIRO-48",
                "automationScheme": "携筛001",
                "experimentalProcedure": "Full-process",
                "productClass": "PreprocessedProduct",
                "projectCode": "CS",
                "routingName": "CS",
                "sequencePlatform": "MGISEQ-2000",
                "chipType": "FCL",
                "status": 1,
                "createUser": "427868391118864384",
                "updateUser": "427868391118864384",
                "plateCodeList": pre_plate_code,
                "sampleList": [{
                    "barcode": 1, "hybridProductConcentration": "", "libProductConcentration": "", "sampleIndex": "",
                    "umi": "", "samplePatientId": "526782660492787713", "sampleInspectionId": "526782660492787712",
                    "sampleProductId": "526782660492787714", "sampleNo": "25B09010352",
                    "sampleTypeCode": "L001", "probandSampleNo": "", "hospitalSampleNo": "",
                    "collectDate": "2025-05-01",
                    "receivedDate": "2025-05-02", "patientName": "test2352", "patientGender": "Female",
                    "patientAge": "", "patientBirthday": "", "patientWeight": "", "patientHeight": "",
                    "patientAddress": "", "patientIdCard": "", "patientMobile": "", "patientEmail": "",
                    "outpatientNo": "", "inpatientNo": "", "extInfo": "{}", "enterPedigreeFlag": "",
                    "knownFamilyRelation": "", "creator": "陈清荣", "createTime": "2025-09-01 15:26:13",
                    "updateUser": "", "updateTime": "", "hospitalId": "451794825952493568", "hospitalName": "罗湖中医院",
                    "doctorId": "", "doctorName": "", "departmentId": "", "departmentName": "", "remark": "",
                    "projectCode": "CS", "productClass": "0", "productNo": "DX2002", "sampleClinicalId": "",
                    "clinicalInfo": "{\"ivfNo\": \"\", \"bhOther\": \"\", \"chorion\": \"\", \"ivfFlag\": \"\", \"bhParity\": \"\", \"apgarScore\": \"\", \"focusGenes\": \"\", \"reportMode\": \"SingleReport\", \"spouseName\": \"\", \"testTubeNo\": \"\", \"bhGravidity\": \"\", \"birthWeight\": \"\", \"patientType\": \"\", \"birthtHeight\": \"\", \"donateStatus\": \"\", \"donorEggFlag\": \"\", \"guardianName\": \"\", \"spouseIdCard\": \"\", \"amniocentesis\": \"\", \"downScreening\": \"\", \"familyHistory\": \"无\", \"gestationalAge\": \"\", \"spouseClinical\": \"\", \"ultrasoundDate\": \"\", \"matingSituation\": \"\", \"typeBultrasonic\": \"\", \"clinicalSymptoms\": \"无\", \"conceptionMethod\": \"\", \"lastMenstruation\": \"\", \"medicationHistory\": \"\", \"otherClinicalInfo\": \"\", \"illnessHistoryPast\": \"\", \"maleMedicalHistory\": \"\", \"pregnancyCondition\": \"\", \"healthInsuranceCard\": \"\", \"maleDetectionMethod\": \"\", \"maleDetectionResult\": \"\", \"reasonForInspection\": \"\", \"ultrasonographyFlag\": \"\", \"childDetectionMethod\": \"\", \"childDetectionResult\": \"\", \"femaleMedicalHistory\": \"\", \"femaleDetectionMethod\": \"\", \"femaleDetectionResult\": \"\", \"illnessHistoryAllergy\": \"\", \"illnessHistoryPresent\": \"\", \"childbirthExpectedDate\": \"\", \"pregnancyDetectionFlag\": \"\", \"adversePregnancyHistory\": \"无\", \"maleChromosomeDetection\": \"\", \"childChromosomeDetection\": \"\", \"femaleChromosomeDetection\": \"\", \"abnormalUltrasonographyFlag\": \"\"}",
                    "experimentFlag": "", "formId": "", "flowId": "3261100", "status": "Sample", "operationCode": "",
                    "patientCountry": "", "patientNation": "", "patientNativePlace": "", "medicalRecordNo": "",
                    "barNumber": "", "familyNumber": "", "spouseSampleNo": "", "__index__": 95, "selectable": "false",
                    "sampleSetting": "Clinical", "sampleId": "526782660492787713", "inspectionType": "Sample",
                    "retestFlag": "No", "holeId": "A1", "pointCode": "A1", "plateCode": pre_plate_code}]
            }
        }]

    init_data = [
        {
            "option": "",
            "task_items": {
                "schemeId": "532574949186080781",
                "instrumentId": "SIRO16_202409110001",
                "instrumentType": "SIRO-48",
                "automationScheme": "携筛001",
                "experimentalProcedure": "Full-process",
                "productClass": "PreprocessedProduct",
                "projectCode": "CS",
                "routingName": "CS",
                "sequencePlatform": "MGISEQ-2000",
                "chipType": "FCL",
                "status": 1,
                "createUser": "427868391118864384",
                "updateUser": "427868391118864384",
                "plateCodeList": pre_plate_code,
                "sampleList": [{
                    "barcode": 1, "hybridProductConcentration": "", "libProductConcentration": "", "sampleIndex": "",
                    "umi": "", "samplePatientId": "526782660492787713", "sampleInspectionId": "526782660492787712",
                    "sampleProductId": "526782660492787714", "sampleNo": "25B09010352",
                    "sampleTypeCode": "L001", "probandSampleNo": "", "hospitalSampleNo": "",
                    "collectDate": "2025-05-01",
                    "receivedDate": "2025-05-02", "patientName": "test2352", "patientGender": "Female",
                    "patientAge": "", "patientBirthday": "", "patientWeight": "", "patientHeight": "",
                    "patientAddress": "", "patientIdCard": "", "patientMobile": "", "patientEmail": "",
                    "outpatientNo": "", "inpatientNo": "", "extInfo": "{}", "enterPedigreeFlag": "",
                    "knownFamilyRelation": "", "creator": "陈清荣", "createTime": "2025-09-01 15:26:13",
                    "updateUser": "", "updateTime": "", "hospitalId": "451794825952493568", "hospitalName": "罗湖中医院",
                    "doctorId": "", "doctorName": "", "departmentId": "", "departmentName": "", "remark": "",
                    "projectCode": "CS", "productClass": "0", "productNo": "DX2002", "sampleClinicalId": "",
                    "clinicalInfo": "{\"ivfNo\": \"\", \"bhOther\": \"\", \"chorion\": \"\", \"ivfFlag\": \"\", \"bhParity\": \"\", \"apgarScore\": \"\", \"focusGenes\": \"\", \"reportMode\": \"SingleReport\", \"spouseName\": \"\", \"testTubeNo\": \"\", \"bhGravidity\": \"\", \"birthWeight\": \"\", \"patientType\": \"\", \"birthtHeight\": \"\", \"donateStatus\": \"\", \"donorEggFlag\": \"\", \"guardianName\": \"\", \"spouseIdCard\": \"\", \"amniocentesis\": \"\", \"downScreening\": \"\", \"familyHistory\": \"无\", \"gestationalAge\": \"\", \"spouseClinical\": \"\", \"ultrasoundDate\": \"\", \"matingSituation\": \"\", \"typeBultrasonic\": \"\", \"clinicalSymptoms\": \"无\", \"conceptionMethod\": \"\", \"lastMenstruation\": \"\", \"medicationHistory\": \"\", \"otherClinicalInfo\": \"\", \"illnessHistoryPast\": \"\", \"maleMedicalHistory\": \"\", \"pregnancyCondition\": \"\", \"healthInsuranceCard\": \"\", \"maleDetectionMethod\": \"\", \"maleDetectionResult\": \"\", \"reasonForInspection\": \"\", \"ultrasonographyFlag\": \"\", \"childDetectionMethod\": \"\", \"childDetectionResult\": \"\", \"femaleMedicalHistory\": \"\", \"femaleDetectionMethod\": \"\", \"femaleDetectionResult\": \"\", \"illnessHistoryAllergy\": \"\", \"illnessHistoryPresent\": \"\", \"childbirthExpectedDate\": \"\", \"pregnancyDetectionFlag\": \"\", \"adversePregnancyHistory\": \"无\", \"maleChromosomeDetection\": \"\", \"childChromosomeDetection\": \"\", \"femaleChromosomeDetection\": \"\", \"abnormalUltrasonographyFlag\": \"\"}",
                    "experimentFlag": "", "formId": "", "flowId": "3261100", "status": "Sample", "operationCode": "",
                    "patientCountry": "", "patientNation": "", "patientNativePlace": "", "medicalRecordNo": "",
                    "barNumber": "", "familyNumber": "", "spouseSampleNo": "", "__index__": 95, "selectable": "false",
                    "sampleSetting": "Clinical", "sampleId": "526782660492787713", "inspectionType": "Sample",
                    "retestFlag": "No", "holeId": "A1", "pointCode": "A1", "plateCode": pre_plate_code}]
            }
        }]

    upload_plate_config = [
        {
            "case_name": "NBS杂洗导入建库板",
            "product": "NBS",
            "procedure": "Hybridization",
            "plate_type": "Lib.xlsx"
        },
        {
            "case_name": "CS杂洗导入建库板",
            "product": "CS",
            "procedure": "Hybridization",
            "plate_type": "Lib.xlsx"
        },
        {
            "case_name": "NBS上机前准备导入杂洗板",
            "product": "NBS",
            "procedure": "SequencingPrep",
            "plate_type": "Hybrid.xlsx"
        },
        {
            "case_name": "CS上机前准备导入杂洗板",
            "product": "CS",
            "procedure": "SequencingPrep",
            "plate_type": "Hybrid.xlsx"
        },
        {
            "case_name": "CNV-seq上机前准备导入建库板",
            "product": "CNV-seq",
            "procedure": "SequencingPrep",
            "plate_type": "Lib.xlsx"
        },
        {
            "case_name": "NIFTY上机前准备导入建库板",
            "product": "NIFTY",
            "procedure": "SequencingPrep",
            "plate_type": "Lib.xlsx"
        }
    ]

    field_config = [
        {
            "page": "ExperimentList",
            "field_base_data": {'productClass': '产品大类', 'createTime': '创建时间', 'expTaskCode': '实验任务编号',
                                'instrumentId': '机器ID', 'experimentalProcedure': '实验工序', 'experimentalState': '实验状态',
                                'experimentalLink': '当前实验环节', 'exceptionReason': '异常原因', 'sampleAmount': '样本数量',
                                'taskStartTime': '实验开始时间', 'taskFinishTime': '实验结束时间', 'automationScheme': '自动化方案'},
            "field_project_data": {'productClass': '产品大类', 'createTime': '创建时间', 'creator': '创建人',
                                   'expTaskCode': '实验任务编号', 'instrumentId': '机器ID', 'experimentalProcedure': '实验工序',
                                   'experimentalState': '实验状态', 'experimentalLink': '当前实验环节', 'exceptionReason': '异常原因',
                                   'sampleAmount': '样本数量', 'taskStartTime': '实验开始时间', 'taskFinishTime': '实验结束时间',
                                   'automationScheme': '自动化方案'}
        }, {
            "page": "Experiment",
            "field_base_data": {'sampleNo': '样本编号', 'productNo': '产品套餐', 'sampleTypeCode': '样本类型',
                                'prepPlateCode': '前处理板号', 'extractProductConcentration': '提取产物浓度',
                                'libPlateCode': '建库板号', 'barcode': 'Barcode ID', 'libProductConcentration': '建库产物浓度',
                                'seqPlateCode': '上机前准备板号', 'poolingId': 'Pooling ID', 'seqProductConcentration': 'DNB浓度',
                                'sampleSetting': '样本设定', 'productClass': '产品大类', 'projectCode': '检测项目'},
            "field_project_data": {'sampleNo': '样本编号', 'productNo': '产品套餐', 'sampleTypeCode': '样本类型',
                                   'routingName': '实验技术路线', 'prepPlateCode': '前处理板号', 'prepPointCode': '前处理孔位',
                                   'dnaReplenishmentVolume': 'DNA补水体积', 'dnaSamlpingVolume': 'DNA取样体积',
                                   'extractProductConcentration': '提取产物浓度', 'extractionProductSignal': '提取产物荧光值',
                                   'libPlateCode': '建库板号', 'libPointCode': '建库孔位', 'barcode': 'Barcode ID',
                                   'sampleIndex': 'Index ID', 'umi': 'UMI', 'libProductConcentration': '建库产物浓度',
                                   'libProductSignal': '建库产物荧光值', 'hybridPlateCode': '杂洗板号', 'hybridPointCode': '杂洗孔位',
                                   'hybridProductConcentration': '杂洗产物浓度', 'hybridProductSignal': '杂洗产物荧光值',
                                   'seqPlateCode': '上机前准备板号', 'seqPointCode': '上机前准备孔位', 'poolingId': 'Pooling ID',
                                   'libraryVolume': '子文库体积', 'poolingReplenishmentVolume': '混合文库补水体积',
                                   'seqProductConcentration': 'DNB浓度', 'seqProductSignal': 'DNB荧光值', 'sampleSetting': '样本设定',
                                   'productClass': '产品大类', 'projectCode': '检测项目', 'planPlateCode': '预排板号',
                                   'planPointCode': '预排孔位号'}
        }
    ]
