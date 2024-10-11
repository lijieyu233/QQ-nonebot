import logging

import gradio as gr
import os

def get_txt_files(directory):
    # 获取指定目录下的所有txt文件
    if os.path.isdir(directory):
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    return []

def load_file(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return "File not found!"

def save_file(filepath, content):
    if os.path.isfile(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        return f"{os.path.basename(filepath)} has been saved!"
    return "File not found!"
def main():
    # Gradio 接口
    with gr.Blocks() as app:
        gr.Markdown("# TXT File Editor")

        with gr.Row():
            directory_input = gr.Textbox(label="输入文件夹路径", placeholder="/opt/QQ-nonebot/awesome_bot/plugins/CloseAi/模型文本")
            load_files_button = gr.Button("加载文件夹")

        file_selector = gr.Dropdown(label="选择模型文本")
        load_button = gr.Button("加载模型文本")

        text_area = gr.Textbox(label="模型", lines=20, interactive=True)
        save_button = gr.Button("保存修改")


        def load_files_callback(directory):
            txt_files = get_txt_files(directory)
            if txt_files:
                return gr.Dropdown(choices=txt_files, label="选择模型文本")
            else:
                return gr.Dropdown(choices=[], label="No TXT files found")
        def load_file_callback(selected_file):
            return load_file(selected_file)

        def save_file_callback(selected_file, content):
            return save_file(selected_file, content)

        load_files_button.click(fn=load_files_callback, inputs=directory_input, outputs=file_selector)
        load_button.click(fn=load_file_callback, inputs=file_selector, outputs=text_area)
        save_button.click(fn=save_file_callback, inputs=[file_selector, text_area], outputs=text_area)

# 启动 Gradio 应用
    logging.info("web启动")
    app.launch(server_port=10086, server_name="0.0.0.0")

if __name__ == "__main__":
    main()