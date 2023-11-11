import random
from datetime import datetime

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import json

class HeadlessChrome():
    def __init__(self):
        url = "https://kick.com/"
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        user_agents = [
            # Add your list of user agents here
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        ]

        user_agent = random.choice(user_agents)
        chrome_options.add_argument(f'user-agent={user_agent}')

        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(chrome_options, service)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
        
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        # self.driver.get(url)

class Kick():
    def __init__(self, channel_name):
        self.channel_name = channel_name

        self.browser = HeadlessChrome()

        self.channel_data = self.channel_raw()
        self.channel_id = self.channel_data['id']
        
    def new_messages(self, message_id=None, message_timestamp=None):
        if message_id == None and message_timestamp == None:
            raise 'No message id or message timestamp'

        new_messages = []

        for message in self.messages_raw():
            created_at = datetime.fromisoformat(message['created_at'])
            id = int(message['id'])

            if(
                (message_id != None and id > message_id) or 
                (message_timestamp != None and created_at > message_timestamp)
            ):
                # TODO: Parse this out from within messages_raw?
                new_messages.append({
                    'id': int(message['id']),
                    'username': message['sender']['username'],
                    'message': message['content'],
                    'timestamp': datetime.fromisoformat(message['created_at'])
                })

        return new_messages

###################################################
#                                                 #
#                  RAW REQUESTS                   #
#                                                 #
###################################################
    def channel_raw(self):
        self.browser.driver.get(f'https://kick.com/api/v1/channels/{self.channel_name}')
        
        while self.browser.driver.execute_script("return document.readyState") != "complete":
            pass
        
        content = self.browser.driver.find_element(By.TAG_NAME, 'body')
        j = json.loads(content.text)
        return j
    
    def messages_raw(self):
        self.browser.driver.get(f'https://kick.com/api/v2/channels/{self.channel_id}/messages')
        while self.browser.driver.execute_script("return document.readyState") != "complete":
            pass
        
        content = self.browser.driver.find_element(By.TAG_NAME, 'body')
        j = json.loads(content.text)

        return j['data']['messages']
        


if __name__ == '__main__':
    stream_http = Kick('konvay')
    print(stream_http.new_messages(message_timestamp=datetime.fromisoformat('2023-08-12T01:50Z')))
