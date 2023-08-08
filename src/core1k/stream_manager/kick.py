import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import json

class HeadlessChrome():
    def __init__(self):
        url = "https://kick.com/"
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

        self.driver = uc.Chrome(chrome_options, use_subprocess=True)
        self.driver.get(url)

class Kick():
    def __init__(self, channel_name):
        self.channel_name = channel_name

        self.browser = HeadlessChrome()

        self.channel_data = self.channel()
        self.channel_id = self.channel_data['id']

    def channel(self):
        self.browser.driver.get(f'https://kick.com/api/v1/channels/{self.channel_name}')
        self.browser.driver.implicitly_wait(0.5)
        
        content = self.browser.driver.find_element(By.TAG_NAME, 'body')
        print(content)
        j = json.loads(content.text)
        return j
        
    def messages(self):
        self.browser.driver.get(f'https://kick.com/api/v2/channels/{self.channel_id}/messages')
        self.browser.driver.implicitly_wait(0.5)
        
        content = self.browser.driver.find_element(By.TAG_NAME, 'body')
        j = json.loads(content.text)

        return j['data']['messages']
        




if __name__ == '__main__':
    stream_http = Kick('konvay')
    # stream_http.channel()
    stream_http.messages()