
from selenium import webdriver

dr = webdriver.Chrome()
dr.get('https://qzone.qq.com/')
# 通过id进入frame框架
dr.switch_to.frame('login_frame')

# 点击账号密码登录按钮
task_1 = dr.find_element_by_id('switcher_plogin')
task_1.click()

# 输入账号密码
element_user = dr.find_element_by_id('u')
element_user.send_keys('2385829744')

element_passwd = dr.find_element_by_id('p')
element_passwd.send_keys('ws19940121**')

# 点击登录按钮
task_2 = dr.find_element_by_id('login_button')
task_2.click()
