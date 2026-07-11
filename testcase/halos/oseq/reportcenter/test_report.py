# -*- coding: utf-8 -*-
import pytest
import allure
import io
from testcase.halos.oseq.reportcenter.report_data import DataList
from testcase.halos.oseq.reportcenter.conftest import extract_records
from utils.tools import calculate_file_buffer


@pytest.mark.usefixtures("res")
class TestReport:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-查询")
    @allure.title("{data[case_name]}")
    @pytest.mark.parametrize("data", DataList.search_data)
    def test_search(self, res, data):
        tmp = data['search_items']
        # 处理可调用值（如lambda函数）
        processed_items = {k: v() if callable(v) else v for k, v in tmp.items()}
        json_data = {
            "page": 1,
            "size": 200
        }
        json_data.update(processed_items)
        response = res.post_request("/prod-api/api/oseq/report/page", json=json_data)
        assert response.status_code == 200
        assert response.json().get('success') == True

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-审核")
    @allure.title("审核报告")
    def test_audit(self, res):
        """查询auditStatus=1的样本，通过审核接口将状态改为2，只审核一个样本"""
        # 查询可审核样本
        query_response = res.post_request("/prod-api/api/oseq/report/page",
                                          json={"auditStatus": 1, "page": 1, "size": 10})
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 提取样本ID
        records = extract_records(query_response.json())
        if not records:
            pytest.skip("没有可审核的样本")

        sample_id = records[0].get('id') or records[0].get('reportId') or records[0].get('sampleId')
        if not sample_id:
            pytest.skip("未找到样本ID")

        # 审核通过
        audit_response = res.post_request("/prod-api/api/oseq/report/audit",
                                          json={"ids": [sample_id], "auditStatus": 2, "auditRemark": ""})
        assert audit_response.status_code == 200
        assert audit_response.json().get('success') == True

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-下载PDF")
    @allure.title("下载PDF")
    def test_download(self, res):
        """查询reportType=3的样本，下载PDF"""
        # 查询reportType=3的样本
        query_response = res.post_request("/prod-api/api/oseq/report/page",
                                          json={"reportType": 3, "page": 1, "size": 10})
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 提取样本ID
        records = extract_records(query_response.json())
        if not records:
            pytest.skip("没有可下载的样本")

        sample_id = records[0].get('id')
        if not sample_id:
            pytest.skip("未找到样本ID")

        # POST请求下载PDF，使用文件流接收响应
        download_response = res.post_request("/prod-api/api/oseq/report/download/pdf",
                                             json={"ids": [sample_id]})
        assert download_response.status_code == 200
        
        # 使用文件流接收响应内容
        file_buffer = io.BytesIO()
        for chunk in download_response.iter_content(chunk_size=8192):
            if chunk:
                if file_buffer.tell() == 0:  # 验证第一个chunk是否为PDF文件头
                    assert chunk[:4].decode('latin-1', errors='ignore').startswith('%PDF')
                file_buffer.write(chunk)
        
        # 验证文件大小
        assert file_buffer.tell() >= 100

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-预览报告")
    @allure.title("预览报告")
    def test_preview(self, res):
        """查询reportType=3的样本，预览PDF"""
        # 查询reportType=3的样本
        query_response = res.post_request("/prod-api/api/oseq/report/page",
                                          json={"reportType": 3, "page": 1, "size": 10})
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 提取样本ID
        records = extract_records(query_response.json())
        if not records:
            pytest.skip("没有可预览的样本")

        sample_id = records[0].get('id')
        if not sample_id:
            pytest.skip("未找到样本ID")

        # GET请求预览PDF，使用文件流接收响应
        preview_response = res.get_request(f"/prod-api/api/oseq/report/preview/{sample_id}")
        assert preview_response.status_code == 200
        
        # 使用文件流接收响应内容
        file_buffer = io.BytesIO()
        for chunk in preview_response.iter_content(chunk_size=8192):
            if chunk:
                if file_buffer.tell() == 0:  # 验证第一个chunk是否为PDF文件头
                    assert chunk[:4].decode('latin-1', errors='ignore').startswith('%PDF')
                file_buffer.write(chunk)
        
        # 验证文件大小
        assert file_buffer.tell() >= 100

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-重新生成报告")
    @allure.title("重新生成报告")
    def test_regenerate(self, res):
        """查询reportType=3或4的样本，重新生成报告"""
        # 查询reportType=3或4的样本
        sample_id = None
        for report_type in [3, 4]:
            query_response = res.post_request("/prod-api/api/oseq/report/page",
                                              json={"reportType": report_type, "page": 1, "size": 10})
            assert query_response.status_code == 200
            assert query_response.json().get('success') == True

            # 提取样本ID
            records = extract_records(query_response.json())
            if records:
                sample_id = records[0].get('id')
                if sample_id:
                    break
        
        if not sample_id:
            pytest.skip("没有可重新生成的样本（reportType=3或4）")
        
        # POST请求重新生成报告
        regenerate_response = res.post_request("/prod-api/api/oseq/report/regenerate",
                                              json={"ids": [sample_id]})
        assert regenerate_response.status_code == 200
        assert regenerate_response.json().get('success') == True

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-推送报告")
    @allure.title("推送报告")
    def test_push(self, res):
        """查询auditStatus=2的样本，推送报告"""
        # 查询auditStatus=2的样本
        query_response = res.post_request("/prod-api/api/oseq/report/page",
                                          json={"auditStatus": 2, "page": 1, "size": 10})
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 提取样本ID
        records = extract_records(query_response.json())
        if not records:
            pytest.skip("没有可推送的样本（auditStatus=2）")

        sample_id = records[0].get('id')
        if not sample_id:
            pytest.skip("未找到样本ID")
        
        # POST请求推送报告
        push_response = res.post_request("/prod-api/api/oseq/peta/push",
                                         json={"ids": [sample_id], "pushType": "pdf"})
        assert push_response.status_code == 200
        assert push_response.json().get('success') == True

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-回退报告")
    @allure.title("回退报告")
    def test_reinterpretation(self, res):
        """查询审核状态为1的样本（未审核），回退报告"""
        # 查询审核状态为1的样本（已审核的报告不能回退）
        query_response = res.post_request("/prod-api/api/oseq/report/page",
                                          json={"auditStatus": 1, "page": 1, "size": 10})
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 提取样本ID
        records = extract_records(query_response.json())
        if not records:
            pytest.skip("没有可回退的样本（auditStatus=1）")

        sample_id = records[0].get('id')
        if not sample_id:
            pytest.skip("未找到样本ID")
        
        # POST请求回退报告
        reinterpretation_response = res.post_request("/prod-api/api/oseq/report/reInterpretation",
                                                     json={"ids": [sample_id]})
        assert reinterpretation_response.status_code == 200
        assert reinterpretation_response.json().get('success') == True

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("解读中心-全量结果导出")
    @allure.title("全量结果导出")
    def test_export(self, res):
        """获取最近的样本ID，导出全量结果"""
        # 查询最近的样本
        query_response = res.post_request("/prod-api/api/oseq/report/page",
                                          json={"page": 1, "size": 10})
        assert query_response.status_code == 200
        assert query_response.json().get('success') == True

        # 提取样本ID（取第一个，即最近的）
        records = extract_records(query_response.json())
        if not records:
            pytest.skip("没有可导出的样本")

        sample_id = records[0].get('id')
        if not sample_id:
            pytest.skip("未找到样本ID")
        
        # POST请求导出全量结果（传参格式为数组）
        export_response = res.post_request("/prod-api/api/oseq/report/all/results/export",
                                           json=[sample_id])
        assert export_response.status_code == 200