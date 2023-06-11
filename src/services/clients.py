import openai
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import Remote


class ChatGptClient:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    @staticmethod
    def send_request(raw_request: str) -> str:
        msg = [
            {
                'role': 'user',
                'content': raw_request,
            }
        ]
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=msg
        )
        reply = chat.choices[0].message.content
        return reply


class BrowserClient:
    @staticmethod
    def _build_driver_(driver_url: str):
        firefox_options = FirefoxOptions()
        firefox_options.set_capability('browserName', 'firefox')
        firefox_options.set_capability('browserVersion', '113.0')
        firefox_options.set_capability('selenoid:options', {
            "enableVideo": False,
            'timeout': '1m',
            'screenResolution': '1920x1080',
        })
        firefox_options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0'
        )

        driver = Remote(
            command_executor=driver_url,
            options=firefox_options,
        )

        return driver

    def __init__(self, driver_url: str):
        self.driver = self._build_driver_(driver_url)
