"""
本模块定义了一个为文本生成有声读物的函数
由于小说每章的字数都大于百度API一次调用所接受的字数，所以采用每2000字左右合成一段声音。如有需要后期可再将这些音频文件拼接组合
用法：gen_mp3(文本路径） 调用后即可在同一目录下生成多段音频文件
"""
from Declaimer import Declaimer
import os


def gen_mp3(novel_path):
    buffer = ''
    count = 0
    decl = Declaimer()
    with open(novel_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 读到空白行
            if '===' in line or len(line) == 0:
                continue
            # 百度语音合成一次只能处理2048个字符
            if len(buffer) + len(line) < 2000:
                # 当前缓冲区未满，继续添加
                buffer += line
            else:
                # 缓冲区已满，提交合成请求，清空缓冲区。
                decl.txt2audio(buffer, str(count), os.path.dirname(novel_path))
                count += 1
                buffer = line


if __name__ == '__main__':
    novel = './books/一念永恒/[全本]一念永恒_耳根_修真小说.txt'
    gen_mp3(novel)
