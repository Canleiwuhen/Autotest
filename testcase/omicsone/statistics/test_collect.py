import pytest
import allure
from utils.tools import calculate_file_buffer



@pytest.mark.usefixtures("res")
class TestStatistics:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-CNVSEQ")
    @allure.title("统计中心-CNVSEQ-查询")
    def test_search_cnvseq(self, res):
        items = ['sample', 'mutation', 'disease', 'reportType', 'chromosomeOther', 'autosomeAndHeterosome',
                 'singleParent', 'pathogen']
        for item in items:
            search_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                           "collectDate": "2024-12-19,2025-12-19", "projectCode": ["CNV-seq"]}
            search_url = '/api/statistic/cnvseq/' + item
            search_data_sample = res.post_request(url=search_url, json=search_data)
            assert search_data_sample.status_code == 200
            assert search_data_sample.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-NIFTY")
    @allure.title("统计中心-NIFTY-查询")
    def test_search_nifty(self, res):
        items = ['comprehensive', 'medicalAdvice', 'detection', 'causeOfFailure', 'classification', 'qualitycontrol',
                 'detail']
        for item in items:
            search_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                           "collectDate": "2024-12-19,2025-12-19", "projectCode": ["NIFTY"]}
            search_url = '/api/statistic/nifty/' + item
            search_data_sample = res.post_request(url=search_url, json=search_data)
            assert search_data_sample.status_code == 200
            assert search_data_sample.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-CS")
    @allure.title("统计中心-CS-查询")
    def test_search_cs(self, res):
        items = ['comprehensive', 'riskSummary', 'overview/time', 'overview/department', 'retestStatistics', 'carrierRateStats',
                 'highRiskDiseaseStats', 'variantDetectionStats', 'diseaseFrequency', 'geneFrequency',
                 'diseasesDetection', 'mutationDetection', 'mutationDisease', 'mutationGene']
        for item in items:
            search_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                           "collectDate": "2024-12-19,2025-12-19", "projectCode": ["CS"]}
            search_url = '/api/statistic/cs/' + item
            search_data_sample = res.post_request(url=search_url, json=search_data)
            assert search_data_sample.status_code == 200
            assert search_data_sample.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-NBS")
    @allure.title("统计中心-NBS-查询")
    def test_search_nbs(self, res):
        items = ['retestValidate', 'categorical', 'sampleSizeOverview', 'variantDetections', 'sampleResultDetails']
        for item in items:
            search_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                           "collectDate": "2024-12-19,2025-12-19", "projectCode": ["NBS"]}
            search_url = '/api/statistic/nbs/' + item
            search_data_sample = res.post_request(url=search_url, json=search_data)
            assert search_data_sample.status_code == 200
            assert search_data_sample.json()['retInfo'] == 'success'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-CNVSEQ")
    def test_load_file_cnvseq(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                     "collectDate": "2024-12-19,2025-12-19", "projectCode": ["CNV-seq"]}
        load_data_res = res.post_request("/api/statistic/cnvseq/download", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-NIFTY")
    def test_load_file_nifty(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                     "collectDate": "2024-12-19,2025-12-19", "projectCode": ["NIFTY"]}
        load_data_res = res.post_request("/api/statistic/nifty/download", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-NIFTY（T13/T18/T21检出）")
    def test_load_file_nifty_trisomy(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-22", "2025-12-22"],
                     "collectDate": "2024-12-22,2025-12-22", "projectCode": ["NIFTY"]}
        load_data_res = res.post_request("/api/statistic/nifty/detail/download/trisomy", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-NIFTY（性染色体检出）")
    def test_load_file_nifty_chrxy(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-22", "2025-12-22"],
                     "collectDate": "2024-12-22,2025-12-22", "projectCode": ["NIFTY"]}
        load_data_res = res.post_request("/api/statistic/nifty/detail/download/chrxy", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-NIFTY（疾病）")
    def test_load_file_nifty_cnv(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-22", "2025-12-22"],
                     "collectDate": "2024-12-22,2025-12-22", "projectCode": ["NIFTY"]}
        load_data_res = res.post_request("/api/statistic/nifty/detail/download/cnv", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-NIFTY（常染色体）")
    def test_load_file_nifty_chrOther(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-22", "2025-12-22"],
                     "collectDate": "2024-12-22,2025-12-22", "projectCode": ["NIFTY"]}
        load_data_res = res.post_request("/api/statistic/nifty/detail/download/chrOther", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-CS")
    def test_load_file_cs(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                     "collectDate": "2024-12-19,2025-12-19", "projectCode": ["CS"]}
        load_data_res = res.post_request("/api/statistic/cs/download", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心-下载-NBS")
    def test_load_file_nbs(self, res):
        load_data = {"dateType": "collectDate", "dateTime": ["2024-12-19", "2025-12-19"],
                     "collectDate": "2024-12-19,2025-12-19", "projectCode": ["NBS"]}
        load_data_res = res.post_request("/api/statistic/nbs/download", json=load_data)
        assert load_data_res.status_code == 200
        if load_data_res.status_code == 200:
            file_size = calculate_file_buffer(load_data_res)
            assert file_size > 0  # 判断文件非空文件
