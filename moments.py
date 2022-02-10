import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from time import sleep
from processor import Processor
from config import *
from bs4 import BeautifulSoup

# 微信登录需要验证，请手动登录微信并打开朋友圈首页后，再运行脚本
class Moments():
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            'platformName': PLATFORM,
            'platformVersion': PLATFORM_VERSION,
            'deviceName': DEVICE_NAME
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        # 保存至非关系型数据库MongoDB
        '''self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]'''
        # 处理器
        self.processor = Processor()
    
    def login(self):
        """
        登录微信
        :return:
        """
        # 登录按钮
        login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cjk')))
        login.click()
        # 手机输入
        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/h2')))
        phone.set_text(USERNAME)
        # 下一步
        next = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/adj')))
        next.click()
        # 密码
        password = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/h2"][1]')))
        password.set_text(PASSWORD)
        # 提交
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/adj')))
        submit.click()
    
    def enter(self):
        """
        进入朋友圈
        :return:
        """
        # 选项卡
        tab = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/bw3"][3]')))
        tab.click()
        # 朋友圈
        moments = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/atz')))
        moments.click()
    
    def crawl(self):
        """
        爬取
        :return:
        """
        while True:
            # 当前页面显示的所有状态
            items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/ju2"]')))
            # 遍历每条状态
            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element(By.ID, 'com.tencent.mm:id/hga').text
                    # 正文
                    content = item.find_element(By.ID, 'com.tencent.mm:id/c28').text
                    # 日期
                    # 已废弃，该方法无法获取日期
                    # date = item.find_element(By.ID, 'com.tencent.mm:id/nf').text
                    # 处理日期
                    # date = self.processor.date(date)
                    data = {
                        'nickname': nickname,
                        'content': content
                    }
                    print(data)
                    # 插入MongoDB
                    # self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
                    sleep(SCROLL_SLEEP_TIME)
                except NoSuchElementException:
                    pass

            # 上滑
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
    
    def main(self):
        """
        入口
        :return:
        """
        # 登录
        # self.login()
        # 进入朋友圈
        # self.enter()
        # 爬取
        self.crawl()


if __name__ == '__main__':
    moments = Moments()
    moments.main()
