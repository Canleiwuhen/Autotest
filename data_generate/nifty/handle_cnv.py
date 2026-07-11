import re
import math
from copy import deepcopy

from exceptiongroup import catch

from utils.logger import logger_other as logger

def handle_cnv_list(cnv_info_list: list):

    # 定义cnv_list，暂时只考虑列表中仅有一个cnv对象
    cnv_list_temp = [
        {
            "annoList": [],
            "chr": "7",
            "cnv": "dup(7:8371736-13730852)",
            "cnvBandInfo": "dup(7p21.3,5.36Mb)",
            "cnvType": "2",
            "end": "13730852",
            "filterFlag": "1",
            "length": "5",
            "start": "8371736"
        }
    ]

    result = []
    for cnv_info in cnv_info_list:

        if cnv_info["cnv_band"] and cnv_info["cnv"]:
            try:
                # 深度拷贝cnv_list_temp
                cnv_list = deepcopy(cnv_list_temp)
                # 判断cnv类型
                if str(cnv_info["cnv"]).startswith('dup'):
                    cnv_list[0]['cnvType'] = "2"
                elif str(cnv_info["cnv"]).startswith('del'):
                    cnv_list[0]['cnvType'] = "1"
                else:
                    cnv_list[0]['cnvType'] = "0"
                cnv_list[0]['cnv'] = cnv_info["cnv"]
                match_cnv = re.findall(r'\d+', cnv_info["cnv"])
                cnv_list[0]['chr'] = match_cnv[0]
                cnv_list[0]['start'] = match_cnv[1]
                cnv_list[0]['end'] = match_cnv[2]
                if "Mb" in cnv_info["cnv_band"] or "mb" in cnv_info["cnv_band"]:
                    cnv_list[0]['cnvBandInfo'] = cnv_info["cnv_band"]
                    match_cnv_length = re.search(r'(\d+\.\d+)Mb', cnv_info["cnv_band"])
                    cnv_list[0]['length'] = math.ceil(float(match_cnv_length.group(1)))
                    # 匹配染色体号
                    # match_chr = re.search(r'\((\d+)', cnv_info["cnv_band"])
                    # cnv_list[0]['chr'] = match_chr.group(1)
            except Exception as e:
                logger.error("cnv信息解析异常，请检查输入信息是否正确！")
                raise Exception(f"cnv信息解析异常，请检查输入信息：{str(cnv_info)}是否正确！ 错误原因：{e}")
        else:
            logger.info("cnv信息不完整：cnv或cnv_band缺失，默认将cnv_list置为空列表")
            cnv_list = []
        result.append(cnv_list)
    # print(str(result))
    return result


if __name__ =='__main__':
    cnv_info_list = [{"cnv_band":None,"cnv":"del(2:196925121-205206940)"},{"cnv_band":None,"cnv":None},{"cnv_band":"del(2q32.3-q33.3,8.28Mb)","cnv":None},{"cnv_band":"del(2q32.3-q33.3,8.28Mb)","cnv":"del(2:196925121-205206940)"},{"cnv_band":"del(2q32.3-q33.3,8.28Mb)-M","cnv":"del(2:196925121-205206940)-M"},{"cnv_band":"dup(13q12.12,1.72Mb)","cnv":"dup(13:23466683-25191588)"},]
    cnv_info_list = [{"cnv_band": None, "cnv": "del(2:196925121-205206940)","test13":"T13高危","test18":"T18高危","test21":"T21高危","testSex":"其它复杂异常(+++)","testAuto":"Test(常染色体)","note3":"T18;T21;T13;完全三体可能性不大，存在一定比例嵌合","note2":"完全三体可能性不大，存在一定比例嵌合", "disease":"疾病名称", "qc":"通过", "report_tag":"$2p33.1_deletion$", "product_no":"DX1331", "fetus_type":"单胎"}]
    handle_cnv_list(cnv_info_list)