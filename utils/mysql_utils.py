import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB

from utils import config

# 数据库配置
host = config.host
port = config.port
user = config.user
password = config.password
database = config.database


class MySQLConnectionPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnectionPool, cls).__new__(cls)
            cls._instance.pool = PooledDB(
                creator=pymysql,
                mincached=1,  # 最小连接数
                maxconnections=2,  # 最大连接数
                blocking=True,  #
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
        return cls._instance

    # 获取连接
    def get_conn(self):
        return self._instance.pool.connection()


class MysqlClient:
    @staticmethod
    def get_conn():
        return MySQLConnectionPool().get_conn()

    @staticmethod
    def execute(sql, args=None):
        with MysqlClient.get_conn() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 执行SQL语句
                cursor.execute(sql, args)

                # 智能判断语句类型
                if sql.strip().upper().startswith(('SELECT', 'SHOW', 'DESC')):
                    # 查询语句：返回结果集
                    return cursor.fetchall()
                else:
                    # 修改语句：提交事务并返回影响行数
                    conn.commit()
                    return cursor.rowcount




    # 直播监控相关
    @staticmethod
    def fetch_monitor_liver():
        """
        查询所有正在监控的直播
        :return:
        """
        sql = "SELECT * FROM monitor_liver where monitor_state=1"
        return MysqlClient.execute(sql)

    @staticmethod
    def fetch_all_liver():
        """
        查询所有直播
        :return:
        """
        sql = "select * from monitor_liver"
        return MysqlClient.execute(sql)

    @staticmethod
    def set_monitor_state(name, monitor_state):
        """
       设置监控状态
       :param id:
       :param monitor_state:
       :return:
       """

        sql = "UPDATE monitor_liver SET monitor_state = %s WHERE name = %s"
        args = (monitor_state, name)
        return MysqlClient.execute(sql, args)


    @staticmethod
    def set_live_stage(id, live_state):
        sql = "UPDATE monitor_liver SET live_state = %s WHERE id = %s"
        args = (live_state, id)
        return MysqlClient.execute(sql, args)


    @staticmethod
    def add_monitor_liver(name, live_url):
        sql = "INSERT INTO monitor_liver (name,live_url) VALUES (%s,%s)"
        return MysqlClient.execute(sql, (name, live_url))


    @staticmethod
    def delete_monitor_liver(name):
        """
        删除监控
        :param name:
        :return:
        """
        sql = "delete  from monitor_liver where name = %s"
        return MysqlClient.execute(sql, (name,))

    # 提示词
    @staticmethod
    def get_prompt_text_by_name(name):
        sql = "SELECT * FROM prompt_template where name = %s"
        return MysqlClient.execute(sql, (name,))[0]
if __name__ == '__main__':
    # print(MysqlClient.fetch_monitor_liver())
    # print(MysqlClient.set_live_stage(1, 1))
    print(MysqlClient.get_prompt_text_by_name("一猫人机器人"))