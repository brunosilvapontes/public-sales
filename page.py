import json

class Page:
    def __init__(self, link):
        self.link = link
        self.text = ""
        self.links_list = []
        self.html_ok = ''
        self.html_status = ''

    def __repr__(self):
        return self.link

    def page_printer(self):
        if not page.link:
            return



class HomePage(Page):
    def __init__(self, link):
        Page.__init__(self, link)
        self.pages_list = []
        self.all_links = []
        self.broken_links = {}

    def __repr__(self):
        return self.link

    def to_json(self, file_name):
        """
        :param file_name: json file name
        :return: a json file with pages object attributes
        """
        pages = {}

        if file_name[-5:] != '.json':
            file_name = f'{file_name}.json'

        file_path = f'crawled pages/{file_name}'

        for page in self.pages_list:
            pages[page.link] = {
                'status': page.html_status,
                'text': str(page.text)
            }

        #pages['broken links'] = self.broken_links

        #pages_json = json.dumps(pages, ensure_ascii=False).encode('utf-8')
        pages_json = json.dumps(pages)

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
            f.write('*************** HOME PAGE ***************\n\n')
            f.write(f'{self.link}\n\n')
            f.write(f'-All links:\n\n')
            f.write(f'Number of links: {len(self.all_links)}\n\n')
            f.write(f'{self.all_links}\n\n')
            f.write('-All pages\n\n')
            f.write(f'Number of pages: {len(self.pages_list)}\n\n')
            f.write('-Broken links\n\n')
            f.write(f'Number of broken links: {len(self.broken_links)}\n\n')
            f.write(f'{self.broken_links}\n\n')
            f.write('-Pages status\n\n')
            for page in self.pages_list:
                f.write(f'{page.link} - {page.html_status}\n')
            f.write('\n\n')
            f.write('-Home page text\n\n')
            f.write(f'{self.text}\n\n\n\n')
            for page in self.pages_list:
                f.write('-------------- NEW PAGE --------------\n\n')
                f.write(f'{page.link}\n\n')
                f.write('Page text\n\n')
                f.write(f'{page.text}\n\n\n\n')


