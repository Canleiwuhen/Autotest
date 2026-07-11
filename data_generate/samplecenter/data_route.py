# path1: 0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:新增容器--5:医学到样定位（新）--6:出库申请--7:出库审核--8:接收确认--9:入库申请--10:入库审核
# path2: 0:包裹补录--1:医学拆包
# path3: 0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:新增容器--5:医学到样定位（新））--6:出库申请--7:出库审核--8:接收确认
# path4: 0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:新增容器--5:医学到样定位（新）--6:医学信息审核
# path5: 0:MYBGI录入送检单--1:MYBGI物流寄送--2:包裹接收--3:医学拆包--4:样本批量接收

# path6: 0:MYBGI录入送检单--1:包裹接收补录--2:医学拆包--3:新增容器--4:医学到样定位（新）--5:出库申请--6:出库审核--7:接收确认--8:入库申请--9:入库审核
# path7：0:包裹接收--1:医学拆包--2:无单样本添加--3:MYBGI补录入送检单--4:无单自动到样--5:医学信息审核
# path8：0:包裹接收--1:医学拆包--2:无单样本添加--3:MYBGI补录入送检单--4:无单自动到样--5:出库申请--6:出库审核--7:接收确认
# path9：0:包裹接收--1:医学拆包--2:无单样本添加--3:MYBGI补录入送检单--4:无单自动到样--5:出库申请--6:出库审核--7:入库申请--8:入库审核
# path10：0:包裹接收--1:医学拆包--2:无单样本添加--3:MYBGI补录入送检单--4:样本批量接收


ROUTE = {'path1': {0: 'sumbit_sample', 1: 'send_package', 2: 'receive_package', 3: 'unpack', 4: 'create_container',
                   5: 'locate_position', 6: 'outbound_apply', 7: 'outbound_audit', 8:'receipt_confirmation', 9: 'inbound_apply',10: 'inbound_audit'},
         'path2': {0: 'replenish_record', 1: 'unpack'},
         'path3': {0: 'sumbit_sample', 1: 'send_package', 2: 'receive_package', 3: 'unpack', 4: 'create_container',
                   5: 'locate_position', 6: 'outbound_apply', 7: 'outbound_audit',8: 'receipt_confirmation'},
         'path4': {0: 'sumbit_sample', 1: 'send_package', 2: 'receive_package', 3: 'unpack', 4: 'create_container',
                   5: 'locate_position', 6: 'medical_info_audit' },
         'path5': {0: 'sumbit_sample', 1: 'send_package', 2: 'receive_package', 3: 'unpack', 4: 'sample_batch_receive'},
         'path6': {0: 'sumbit_sample', 1: 'replenish_record', 2: 'unpack', 3: 'create_container', 4: 'locate_position',
                   5: 'outbound_apply', 6: 'outbound_audit', 7:'receipt_confirmation', 8: 'inbound_apply',9: 'inbound_audit'},
         'path7': {},
         'path8': {},
         'path9': {},
         'path10': {}
         }






if __name__ == '__main__':
    print(ROUTE['path1'][2])