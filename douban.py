import json

import requests


class Douban(object):
    def __init__(self):

        self.n = 0
        self.url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?os=android&for_mobile=1&start={}&count=18'
        self.headers = {
            'Referer': 'https://m.douban.com/tv/american',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'
        }
        self.file = open('tv.json','w')

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def save_data(self,data_list):
        for data in data_list:
            str_data = json.dumps(data,ensure_ascii=False) + ',' + '\n'
            self.file.write(str_data)

    def __del__(self):
        self.file.close()

    def parse_data(self, data):
        dict_data = json.loads(data)
        tv_list = dict_data['subject_collection_items']
        result = []
        for tv in tv_list:
            temp = {}
            temp['title'] = tv['title']
            temp['url'] = tv['url']
            result.append(temp)
        return result

    def run(self):
        while True:
            url = self.url.format(self.n)
            data = self.get_data(url)
            data_list = self.parse_data(data)
            self.save_data(data_list)
            self.n += 18
            if len(data_list) is 0:
                break


if __name__ == '__main__':
    douban = Douban()
    douban.run()