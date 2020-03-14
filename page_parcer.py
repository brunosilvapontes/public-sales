import re
from bs4 import BeautifulSoup as bs


class PageParcer():
    """
    A parser for HTML
    """
    def __init__(self, html):
        """
        :param html: HTML raw text
        """
        self.soup = bs(html, 'html.parser')

    def text(self):
        """
        :return: parsed text
        """
        text = self.soup.get_text()
        text = re.sub(r'\n{2,}|\n +|\n\t', '\n', text)
        text = re.sub(r" {2,}|\t+", " ", text)
        return text

    def links(self, home_page_url):
        """
        :param home_page_url: URL of the home page
        :return: List with the links that contains the home page in it
        """
        links = []
        for link in self.soup.find_all('a'):
            link_str = str(link.get('href'))
            # Search if the link belongs to the root page or if the href refers to itself
            if 'http' not in link_str and '.png' not in link_str and '.pdf' not in link_str and '.jpeg' not in link_str and '.jpg' not in link_str and link_str != '#' and link_str != './':
                links.append(f"{home_page_url}{link_str}")
        return links



