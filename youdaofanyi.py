#coding:utf-8
import requests
import time,random
import re
import hashlib
import json


class Youdao(object):

    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'Cookie':'OUTFOX_SEARCH_USER_ID=-1219948016@101.81.190.192; P_INFO=itcast_soft_test@126.com|1515861142|2|mail126|00&99|nmg&1515730516&mail126#shh&null#10#0#0|&0|mail126|itcast_soft_test@126.com; OUTFOX_SEARCH_USER_ID_NCOO=309526661.26247734; fanyi-ad-id=39535; fanyi-ad-closed=1; JSESSIONID=aaaCF6WRTPQF7b3pgE_dw; SESSION_FROM_COOKIE=unknown; _ntes_nnid=6bfa8afc526cdbcb2f03111b5ec3ef0f,1516105554018; ___rl__test__cookies=1516239512654',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer':'http://fanyi.youdao.com/'
        }
        self.post_data = None

    def generate_post_data(self, word):
        # 生成时间戳
        now = time.time()
        # 因为时间戳短所以平提取所有的时间
        timestamp = re.match('(\d+).(\d+)', str(now))
        # 拼接
        tempstr = timestamp.group(1) + timestamp.group(2)
        # 截取
        tempstr = tempstr[0:13]

        # 生成随机数
        randomint = random.randint(0, 9)
        salt = str(int(tempstr) + randomint)
        # print(salt)

        # 构建 sign
        # u.md5(E + n + r + O)
        E = "fanyideskweb"
        n = word
        r = salt
        O = "aNPG!!u6sesA>hBAW1@(-"
        md5str = E + n + r + O

        # 创建hash对象
        md5 = hashlib.md5()

        # 填充数据
        md5.update(md5str.encode())

        # 获取hash值
        sign = md5.hexdigest()

        self.post_data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': False,
        }
        # print(temp_data)

    def get_data(self):
        response = requests.post(self.url, headers=self.headers, data=self.post_data)
        return response.content.decode()

    def parse_data(self, data):
        json_data = json.loads(data)
        result = json_data['translateResult'][0][0]['tgt']
        print(result)

    def run(self):
        # 构造目标url
        # 构造请求头
        # 构造post数据
        self.generate_post_data('人生苦短,及时行乐')
        # 发送请求获取响应
        data = self.get_data()
        # print(data)
        # 解析响应抽取数据
        self.parse_data(data)


if __name__ == '__main__':
    youdao = Youdao()
    youdao.run()