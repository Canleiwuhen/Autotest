# -*- coding: utf-8 -*-


def extract_records(response_json):
    """
    从响应JSON中提取records列表
    支持多种响应格式：data.records, result.rows, records, rows
    :param response_json: 响应JSON对象
    :return: records列表
    """
    return (response_json.get('data', {}).get('records') or
            response_json.get('result', {}).get('rows') or
            response_json.get('records') or
            response_json.get('rows') or [])