import logging
import time

logging.basicConfig(level=logging.INFO,   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import  nonebot
from pathlib import Path
from nonebot.adapters.qq import Adapter as QQAdapter
from nonebot import  get_bot

#驱动器
# from  nonebot.drivers.httpx import Driver as HttpxDriver
# 1 初始化 NoneBot
nonebot.init()


# 2 设置驱动器 用于信息交互
driver = nonebot.get_driver()
driver.register_adapter(QQAdapter)

# 3.设置qq适配器
qq_adapter=(nonebot.get_adapter(QQAdapter.get_name()))
# qq_bot=get_bot()
# qq_bot=nonebot.get_bot("102399732")
# logging.info(f"qq_bot:{qq_bot}")
# bots=qq_adapter.bot
# print(f"bots:{bots}")
# print(f"qq_adapter:{qq_adapter}")
# 获取bot对象
# qq_bot=nonebot.get_bot("102377271") #在env文件中配置的qq机器人id
# qq_bot.send(message="hello",to_me=True)
# qq_bot=get_bot("102399732")
# print(qq_bot)
bots=nonebot.get_bots()
print(f"bots:{bots}")

# 4 在这里加载插件
# nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_plugin(Path('awesome_bot/plugins/chatbot/main.py'))
logging.info("bot启动")
# time.sleep(30)
# qq_bot = nonebot.get_bots()
# qq_bot=nonebot.get_bot("102399732")
# logging.info(f"qq_bot:{qq_bot}")
if __name__ == "__main__":
    nonebot.run()
