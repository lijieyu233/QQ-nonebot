import logging
import time
import nonebot
from core.douyinliverecorder import spider
logging.basicConfig(level=logging.INFO,   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.rule import to_me
gun_live=False
logging.info("chatbot插件加载完毕")
def is_gun_live():
    record_url = "https://www.douyu.com/12306"
    json_data = spider.get_douyu_info_data(
        url=record_url,
        # proxy_addr=proxy_address,
        cookies='')
    return  json_data['is_live']
question = on_command("命令", rule=to_me(), aliases={"question"}, priority=10, block=True)
@question.handle()
async def handle_function(args: Message = CommandArg()):
    global gun_live
    logging.info("开始执行提问命令")
    if user_content := args.extract_plain_text():
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
                        await question.send("棍神直播了,兄弟们撤 ")
                        continue
                    else:
                        gun_live = is_live
                        await question.send("电棍死了了")
                        continue








