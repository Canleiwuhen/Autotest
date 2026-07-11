import pytest
import allure
import os
from utils.tools import create_sample, calculate_file_buffer
from testcase.omicsone.samplecenter.sample_data import DataList


@pytest.mark.usefixtures("res", "res_file")
class TestSample:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本添加")
    @allure.title("样本中心-CNV-seq样本添加")
    def test_add_sample_cnvseq(self, res):
        data = {
            "projectCode": "CNV-seq",
            "formId": "1850818129993592834",
            "productName": "DX0006  染色体非整倍体_1M以上缺失重复检测",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX0006",
            "sampleNo": create_sample(),
            "sampleTypeCode": "S370",
            "collectDate": "2025-07-01",
            "receivedDate": "2025-07-02",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "测试1",
            "patientGender": "Female",
            "patientAge": "34",
            "enterPedigreeFlag": "No",
            "reasonForInspection": "测试1",
            "familyHistory": "测试2",
            "patientType": "ConfirmedPatient",
            "gestationalAge": "3,3",
            "donorEggFlag": "Yes",
            "lastMenstruation": "2025-04-09",
            "pregnancyDetectionFlag": "No",
            "ultrasonographyFlag": "No",
            "maleChromosomeDetection": "No",
            "femaleChromosomeDetection": "No",
            "childChromosomeDetection": "No",
            "maleMedicalHistory": "测试3",
            "femaleMedicalHistory": "测试4",
            "remark": "测试5",
            "editMode": "add"
        }
        response = res.post_request("/api/sample/add", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本添加")
    @allure.title("样本中心-NIFTY样本添加")
    def test_add_sample_nifty(self, res):
        data = {
          "projectCode": "NIFTY",
          "formId": "1850857961721663489",
          "productName": "DX0558  NIFTY基础",
          "departmentName": "骨科",
          "doctorName": "陈医生",
          "hospitalName": "罗湖中医院",
          "productNo": "DX0558",
          "sampleNo": create_sample(),
          "sampleTypeCode": "S052",
          "shipmentCondition": "4",
          "collectDate": "2025-12-22",
          "receivedDate": "2025-12-22",
          "gestationalAge": "1,2",
          "fetusType": "Single",
          "tubeType": "STRECK",
          "additionalReportFlag": "No",
          "hospitalSampleNo": "123123123",
          "patientName": "姓名",
          "patientIdCard": "证件·",
          "patientBirthday": "2025-12-01",
          "patientAge": "13",
          "outpatientNo": "门诊号",
          "hospitalId": "451794825952493568",
          "departmentId": "494538674420187136",
          "doctorId": "494538674462130176",
          "patientHeight": "133",
          "patientWeight": "11",
          "patientMobile": "2123123",
          "patientTel": "123123123",
          "patientAddress": "Aa1!字符",
          "emergentName": "123123",
          "emergentRelation": "123123",
          "emergentTel": "1+-23123",
          "childbirthExpectedDate": "2025-12-10",
          "lastMenstruation": "2025-12-17",
          "chorion": "DC",
          "downScreening": "T21MediumRisk",
          "typeBultrasonic": "NormalSingle",
          "ivfFlag": "Yes",
          "conceptionMethod": "NaturalConception",
          "bhGravidity": "11",
          "bhParity": "2",
          "bhOther": "Aa1!字符",
          "amniocentesis": "Aa1!字符",
          "illnessHistoryPast": "Aa1!字符",
          "illnessHistoryPresent": "Aa1!字符",
          "illnessHistoryAllergy": "Aa1!字符",
          "familyHistory": "Aa1!字符",
          "remark": "Aa1!字符",
          "editMode": "add"
        }
        response = res.post_request("/api/sample/add", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本添加")
    @allure.title("样本中心-CS样本添加")
    def test_add_sample_cs(self, res):
        data = {
            "projectCode": "CS",
            "formId": "1850857961721663450",
            "productName": "DX1412  单基因遗传病扩展性携带者筛查10种",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX1412",
            "sampleNo": create_sample(),
            "hospitalSampleNo": "25S123123",
            "receivedDate": "2025-12-24",
            "collectDate": "2025-12-24",
            "sampleTypeCode": "L001",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "姓名",
            "patientGender": "Male",
            "patientBirthday": "1999-09-09",
            "patientAge": 26,
            "patientIdCard": "45130219990909091X",
            "healthInsuranceCard": "123123123123",
            "patientNation": "汉族",
            "patientNativePlace": "广东",
            "patientMobile": "+131-01010101",
            "patientAddress": "Aa1!字符",
            "patientEmail": "100001@qq.com",
            "outpatientNo": "123123123",
            "medicalRecordNo": "123123123",
            "inpatientNo": "123123123",
            "barNumber": "123123123",
            "reportMode": "SingleReport",
            "gestationalAge": "1,2",
            "focusGenes": "F8",
            "donateStatus": "Yes",
            "ivfNo": "IVF123",
            "testTubeNo": "sg1231233123",
            "clinicalSymptoms": "Aa1!字符",
            "familyHistory": "Aa1!字符",
            "adversePregnancyHistory": "Aa1!字符",
            "pregnancyCondition": "Aa1!字符",
            "matingSituation": "Aa1!字符",
            "otherClinicalInfo": "Aa1!字符",
            "spouseClinical": "Aa1!字符",
            "remark": "Aa1!字符",
            "editMode": "add"
            }
        response = res.post_request("/api/sample/add", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本添加")
    @allure.title("样本中心-NBS样本添加")
    def test_add_sample_nbs(self, res):
        data = {
            "projectCode": "NBS",
            "formId": "1850857961721663451",
            "productName": "DX1968  安馨可-新生儿及儿童遗传病基因检测（专业版）",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX1968",
            "sampleNo": create_sample(),
            "hospitalSampleNo": "25B123123123",
            "receivedDate": "2025-12-24",
            "collectDate": "2025-12-24",
            "sampleTypeCode": "L001",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "姓名",
            "patientGender": "Female",
            "patientAge": 26,
            "patientBirthday": "1999-09-09",
            "patientIdCard": "44411119990909091X",
            "patientNation": "汉族",
            "patientNativePlace": "广东",
            "guardianName": "监护人",
            "outpatientNo": "123123123",
            "medicalRecordNo": "123123123123",
            "inpatientNo": "123123123",
            "barNumber": "123123123",
            "healthInsuranceCard": "123123123123",
            "birthWeight": "4",
            "birthtHeight": "30",
            "patientEmail": "123123123@qq.com",
            "patientAddress": "Aa1!字符",
            "patientMobile": "+1313-111111",
            "apgarScore": "6",
            "focusGenes": "F6",
            "donateStatus": "Yes",
            "clinicalSymptoms": "Aa1!字符",
            "familyHistory": "Aa1!字符",
            "medicationHistory": "Aa1!字符",
            "otherClinicalInfo": "Aa1!字符",
            "remark": "Aa1!字符",
            "editMode": "add"
            }
        response = res.post_request("/api/sample/add", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-查询样本")
    @allure.title("样本中心-查询样本：{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search_sample(self, res, data):
        """
        样本中心查询，只做了单个字段搜索
        :param res:
        :param data:
        :return:
        """
        tmp = data['search_items']
        json_data = {
            "createTime": {
                "startDate": "2024-07-28 00:00",
                "endDate": "2025-07-28 23:59"
            },
            "page": 1,
            "pageNum": 1,
            "limit": 500,
            "pageSize": 500
        }
        json_data.update(tmp)
        response = res.post_request("/api/sample/list", json=json_data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本编辑")
    @allure.title("样本中心-CNV-seq样本编辑")
    def test_edit_sample_cnvseq(self, res):
        sampleno = create_sample()
        data1 = {
            "projectCode": "CNV-seq",
            "formId": "1850818129993592834",
            "productName": "DX0006  染色体非整倍体_1M以上缺失重复检测",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX0006",
            "sampleNo": sampleno,
            "sampleTypeCode": "S370",
            "collectDate": "2025-07-01",
            "receivedDate": "2025-07-02",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "测试1",
            "patientGender": "Female",
            "patientAge": "34",
            "enterPedigreeFlag": "No",
            "reasonForInspection": "测试1",
            "familyHistory": "测试2",
            "patientType": "ConfirmedPatient",
            "gestationalAge": "3,3",
            "donorEggFlag": "Yes",
            "lastMenstruation": "2025-04-09",
            "pregnancyDetectionFlag": "No",
            "ultrasonographyFlag": "No",
            "maleChromosomeDetection": "No",
            "femaleChromosomeDetection": "No",
            "childChromosomeDetection": "No",
            "maleMedicalHistory": "测试3",
            "femaleMedicalHistory": "测试4",
            "remark": "测试5",
            "editMode": "add"
        }
        res.post_request("/api/sample/add", json=data1)   # 先新增样本
        detailurl = "/api/sample/detail/" + sampleno
        detairesp = res.get_request(url=detailurl)  # 获取样本详情
        data2 = detairesp.json()['result']
        data2.update({"editMode": "edit"})
        data2['patientAge'] = '35'
        response = res.post_request("/api/sample/edit", json=data2)  # 执行编辑操作
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本编辑")
    @allure.title("样本中心-NIFTY样本编辑")
    def test_edit_sample_nifty(self, res):
        sampleno = create_sample()
        data1 = {
          "projectCode": "NIFTY",
          "formId": "1850857961721663489",
          "productName": "DX0558  NIFTY基础",
          "departmentName": "骨科",
          "doctorName": "陈医生",
          "hospitalName": "罗湖中医院",
          "productNo": "DX0558",
          "sampleNo": sampleno,
          "sampleTypeCode": "S052",
          "shipmentCondition": "4",
          "collectDate": "2025-12-22",
          "receivedDate": "2025-12-22",
          "gestationalAge": "1,2",
          "fetusType": "Single",
          "tubeType": "STRECK",
          "additionalReportFlag": "No",
          "hospitalSampleNo": "123123123",
          "patientName": "姓名",
          "patientIdCard": "证件·",
          "patientBirthday": "2025-12-01",
          "patientAge": "13",
          "outpatientNo": "门诊号",
          "hospitalId": "451794825952493568",
          "departmentId": "494538674420187136",
          "doctorId": "494538674462130176",
          "patientHeight": "133",
          "patientWeight": "11",
          "patientMobile": "2123123",
          "patientTel": "123123123",
          "patientAddress": "Aa1!字符",
          "emergentName": "123123",
          "emergentRelation": "123123",
          "emergentTel": "1+-23123",
          "childbirthExpectedDate": "2025-12-10",
          "lastMenstruation": "2025-12-17",
          "chorion": "DC",
          "downScreening": "T21MediumRisk",
          "typeBultrasonic": "NormalSingle",
          "ivfFlag": "Yes",
          "conceptionMethod": "NaturalConception",
          "bhGravidity": "11",
          "bhParity": "2",
          "bhOther": "Aa1!字符",
          "amniocentesis": "Aa1!字符",
          "illnessHistoryPast": "Aa1!字符",
          "illnessHistoryPresent": "Aa1!字符",
          "illnessHistoryAllergy": "Aa1!字符",
          "familyHistory": "Aa1!字符",
          "remark": "Aa1!字符",
          "editMode": "add"
        }
        res.post_request("/api/sample/add", json=data1)   # 先新增样本
        detailurl = "/api/sample/detail/" + sampleno
        detairesp = res.get_request(url=detailurl)  # 获取样本详情
        data2 = detairesp.json()['result']
        data2.update({"editMode": "edit"})
        data2['patientAge'] = '35'
        response = res.post_request("/api/sample/edit", json=data2)  # 执行编辑操作
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本编辑")
    @allure.title("样本中心-CS样本编辑")
    def test_edit_sample_cs(self, res):
        sampleno = create_sample()
        data1 = {
            "projectCode": "CS",
            "formId": "1850857961721663450",
            "productName": "DX1412  单基因遗传病扩展性携带者筛查10种",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX1412",
            "sampleNo": sampleno,
            "hospitalSampleNo": "25S123123",
            "receivedDate": "2025-12-24",
            "collectDate": "2025-12-24",
            "sampleTypeCode": "L001",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "姓名",
            "patientGender": "Male",
            "patientBirthday": "1999-09-09",
            "patientAge": 26,
            "patientIdCard": "45130219990909091X",
            "healthInsuranceCard": "123123123123",
            "patientNation": "汉族",
            "patientNativePlace": "广东",
            "patientMobile": "+131-01010101",
            "patientAddress": "Aa1!字符",
            "patientEmail": "100001@qq.com",
            "outpatientNo": "123123123",
            "medicalRecordNo": "123123123",
            "inpatientNo": "123123123",
            "barNumber": "123123123",
            "reportMode": "SingleReport",
            "gestationalAge": "1,2",
            "focusGenes": "F8",
            "donateStatus": "Yes",
            "ivfNo": "IVF123",
            "testTubeNo": "sg1231233123",
            "clinicalSymptoms": "Aa1!字符",
            "familyHistory": "Aa1!字符",
            "adversePregnancyHistory": "Aa1!字符",
            "pregnancyCondition": "Aa1!字符",
            "matingSituation": "Aa1!字符",
            "otherClinicalInfo": "Aa1!字符",
            "spouseClinical": "Aa1!字符",
            "remark": "Aa1!字符",
            "editMode": "add"
            }
        res.post_request("/api/sample/add", json=data1)  # 先新增样本
        detailurl = "/api/sample/detail/" + sampleno
        detairesp = res.get_request(url=detailurl)  # 获取样本详情
        data2 = detairesp.json()['result']
        data2.update({"editMode": "edit"})
        data2['patientAge'] = '35'
        response = res.post_request("/api/sample/edit", json=data2)  # 执行编辑操作
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本编辑")
    @allure.title("样本中心-NBS样本编辑")
    def test_edit_sample_nbs(self, res):
        sampleno = create_sample()
        data1 = {
            "projectCode": "NBS",
            "formId": "1850857961721663451",
            "productName": "DX1968  安馨可-新生儿及儿童遗传病基因检测（专业版）",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX1968",
            "sampleNo": sampleno,
            "hospitalSampleNo": "25B123123123",
            "receivedDate": "2025-12-24",
            "collectDate": "2025-12-24",
            "sampleTypeCode": "L001",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "姓名",
            "patientGender": "Female",
            "patientAge": 26,
            "patientBirthday": "1999-09-09",
            "patientIdCard": "44411119990909091X",
            "patientNation": "汉族",
            "patientNativePlace": "广东",
            "guardianName": "监护人",
            "outpatientNo": "123123123",
            "medicalRecordNo": "123123123123",
            "inpatientNo": "123123123",
            "barNumber": "123123123",
            "healthInsuranceCard": "123123123123",
            "birthWeight": "4",
            "birthtHeight": "30",
            "patientEmail": "123123123@qq.com",
            "patientAddress": "Aa1!字符",
            "patientMobile": "+1313-111111",
            "apgarScore": "6",
            "focusGenes": "F6",
            "donateStatus": "Yes",
            "clinicalSymptoms": "Aa1!字符",
            "familyHistory": "Aa1!字符",
            "medicationHistory": "Aa1!字符",
            "otherClinicalInfo": "Aa1!字符",
            "remark": "Aa1!字符",
            "editMode": "add"
            }
        res.post_request("/api/sample/add", json=data1)  # 先新增样本
        detailurl = "/api/sample/detail/" + sampleno
        detairesp = res.get_request(url=detailurl)  # 获取样本详情
        data2 = detairesp.json()['result']
        data2.update({"editMode": "edit"})
        data2['patientAge'] = '35'
        response = res.post_request("/api/sample/edit", json=data2)  # 执行编辑操作
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-CNV-seq样本删除")
    @allure.title("样本中心-CNV-seq样本删除")
    def test_delete_sample(self, res):
        """
        只做了康孕样本的删除
        :param res:
        :return:
        """
        sampleno = create_sample()
        data1 = {
            "projectCode": "CNV-seq",
            "formId": "1850818129993592834",
            "productName": "DX0006  染色体非整倍体_1M以上缺失重复检测",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX0006",
            "sampleNo": sampleno,
            "sampleTypeCode": "S370",
            "collectDate": "2025-07-01",
            "receivedDate": "2025-07-02",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "测试1",
            "patientGender": "Female",
            "patientAge": "34",
            "enterPedigreeFlag": "No",
            "reasonForInspection": "测试1",
            "familyHistory": "测试2",
            "patientType": "ConfirmedPatient",
            "gestationalAge": "3,3",
            "donorEggFlag": "Yes",
            "lastMenstruation": "2025-04-09",
            "pregnancyDetectionFlag": "No",
            "ultrasonographyFlag": "No",
            "maleChromosomeDetection": "No",
            "femaleChromosomeDetection": "No",
            "childChromosomeDetection": "No",
            "maleMedicalHistory": "测试3",
            "femaleMedicalHistory": "测试4",
            "remark": "测试5",
            "editMode": "add"
        }
        res.post_request("/api/sample/add", json=data1)  # 先新增样本
        data = [sampleno]
        response = res.post_request("/api/sample/delete", json=data)  # 执行删除操作
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-样本导出")
    @allure.title("样本中心-样本导出")
    def test_export_sample(self, res):
        """
        只做了康孕样本的导出，判断导出文件非空文件
        :param res:
        :return:
        """
        sampleno1 = create_sample()
        sampleno2 = create_sample()
        data1 = {
            "projectCode": "CNV-seq",
            "formId": "1850818129993592834",
            "productName": "DX0006  染色体非整倍体_1M以上缺失重复检测",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX0006",
            "sampleNo": sampleno1,
            "sampleTypeCode": "S370",
            "collectDate": "2025-07-01",
            "receivedDate": "2025-07-02",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "测试1",
            "patientGender": "Female",
            "patientAge": "34",
            "enterPedigreeFlag": "No",
            "reasonForInspection": "测试1",
            "familyHistory": "测试2",
            "patientType": "ConfirmedPatient",
            "gestationalAge": "3,3",
            "donorEggFlag": "Yes",
            "lastMenstruation": "2025-04-09",
            "pregnancyDetectionFlag": "No",
            "ultrasonographyFlag": "No",
            "maleChromosomeDetection": "No",
            "femaleChromosomeDetection": "No",
            "childChromosomeDetection": "No",
            "maleMedicalHistory": "测试3",
            "femaleMedicalHistory": "测试4",
            "remark": "测试5",
            "editMode": "add"
        }
        data2 = {
            "projectCode": "CNV-seq",
            "formId": "1850818129993592834",
            "productName": "DX0006  染色体非整倍体_1M以上缺失重复检测",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX0006",
            "sampleNo": sampleno2,
            "sampleTypeCode": "S370",
            "collectDate": "2025-07-01",
            "receivedDate": "2025-07-02",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "测试1",
            "patientGender": "Female",
            "patientAge": "34",
            "enterPedigreeFlag": "No",
            "reasonForInspection": "测试1",
            "familyHistory": "测试2",
            "patientType": "ConfirmedPatient",
            "gestationalAge": "3,3",
            "donorEggFlag": "Yes",
            "lastMenstruation": "2025-04-09",
            "pregnancyDetectionFlag": "No",
            "ultrasonographyFlag": "No",
            "maleChromosomeDetection": "No",
            "femaleChromosomeDetection": "No",
            "childChromosomeDetection": "No",
            "maleMedicalHistory": "测试3",
            "femaleMedicalHistory": "测试4",
            "remark": "测试5",
            "editMode": "add"
        }
        res.post_request("/api/sample/add", json=data1)  # 先新增样本
        res.post_request("/api/sample/add", json=data2)
        data = [sampleno1, sampleno2]
        response = res.post_request("/api/sample/excel/export?dataId=", json=data)  # 执行导出操作
        assert response.status_code == 200
        if response.status_code == 200:
            file_size = calculate_file_buffer(response)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-下载模板")
    @allure.title("样本中心-下载模板")
    def test_export_template(self, res):
        """
        导出系统上所有检测项目模板，校验导出非空文件
        :param res:
        :return:
        """
        response1 = res.get_request("/api/sample/template/list")  # 获取模板配置数据
        assert response1.status_code == 200
        assert response1.json()['retInfo'] == 'success'
        if response1.status_code == 200:
            tmp = response1.json()['result']
            result = {}
            for i in tmp:
                result.update({i['projectCode']: i['filePath']})
            print(f"字典内容为{result}")
        for key in result.keys():  # 遍历所有检测项目的导入模板
            print(f"当前检测项目为：{key}")
            urltmp = "/api/base/file/downloadFile?filePathOrBusinessType=" + result[key]
            response2 = res.get_request(url=urltmp)
            assert response2.status_code == 200
            if response2.status_code == 200:
                file_size = calculate_file_buffer(response2)
                assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-列表字段配置")
    @allure.title("样本中心-列表字段配置")
    @pytest.mark.parametrize("base_data", DataList.field_base_data)
    @pytest.mark.parametrize("project_data", DataList.field_project_data)
    def test_field_config(self, res, base_data, project_data):
        """
        校验列表配置上常用字段和全量字段，包含所有检测项目
        :param res:
        :param base_data:
        :param project_data:
        :return:
        """
        data = {"configModule": "Sample"}
        response = res.post_request("/api/base/searchconfig/config/fields", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        if response.status_code == 200:
            projectFields = response.json()['result']['projectFields']  # 全量字段
            baseFields = response.json()['result']['baseFields']  # 常用字段
            new_baseFields = dict()
            for i in baseFields:
                new_baseFields.update({i["fieldCode"]: i["fieldName"]})
            print(f"最终整合字典为new_baseFields:{new_baseFields}")

            tmp = set()
            for j in projectFields:
                tmp.add(j['projectCode'])
            tmp_list = list(tmp)  # 整理出所有检测项目
            tmp_dict = dict()
            for p in tmp_list:
                tmp_dict.update({p: {}})
                for q in projectFields:
                    if q['projectCode'] == p:
                        tmp_dict[p].update({q["fieldCode"]: q["fieldName"]})
            print(f"最终整合字典为tmp_dict:{tmp_dict}")
        assert new_baseFields == base_data
        assert tmp_dict == project_data

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-列表字段配置")
    @allure.title("样本中心-CNV-seq列表字段配置")
    @pytest.mark.parametrize("base_data", DataList.field_base_data)
    @pytest.mark.parametrize("project_data", DataList.field_project_all_data)
    def test_field_config_cnvseq(self, res_cnvseq, base_data, project_data):
        """
        CNV-seq列表常用、全部字段
        """
        data = {"configModule": "Sample"}
        response = res_cnvseq.post_request("/api/base/searchconfig/config/fields", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        if response.status_code == 200:
            projectFields = response.json()['result']['projectFields']  # 全量字段
            baseFields = response.json()['result']['baseFields']  # 常用字段
            new_baseFields = dict()
            for i in baseFields:
                new_baseFields.update({i["fieldCode"]: i["fieldName"]})
            print(f"最终整合字典为new_baseFields:{new_baseFields}")

            tmp_dict = {}
            for q in projectFields:
                if q['projectCode'] == 'CNV-seq':
                    tmp_dict.update({q["fieldCode"]: q["fieldName"]})
            print(f"最终整合字典为tmp_dict:{tmp_dict}")
        assert new_baseFields == base_data
        assert tmp_dict == project_data['CNV-seq']

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-列表字段配置")
    @allure.title("样本中心-NIFTY列表字段配置")
    @pytest.mark.parametrize("base_data", DataList.field_base_data)
    @pytest.mark.parametrize("project_data", DataList.field_project_all_data)
    def test_field_config_nifty(self, res_nifty, base_data, project_data):
        """
        NIFTY列表常用、全部字段
        """
        data = {"configModule": "Sample"}
        response = res_nifty.post_request("/api/base/searchconfig/config/fields", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        if response.status_code == 200:
            projectFields = response.json()['result']['projectFields']  # 全量字段
            baseFields = response.json()['result']['baseFields']  # 常用字段
            new_baseFields = dict()
            for i in baseFields:
                new_baseFields.update({i["fieldCode"]: i["fieldName"]})
            print(f"最终整合字典为new_baseFields:{new_baseFields}")

            tmp_dict = {}
            for q in projectFields:
                if q['projectCode'] == 'NIFTY':
                    tmp_dict.update({q["fieldCode"]: q["fieldName"]})
            print(f"最终整合字典为tmp_dict:{tmp_dict}")
        assert new_baseFields == base_data
        assert tmp_dict == project_data['NIFTY']

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-列表字段配置")
    @allure.title("样本中心-CS列表字段配置")
    @pytest.mark.parametrize("base_data", DataList.field_base_data)
    @pytest.mark.parametrize("project_data", DataList.field_project_all_data)
    def test_field_config_cs(self, res_cs, base_data, project_data):
        """
        CS列表常用、全部字段
        """
        data = {"configModule": "Sample"}
        response = res_cs.post_request("/api/base/searchconfig/config/fields", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        if response.status_code == 200:
            projectFields = response.json()['result']['projectFields']  # 全量字段
            baseFields = response.json()['result']['baseFields']  # 常用字段
            new_baseFields = dict()
            for i in baseFields:
                new_baseFields.update({i["fieldCode"]: i["fieldName"]})
            print(f"最终整合字典为new_baseFields:{new_baseFields}")

            tmp_dict = {}
            for q in projectFields:
                if q['projectCode'] == 'CS':
                    tmp_dict.update({q["fieldCode"]: q["fieldName"]})
            print(f"最终整合字典为tmp_dict:{tmp_dict}")
        assert new_baseFields == base_data
        assert tmp_dict == project_data['CS']

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-列表字段配置")
    @allure.title("样本中心-NBS列表字段配置")
    @pytest.mark.parametrize("base_data", DataList.field_base_data)
    @pytest.mark.parametrize("project_data", DataList.field_project_all_data)
    def test_field_config_nbs(self, res_nbs, base_data, project_data):
        """
        NBS列表常用、全部字段
        """
        data = {"configModule": "Sample"}
        response = res_nbs.post_request("/api/base/searchconfig/config/fields", json=data)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        if response.status_code == 200:
            projectFields = response.json()['result']['projectFields']  # 全量字段
            baseFields = response.json()['result']['baseFields']  # 常用字段
            new_baseFields = dict()
            for i in baseFields:
                new_baseFields.update({i["fieldCode"]: i["fieldName"]})
            print(f"最终整合字典为new_baseFields:{new_baseFields}")

            tmp_dict = {}
            for q in projectFields:
                if q['projectCode'] == 'NBS':
                    tmp_dict.update({q["fieldCode"]: q["fieldName"]})
            print(f"最终整合字典为tmp_dict:{tmp_dict}")
        assert new_baseFields == base_data
        assert tmp_dict == project_data['NBS']

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-送检单导入")
    @allure.title("样本中心-送检单导入")
    def test_export_sample(self, res_file):
        """
        导入所有检测项目的送检单，目前只做了CNVseq\nifty\cs\nbs,导入文件数据非动态数据
        :param res_file:
        :return:
        """
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(parent_dir, 'import_files')
        formid_list = res_file.get_request("/api/sample/template/list").json()['result']
        for i in formid_list:  # 循环导入所有送检单
            file = os.path.join(base_path, i['projectCode']+'.xlsx')
            data = {"formId": i['formId']}
            response = res_file.post_request("/api/sample/excel/import", data=data, file_path=file)
            assert response.status_code == 200
            assert response.json()['retInfo'] == 'success'
            assert len(response.json()['result']['success']) != 0    # 正常导入成功，返回是非空列表
            assert len(response.json()['result']['fail']) == 0  # 正常导入成功，返回是空列表
            sample = response.json()['result']['success'][0]['sampleNo']
            datatmp = [sample]
            res_file.post_request("/api/sample/delete", json=datatmp)  # 执行删除操作


    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("样本中心-批量编辑")
    @allure.title("样本中心-批量编辑")
    def test_batch_edit(self, res):
        """
        NBS做示例，批量编辑
        """
        sampleno = create_sample()
        data1 = {
            "projectCode": "NBS",
            "formId": "1850857961721663451",
            "productName": "DX1968  安馨可-新生儿及儿童遗传病基因检测（专业版）",
            "departmentName": "骨科",
            "doctorName": "陈医生",
            "hospitalName": "罗湖中医院",
            "productNo": "DX1968",
            "sampleNo": sampleno,
            "hospitalSampleNo": "25B123123123",
            "receivedDate": "2025-12-24",
            "collectDate": "2025-12-24",
            "sampleTypeCode": "L001",
            "hospitalId": "451794825952493568",
            "departmentId": "494538674420187136",
            "doctorId": "494538674462130176",
            "patientName": "姓名",
            "patientGender": "Female",
            "patientAge": 26,
            "patientBirthday": "1999-09-09",
            "patientIdCard": "44411119990909091X",
            "patientNation": "汉族",
            "patientNativePlace": "广东",
            "guardianName": "监护人",
            "outpatientNo": "123123123",
            "medicalRecordNo": "123123123123",
            "inpatientNo": "123123123",
            "barNumber": "123123123",
            "healthInsuranceCard": "123123123123",
            "birthWeight": "4",
            "birthtHeight": "30",
            "patientEmail": "123123123@qq.com",
            "patientAddress": "Aa1!字符",
            "patientMobile": "+1313-111111",
            "apgarScore": "6",
            "focusGenes": "F6",
            "donateStatus": "Yes",
            "clinicalSymptoms": "Aa1!字符",
            "familyHistory": "Aa1!字符",
            "medicationHistory": "Aa1!字符",
            "otherClinicalInfo": "Aa1!字符",
            "remark": "Aa1!字符",
            "editMode": "add"
            }
        res.post_request("/api/sample/add", json=data1)  # 先新增样本
        detailurl = "/api/sample/detail/" + sampleno
        detairesp = res.get_request(url=detailurl)  # 获取样本详情
        data2 = detairesp.json()['result']
        del data2['updateUser']
        del data2['createUser']
        data2.update({"__index__": "0","creator": "autotest_omics1"})
        data2['patientAge'] = '35'
        data3 = [data2]
        response = res.post_request("/api/sample/edit/batch", json=data3)  # 执行编辑操作
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'






























