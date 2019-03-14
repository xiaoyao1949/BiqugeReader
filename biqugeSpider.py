import requests
from lxml import etree
import threading

lock = threading.Lock()
page_list = list(range(1, 389))
book_set = set()


def get_books():
    pool = []
    for i in range(10):
        p = threading.Thread(target=parser_page, args=(lock,))
        pool.append(p)
        p.start()

    for p in pool:
        p.join()
    return book_set


def parser_page(lock):
    while True:
        try:
            lock.acquire()
            num = page_list.pop()
            lock.release()
        except:
            # 出现异常时不释放锁会导致程序无限等待
            lock.release()
            break

        api = 'https://www.biquge.info/wanjiexiaoshuo/{}'.format(str(num))
        try:
            r = requests.get(api)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
        except:
            print('资源获取失败')
            continue
        html = etree.HTML(r.text)
        book_name = html.xpath('//div[@class="novelslistss"]/ul/li/span[@class="s2"]/a/text()')
        book_addr = html.xpath('//div[@class="novelslistss"]/ul/li/span[@class="s2"]/a/@href')
        lock.acquire()
        book_set.update(list(zip(book_addr, book_name)))
        lock.release()
        print('%s 解析完毕'% api)


if __name__ == '__main__':
    books = get_books()
    print(len(books))
    print(books)
