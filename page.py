import requests
from page_parcer import *
from urllib3.exceptions import NewConnectionError, LocationParseError
from requests.exceptions import ConnectionError, InvalidURL

class Page:
    def __init__(self, link, parcer_name='first_parcer'):
        self.html_status = None
        self.label = None
        self.depth = None
        self.links_list = []
        self.text = ''
        self.link = link
        self.broken = False
        headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
        try:
            self.html = requests.get(self.link, headers=headers)
        except ConnectionError as e:
            self.broken = True
            self.text = e
        except NewConnectionError as e:
            self.broken = True
            self.text = e
        except LocationParseError as e:
            self.broken = True
            self.text = e
        except InvalidURL as e:
            self.broken = True
            self.text = e
        if not self.broken:
            self.parcer = PageParcer(self.html.text, parcer_name)


    def get_page_text(self):
        if not self.broken:
            try:
                self.text = self.parcer.text()
            except UnicodeEncodeError:
                self.text = f'UnicodeEncodeError. Encode used: {self.encoding}. ' \
                                f'Apparent encode: {html.apparent_encoding}'
            # Get the status of the Response object
            try:
                self.html_status = self.html.status_code
            except UnicodeEncodeError:
                self.html_status = f'UnicodeEncodeError. Encode used: {self.encoding}. ' \
                                       f'Apparent encode: {html.apparent_encoding}'

    def get_page_links(self, homepage_link):
        if not self.broken:
            self.links_list = self.parcer.links(homepage_link)


    def __repr__(self):
        return self.link


