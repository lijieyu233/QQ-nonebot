import logging
import os

from nonebot import on_command, Bot
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.rule import to_me
from openai import OpenAI

from tools.FileOperations import FileOperations


def my_openai_call(apikey="sk-NPTWOw0zNXh7iMCQ5jsYve1e9LFGcli6DM4R0K0LWMU7Yaht",
                   model="gpt-4o-mini-2024-07-18",
                   user_content="如何做西红柿炖牛腩？",
                   system_content=None):
    print("apikey:" + apikey)
    print("model:" + model)
    print("user_content:" + user_content)
    print("system_content:" + str(system_content))
    client = OpenAI(
        # This is the default and can be omitted
        base_url='https://api.openai-proxy.org/v1',
        api_key=apikey,
    )
    if system_content is not None and len(system_content.strip()):
        messages = [
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': user_content}
        ]
    else:
        messages = [
            {'role': 'user', 'content': user_content}
        ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    logging.info("Openai model inference done.")
    print("chatgpt返回信息:" + chat_completion.choices[0].message.json())
    return chat_completion.choices[0].message.content


default_model = "system_content"  # 默认模型名称
current_model = "system_content"  # 当前模型名称
current_model_path = "system_content.txt"  # 当前模型路径
current_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录
model_list_path = current_directory + '\\模型文本\\' + "model_list.txt"

# 注册一个名为"提问"的命令，匹配"提问"、"question"、"查天气"三个关键词，优先级为10，阻止
question = on_command("提问", rule=to_me(), aliases={"question"}, priority=10, block=True)


@question.handle()
async def handle_function(args: Message = CommandArg()):
    # 提取参数纯文本作为地名，判断是否有效
    if user_content := args.extract_plain_text():
        # 调用tools中的方法读取system_content.txt文件，赋值给system_content变量
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建文件的绝对路径
        file_path = f'{current_dir}\\模型文本\\{current_model}.txt'
        system_content = FileOperations.read_txt_file(file_path)
        text = my_openai_call(system_content=system_content, user_content=user_content)
        await question.finish(text)
    else:
        await question.finish("请输入地名")


# 注册一个名为’模型训练‘的命令，匹配"模型训练"、"train"、"训练"三个关键词，优先级为10，阻止
train = on_command("模型训练", rule=to_me(), aliases={"train", "训练"}, priority=10, block=True)


@train.handle()
async def handle_function(args: Message = CommandArg()):
    content = args.extract_plain_text()
    if content:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '模型文本', current_model + '.txt')
        FileOperations.append_to_txt_file(file_path, content)
        await train.finish("模型训练成功")


# 创建
# 注册一个名为"模型创建的命令 "，匹配"模型创建"、"create"、"创建"三个关键词，优先级为10，阻止
create = on_command("模型创建", rule=to_me(), aliases={"create", "创建"}, priority=10, block=True)


@create.handle()
async def handle_create_function(args: Message = CommandArg()):
    name = args.extract_plain_text()
    if name:

        model_path = os.path.dirname(os.path.abspath(__file__)) + '\\模型文本\\' + name + ".txt"
        print("模型路径:" + model_path)
        logging.info(f"模型路径: {model_path}")
        try:
            # 检查文件是否存在，如果不存在则创建
            if not os.path.exists(model_path):
                FileOperations.create_txt_file(model_path)
                # 添加模型名称到列表文件，先检查是否已存在
                if name not in FileOperations.load_list_from_txt(model_list_path):
                    FileOperations.add_element_to_txt(model_list_path, name)
                await create.finish(f"{name} 模型创建完成")
            else:
                await create.finish(f"{name} 模型已存在")
        except Exception as e:
            logging.error(f"创建模型时出错: {e}")
            # await create.finish("模型创建失败")
    else:
        await create.finish("模型创建失败，未输入模型名称")


# 查看
# 注册一个名为"当前模型查看的命令 "，匹配"当前模型查看"、"view"、"current_model"三个关键词，优先级为10，阻止
view = on_command("当前模型", rule=to_me(), aliases={"current"}, priority=10, block=True)


@view.handle()
async def handle_view_function(args: Message = CommandArg()):
    if current_model:
        await view.finish(f"当前模型:{current_model}")


# 选择
# 注册一个名为'模型选择的命令 '，匹配"模型选择"、"select"、"选择"三个关键词，优先级为10，阻止
select = on_command("模型选择", rule=to_me(), aliases={"select", "选择"}, priority=10, block=True)


@select.handle()
async def handle_select_function(args: Message = CommandArg()):
    global current_model
    global current_model_path
    if name := args.extract_plain_text():
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建文件的绝对路径
        file_path = os.path.join(current_dir, '模型文本', name + '.txt')
        if os.path.isfile(file_path):
            current_model = name
            current_model_path = file_path
            await select.finish(f"成功切换至{name}模型")


# 删除
# 注册一个名为"模型删除的命令 "，匹配"模型删除"、"delete"、"删除"三个关键词，优先级为10，阻止
delete = on_command("模型删除", rule=to_me(), aliases={"delete", "删除"}, priority=1, block=True)


@delete.handle()
async def handle_delete_function(args: Message = CommandArg()):
    global current_model
    global current_model_path
    if name := args.extract_plain_text():
        if name == default_model:
            await delete.finish("默认模型无法删除")
        if name == current_model:
            await delete.finish("当前模型无法删除")
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建文件的绝对路径
        file_path = os.path.join(current_dir, '模型文本', name + '.txt')
        if os.path.isfile(file_path):
            os.remove(file_path)
            current_model = None
            await delete.finish(f"成功删除{name}模型")


# 列表
# 注册一个名为模型列表 的命令，匹配"模型列表"、"list"、"列表"三个关键词，优先级为1，阻止
model_list = on_command("模型列表", rule=to_me(), aliases={"list", "列表"}, priority=1, block=True)


@model_list.handle()
async def handle_delete_function(args: Message = CommandArg()):
    list = FileOperations.load_list_from_txt(model_list_path)
    await model_list.finish(f"当前模型列表:{list}")


# 查看模型
# 注册一个名为"查看模型"的命令，匹配"查看模型"、"view_model"、"查看"三个关键词，优先级为1，
view_model = on_command("查看模型", rule=to_me(), aliases={"view", "查看"}, priority=1, block=True)


@view_model.handle()
async def handle_view_model_function(args: Message = CommandArg()):
    name = args.extract_plain_text()
    if name:
        text = FileOperations.read_txt_file(f'{current_directory}/模型文本/{name}.txt')
        await view_model.finish(f"{name}模型的内容:\n{text}")
    elif current_model:
        text = FileOperations.read_txt_file(current_model_path)
        await view_model.finish(f"{current_model}模型的内容:\n{text}")
    else:
        await view_model.finish("没有模型")