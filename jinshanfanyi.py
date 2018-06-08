import requests, sys ,json


class Jinshan(object):
    """金山翻译"""
    def __init__(self, word):
        self.url = 'http://fy.iciba.com/ajax.php?a=fy'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }
        self.post_data = {
            'f': 'auto',
            't': 'auto',
            'w': word,
        }

    # 获取响应
    def get_data(self):
        response = requests.post(self.url,headers=self.headers,data=self.post_data)
        return response.content

    # 解析数据
    def parse_data(self, data):
        dict_data = json.loads(data)
        # print(dict_data)
        word = dict_data['content']['out']
        print(word)

    # 启动爬虫
    def run(self):
        data =self.get_data()
        self.parse_data(data)


if __name__ == '__main__':
    fanyi = Jinshan(sys.argv[1])
    fanyi.run()