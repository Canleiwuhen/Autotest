class DataList:
    query_validity_manager_list = [
        {
            "case_name": "输入样本编号、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"10B00151860","zmatnr_ty":"","zsfxhfy":"否","zsample":"","zyblx_code":""}
            }
        },
        {
            "case_name": "输入样例编号、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"否","zsample":"10B00151860","zyblx_code":""}
            }
        },
        {
            "case_name": "输入客户名称、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"是","zsample":"","zyblx_code":"","kunnr":"1000000001,1000000000"}
            }
        },
        {
            "case_name": "输入产品组合、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"T002,T003","zsfxhfy":"否","zsample":"","zyblx_code":"","kunnr":""}
            }
        },
        {
            "case_name": "输入产品、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"否","zsample":"","zyblx_code":"","kunnr":"","matnr":"HW0040,GBI0606030040"}
            }
        },
        {
            "case_name": "输入样本类型、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"否","zsample":"","zyblx_code":"S020,S008,S009","kunnr":"","matnr":""}
            }
        },
        {
            "case_name": "输入项目名称、客户名称",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsample":"","zyblx_code":"","kunnr":"1000000001","matnr":"","zxmbh":"F16ZD3I1QS2480"}
            }
        },
        {
            "case_name": "输入到样日期、项目名称",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zxmbh":"F16ZD3I1QS2480","zreceiveddatenew":"20230905","zreceiveddatenewend":"20231125"}
            }
        },
        {
            "case_name": "输入是否有浮动、到样日期",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zreceiveddatenew":"20230905","zreceiveddatenewend":"20231125","zfloat":"无"}
            }
        },
        {
            "case_name": "输入预计销毁日期、是否有浮动",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zfloat":"有","zyjxhdate":"20231004","zyjxhdateend":"20241009"}
            }
        },
        {
            "case_name": "输入库存状态（入库定位）、预计销毁日期",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zyjxhdate":"20231004","zyjxhdateend":"20241009","zkc_status":"rkdw"}
            }
        },
        {
            "case_name": "输入库存状态（出库锁定）、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"否","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zkc_status":"cksd"}
            }
        },
        {
            "case_name": "输入库存状态（入库申请）、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"否","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zkc_status":"rksd"}
            }
        },
        {
            "case_name": "输入库存状态（手工入库）、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"否","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zkc_status":"sgrk"}
            }
        },
        {
            "case_name": "输入库存状态（出库）、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsfxhfy":"否","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zkc_status":"sgck"}
            }
        },
        {
            "case_name": "输入容器编码、产品组合",
            "data": {
                "task": {"zybzx":"X","zcontainer_num":"1","zmatnr_ty":"T002,T003,T004,T001","zfridge_name":""}
            }
        },
        {
            "case_name": "输入冰箱名称、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcontainer_num":"","zmatnr_ty":"","zfridge_name":"1","zsfxhfy":"否","zbox":""}
            }
        },
        {
            "case_name": "输入箱子编号、是否销毁返样",
            "data": {
                "task": {"zybzx":"X","zcontainer_num":"","zmatnr_ty":"","zfridge_name":"","zsfxhfy":"否","zbox":"1"}
            }
        },
        {
            "case_name": "输入产品组合、产品、样本类型、到样日期、是否有浮动、预计销毁日期、库存状态、是否销毁返样、容器编码、冰箱名称",
            "data": {
                "task": {"zybzx":"X","zcontainer_num":"1","zkc_status":"rkdw","zmatnr_ty":"T014,T013,T011,T003,T002,T001","zfridge_name":"1","zsfxhfy":"否","zbox":"","zyjxhdate":"20241001","zyjxhdateend":"20261119","zyblx_code":"S028,S067,S051","zfloat":"有","zreceiveddatenew":"20200929","zreceiveddatenewend":"20201120","matnr":"DX0558"}
            }
        }
    ]

    query_validity_manager_fail_list = [
        {
            "case_name": "全部查询条件为空，请再输入一个查询条件",
            "msg": "请再输入一个查询条件",
            "data": {
                "task": {"zybzx":"X"}
            }
        },
        {
            "case_name": "只输入一个查询条件，请再输入一个查询条件",
            "msg": "请再输入一个查询条件",
            "data": {
                "task": {"zybzx":"X","zcatalo":"10B00151860","zmatnr_ty":"","zsample":"","zyblx_code":""}
            }
        },
        {
            "case_name": "到样日期搜索不能超过365天",
            "msg": "到样日期搜索不能超过365天",
            "data": {
                "task": {"zybzx":"X","zcatalo":"","zmatnr_ty":"","zsample":"","zyblx_code":"","kunnr":"","matnr":"","zxmbh":"F16ZD3I1QS2480","zreceiveddatenew":"20230926","zreceiveddatenewend":"20241122"}
            }
        }
    ]
