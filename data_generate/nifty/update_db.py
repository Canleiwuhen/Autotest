import datetime

from dateutil.relativedelta import relativedelta
from sympy.categories.baseclasses import Class

from utils.logger import logger_other as logger
from utils.handle_db import HandleDB

# 测试环境千寻数据库配置
# chihiro_db_host = "10.227.5.153"
# chihiro_db_port = "5052"
# chihiro_db_user = "usr_chihiro"
# chihiro_db_password = "eeC227$v5"
# chihiro_db_database = "chihiro"

class UpdateDB:
    def __init__(self, handler_db):
        self.handler_db = handler_db

    def update_chihiro_db_chip_info(self, chip_id, zebra_id, start_time, seq_platform, seq_type, area_code, laboratory):
        """
        千寻数据库插入芯片信息
        :param chip_id: 芯片号
        :param zebra_id: 机器号
        :param start_time: 开始时间
        :param seq_platform: 测序平台
        :param seq_type: 测序类型
        :param area_code: 片区编码
        :param laboratory: 实验室
        :return:
        """
        is_chip_exist = False  # 芯片在千寻数据库是否存在
        is_chip_finish = None  # 如已存在，芯片状态是否为已完成
        chip_table_id = int(str(888) + str(int(datetime.datetime.now().timestamp() * 1000)))
        logger.info("machine500order：开始向千寻数据库插入{}芯片信息！", seq_platform)
        query_sql = f"select area_code, state_run from chihiro_chip where flowcell_id ='{chip_id}' and state = 1;"
        query_sql_result = self.handler_db.select(query_sql)
        if query_sql_result:
            is_chip_exist = True
            logger.info(f"machine500order：芯片号{chip_id}已存在，开始查询芯片的下机数据状态！")
            is_chip_finish = False if query_sql_result[0]["state_run"] != "finish" else True
            if is_chip_finish and query_sql_result[0]["area_code"] == area_code:
                logger.info(f"machine500order：芯片号{chip_id}的状态为已完成，无需更新！")
            elif not is_chip_finish and query_sql_result[0]["area_code"] == area_code:
                logger.warning(f"machine500order：芯片号{chip_id}的状态为未完成，请手动更新状态！")
        else:
            logger.info(f"machine500order：向千寻数据库插入芯片信息，芯片号：{chip_id}")
            insert_sql = "insert into chihiro_chip (id, area_code, sequencer_code, sequencer_sn, flowcell_id, type_run, " \
                         "laboratory, sequencing_start_time, start_machine_time,flowcell_pos, state_run) values " \
                         f"({chip_table_id}, '{area_code}', '{seq_platform}', '{zebra_id}', '{chip_id}', '{seq_type}', " \
                         f"'{laboratory}', '{start_time}', '{start_time}', 'A', 'sequencing');"
            if self.handler_db.execute(insert_sql):
                finish_time = (datetime.datetime.now() + relativedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                update_sql = f"update chihiro_chip set end_machine_time ='{finish_time}', state_run ='finish' where flowcell_id ='{chip_id}';"
                self.handler_db.execute(update_sql)
            else:
                logger.error("{}:芯片信息插入异常，检查数据库连接配置是否正确", chip_id)
            if not query_sql_result:
                logger.info("machine500order：向千寻数据库插入{}芯片信息成功！芯片号：{}", seq_platform, chip_id)
        self.handler_db.close_database()
        return is_chip_exist, is_chip_finish