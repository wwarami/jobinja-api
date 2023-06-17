import json
from abc import ABC, abstractmethod
import requests
from config.config import COOKIES_JSON_PATH, REQUEST_USER_AGENT, JOBINJA_JOBS_URL
from crawler.parser import JobsParser, JobDetailParser


class BaseCrawler(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        # make sure only one instance will be created
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cookies_path=COOKIES_JSON_PATH, *args, **kwargs):
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
            raise FileNotFoundError('Can not find cookies file. Check config.config.py file.\n\
Check for "COOKIES_JSON_PATH".')
        except json.JSONDecodeError:
            raise Exception("Provided cookies file is not valid. Get the cookies again please.")

    @abstractmethod
    def get_source(self, *args):
        pass

    @abstractmethod
    def parser(self, source):
        pass

    @abstractmethod
    def start(self, *args):
        pass


class GetJobDetail(BaseCrawler):
    URL = None

    def start(self, url: str):
        self.URL = url
        source, url, status = self.get_source()
        return self.parser(source)

    def get_source(self):
        # get jobs detail source code
        try:
            response = self.session.get(self.URL)
        except requests.RequestException as error:
            raise Exception(f'Something went wrong while connecting to {self.URL}.\nDetail: {error}')
        # handle 404 error
        if response.status_code == 404:
            raise Exception(f"404 Error: Your provided url does not exists.\n {self.URL}")

        return response.text, response.url, response.status_code

    def parser(self, source):
        return dict(url=self.URL, detail=JobDetailParser(source).start())


class GetJobs(BaseCrawler):
    _LINKS = []  # to store all parsed links

    def __init__(self, cookies_path=COOKIES_JSON_PATH, page=1, *args, **kwargs):
        super().__init__(cookies_path, *args, **kwargs)
        # create filter base on arguments
        self.filters = dict(locations=[kwargs.get('locations')],
                            categories=[kwargs.get('categories')],
                            keywords=[kwargs.get('keywords')])
        self.page = page

    def start(self):
        """
        class manager
        """
        for page in range(self.page):
            # request and get source code
            source, url, status = self.get_source(JOBINJA_JOBS_URL, page=page + 1)
            # parse the source code
            pars_result = self.parser(source)
            # break the loop if there is no result
            if not pars_result:
                break
            # add parsed links to links container
            self._LINKS.extend(pars_result)

    def _pars_filter(self):
        """
        use filter to create params which jobinja website will except.
        """
        params = dict()
        for key in self.filters:
            for item in self.filters[key]:
                if item is None:
                    # if there is no item, we break the loop
                    break
                for index, value in enumerate(item):
                    params[f'filters[{key}][{index}]'] = value
        return params

    def get_source(self, url: str, page: int):
        """
        :param url: the url to request
        :param page: the page parameter
        :return: the source code
        """
        # get request params
        params = self._pars_filter()
        params['page'] = page
        # request
        try:
            response = self.session.get(url, params=params)
        except requests.RequestException:
            raise Exception(f'Something went wrong while connecting to jobinja.ir')

        # return response
        return response.text, response.url, response.status_code

    def parser(self, source):
        """
        :param source: get the html source code to parse
        :return: the parsed links of jobs
        """
        return JobsParser(source).start()

    def get_jobs_detail(self, crawler :GetJobDetail=GetJobDetail()):
        """
        this method will use GetJobDetail crawler to crawl each links.
        this will keep our main.py file clean.
        """
        final_crawled = list()
        for link in self.links:
            result = crawler.start(link)
            final_crawled.append(dict(url=link,
                                      detail=result))
        return tuple(final_crawled)
    
    @property
    def links(self):
        return tuple(self._LINKS)
