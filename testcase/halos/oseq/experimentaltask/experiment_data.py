# -*- coding: utf-8 -*-
class DataList:
    search_data = [
        {
            "case_name": "样本编号精准搜索",
            "search_items": {"sampleNo": "25S06160003"}
        },
        {
            "case_name": "样本编号模糊搜索",
            "search_items": {"sampleNo": "111"}
        },
        {
            "case_name": "板号模糊搜索",
            "search_items": {"panelNo": "L2025"}
        }
        # {
        #     "case_name": "检测项目批量搜索",
        #     "search_items": {"projectCode": ["CNV-seq", "CS"]}
        # }
        # {
        #     "case_name": "实验状态批量搜索",
        #     "search_items": {"experimentalState": ["InDelivery", "ExperimentCompletion"]}
        # },
        # {
        #     "case_name": "组合搜索",
        #     "search_items": {"experimentalState": ["ExperimentCompletion", "InExperiment"],
        #                      "createTime": "2025-05-01,2025-09-16",
        #                      "plateCode": "S",
        #                      "poolingId": "SEQ",
        #                      "projectCode": ["CS", "NIFTY"],
        #                      "sampleNo": ["25"]}
        # }
    ]