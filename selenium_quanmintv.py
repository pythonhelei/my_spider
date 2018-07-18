import json
from selenium import webdriver
import time


class Quanmin(object):
    '''使用selenium爬取全民TV直播信息'''
    def __init__(self):
        self.url = 'https://www.quanmin.tv/game/all'
        self.driver = webdriver.Chrome()
        self.file = open('quanmintv.json','w')

    def __del__(self):
        self.driver.close()
        self.file.close()

    def get_data(self):
        nodelist = self.driver.find_elements_by_xpath('//*[@id="list_w-video-list"]/div[2]/ul/li/div')
        # print(len(nodelist))
        data_list = list()
        for node in nodelist:
            temp = dict()
            temp['owner'] = node.find_element_by_xpath(
                './div/a[1]/div/div/div/span[@class="common_w-card_host-name"]').text
            temp['title'] = node.find_element_by_xpath('./div/a[1]/div/div/p').text
            temp['vistor'] = node.find_element_by_xpath('./div/a[1]/div/div/div/span[2]').text
            temp['link'] = node.find_element_by_xpath('./div/a[1]').get_attribute('href')
            try:
                temp['cover'] = node.find_element_by_xpath('./div/a[1]/div[1]/picture/source').get_attribute('srcset')
            except:
                temp['cover'] = node.find_element_by_xpath('./div/a[1]/div[1]/img').get_attribute('src')
            data_list.append(temp)
        return data_list

    def save_data(self,data_list):
        for data in data_list:
            str_data = json.dumps(data,ensure_ascii=False) + ',\n'
            self.file.write(str_data)


    def run(self):
        self.driver.get(self.url)
        while True:
            data_list = self.get_data()
            self.save_data(data_list)
            try:
                to_next_page = self.driver.find_element_by_xpath('//*[@id="main_page"]/div/div[2]/div[2]/a[12]')

                if to_next_page.get_attribute('href') == '':
                    break
                to_next_page.click()
                time.sleep(1)
            except:
                break


if __name__ == '__main__':
    quanmin = Quanmin()
    quanmin.run()