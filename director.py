import biqugeSpider
from threading import Semaphore
from NovelSpider import NovelSpider
from WordCloudGen import gen_wordcloud
from Mp3Gen import gen_mp3
import os

books = biqugeSpider.get_books()
sema = Semaphore(10)
pool = []


def rele(func, name):
    def wrapper():
        func()
        # 爬取完一本小说后要做的事
        path = './books/{0}/{1}'.format(name, os.listdir('./books/' + name)[0])
        # 1. 生成这本书对应的词云图片
        gen_wordcloud(path)
        # 2. 生成这本书对于的音频文件
        gen_mp3(path)
        # 全部处理完后释放锁，让其他线程启动
        sema.release()
        print('\033[1;31;40m')
        print('+' * 60)
        print('{} 处理完成，可进行打包发布等后续操作'.format(name))
        print('+' * 60)
        print('\033[0m')

    return wrapper


for link, name in books:
    sema.acquire()
    p = NovelSpider(url=link, book_name=name)
    p.run = rele(p.run, name)
    pool.append(p)
    p.start()
