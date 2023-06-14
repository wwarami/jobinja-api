from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self, source):
        self.parser = BeautifulSoup(source, 'html.parser')

    @abstractmethod
    def start(self):
        pass


class JobsParser(Parser):
    def start(self):
        # get jobs list
        try:
            container = self.parser.find('ul', attrs={'class': 'o-listView__list c-jobListView__list'})
            links = container.find_all('a', attrs={'class': 'c-jobListView__titleLink'})
            return (link.get('href') for link in links)
        except AttributeError:
            return False


class JobDetailParser(Parser):
    def start(self):
        """
        class manager
        """
        data = dict(
            title=self.__get_title__(),
            category=self.__get_category__(),
            location=self.__get_location__(),
            salary=self.__get_salary__(),
            description=self.__get_description__(),
            job_id=self.__get_job_id__()
        )
        return data

    def __get_title__(self):
        try:
            container = self.parser.find('div',
                                    attrs={'class': 'c-jobView__titleText'}
                                    )  # delete the space at the end of title
            return container.find('h1').text[2:]
        except:
            pass

    def __get_category__(self):
        try:
            # get category container
            selector = '.c-jobView__firstInfoBox > li:nth-child(1) > div:nth-child(2)'
            container = self.parser.select_one(selector)

            return container.find('span').text
        except:
            pass

    def __get_location__(self):
        try:
            # get location container
            selector = '.c-jobView__firstInfoBox > li:nth-child(2)'
            container = self.parser.select_one(selector)
            # return only state, so we split the text
            item = container.find('span').text
            return item.split()[0]
        except:
            pass

    def __get_salary__(self):
        try:
            # get the ul that holds salary using css selector
            ul_selector = '.c-jobView__firstInfoBox'
            ul_container = self.parser.select_one(ul_selector)
            # loop threw ul items until we get the one with title salary
            for li in ul_container.find_all('li'):
                if li.find_next('h4').text == 'حقوق':
                    return li.find_next('span').text  # return the salary
        except:
            pass

    def __get_description__(self):
        try:
            # get description div
            container = self.parser.find('div',
                                         attrs={
                                             'class': ['o-box__text s-jobDesc c-pr40p',
                                                       'o-box__text s-jobDesc u-ltr c-pl40p'
                                                       ]
                                         }
                                         )
            # print inner HTML content without the div tag around it
            inner_html = ''.join(str(tag) for tag in container.contents)
            return inner_html
        except:
            pass

    def __get_job_id__(self):
        try:
            uniq_url = self.parser.find('a', attrs={'class': 'c-sharingJobOnMobile__uniqueURL u-textSmall c-muteLink'})
            # get jib's id from it's uniq url
            return uniq_url.get('href').split('/')[-1]
        except:
            pass
