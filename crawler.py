import requests
from bs4 import BeautifulSoup as bs
from page import *
from page_parcer import PageParcer

# List of sites to be crawled
sites_list = {'flex_leiloes': 'https://www.flexleiloes.com.br/'}

#
for home_page_name, home_page_link in sites_list.items():
    home_page = HomePage(home_page_link)
    # Get the raw html text from the home page
    html_raw_text = requests.get(home_page.link).text
    parcer = PageParcer(html_raw_text)
    # Get the links from the home page if the link is a child of the home page url
    home_page.links_list = parcer.links(home_page.link)
    # Parce the raw text from the home page
    home_page.text = parcer.text()

    # Recursive function to create a Page object for each page that contains the home page path in the url
    # Append all Page objects in the home_page.pages_list attribute
    def search_links(page, verbose=0):
        new_links = []
        # Verify if the links from the current page was already crawled
        for link in page.links_list:
            if link not in home_page.all_links:
                # If it is a new link, append it to the list of all links in the home_page object
                home_page.all_links.append(link)
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
            print('\n-------------------------------------------\n')

        # Return condition for the recursive function
        if len(new_links) == 0:
            return

        # If there are links to be crawled
        else:
            for link in new_links:
                new_page = Page(link)
                # Return a Response object for the link
                html = requests.get(link)
                # Get the raw text from the html (Response) object
                html_raw_text = html.text
                parcer = PageParcer(html_raw_text)
                # Get the links from the new page
                new_page.links_list = parcer.links(home_page.link)
                # Parce the raw text from the new page
                new_page.text = parcer.text()
                # Get the status of the Response object
                new_page.html_status = html.status_code
                # Check if the Response status code is less then 400
                new_page.html_ok = html.ok
                home_page.pages_list.append(new_page)
                search_links(new_page, verbose=int(verbose))

    search_links(home_page, verbose=0)


    with open(f'/Users/gustavo/Desktop/Gustavo/Projetos/public-sales/{home_page_name}.txt', 'w') as file:
        file.write('*************** HOME PAGE ***************\n')
        file.write(f'{home_page.link}\n')
        file.write('\n')
        file.write(f'All links:\n')
        file.write(f'Number of links: {len(home_page.all_links)}\n')
        file.write(f'{home_page.all_links}\n')
        file.write('\n')
        file.write('All pages\n')
        file.write(f'Number of pages: {len(home_page.pages_list)}\n')
        for page in home_page.pages_list:
            file.write(f'{page.link} - {page.html_status} | ')
        file.write('\n\n')
        file.write('Home page text\n')
        file.write(f'{home_page.text}\n')
        file.write('\n')
        file.write('\n')
        file.write('\n')
        for page in home_page.pages_list:
            file.write('-------------- NEW PAGE --------------\n')
            file.write(f'{page.link}\n')
            file.write('\n')
            file.write('Page text\n')
            file.write(f'{page.text}\n')
            file.write('\n')
            file.write('\n')
            file.write('\n')

'''
    for page in home_page.pages_list:
        print('Link da pagina')
        print(page.link)
        print('Status da pagina')
        print(page.html_status)
        print('Texto da pagina')
        print(page.text)
        print('\n---------------------------------------\n')

    print(len(home_page.pages_list))

'''