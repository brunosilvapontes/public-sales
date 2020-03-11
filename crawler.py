import socket
import requests
from bs4 import BeautifulSoup as bs
from page import *
from page_parcer import PageParcer
from urllib3.exceptions import NewConnectionError, LocationParseError
from requests.exceptions import ConnectionError, InvalidURL



# List of sites to be crawled
sites_list = {'df_leiloes': 'https://www.dfleiloes.com.br'} # Insert the link with out the '/' in the end

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
                try:
                    html = requests.get(link)
                except ConnectionError as e:
                    home_page.exception_links[link] = e
                    return
                except NewConnectionError as e:
                    home_page.exception_links[link] = e
                    return
                except LocationParseError as e:
                    home_page.exception_links[link] = e
                    return
                except InvalidURL as e:
                    home_page.exception_links[link] = e
                    return

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

    search_links(home_page, verbose=1)


    with open(f'/Users/gustavo/Desktop/Gustavo/Projetos/public-sales/{home_page_name}.txt', 'w') as file:
        file.write('*************** HOME PAGE ***************\n\n')
        file.write(f'{home_page.link}\n\n')
        file.write(f'-All links:\n\n')
        file.write(f'Number of links: {len(home_page.all_links)}\n\n')
        file.write(f'{home_page.all_links}\n\n')
        file.write('-All pages\n\n')
        file.write(f'Number of pages: {len(home_page.pages_list)}\n\n')
        file.write('-Exception links\n\n')
        file.write(f'Number of exceptions: {len(home_page.exception_links)}\n\n')
        file.write(f'{home_page.exception_links}\n\n')
        file.write('-Pages status\n\n')
        for page in home_page.pages_list:
            file.write(f'{page.link} - {page.html_status} | ')
        file.write('\n\n')
        file.write('-Home page text\n\n')
        file.write(f'{home_page.text}\n\n\n\n')
        for page in home_page.pages_list:
            file.write('-------------- NEW PAGE --------------\n\n')
            file.write(f'{page.link}\n\n')
            file.write('Page text\n\n')
            file.write(f'{page.text}\n\n\n\n')

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