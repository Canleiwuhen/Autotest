class DataList:
    query_wait_outbound_list = [
        {
            "case_name": "输入产品组合",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "", "zcatalo": "", "zmatnr_ty": "T003,T002", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入产品编码",
            "data": {
                "task": {"zybzx": "X", "zmatnr_ty": "", "matnr": "DX0017,DX0016", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入样本编号",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "", "zcatalo": "24X052102761", "zmatnr_ty": "",
                         "zsjd_type": "YX", "zsample": ""}
            }
        },
        {
            "case_name": "输入样例编号",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "", "zcatalo": "", "zsample": "24X052102761", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入到样日期",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "20240301", "zcatalo": "", "zsample": "",
                         "zreceiveddateend": "20240308", "zsjd_type": "YX"}
            }
        },
        # {
        #     "case_name": "输入是否停测",
        #     "data": {
        #         "task": {"zybzx":"X","zcatalo":"","zsample":"","zsftc":"是","zsjd_type":"YX"}
        #     }
        # },
        {
            "case_name": "输入送检单号",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "INSP230000000699",
                         "zcwlx": "", "zplate_num": "", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入送检单类型",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "", "zsjdlx": "自建库",
                         "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入样本类型",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "",
                         "zcwlx": "S051,S287,S367,S379,S216,S221", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入是否捐献",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "", "zcwlx": "",
                         "zzqty": "否", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入容器小类",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "", "zcwlx": "",
                         "zrqlx": "WFX-E", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入采血管类型",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "", "zcwlx": "",
                         "ztubetype": "G牌采血管,G管", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入容器编号",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "", "zcwlx": "",
                         "zplate_num": "23SZBY01-0007", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入在自动化设备",
            "data": {
                "task": {"zybzx": "X", "zcatalo": "", "zsample": "", "zmatnr_ty": "", "zsjdid": "", "zcwlx": "",
                         "zplate_num": "", "zsfsb": "是", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "输入产品组合+产品编码+到样日期+是否停测+送检单类型+样本类型+是否捐献+容器小类+在自动化设备+样本编号+样例编号+送检单号+容器编号",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "20230620", "zcatalo": "23X062500009",
                         "zsample": "23X062500009",
                         "zreceiveddateend": "20230627", "zsftc": "否", "zmatnr_ty": "T003,T002,T007,T001",
                         "zsjdid": "INSP230000560050",
                         "zsjdlx": "自建库", "zcwlx": "S367,S051", "zrqlx": "SZBY", "zzqty": "是",
                         "zplate_num": "23SZSZBY01-7316",
                         "zsfsb": "是", "matnr": "DX1373", "zsjd_type": "YX"}
            }
        }
    ]

    query_wait_outbound_fail_list = [
        {
            "case_name": "输入不存在的样本编号，该查询无值.",
            "msg": "筛选条件没有查询到数据！",
            "data": {
                "task": {"zybzx": "X", "zreceiveddate": "", "zcatalo": "1111111", "zmatnr_ty": "", "zsjd_type": "YX"}
            }
        }
    ]

    apply_outbound_list = [
        {
            "case_name": "生产出库+直接出库",
            "sample_donate": 0,
            "data": {
                "params": {"zzzbm": "BC01", "zreson": "生产出库", "zyqyrq": "", "zghyrq": "", "lgort_t": "BC01",
                           "lgort_f": "XB39", "zydate": "", "zcmode": "0", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "外包出库+预出库",
            "sample_donate": 0,
            "data": {
                "params": {"zzzbm": "CK01", "zreson": "外包出库", "zyqyrq": "", "zghyrq": "", "lgort_t": "CK01",
                           "lgort_f": "XB39", "zydate": "2024-09-24 19:43:00", "zcmode": "1", "zsjd_type": "YX"}
            }
        },
        {
            "case_name": "销毁+直接出库",
            "sample_donate": 0,
            "data": {
                "params": {"zzzbm": "XB19", "zreson": "销毁", "zyqyrq": "", "zghyrq": "", "lgort_t": "XB19",
                           "lgort_f": "XB39", "zydate": "", "zcmode": "0", "zsjd_type": "YX"}
            }
        }
        # {
        #     "case_name": "研发出库+预出库",
        #     "sample_donate": 1,
        #     "data": {
        #         "params": {"zzzbm":"XB19","zreson":"研发出库","zyqyrq":"","zghyrq":"","lgort_t":"XB19","lgort_f":"XB39","zydate":"","zcmode":"1","zsjd_type":"YX"}
        #     }
        # },
        # {
        #     "case_name": "内部测试出库+直接出库",
        #     "sample_donate": 1,
        #     "data": {
        #         "params": {"zzzbm":"XB19","zreson":"内部测试出库","zyqyrq":"","zghyrq":"","lgort_t":"XB19","lgort_f":"XB39","zydate":"","zcmode":"0","zsjd_type":"YX"}
        #     }
        # }
    ]

    query_apply_uncheck_outbound_list = [
        {
            "case_name": "输入出库申请单号",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "", "syncdate": "", "zscdh": "OBR"}
            }
        },
        {
            "case_name": "输入样本编号",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "", "syncdate": "", "zscdh": "", "zcatalo": "1"}
            }
        },
        {
            "case_name": "输入申请部门",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "", "syncdate": "", "zscdh": "", "zcatalo": "", "zzzbm": "半成品仓"}
            }
        },
        {
            "case_name": "输入申请人",
            "data": {
                "task": {"zybzx": "X", "zzzbm": "", "zcjnam": "huxiaofeng_A020"}
            }
        },
        {
            "case_name": "输入申请日期",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "20240908", "zcjdatend": "20241008"}
            }
        },
        {
            "case_name": "输入状态",
            "data": {
                "task": {"zybzx": "X", "zreqstat_t": "已申请"}
            }
        },
        {
            "case_name": "输入出库原因",
            "data": {
                "task": {"zybzx": "X", "zreson": "生产出库"}
            }
        },
        {
            "case_name": "输入出库申请人",
            "data": {
                "task": {"zybzx": "X", "zdlvowner": "autotest1"}
            }
        },
        {
            "case_name": "输入出库日期",
            "data": {
                "task": {"zybzx": "X", "zdlvowner": "", "zdlvdate": "20240703", "zdlvdateend": "20240726"}
            }
        },
        {
            "case_name": "输入签收人",
            "data": {
                "task": {"zybzx": "X", "zsignowner": "huxiaofeng_A020"}
            }
        },
        {
            "case_name": "输入同步ZLIMS状态",
            "data": {
                "task": {"zybzx": "X", "zsignowner": "", "zlimssyncstatus": "S"}
            }
        },
        {
            "case_name": "输入同步ZLIMS日期",
            "data": {
                "task": {"zybzx": "X", "zsignowner": "", "syncdate": "20200401", "syncdateend": "20200731"}
            }
        },
        {
            "case_name": "输入出库申请单号+申请部门+申请人+申请日期+状态+出库原因+出库申请人+出库日期+签收人",
            "data": {
                "task": {"zybzx": "X", "zscdh": "OBR", "zcatalo": "", "zzzbm": "半成品仓", "zcjnam": "huxiaofeng_A020",
                         "zcjdat": "20240730", "zcjdatend": "20241022", "zreqstat_t": "已确认", "zreson": "生产出库",
                         "zdlvdate": "20240702", "zdlvdateend": "20241130", "zsignowner": "huxiaofeng_A020",
                         "zdlvowner": "huxiaofeng_A020"}
            }
        }
    ]

    query_apply_uncheck_outbound_fail_list = [
        {
            "case_name": "输入不存在的出库单号，该查询无值.",
            "msg": "该查询无值.",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "", "syncdate": "", "zscdh": "12312321"}
            }
        },
        {
            "case_name": "空搜,查询条件不能为空",
            "msg": "查询条件不能为空",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "", "syncdate": "", "zscdh": ""}
            }
        }
    ]

    delete_order_fail_list = [
        {
            "case_name": "输入不存在的申请单号，申请单号错误，请重新输入!",
            "msg": "申请单号错误，请重新输入!",
            "data": {
                "datas": [{"zscdh": "121212"}]
            }
        },
        {
            "case_name": "申请单状态不正确,申请单状态不是已申请，无法删除!",
            "msg": "申请单状态不是已申请，无法删除!",
            "data": {
                "datas": [{"zscdh": "OBR200300000060"}]
            }
        },
        {
            "case_name": "样本编号不正确,样本编号1111111111111与出入库申请单不对应，请重新输入！",
            "msg": "样本编号1111111111111与出入库申请单不对应，请重新输入！",
            "data": {
                "datas": [{"zscdh": "OBR200300000059", "zcatalo": "1111111111111"}]
            }
        },
        {
            "case_name": "样本编号不正确,只允许申请单号创建者删除申请单",
            "msg": "只允许申请单号创建者删除申请单",
            "data": {
                "datas": [{"zscdh": "OBR200300000059"}]
            }
        }
    ]

    query_uncheck_outbound_list = [
        {
            "case_name": "输入出库申请单号",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "", "zscdh": "OBR2409000"}
            }
        },
        {
            "case_name": "输入申请部门",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "", "zzzbm": "半成品仓"}
            }
        },
        {
            "case_name": "输入申请人",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "", "zcjnam": "autotest2"}
            }
        },
        {
            "case_name": "输入申请日期起",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "20240916", "zcjdatend": "", "zdlvdate": "", "zcjnam": ""}
            }
        },
        {
            "case_name": "输入申请日期止",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "20240923", "zdlvdate": "", "zcjnam": ""}
            }
        },
        {
            "case_name": "输入状态",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "", "zcjnam": "", "zreqstat_t": "已申请"}
            }
        },
        {
            "case_name": "输入出库原因",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "", "zreson": "生产出库", "zcjnam": ""}
            }
        },
        {
            "case_name": "输入出库审核人",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "", "zcjnam": "",
                         "zdlvowner": "huxiaofeng_A020", "zsignowner": ""}
            }
        },
        {
            "case_name": "输入出库日期",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "20240912", "zcjnam": "",
                         "zdlvowner": ""}
            }
        },
        {
            "case_name": "输入签收人",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "", "zcjdatend": "", "zdlvdate": "", "zcjnam": "", "zdlvowner": "",
                         "zsignowner": "huxiaofeng_A020"}
            }
        },
        {
            "case_name": "输入出库申请单号+申请日期起+申请日期止+状态+出库原因",
            "data": {
                "task": {"zybzx": "X", "zcjdat": "20230906", "zcjdatend": "20240917", "zdlvdate": "", "zreson": "生产出库",
                         "zcjnam": "", "zreqstat_t": "已申请", "zdlvowner": "", "zsignowner": "", "zjob_code": "",
                         "zscdh": "1"}
            }
        }
    ]

    query_uncheck_outbound_fail_list = [
        {
            "case_name": "全部查询条件为空，查询条件不能为空!",
            "msg": "查询条件不能为空",
            "data": {
                "task": {"zybzx": "X"}
            }
        },
        {
            "case_name": "输入不存在的出库申请单号，该查询无值.",
            "msg": "该查询无值.",
            "data": {
                "task": {"zybzx": "X", "zscdh": "1111"}
            }
        }
    ]

    query_outbound_bill_list = [
        {
            "case_name": "输入出库单号",
            "data": {
                "task": {"zybzx": "X", "zscdh": "OBR240900000228"}
            }
        },
        {
            "case_name": "输入出库日期",
            "data": {
                "task": {"zybzx": "X", "zdlvdate": "20240824", "zdlvdateend": "20240923"}
            }
        },
        {
            "case_name": "输入出库审核人",
            "data": {
                "task": {"zybzx": "X", "zdlvowner": "huxiaofeng_A020"}
            }
        },
        {
            "case_name": "输入出库单号+出库日期+出库审核人",
            "data": {
                "task": {"zybzx": "X", "zdlvowner": "huxiaofeng_A020", "zscdh": "OBR240900000219", "zjob_code": "",
                         "zdlvdate": "20240824", "zdlvdateend": "20240923"}
            }
        },
        {
            "case_name": "空搜",
            "data": {
                "task": {"zybzx": "X"}
            }
        }
    ]

    query_outbound_bill_fail_list = [
        {
            "case_name": "输入不存在的出库申请单号，该查询无值.",
            "msg": "该查询无值.",
            "data": {
                "task": {"zybzx": "X", "zscdh": "123213"}
            }
        }
    ]
