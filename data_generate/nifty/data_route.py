# path1: 0:提交送检单--1:技术路线确认--2:血浆分离--3:建库--4:BMG--5:Pooling--6:单链环化--7:MakeDNB-8:上机--9:信息分析--10：数据审核
# path2: 0:提交送检单--1:技术路线确认--2:血浆分离--3:建库--4:BMG--5:Pooling--6：质检产物
# path3: 0:提交送检单--1:技术路线确认--2:血浆分离--3：重复质控品
# path4: 0:提交送检单--1:技术路线确认--2:血浆分离--3：产物补录
# path5: 0:提交送检单--1:技术路线确认--2:血浆分离--3:建库--4:BMG--5:Pooling--6:单链环化--7:MakeDNB-8:上机--9:信息分析--10：数据审核
# --11：报告生成--12：报告确认--13：报告审核--14：报告认领--15：报告复核



ROUTE = {'path1': {0: 'sumbit_sample', 1: 'technical_route_confirmation', 2: 'plasma_separation', 3: 'build_the_library', 4: 'bmg',
                   5: 'pooling', 6: 'dlhhorder', 7: 'makednb500order',8: 'sequencing',9:'information_analysis',10:'data_review'},
         'path2': {0: 'sumbit_sample', 1: 'technical_route_confirmation', 2: 'plasma_separation', 3: 'build_the_library', 4: 'bmg',
                   5: 'pooling',6: 'quality_inspection_products'},
         'path3': {0: 'sumbit_sample', 1: 'technical_route_confirmation', 2: 'plasma_separation', 3: 'repeat_controller'},
         'path4': {0: 'sumbit_sample', 1: 'technical_route_confirmation', 2: 'plasma_separation', 3: 'product_supplement'},
         'path5': {0: 'sumbit_sample', 1: 'technical_route_confirmation', 2: 'plasma_separation', 3: 'build_the_library', 4: 'bmg',
                   5: 'pooling', 6: 'dlhhorder', 7: 'makednb500order', 8: 'sequencing', 9: 'information_analysis', 10: 'data_review',
                   11: 'generate_report', 12: 'report_confirmation', 13: 'report_review', 14: 'report_claim', 15: 'report_composite'},
         'path8': {},
         'path9': {},
         'path10': {}
         }






if __name__ == '__main__':
    print(ROUTE['path1'][2])