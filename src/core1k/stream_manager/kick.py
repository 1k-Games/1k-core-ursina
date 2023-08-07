from requests_html import HTMLSession

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import json

class HeadlessChrome():
    def __init__(self):
        url = "https://google.com/"
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')

class Kick():
    def __init__(self, channel_id, channel_name):
        self.channel_id = channel_id
        self.channel_name = channel_name

        self.session = HTMLSession()
        self.browser = HeadlessChrome()

    def channel(self):
        self.browser.driver.get(f'https://kick.com/api/v1/channels/{self.channel_name}')
        self.browser.driver.implicitly_wait(0.5)
        
        a = self.browser.driver.find_element(By.TAG_NAME, 'body')
        j = json.loads(a.text)
        print(j)

    def messages(self):
        print('retrieving messages')

        self.browser.driver.get(f'https://kick.com/api/v2/channels/{self.channel_id}/messages')
        self.browser.driver.implicitly_wait(0.5)
        
        a = self.browser.driver.find_element(By.TAG_NAME, 'body')
        j = json.loads(a.text)
        print(j['data']['messages'])

        return j['data']['messages']

if __name__ == '__main__':
    stream_http = Kick(8040048, 'konvay')
    # stream_http.channel()
    stream_http.messages()