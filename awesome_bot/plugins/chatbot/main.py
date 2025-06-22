import logging

logging.basicConfig(level=logging.INFO,   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.plugin.on import on_keyword, on, on_message

import time
from core.douyinliverecorder import spider
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot import  get_bot
async def is_enable() -> bool:
    return True
gun_live=False
logging.info("chatbot插件加载完毕")

command_help = on_command("帮助", rule=is_enable, aliases={"question"}, priority=10, block=True)
@command_help.handle()
async def handle_function(event: MessageEvent):
    message= """命令列表:
1. /直播 直播列表
2. /直播 监控列表
3. /直播 开启监控 name
4. /直播 关闭监控 name
5. /直播 给老子滚 name
6. /直播 添加监控 name live_url"""
    await command_help.finish(message)






test = on_command("test",  priority=10, block=True)
@test.handle()
async def handle_function(event: MessageEvent):
    bot = get_bot()
    await bot.call_api("send_group_msg",group_id=609302019,message="你好")
    # await  bot.send(message="test",event=event,at_sender =True)
    print(bot)


