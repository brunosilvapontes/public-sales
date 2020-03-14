import requests
from page import *
from page_parcer import PageParcer
from urllib3.exceptions import NewConnectionError, LocationParseError
from requests.exceptions import ConnectionError, InvalidURL



# List of sites to be crawled
sites_list = {'capital_leiloes': 'https://www.capitalleiloes.com.br',
              'leiloes_judiciais': 'https://www.leiloesjudiciaisdf.com.br',
              'leiloeiros_de_brasilia': 'https://www.leiloeirosdebrasilia.com.br',
              'brasilia_leiloes': 'https://www.brasilialeiloes.com.br',
              'df_leiloes': 'https://www.dfleiloes.com.br',
              'mult_leiloes': 'https://multleiloes.vlance.com.br',
              'parque_dos_leiloes': 'https://www.parquedosleiloes.com.br',
              'flex_leiloes': 'https://www.flexleiloes.com.br',
              'jussiara_leiloes': 'https://www.jussiaraleiloes.com',
              'luiz_leiloes': 'https://www.luizleiloes.com.br',
              'maria_vitorino_leiloeira': 'https://www.mariavitorinoleiloeira.com.br',
              'moacira': 'https://www.moacira.lel.br',
              'paulo_tolentino': 'https://www.paulotolentino.com.br',



              } # Insert the link with out the '/' in the end

# Iterate over sites is sites_list
for home_page_name, home_page_link in sites_list.items():
    home_page = HomePage(home_page_link)
    # Get the Response object
    html = requests.get(home_page.link)
    # Get the raw html text from the home page
    html_raw_text = html.text
    parcer = PageParcer(html_raw_text)
    # Get the links from the home page if the link is a child of the home page url
    home_page.links_list = parcer.links(home_page.link)
    # Parce the raw text from the home page
    home_page.text = parcer.text()


    # Recursive function to create a Page object for each page that contains the home page path in the url
    # Append all Page objects in the home_page.pages_list attribute
    def search_links(page, encoding=html.apparent_encoding, verbose=0):
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
            print('\n-----------------------------------------\n')

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
                    home_page.broken_links[link] = e
                    return
                except NewConnectionError as e:
                    home_page.broken_links[link] = e
                    return
                except LocationParseError as e:
                    home_page.broken_links[link] = e
                    return
                except InvalidURL as e:
                    home_page.broken_links[link] = e
                    return

                # Get the Response object
                html = requests.get(page.link)
                # Get the raw text from the html (Response) object
                html_raw_text = html.text
                parcer = PageParcer(html_raw_text)
                # Get the links from the new page
                new_page.links_list = parcer.links(home_page.link)
                # Parce the raw text from the new page
                try:
                    #new_page.text = bytes(parcer.text(), encoding=encoding)
                    new_page.text = parcer.text()
                except UnicodeEncodeError:
                    new_page.text = f'UnicodeEncodeError. Encode used: {encoding}. ' \
                                    f'Apparent encode: {html.apparent_encoding}'
                # Get the status of the Response object
                try:
                    new_page.html_status = html.status_code
                except UnicodeEncodeError:
                    new_page.html_status = f'UnicodeEncodeError. Encode used: {encoding}. ' \
                                           f'Apparent encode: {html.apparent_encoding}'
                # Check if the Response status code is less then 400
                new_page.html_ok = html.ok
                home_page.pages_list.append(new_page)
                search_links(new_page, verbose=int(verbose))



    search_links(home_page, verbose=0)
    home_page.to_json(home_page_name)
    home_page.to_txt(home_page_name)



