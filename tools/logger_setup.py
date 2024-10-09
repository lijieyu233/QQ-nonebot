import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def setup_logger(log_directory='../log'):
    """
    设置日志记录器，记录日志到指定目录的文件中，且每天自动创建新的日志文件。

    :param log_directory: 日志文件存储目录
    :return: 配置好的 logger 对象
    """
    # 确保日志目录存在
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 获取当前日期并格式化为字符串
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_filename = f'subtitle_generation_{current_date}.log'  # 创建包含日期的日志文件名

    # 创建 Logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)  # 设置日志记录器的级别为 DEBUG

    # 创建文件处理器，每天轮转日志文件
    log_file_path = os.path.join(log_directory, log_filename)  # 日志文件路径
    file_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1)  # 每天午夜创建新的日志文件
    # 不设置 backupCount，以不限制备份文件数量

    # 创建 Formatter 并将其添加到 Handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将 Handler 添加到 Logger
    logger.addHandler(file_handler)

    return logger


