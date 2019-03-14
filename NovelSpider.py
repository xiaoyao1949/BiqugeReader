import requests
from lxml import etree
import os
import threading


class NovelSpider(threading.Thread):
    def __init__(self, url, book_name):
        super(NovelSpider, self).__init__()
        self.url = url
        self.book_name = book_name
        self.book_dir = './books/' + book_name

        # 创建小说根目录
        if not os.path.exists('./books/'):
            os.mkdir('./books/')
        if not os.path.exists(self.book_dir):
            print('成功创建小说文件夹{path}'.format(path=os.path.abspath(self.book_dir)))
            os.mkdir(self.book_dir)

        # 为当前小说配置爬取规则
        from sites import sites
        for site, cfg in sites.items():
            if cfg['base_url'] in self.url:
                self.novel_rule = cfg['novel_rule']
                self.chapter_rule = cfg['chapter_rule']
                self.site = site
                break
        else:
            print(site, '网站没有相应的匹配规则')

    def get_novel_info(self):
        # 获取小说主页
        try:
            rsp = requests.get(url=self.url)
            rsp.raise_for_status()
            rsp.encoding = rsp.apparent_encoding
        except Exception as e:
            print(e)
            print(rsp.status_code, '小说信息获取失败。')
        # 提取作者、小说类型、最近更新时间、章节链接
        html = etree.HTML(rsp.text)
        self.book_author = html.xpath(self.novel_rule['author'])[0].split(':')[-1].split('：')[-1]
        self.book_type = html.xpath(self.novel_rule['type'])[0].strip().split(':')[-1]
        self.book_last_update_time = html.xpath(self.novel_rule['last_update_time'])[0].strip().split(':', maxsplit=1)[
            -1]
        # 章节链接列表
        pre_chapter_list = html.xpath(self.novel_rule['chapter_list'])

        if self.site == 'biquge':
            self.chapter_list = [self.url + i for i in pre_chapter_list]

        elif self.site == 'biquge5200':
            self.chapter_list = pre_chapter_list[9:]



    def get_chapters(self):
        # 创建小说空文件
        open(os.path.join(self.book_dir,
                          '[全本]{name}_{author}_{btype}.txt'.format(name=self.book_name, author=self.book_author,
                                                                   btype=self.book_type)), 'w').close()
        novel = open(os.path.join(self.book_dir,
                                  '[全本]{name}_{author}_{btype}.txt'.format(name=self.book_name, author=self.book_author,
                                                                           btype=self.book_type)), 'a',
                     encoding='utf-8')
        # 写入内容
        for chapter in self.chapter_list:
            title, filled = self._get_chapter_content(chapter)
            novel.write(filled)
            print(
                '{name}（{cur}/{total}）:{file} 下载成功'.format(name=self.book_name, cur=self.chapter_list.index(chapter),
                                                           total=len(self.chapter_list),
                                                           file=title))
        novel.close()
        print('Done!')

    def _get_chapter_content(self, url):
        try:
            rsp = requests.get(url)
            rsp.raise_for_status()
            rsp.encoding = rsp.apparent_encoding
        except:
            print('章节内容出错', url)
            return -1
        xpath_rule = self.chapter_rule
        html = etree.HTML(rsp.text)
        title = html.xpath(xpath_rule['title'])[0]
        content = '\n'.join([sentence.strip() for sentence in html.xpath(xpath_rule['content'])])
        filled = title + '\n' + '=' * 30 + '\n' + content + '\n\n'
        return title, filled

    def run(self):
        self.get_novel_info()
        self.get_chapters()


if __name__ == '__main__':
    threadpool = []
    for url, book_name in [('https://www.biquge.info/10_10582/', '三寸人间'),
                           ('https://www.biquge5200.cc/38_38857/', '一念永恒')]:
        threadpool.append(NovelSpider(url, book_name))
    for p in threadpool:
        p.start()

    for p in threadpool:
        p.join()

    print('all over')
