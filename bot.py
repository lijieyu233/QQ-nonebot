import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import  nonebot
from nonebot.adapters.onebot.v11 import  Adapter

# 1.初始化nonebot
nonebot.init()


# 2 设置驱动器 用于信息交互
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 3.设置qq适配器
nonebot.load_plugin(Path('awesome_bot/plugins/chatbot/main.py'))
nonebot.load_plugin(Path('awesome_bot/plugins/live_monitor/bot.py'))
logging.info("bot启动")
# time.sleep(30)
# qq_bot = nonebot.get_bots()
# qq_bot=nonebot.get_bot("102399732")
# logging.info(f"qq_bot:{qq_bot}")
nonebot.run()
