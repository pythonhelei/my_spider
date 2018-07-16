import json
import requests
from lxml import etree


class Qiubai(object):
    """使用xpath抽取数据，爬取糗事百科用户信息"""
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/text/page/{}/'
        self.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.urllist = None
        self.file = open('qiushi.json','w')
        # self.file = open('joke.txt', 'w')

    def generate_urllist(self):
        self.urllist = [self.url.format(i) for i in range(1,14)]

    def get_data(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content

    def parse_data(self,data):
        html = etree.HTML(data)
        node_list = html.xpath('//*[contains(@id,"qiushi_tag")]')
        result = list()
        joke = list()
        for node in node_list:
            temp = dict()
            try:
                temp['user'] = node.xpath('./div[1]/a[2]/h2/text()')[0].strip()
                temp['link'] = 'https://www.qiushibaike.com'+node.xpath('./div[1]/a[2]/@href')[0]
                temp['age'] = node.xpath('./div[1]/div/text()')[0]
                temp['gender'] = node.xpath('./div[1]/div/@class')[0].split(' ')[-1].replace('Icon','')
                t = node.xpath('./a/div/span/text()')
            except:
                temp['user'] = '匿名用户'
                temp['link'] = None
                temp['age'] = None
                temp['gender'] = None
                t = ''
            result.append(temp)
            joke.append(t)
        return result, joke

    def save_data(self,result, joke):
        for data in result:
            str_data = json.dumps(data,ensure_ascii=False) + ',\n'
            self.file.write(str_data)
        # for j in joke:
        #     try:
        #         self.file.write(j)
        #     except:
        #         for i in j:
        #             self.file.write(i)


    def __del__(self):
        self.file.close()


    def run(self):
        self.generate_urllist()
        for url in self.urllist:
            data = self.get_data(url)
            result, joke = self.parse_data(data)
            self.save_data(result, joke)
            # print(result)


if __name__ == '__main__':
    qiubai = Qiubai()
    qiubai.run()