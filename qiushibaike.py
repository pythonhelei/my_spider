import json
import re

import requests

class Qiubai(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/text/page/'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.file = open('qiubai.json', 'w')


    def parse_data(self, html):
        result = re.findall(r'<a href="(.*?)".*?<span>(.*?)</span>', html, re.S)
        data_list = list()
        for i in result:
            temp = dict()
            temp['url'] = 'https://www.qiushibaike.com' + i[0]
            temp['content'] = re.sub(r'\n|…|<br/>', '', i[1])
            data_list.append(temp)
        return data_list

    def save_data(self, data):
        for i in data:
            str_data = json.dumps(i, ensure_ascii=False) + ',\n'
            self.file.write(str_data)

    def __del__(self):
        self.file.close()

    def run(self):
        n = 1
        while True:
            url = self.url + str(n) + '/'
            html = requests.get(url, headers=self.headers)
            page = re.findall(r'<span class="next">', html.content.decode(),re.S)
            if page == []:
                break
            # print(html.content.decode())
            data = self.parse_data(html.content.decode())
            self.save_data(data)
            n += 1




if __name__ == '__main__':
    qiubai = Qiubai()
    qiubai.run()