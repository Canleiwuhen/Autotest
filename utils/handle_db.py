# -*-coding:utf-8-*-
import pymysql

from utils.logger import logger_other as logger


class HandleDB:
    __db = None

    def __init__(self, host, port, user, password, database, charset=None):
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        if charset:
            self.charset = charset
        else:
            self.charset = "utf8"
        self.cur = self.connection_database()

    def __del__(self):
        if self.__db is not None:
            self.__db.close()

    def connection_database(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=int(self.port), user=self.user,
                password=self.password, database=self.database, charset=self.charset)
        except Exception as e:
            logger.error("connectDatabase failed:{}", e)
            return False
        logger.info("连接数据库成功！")
        return self.conn.cursor(pymysql.cursors.DictCursor)

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql):
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql)
                self.conn.commit()
        except:
            logger.error("execute failed: " + sql)
            self.close_database()
            return False
        return True

    # 用来查询表数据
    def select(self, sql):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            logger.info("select success：" + sql)
            self.conn.commit()
            return result
        except Exception as e:
            logger.error("select failed：" + sql)
            logger.error(e)
            return e

    # 关闭数据库
    def close_database(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        logger.info("数据库连接已关闭！")
        return True


if __name__ == "__main__":
    handledb = HandleDB("sunburst")
    # sql = "select sb.slide_id ,sb.lane_no ,sb.barcode_no from sequence_slide ss , sequence_barcode sb " \
    #       "where ss.slide_id = sb.slide_id and ss.stage_type <> 60 and sb.qc_status = 'POLLUTED' and ss.area_code in ('WH','HK','TJ') " \
    #       "order by ss.seq_end_time desc limit 1;"
    # result = handledb.select(sql)
    # print(result)
