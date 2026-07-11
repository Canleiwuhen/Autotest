import pytest
import allure
import os
from utils.tools import create_sample, calculate_file_buffer
from utils.handle_excel import OperationExcel
from testcase.omicsone.samplecenter.sample_data import DataList


@pytest.mark.usefixtures("res", "res_file")
class TestRun:
    """
    该用例日常执行自动化时不执行，单纯为简化手动起分析用
    """

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("特殊功能")
    @allure.title("执行跑分析-CNVseq")
    def test_run_analys_cnvseq(self, res_file):
        """
        实现导入送检单并导入测序文件启动分析任务，简化手动造文件场景，目前模板上用的芯片号为V352404121
        :param res_file:
        :return:
        """
        # 先导入送检单数据
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        sample_base_path = os.path.join(parent_dir, 'import_sample_files')
        sample_file = os.path.join(sample_base_path, 'CNV-seq.xlsx')
        data = {"formId": '1850818129993592834'}
        # 读取送检单文件，填充或更新样本编号
        sample_file_objec = OperationExcel(file_name=sample_file, sheet_name='Sheet1')
        lines_num = sample_file_objec.get_lines()
        sample_num = lines_num - 1
        sample_list = []
        if sample_num > 0:
            for i in range(sample_num):
                sample_list.append(create_sample())
        for i in range(sample_num):
            sample_file_objec.write_value(row=i+1, col=1, value=sample_list[i])
        # 导入送检单模板数据
        response = res_file.post_request("/api/sample/excel/import", data=data, file_path=sample_file)
        assert response.status_code == 200
        assert response.json()['retInfo'] == 'success'
        assert len(response.json()['result']['success']) != 0  # 正常导入成功，返回是非空列表
        assert len(response.json()['result']['fail']) == 0  # 正常导入成功，返回是空列表

        # 再导入测序模板数据
        sequence_base_path = os.path.join(parent_dir, 'import_sequence_files')
        sequence_file = os.path.join(sequence_base_path, '测序任务导入CNV-seq.xlsx')
        # 读取测序模板文件，填充或更新样本编号
        sequence_file_object = OperationExcel(file_name=sequence_file, sheet_name='Sheet1')
        for i in range(sample_num):
            sequence_file_object.write_value(row=i+1, col=0, value=sample_list[i])
        response2 = res_file.post_request("/api/sequencing/import", file_path=sequence_file)
        assert response2.status_code == 200
        assert response2.json()['retInfo'] == 'success'
        assert len(response2.json()['result']['errorList']) == 0  # 正常导入成功，返回是空列表