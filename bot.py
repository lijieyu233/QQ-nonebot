import  nonebot
from pathlib import Path
from  nonebot.adapters.console import Adapter as ConsoleAdapter
from nonebot.adapters.qq import Adapter as QQAdapter

from tools.logger_setup import setup_logger

#驱动器
# from  nonebot.drivers.httpx import Driver as HttpxDriver
# 初始化 NoneBot
logger=setup_logger()
nonebot.init()


# 注册适配器
driver = nonebot.get_driver()
# driver.register_adapter(ConsoleAdapter)
driver.register_adapter(QQAdapter)
#获取已经注册适配器
qq_adapter=(nonebot.get_adapter(QQAdapter.get_name()))
#获取bot对象
# qq_bot=nonebot.get_bot("102377271") #在env文件中配置的qq机器人id
bots=nonebot.get_bots()

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
# nonebot.load_plugin("awesome_bot/plugins/question/__init__.py")  # 第三方插件
nonebot.load_plugins("awesome_bot/plugins/question")  # 本地插件
# nonebot.load_plugins("awesome_bot/plugins/CloseAI")  # 本地插件
# nonebot.load_plugins('awesome_bot/plugins/CloseAi')
nonebot.load_plugin(Path('./awesome_bot/plugins/CloseAi/__init__.py'))
logger.info("bot启动")
if __name__ == "__main__":
    nonebot.run()