class Page:
    def __init__(self, link):
        self.link = link
        self.text = ""
        self.links_list = []
        self.html_ok = ''
        self.html_status = ''

    def __repr__(self):
        return self.link


class HomePage(Page):
    def __init__(self, link):
        Page.__init__(self, link)
        self.pages_list = []
        self.all_links = []
        self.exception_links = {}

    def __repr__(self):
        return self.link


