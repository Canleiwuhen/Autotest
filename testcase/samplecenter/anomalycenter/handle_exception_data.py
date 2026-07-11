class DataList:
    query_except_data = [
        {
            "case_name": "无筛选条件查询所有数据",
            "task": {"zybzx": "X", "zcatalo": ""}
        },
        {
            "case_name": "按样本编号查询数据",
            "task": {"zybzx": "X", "zcatalo":"18D0000195"}
        },
        {
            "case_name": "按异常处理状态-未处理查询数据",
            "task": {"zybzx": "X", "zstatus": "01"}
        },
        {
            "case_name": "按异常处理状态-待审核查询数据",
            "task": {"zybzx": "X", "zstatus": "04"}
        },
        {
            "case_name": "按异常处理状态-已撤销查询数据",
            "task": {"zybzx": "X", "zstatus": "06"}
        },
        {
            "case_name": "按异常处理状态-已处理查询数据",
            "task": {"zybzx": "X", "zstatus": "03"}
        },
        {
            "case_name": "按登记人查询数据",
            "task": {"zybzx": "X", "zcreator": "admin"}
        },
        {
            "case_name": "按前端反馈措施-销毁查询数据",
            "task": {"zybzx": "X", "zclcs": "02"}
        },
        {
            "case_name": "按前端反馈措施-返样查询数据",
            "task": {"zybzx": "X", "zclcs": "03"}
        },
        {
            "case_name": "按前端反馈措施-补送送检单/知情同意查询数据",
            "task": {"zybzx": "X", "zclcs": "09"}
        },
        {
            "case_name": "按异常大类-物流异常查询数据",
            "task": {"zybzx": "X", "zyclx": "WL"}
        },
        {
            "case_name": "按异常大类-物流异常查询数据",
            "task": {"zybzx": "X", "zyclx": "WL"}
        },
        {
            "case_name": "按异常大类-样本异常查询数据",
            "task": {"zybzx": "X", "zyclx": "YB"}
        },
        {
            "case_name": "按异常小类-包裹异常查询数据",
            "task": {"zybzx": "X", "zycxl":"PE"}
        },
        {
            "case_name": "按异常小类-样本实物异常查询数据",
            "task": {"zybzx": "X", "zycxl": "SE"}
        },
        {
            "case_name": "按异常小类-样本信息异常查询数据",
            "task": {"zybzx": "X", "zycxl": "IE"}
        },
        {
            "case_name": "按快递单号查询数据",
            "task": {"zybzx": "X", "zexpressnumber": "PAG0000000765"}
        },
        {
            "case_name": "按到达序列号查询数据",
            "task": {"zybzx": "X", "zarrvseries": "WH1907230008"}
        },
        {
            "case_name": "按到异常单号查询数据",
            "task": {"zybzx": "X", "yc_no": "CBEXP190000000910"}
        },
        {
            "case_name": "按到送检单号查询数据",
            "task": {"zybzx": "X", "zsjdid": "INSP190000422473"}
        }
    ]

    file_data = [
        [
            [
                "序号",
                "样本编号",
                "样例编号",
                "消息",
                "备注",
                "异常处理类型",
                "异常情况",
                "异常备注",
                "处理状态",
                "到达序列号",
                "补录送检单号",
                "异常邮件类型",
                "异常邮件收件人",
                "产品",
                "产品描述",
                "省份",
                "异常附件",
                "录单人",
                "送检单类型",
                "快递单",
                "登记人",
                "登记时间",
                "处置人",
                "处置时间",
                "完结人",
                "完结时间",
                "客户单位名称",
                "国家",
                "送检单/信息单",
                "异常单"
            ],
            [
                1,
                "19B920190619006",
                "19B920190619006",
                "补送样本/备份管-快递单:32",
                "14",
                "补送样本/备份管",
                "系统中送检（信息）单填写错误/不完整",
                "",
                "待审核",
                "SZ1907250001",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "PAG0000005966",
                "LXJ_A020",
                "2019-07-25+11:05:33",
                "LXJ2",
                "2019-07-25+11:05:54",
                "",
                "",
                "",
                "",
                "INSP190000500824",
                "EXP190000000967"
            ]
        ]
    ]