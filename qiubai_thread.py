import json
import threading

import requests
from lxml import etree
from queue import Queue

class Qiubai(object):
    """升级！多线程爬虫爬取糗事百科"""
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/text/page/{}/'
        self.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.urllist = None
        self.file = open('qiushi.json','w')
        self.url_queue = Queue()
        self.response_queue = Queue()
        self.data_queue = Queue()

    def generate_urllist(self):
        for i in range(1, 14):
            self.url_queue.put(self.url.format(i))


    def get_data(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url,headers=self.headers)
            # print(response.status_code) # 查看响应状态码，判断是否被反爬
            self.response_queue.put(response.content)
            self.url_queue.task_done()


    def parse_data(self):
        while True:
            data = self.response_queue.get()
            html = etree.HTML(data)
            node_list = html.xpath('//*[contains(@id,"qiushi_tag")]')
            result = list()
            for node in node_list:
                temp = dict()
                try:
                    temp['user'] = node.xpath('./div[1]/a[2]/h2/text()')[0].strip()
                    temp['link'] = 'https://www.qiushibaike.com'+node.xpath('./div[1]/a[2]/@href')[0]
                    temp['age'] = node.xpath('./div[1]/div/text()')[0]
                    temp['gender'] = node.xpath('./div[1]/div/@class')[0].split(' ')[-1].replace('Icon','')
                except:
                    temp['user'] = '匿名用户'
                    temp['link'] = None
                    temp['age'] = None
                    temp['gender'] = None
                result.append(temp)
            self.data_queue.put(result)
            self.response_queue.task_done()

    def save_data(self):
        while True:
            result = self.data_queue.get()
            for data in result:
                str_data = json.dumps(data,ensure_ascii=False) + ',\n'
                self.file.write(str_data)
            self.data_queue.task_done()

    def __del__(self):
        self.file.close()


    def run(self):
        # 创建列表，存储线程
        thread_list = list()

        # 创建1个url生成线程
        t_generate_url = threading.Thread(target=self.generate_urllist)
        thread_list.append(t_generate_url)

        # 创建3个获取数据的线程
        for i in range(3):
            t_get_data = threading.Thread(target=self.get_data)
            thread_list.append(t_get_data)

        # 创建3个解析数据的线程
        for i in range(3):
            t_parse_data = threading.Thread(target=self.parse_data)
            thread_list.append(t_parse_data)

        # 存储数据的线程
        t_save_data = threading.Thread(target=self.save_data)
        thread_list.append(t_save_data)

        # 开启线程
        for t in thread_list:
            # 设置守护线程，守护线程随主线程结束而结束
            t.setDaemon(True)
            t.start()
        # 主线程监听队列状态
        for q in [self.url_queue, self.response_queue, self.data_queue]:
            q.join()



if __name__ == '__main__':
    qiubai = Qiubai()
    qiubai.run()