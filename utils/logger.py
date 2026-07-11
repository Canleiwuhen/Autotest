from loguru import logger
import os
import time
from utils.handle_yaml import GetConfig

# 获取日志文件根目录
base_path = GetConfig(configname="sys_config.yaml").get_key(key='log_path')
# base_path = '/opt/local/log/apiforward/'
if os.path.exists(base_path):
    log_path = base_path
else:
    log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../log/')

# 定制日志-工具日志utils
time = time.strftime('%Y-%m-%d')
log_file_tool = log_path + time + "-tool.log"
logger.add(log_file_tool,
           rotation='00:00',  # 每天0点创建一个log文件
           compression='zip',  # 配置文件的压缩格式，以zip文件格式保存
           encoding='utf_8',  # 编码格式用‘utf-8'
           retention=7,  # 日志保存7份
           filter=lambda record: record["extra"]["name"] == "tool_log"
           )
logger_t = logger.bind(name="tool_log")

# 定制日志-造数工具日志data_generate样本中心系统日志，其他系统需要相应增加定制代码
log_file_dg = log_path + time +"-samplecenter-dg.log"
logger.add(log_file_dg,
           rotation='00:00',
           compression='zip',
           encoding='utf_8',
           retention=7,
           filter=lambda record: record["extra"]["name"] == "samplecenter_dg_log"
           )
logger_samplecenter_dg = logger.bind(name="samplecenter_dg_log")

# 定制日志-造数工具日志data_generateNIFTY系统日志，其他系统需要相应增加定制代码
log_file_dg = log_path + time +"-nifty-dg.log"
logger.add(log_file_dg,
           rotation='00:00',
           compression='zip',
           encoding='utf_8',
           retention=7,
           filter=lambda record: record["extra"]["name"] == "nifty_dg_log"
           )
logger_nifty_dg = logger.bind(name="nifty_dg_log")

# 定制日志-其他日志
log_file_other = log_path + time + "-other.log"
logger.add(log_file_other,
           rotation='00:00',
           compression='zip',
           encoding='utf_8',
           retention=7,
           filter=lambda record: record["extra"]["name"] == "other_log"
           )
logger_other = logger.bind(name="other_log")



if __name__ == '__main__':
    logger.info("业务日志:{}", "info")
    logger.error("业务日志:{}", "error")
    logger.debug("业务日志")

