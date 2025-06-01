import logging
import sys

logging.basicConfig(level=logging.INFO,   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.plugin.on import on_keyword, on, on_message

import time
import nonebot
from core.douyinliverecorder import spider
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.rule import to_me, keyword, command
from nonebot import  get_bot
async def is_enable() -> bool:
    return True
gun_live=False
logging.info("chatbot插件加载完毕")
def is_gun_live():
    record_url = "https://www.douyu.com/12306"
    json_data = spider.get_douyu_info_data(
        url=record_url,
        # proxy_addr=proxy_address,
        cookies='')
    return  json_data['is_live']
command_help = on_command("帮助", rule=is_enable, aliases={"question"}, priority=10, block=True)
@command_help.handle()
async def handle_function(event: MessageEvent):
    message= """命令列表:
1. /直播 直播列表
2. /直播 监控列表
3. /直播 开启监控 name
4. /直播 关闭监控 name
5. /直播 给老子滚 name"""
    await command_help.finish(message)














question = on_command("命令", rule=is_enable, aliases={"question"}, priority=10, block=True)
@question.handle()
async def handle_function(args: Message = CommandArg()):
    global gun_live
    logging.info("开始执行提问命令")
    if user_content := args.extract_plain_text(): # 获取结果赋值 并判断非空
        logging.info(f"user_content:{user_content}")
        if "电棍还活着吗" in user_content:
            record_url = "https://www.douyu.com/12306"
            json_data = spider.get_douyu_info_data(
                url=record_url,
                # proxy_addr=proxy_address,
                cookies='')
            is_live = json_data['is_live']
            if is_live:
                await question.finish("电棍还活着")
            else:
                await question.finish("电棍没活了")
        if "启动监控" in user_content:
            await question.send("启动监控")
            while True:
                is_live=is_gun_live()
                if is_live ==gun_live:
                    time.sleep(60)
                    continue
                else:
                    if is_live:
                        gun_live=is_live
                        await question.send("报告同志们一个好消息: 棍神直播了")
                        continue
                    else:
                        gun_live = is_live
                        await question.send("电棍死了了")
                        continue


call_name = on_keyword(keywords={"一猫人", "小王同志"},  priority=100, block=True)
@call_name.handle()
async def handle_function():
    logging.info("开始执行test命令")
    print("开始执行tst命令")
    await call_name.finish("test")


test = on_command("test",  priority=10, block=True)
@test.handle()
async def handle_function(event: MessageEvent):
    bot = get_bot()
    await bot.call_api("send_group_msg",group_id=609302019,message="你好")
    # await  bot.send(message="test",event=event,at_sender =True)
    print(bot)


