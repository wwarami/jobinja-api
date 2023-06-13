import json
from abc import ABC

import requests

from config.config import COOKIES_JSON_PATH, REQUEST_USER_AGENT, JOBINJA_JOBS_URL


class BaseCrawler(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        # make sure only one instance will be created
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cookies_path=COOKIES_JSON_PATH):
        # create a request session
        self.session = requests.session()
        # add cookies to session
        self._add_cookies(cookies_path)
        # add headers to session(to get access from jobinja)
        self.session.headers['User-Agent'] = REQUEST_USER_AGENT

    def _add_cookies(self, path):
        # read the cookies and set them for the session.
        try:
            with open(path, 'r') as file:
                cookies = json.load(file)
                for cookie in cookies:
                    self.session.cookies.set(cookie['name'], cookie['value'])
        except FileNotFoundError:
            raise FileNotFoundError('Can not find cookies file. Check config.config.py file.')
        except json.JSONDecodeError:
            raise Exception("Provided cookies file is not valid. Get the cookies again please.")


class GetJobs(BaseCrawler):
    def __init__(self, cookies_path=COOKIES_JSON_PATH, page=1, **kwargs):
        super().__init__(cookies_path)
        # create filter base on arguments
        self.filters = dict(locations=[kwargs.get('locations')],
                            categories=[kwargs.get('categories')],
                            keywords=[kwargs.get('keywords')])
        self.page = page

    def start(self):
        # get the source code
        source = self.get_source(JOBINJA_JOBS_URL)[0]
        print(source)

    def get_source(self, url):
        # create url parametrs base on filter
        params = {'page': self.page}
        for key in self.filters:
            for item in self.filters[key]:
                if item is None:
                    # if there is no item, we break the loop
                    break
                for index, value in enumerate(item):
                    params[f'filters[{key}][{index}]'] = value

        # use BaseCrawler session to send request
        response = self.session.get(url, params=params)
        # return response
        return response.text, response.url, response.status_code


GetJobs(page=2).start()
