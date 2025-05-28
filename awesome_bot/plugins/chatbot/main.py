import logging
import time

import nonebot

from core.douyinliverecorder import spider

logging.basicConfig(level=logging.INFO,   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import os
import uuid
from nonebot import on_command
from nonebot.adapters.qq import MessageSegment
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.rule import to_me
from openai import OpenAI
import sqlite3

# conn = sqlite3.connect(get_absolute_path_from_script(__file__, '../../../asset/nonebot.db'))
# cursor = conn.cursor()
current_model = 2  # 当前使用的模型默认为小王


# def my_openai_call(apikey="sk-NPTWOw0zNXh7iMCQ5jsYve1e9LFGcli6DM4R0K0LWMU7Yaht",
#                    model="gpt-4o-mini-2024-07-18",
#                    user_content="如何做西红柿炖牛腩？",
#                    system_content=None):
#     print("apikey:" + apikey)
#     print("model:" + model)
#     print("user_content:" + user_content)
#     print("system_content:" + str(system_content))
#     client = OpenAI(
#         # This is the default and can be omitted
#         base_url='https://api.openai-proxy.org/v1',
#         api_key=apikey,
#     )
#     if system_content is not None and len(system_content.strip()):
#         messages = [
#             {'role': 'system', 'content': system_content},
#             {'role': 'user', 'content': user_content}
#         ]
#     else:
#         messages = [
#             {'role': 'user', 'content': user_content}
#         ]
#
#     chat_completion = client.chat.completions.create(
#         messages=messages,
#         model=model,
#     )
#     logging.info("Openai model inference done.")
#     print("chatgpt返回信息:" + chat_completion.choices[0].message.json())
#     return chat_completion.choices[0].message.content

gun_live=False

logging.info("chatbot插件加载完毕")

def is_gun_live():
    record_url = "https://www.douyu.com/12306"
    json_data = spider.get_douyu_info_data(
        url=record_url,
        # proxy_addr=proxy_address,
        cookies='')
    return  json_data['is_live']

# 注册一个名为"提问"的命令
question = on_command("命令", rule=to_me(), aliases={"question"}, priority=10, block=True)
# question.finish("你好")


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

                # record_url = "https://www.douyu.com/12306"
                # json_data = spider.get_douyu_info_data(
                #     url=record_url,
                #     # proxy_addr=proxy_address,
                #     cookies='')
                # is_live = json_data['is_live']
                # if is_live:
                #     await question.send("棍神直播了,兄弟们撤 ")
                # else:
                #     await question.send("电棍没活了")
                #     pass
                # time.sleep(1)
                    # await question.finish("电棍没活了")
            # qq_bot=nonebot.get_bot("102399732")







# 查看
# 注册一个名为"当前模型查看的命令 "，匹配"当前模型查看"、"view"、"current_model"三个关键词，优先级为10，阻止
view = on_command("当前模型", rule=to_me(), aliases={"current"}, priority=10, block=True)


# @view.handle()
# async def handle_view_function(args: Message = CommandArg()):
#     logging.info("开始执行模型查看命令")
#     model_name = Mysqlite.get_model_name(current_model)
#     await view.finish(f"当前为{current_model}号模型:{model_name}")


# 选择
# 注册一个名为'模型选择的命令 '，匹配"模型选择"、"select"、"选择"三个关键词，优先级为10，阻止
select = on_command("模型选择", rule=to_me(), aliases={"select", "选择"}, priority=10, block=True)


# @select.handle()
# async def handle_select_function(args: Message = CommandArg()):
#     logging.info("开始执行模型选择命令")
#     if model_id := args.extract_plain_text():
#         is_existed = Mysqlite.is_model_exist(model_id)
#         if is_existed:
#             global current_model
#             current_model= model_id


# 删除
# 注册一个名为"模型删除的命令 "，匹配"模型删除"、"delete"、"删除"三个关键词，优先级为10，阻止
delete = on_command("模型删除", rule=to_me(), aliases={"delete", "删除"}, priority=1, block=True)


# @delete.handle()
# async def handle_delete_function(args: Message = CommandArg()):
#     logging.info("开始执行模型删除命令")
#     if name := args.extract_plain_text():
#         if name == "默认模型":
#             await delete.finish("默认模型无法删除")
#         elif name == Mysqlite.get_model_name(current_model):
#             await delete.finish("当前模型无法删除")
#         else:
#             if Mysqlite.delete_model(name):
#                 await delete.finish(f"{name}模型删除成功")
#             else:
#                 await delete.finish(f"{name}模型不存在")

        # 获取当前脚本所在的目录
        # 构建文件的绝对路径


# 列表
# 注册一个名为模型列表 的命令，匹配"模型列表"、"list"、"列表"三个关键词，优先级为1，阻止
model_list = on_command("模型列表", rule=to_me(), aliases={"list", "列表"}, priority=1, block=True)


# @model_list.handle()
# async def handle_delete_function(args: Message = CommandArg()):
#     logging.info("开始执行模型列表命令")
#     models=Mysqlite.list_models()
#     await model_list.finish(f"当前模型列表:\n{models}")
#


# 查看模型
# 注册一个名为"查看模型"的命令，匹配"查看模型"、"view_model"、"查看"三个关键词，优先级为1，
view_model = on_command("查看模型", rule=to_me(), aliases={"view", "查看"}, priority=1, block=True)


# @view_model.handle()
# async def handle_view_model_function(args: Message = CommandArg()):
#     logging.info("开始执行查看模型命令")
#     name = args.extract_plain_text()
#     if name:
#         prompt_text=Mysqlite.get_prompt_text_by_name(name)
#         logging.info(prompt_text)
#         image_path=f'./{uuid.uuid4()}.png'
#         # output_files = [f"output_image.png"]
#         # output_files = [f"{image_path}"]
#         output_file = "output_image.png"  # 修改为 PNG 格式以确保兼容性
#         url=markdown_to_images(prompt_text,output_file)
#         image_message = MessageSegment.image(url)
#         # await view_model.finish(f"{name}模型的prompt文本是:\n{prompt_text}")
#         await view_model.finish(image_message)
#         if os.path.exists(image_path):
#             os.remove(image_path)


# picture = on_command("图片", rule=to_me(), aliases={"picture", "图片"}, priority=1, block=True)


# @picture.handle()
# async def handle_picture_function(args: Message = CommandArg()):
#     logging.info("开始执行图片命令")
#     image_url = 'https://mypictures-1314100263.cos.ap-beijing.myqcloud.com//obsidian/202410201626803.png'
#     image_message = MessageSegment.image(image_url)
#     await picture.finish(image_message)
