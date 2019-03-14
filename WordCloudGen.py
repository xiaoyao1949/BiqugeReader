"""
本模块定义了一个为文本生成词云的函数
用法：gen_wordcloud(文本文件路径)。调用后即可在同一目录下生成.png格式的词云图片
"""
from wordcloud import WordCloud
import jieba
import os
import re


def gen_wordcloud(novel_path):
    filename = re.search(r'\[全本](\w+?)_.*', novel_path).group(1)
    dirname = os.path.dirname(novel_path)
    w = WordCloud(font_path=r'C:\Windows\Fonts\simsun.ttc', width=1000, height=700,margin=20,max_words=50)
    w.generate(' '.join(jieba.cut(open(novel_path, 'r',encoding='utf-8').read())))
    w.to_file(os.path.join(dirname, filename + '.png'))


if __name__ == '__main__':
    novel = './books/一念永恒/[全本]一念永恒_耳根_修真小说.txt'
    gen_wordcloud(novel)
