import re
from bs4 import BeautifulSoup as bs


class PageParcer():
    """
    A parser for HTML
    """

    def __init__(self, html, parcer):
        """
        :param html: html raw text
        :param parcer: parcer used to parce the page
        """

        self.soup = bs(html, 'html.parser')
        # Indicates which parser to choose
        self.parcer = parcer


    def text(self):
        """
        :return: parsed text
        """

        if self.parcer == 'first_parcer':
            text = self.soup.get_text(separator=' ')
            text = re.sub(r'\n', ' ', text)
            text = re.sub(r'\t', ' ', text)
            text = re.sub(r' +', ' ', text)
            return text

        if self.parcer == 'second_parcer':
            text = self.soup.get_text(separator=' ')
            text = re.sub(r'', ' ', text)
            text = re.sub(r'\t', ' ', text)
            text = re.sub(r' +', ' ', text)
            return text

    def links(self, home_page_url):
        """
        :param home_page_url: URL of the homepage
        :return: List with the links that contains the homepage path in it path
        """

        if self.parcer == 'first_parcer':
            links = []
            for link in self.soup.find_all('a'):
                link_str = str(link.get('href'))
                # Search if the link belongs to the root page or if the href refers to itself
                if 'http' not in link_str  and '.pdf' not in link_str and '.png' not in link_str and '.PNG' not in link_str \
                        and '.jpeg' not in link_str and '.JPEG' not in link_str and '.jpg' not in link_str \
                        and '.JPG' not in link_str and link_str != '#' and link_str != './':

                    if len(link_str) > 0 and link_str[0] == '/':
                        while link_str[0] == '/':
                            link_str = link_str[1:]
                            if len(link_str) == 0:
                                break
                    link_str = f'/{link_str}'

                    link_split = link_str.split('/')
                    if len(link_split) > 1:
                        if link_split[-1] != link_split[-2]:
                            links.append(f"{home_page_url}{link_str}")
                    else:
                        links.append(f"{home_page_url}{link_str}")

            return links



