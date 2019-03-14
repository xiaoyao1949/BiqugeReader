sites = {
    'biquge': {
        'name': '笔趣阁',
        'base_url': 'https://www.biquge.info/',
        'novel_list': 'https://www.biquge.info/wanjiexiaoshuo/',
        'novel_rule': {
            'name': '//*[@id="info"]/h1/text()',
            'author': '//*[@id="info"]/p[1]/text()',
            'type': '//*[@id="info"]/p[2]/text()',
            'last_update_time': '//*[@id="info"]/p[3]/text()',
            'chapter_list': '//*[@id="list"]/dl/dd/a/@href',
        },
        'chapter_rule': {
            'title': '//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()',
            'content': '//*[@id="content"]/text()',
        }
    },
    'biquge5200': {
        'name': '笔趣阁5200',
        'base_url': 'https://www.biquge5200.cc/',
        'novel_rule': {
            'name': '//*[@id="info"]/h1/text()',
            'author': '//div[@id="info"]/p[1]/text()',
            'type': '//div[@class="con_top"]/a[2]/text()',
            'last_update_time': '//*[@id="info"]/p[3]/text()',
            'chapter_list': '//*[@id="list"]/dl/dd/a/@href',
        },
        'chapter_rule': {
            'title': '//div[@class="bookname"]/h1/text()',
            'content': '//div[@id="content"]/p/text()',
        }
    }
}
