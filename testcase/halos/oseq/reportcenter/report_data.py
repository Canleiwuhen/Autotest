# -*- coding: utf-8 -*-
from datetime import datetime, time

class DataList:
    search_data = [
        {
            "case_name": "任务编号精准搜索",
            "search_items": {"batchNoFuzzy": "R250929000837"}
        },
        {
            "case_name": "任务编号模糊搜索",
            "search_items": {"batchNoFuzzy": "11"}
        },
        {
            "case_name": "样本编号精确搜索",
            "search_items": {"sampleIdFuzzy": "25DSP53423233"}
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleIdFuzzy": "25D"}
        },
        {
            "case_name": "芯片ID搜索",
            "search_items": {"slideNoFuzzy": "V35"}
        },
        {
            "case_name": "产品套餐精准搜索",
            "search_items": {"productNo": "DX196MC"}
        },
        {
            "case_name": "肿瘤类型搜索",
            "search_items": {"tumorType": 106}
        },
        {
            "case_name": "原样本编号精确搜索",
            "search_items": {"oldSampleNumFuzzy": "25B0115004"}
        },
        {
            "case_name": "原样本编号精确搜索",
            "search_items": {"oldSampleNumFuzzy": "25B0"}
        },
        {
            "case_name": "组合搜索",
            "search_items": {"batchNoFuzzy": "R251231000852", "sampleIdFuzzy": "25DSP53423233", "slideNoFuzzy": "V350266219",
                             "productNo": "DX196MC", "tumorType": 106, "oldSampleNumFuzzy": "25B0115004"}
        },
        {
            "case_name": "报告日期搜索",
            "search_items": {
                "sampleIdFuzzy": "11",
                "batchNoFuzzy": "22",
                "productNo": "DX0503",
                "tumorType": 106,
                "reportCreateTimeCollection": lambda: _get_current_date_timestamps(),
                "auditStatus": 1,
                "oldSampleNumFuzzy": "111",
                "report_date": lambda: datetime.now().strftime("%Y-%m-%d"),
                "page": 1,
                "size": 100
            }
        }
    ]


def _get_current_date_timestamps():
    """获取当前日期的开始和结束时间戳（毫秒）"""
    now = datetime.now()
    start_of_day = datetime.combine(now.date(), time.min)
    end_of_day = datetime.combine(now.date(), time.max)
    start_timestamp = int(start_of_day.timestamp() * 1000)
    end_timestamp = int(end_of_day.timestamp() * 1000)
    return f"{start_timestamp},{end_timestamp}"
