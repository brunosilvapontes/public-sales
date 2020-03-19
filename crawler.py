import json
import csv
from page import Page



class Crawler:
    def __init__(self, homepage_name, homepage_link, parcer_name='first_parcer', encoding='utf-8'):
        """
        :param homepage: HomePage object to be crawled
        :param parcer: parcer chosen
        """
        self.all_links = []
        self.broken_links = {}
        self.pages_list = []
        self.parcer_name = parcer_name
        self.encoding = encoding
        self.homepage = Page(homepage_link, parcer_name=parcer_name)
        self.homepage.get_page_text()
        self.homepage.get_page_links(homepage_link)
        self.homepage.depth = 0
        self.pages_list.append(self.homepage)


    # Recursive function to create a Page object for each page that contains the home page path in the url
    # Append all Page objects in the home_page.pages_list attribute
    def crawl(self, page='homepage', verbose=0):
        new_links = []
        if page == 'homepage':
            page = self.homepage

        # Verify if the links from the current page was already crawled
        if page.links_list:
            for link in page.links_list:
                if link not in self.all_links:
                    # If it is a new link, append it to the list of all links in the home_page object
                    self.all_links.append(link)
                    # List of links to be crawled
                    new_links.append(link)

        if verbose == 1:
            print('link da pagina')
            print(page.link)
            print(page.html_status)
            print('lista de links da pagina')
            print(page.links_list)
            print('novos links')
            print(len(new_links))
            print(new_links)
            print('\n-----------------------------------------\n')

        # Return condition for the recursive function
        if len(new_links) == 0:
            return

        # If there are links to be crawled
        else:
            for link in new_links:
                new_page = Page(link=link)
                new_page.get_page_text()
                new_page.get_page_links(self.homepage.link)
                new_page.depth = page.depth + 1
                self.pages_list.append(new_page)
                self.crawl(page=new_page, verbose=int(verbose))



    def to_json(self, file_name):
        """
        :param file_name: json file name
        :return: a json file with pages object attributes
        """
        pages_attributes_list = []

        if file_name[-5:] != '.json':
            file_name = f'{file_name}.json'

        file_path = f'crawled pages/{file_name}'

        for page in self.pages_list:
            pages_attributes_list.append(
                {
                'link': page.link,
                'status': page.html_status,
                'label': '',
                'text': str(page.text)
                })

        #TODO pages['broken links'] = self.broken_links

        pages_json = json.dumps({'pages': pages_attributes_list}, ensure_ascii=False).encode(encoding=self.encoding)

        with open(file_path, 'w') as f:
            f.write(pages_json.decode())

    def to_txt(self, file_name):
        """
        :param file_name: txt file name
        :return: txt file with pages object attributes
        """
        if file_name[-4:] != '.txt':
            file_name = f'{file_name}.txt'

        file_path = f'crawled pages/{file_name}'

        with open(file_path, 'w') as f:
            f.write('########## RESUME ##########\n\n')
            f.write(f'Number of pages: {len(self.pages_list)}\n\n')
            for page in self.pages_list:
                f.write(f'{page.link} - {page.html_status}\n')
            f.write('\n\n\n')


            f.write('########## PAGES CONTENT ##########')
            f.write('\n\n\n')
            for page in self.pages_list:
                f.write(f'{page.link}\n\n')
                f.write(f'Page depth: {page.depth}\n\n')
                f.write(f'Page status: {page.html_status}\n\n')
                if page.links_list:
                    f.write(f'Number of links: {len(page.links_list)}\n\n')
                    for link in page.links_list:
                        f.write(f'{link}\n')
                    f.write('\n')
                else:
                    f.write(f'Number of links: 0\n\n')
                f.write('Page text\n\n')
                f.write(f'{page.text}\n\n\n')
                f.write('-------------- NEW PAGE --------------\n\n')


    def to_csv(self, file_name):
        """
        :param file_name: csv file name
        :return: csv file
        """

        if file_name[-4:] != '.csv':
            file_name = f'{file_name}.csv'

        file_path = f'crawled pages/{file_name}'

        with open(file_path, 'w') as f:
            writer = csv.DictWriter(f, ['link', 'status', 'label', 'text'])
            writer.writeheader()
            for page in self.pages_list:
                dic = {'link':page.link, 'status': page.html_status, 'label':'?', 'text': page.text}
                writer.writerow(dic)
