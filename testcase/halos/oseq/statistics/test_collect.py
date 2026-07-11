# -*- coding: utf-8 -*-
import pytest
import allure
import io
from testcase.halos.oseq.statistics.statistics_data import DataList



@pytest.mark.usefixtures("res")
class TestStatistics:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-查询")
    @allure.title("统计中心-查询")
    def test_search(self, res):
        """统计中心概览查询"""
        search_response = res.post_request("/prod-api/api/oseq/statistic/overview", json=DataList.search_data)
        assert search_response.status_code == 200
        assert search_response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-体系突变")
    @allure.title("统计中心-体系突变")
    def test_somatic(self, res):
        """统计中心体系突变查询"""
        somatic_response = res.post_request("/prod-api/api/oseq/statistic/somatic", json=DataList.somatic_data)
        assert somatic_response.status_code == 200
        assert somatic_response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-体系核苷酸突变")
    @allure.title("统计中心-体系核苷酸突变")
    def test_somatic_nucleotide(self, res):
        """统计中心体系核苷酸突变查询"""
        somatic_nucleotide_response = res.post_request("/prod-api/api/oseq/statistic/somatic", json=DataList.somatic_nucleotide_data)
        assert somatic_nucleotide_response.status_code == 200
        assert somatic_nucleotide_response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-下载")
    @allure.title("统计中心下载")
    def test_export(self, res):
        """统计中心导出下载"""
        download_response = res.post_request("/prod-api/api/oseq/statistic/overview/export", json={})
        assert download_response.status_code == 200

        # 使用文件流接收响应内容
        file_buffer = io.BytesIO()
        for chunk in download_response.iter_content(chunk_size=8192):
            if chunk:
                file_buffer.write(chunk)

        # 验证文件大小
        assert file_buffer.tell() >= 100

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-体系突变导出")
    @allure.title("体系突变导出")
    def test_somatic_export(self, res):
        """统计中心体系突变导出"""
        download_response = res.post_request("/prod-api/api/oseq/statistic/somatic/export", json={"gene": ""})
        assert download_response.status_code == 200

        # 使用文件流接收响应内容
        file_buffer = io.BytesIO()
        for chunk in download_response.iter_content(chunk_size=8192):
            if chunk:
                file_buffer.write(chunk)

        # 验证文件大小
        assert file_buffer.tell() >= 100

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-体系突变单基因导出")
    @allure.title("体系突变单基因导出")
    def test_somatic_gene_export(self, res):
        """统计中心体系突变导出"""
        download_response = res.post_request("/prod-api/api/oseq/statistic/somatic/gene/export", json={"gene":"TP53"})
        assert download_response.status_code == 200

        # 使用文件流接收响应内容
        file_buffer = io.BytesIO()
        for chunk in download_response.iter_content(chunk_size=8192):
            if chunk:
                file_buffer.write(chunk)

        # 验证文件大小
        assert file_buffer.tell() >= 100

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-胚系突变")
    @allure.title("统计中心-胚系突变")
    def test_germline(self, res):
        """统计中心胚系突变查询"""
        germline_response = res.post_request("/prod-api/api/oseq/statistic/germline", json=DataList.germline_data)
        assert germline_response.status_code == 200
        assert germline_response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-胚系位点导出")
    @allure.title("胚系位点导出")
    def test_germline_verify_export(self, res):
        """统计中心胚系位点导出"""
        export_response = res.post_request("/prod-api/api/oseq/statistic/germline/verify/export",
                                           json=DataList.germline_verify_export_data)
        assert export_response.status_code == 200

        # 使用文件流接收响应内容
        file_buffer = io.BytesIO()
        for chunk in export_response.iter_content(chunk_size=8192):
            if chunk:
                file_buffer.write(chunk)

        # 验证文件大小
        assert file_buffer.tell() >= 100

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-胚系基因导出")
    @allure.title("胚系基因导出")
    def test_germline_gene_export(self, res):
        """统计中心胚系基因导出"""
        export_response = res.post_request("/prod-api/api/oseq/statistic/germline/gene/export",
                                           json=DataList.germline_gene_export_data)
        assert export_response.status_code == 200

        # 使用文件流接收响应内容
        file_buffer = io.BytesIO()
        for chunk in export_response.iter_content(chunk_size=8192):
            if chunk:
                file_buffer.write(chunk)

        # 验证文件大小
        assert file_buffer.tell() >= 100

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心_本地库管理")
    @allure.title("统计中心-本地库管理")
    def test_lib(self, res):
        """统计中心本地库管理"""
        lib_response = res.post_request("/prod-api/api/oseq/statistic/local/lib/medication", json=DataList.lib_data)
        assert lib_response.status_code == 200
        assert lib_response.json().get('success') == True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("统计中心-胚系解读库")
    @allure.title("胚系解读库")
    def test_germline_read(self, res):
        """统计中心胚系解读库查询"""
        germline_read_response = res.post_request("/prod-api/api/oseq/statistic/local/lib/germline/read",
                                                  json=DataList.germline_read_data)
        assert germline_read_response.status_code == 200
        assert germline_read_response.json().get('success') == True

