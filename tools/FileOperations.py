import os


class FileOperations:

    #输入文件路径,创建一个txt空文件，如果路径不存在则先创建目录 再创建文件
    @staticmethod
    def create_txt_file(file_path):
        dirname = os.path.dirname(file_path) #获取文件路径的目录名
        print("目录名"+dirname)
        if not os.path.exists(dirname): # 如果目录不存在，则创建目录
            os.makedirs(dirname)
        with open(file_path, "w",encoding='utf-8') as file:
            pass


    # 读文件
    @staticmethod
    def read_txt_file(file_path):
        try:
            with open(file_path, 'r',encoding='utf-8') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
    # 写文件
    @staticmethod
    def write_to_txt_file(file_path, content):
        try:
            with open(file_path, 'w',encoding='utf-8') as file:
                file.write(content)
            print(f"Successfully wrote to {file_path}")
        except PermissionError:
            print(f"Permission denied to write to {file_path}")

    # 静态方法，以追加的方式写入文件 要求每次写入换行 编码为utf-8
    @staticmethod
    def append_to_txt_file(file_path, content):
        try:
            with open(file_path, 'a',encoding='utf-8') as file:
                file.write('\n'+content )
            print(f"Successfully appended to {file_path}")
        except PermissionError:
            print(f"Permission denied to append to {file_path}")









    ## 列表和文件操作
    # 静态方法:从txt文件中读取列表
    @staticmethod
    def load_list_from_txt(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f]
            return lines
        except Exception as e:
            print("An error occurred while loading the list:", str(e))
            return []
    # 静态方法:输入知道列表中的元素名，删除txt文件中的元素
    @staticmethod
    def delete_element_in_txt(file_path, element):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            updated_lines = [line for line in lines if line != element]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
            print(f"{element} deleted from {file_path}")
        except Exception as e:
            print("An error occurred while deleting the element:", str(e))
    # 静态方法:往txt文件中添加列表元素
    @staticmethod
    def add_element_to_txt(file_path, element):
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(element+"\n")
            print(f"{element} added to {file_path}")
        except Exception as e:
            print("An error occurred while adding the element:", str(e))



