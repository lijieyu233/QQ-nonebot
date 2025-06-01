import asyncio
import logging
from datetime import datetime

from awesome_bot.plugins.live_monitor.test import is_liver_living

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
from nonebot.params import CommandArg
from nonebot.adapters import Message
import nonebot
from nonebot import require
from nonebot.plugin.on import on_command
from utils.mysql_utils import MysqlClient
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

driver = nonebot.get_driver()

# 查询直播
live_query = on_command("直播", priority=5, block=True)


@live_query.handle()
async def handle_function(args: Message = CommandArg()):
    if user_content := args.extract_plain_text():

        if "直播列表" == user_content:
            message_living = "正在直播中:\n"
            message_not_living = "休息中:\n"
            livers = MysqlClient.fetch_all_liver()
            for live in livers:
                if live['live_state'] == 1:
                    message_living += f"   {live['id']},{live['name']} 直播间 {live['live_url']}\n"
                else:
                    message_not_living += f"   {live['id']},{live['name']} 休息中 {live['live_url']}\n"
            await   live_query.finish(message_living + message_not_living)
        if "添加监控" in  user_content:
            params= user_content.split()
            logging.info(params)
            rows=MysqlClient.add_monitor_liver(params[2],params[3])
            if rows:
                await live_query.finish("添加成功")
            else:
                await live_query.finish("添加失败")
        if "监控列表" in user_content:
            message_monitoring = "正在监控中:\n"
            message_not_monitoring = "未监控:\n"
            livers = MysqlClient.fetch_all_liver()
            for live in livers:
                if live['monitor_state'] == 1:
                    message_monitoring += f"   {live['id']},{live['name']} 直播间 {live['live_url']}\n"
                else:
                    message_not_monitoring += f"   {live['id']},{live['name']} 直播间 {live['live_url']}\n"
            await live_query.finish(message_monitoring + message_not_monitoring)

        if "开启监控" in user_content:
            params = user_content.split()
            logging.info(params)
            rows = MysqlClient.set_monitor_state(params[1], 1)
            if rows:
                await live_query.finish("开启成功")
            else:
                await live_query.finish("开启失败")
        if "关闭监控" in user_content:
            params = user_content.split()
            rows = MysqlClient.set_monitor_state(params[1], 0)
            if rows:
                await live_query.finish("关闭成功")
            else:
                await live_query.finish("关闭失败")
        if "给老子滚" in user_content:
            params = user_content.split()
            logging.info(params)
            rows = MysqlClient.delete_monitor_liver(params[1])
            if rows:
                await live_query.finish("删除成功")
            else:
                await live_query.finish("删除失败")


async def monitor_diangun():
    bot = nonebot.get_bot()
    await bot.call_api("send_group_msg", group_id=609302019, message="监控开始")
    while True:
        livers = MysqlClient.fetch_monitor_liver()
        for live in livers:
            id = live['id']  # id
            live_url = live['live_url']  # 直播间号
            live_state = live['live_state']  # 历史直播状态
            is_live = is_liver_living(id, live_url)  # 当前直播状态
            open_message = live.get('open_message')
            if not open_message:
                open_message = f"{live['name']} 开始直播了"
            close_message = live.get('close_message')
            if not close_message:
                close_message = f"{live['name']} 直播已结束"

            if live_state != is_live:  # 直播状态改变
                MysqlClient.set_live_stage(id, is_live)  # 更新数据库
                if is_live:
                    await bot.call_api("send_group_msg", group_id=609302019, message=open_message)
                else:
                    await bot.call_api("send_group_msg", group_id=609302019, message=close_message)
        await asyncio.sleep(60)


@driver.on_bot_connect
async def start_monitor():
    pass
    scheduler.add_job(monitor_diangun, trigger="date", run_date=datetime.now(), id='gun_live_monitor')
