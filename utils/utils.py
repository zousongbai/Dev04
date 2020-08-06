
# 创建一个生成器，获取文件流，每次获取的是文件字节数据
# chunk_size“每次读取多少字节
def get_file_content(filename, chunk_size=1024):
    # 打开文件
    with open(filename, encoding='utf-8') as file:
        while True:
            # 使用文件对象的read方法获取数据
            content = file.read(chunk_size)
            # 如果文件结尾，那么content为None，则退出循环
            if not content:
                break
            # 如果不为空，生成器就返回
            yield content
