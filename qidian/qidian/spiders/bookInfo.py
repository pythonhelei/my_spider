# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qidian.items import QidianItem
from fontTools.ttLib import TTFont
from io import BytesIO
import re
from scrapy_redis.spiders import RedisCrawlSpider



class BookinfoSpider(RedisCrawlSpider):
# class BookinfoSpider(CrawlSpider):
    '''利用redis实现scrapy分布式爬虫爬取起点文学网书籍信息，数据保存在mongodb数据库'''
    name = 'bookInfo'
    # allowed_domains = ['qidian.com']
    # start_urls = ['https://www.qidian.com/all']

    redis_key = 'bookinfo'

    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None,domain.split(',')))
        super(BookinfoSpider, self).__init__(*args, **kwargs)

    rules = (
        # 详情页
        Rule(LinkExtractor(allow=r'info/\d+'), callback='parse_item'),
        # 翻页
        Rule(LinkExtractor(allow=r'hiddenField=0&page='), follow=True),
    )

    def parse_item(self, response):
        item = QidianItem()

        item['book_name'] = response.xpath('//div[@class="book-info "]/h1/em/text()').extract()[0]
        item['author'] = response.xpath('//div[@class="book-info "]/h1/span/a/text()').extract()[0]
        item['status'] = response.xpath('//span[@class="blue"]/text()').extract()[0]
        classname = response.xpath('//div[@class="book-info "]/p[3]/em[1]/span/@class').extract()[0]
        url = "https://qidian.gtimg.com/qd_anti_spider/{}.woff".format(classname)
        resp = response.body.decode('utf-8')

        pattern = re.compile('</style><span class="\w+">(.*?);</span></em><cite>')
        word_list = pattern.search(resp).group(1).split(';')
        word_count = parse_font(url, word_list)
        item['word_count'] = word_count + '万字'

        item['ticket'] = response.xpath('//*[@id="monthCount"]/text()').extract_first()
        yield item




import requests


def parse_font(url,word_list):
    # 破解自定义字典，换回真实数据
    # {100416: 'zero', 100418: 'period', 100419: 'two', 100420: 'eight', 100421: 'six', 100422: 'three',
    #  100423: 'seven', 100424: 'nine', 100425: 'five', 100426: 'one', 100427: 'four'}
    word_map = {'period': '.', 'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
                'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    resp = requests.get(url)
    font = TTFont(BytesIO(resp.content))
    cmap = font.getBestCmap()
    font.close()
    res = ""
    for word in word_list:
        En = cmap[int(word[2:])]
        res += word_map[En]
    return res
