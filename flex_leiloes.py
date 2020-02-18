# Python 3.7.4
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
from database.models import testcollection

source = 'FlexLeilões'

def exec():
    home_page = "https://www.flexleiloes.com.br/"

    # Access properties page
    propertiesPage = 'https://www.flexleiloes.com.br/categorias/1/'
    html = urlopen(propertiesPage)
    bsObj = BeautifulSoup(html.read(), 'html.parser')

    # Create a list of property links
    list_link_properties = []
    for link in bsObj.find_all('a'):
        if 'detalhe' in str(link.get('href')):
            list_link_properties.append(link.get('href'))
    list_link_properties = list(set(list_link_properties))
    list_link_properties.sort()

    list_link_properties = ['detalhe-lote/1192/1/'] # TODO REMOVE

    # Get informations in the property page
    for property_link in list_link_properties:
        # Get property page
        property_page = home_page + property_link
        html = urlopen(property_page)
        bsObj = BeautifulSoup(html.read(), 'html.parser', from_encoding="utf-8") 

        # Get auction title
        title = bsObj.find('h2', {'class': 'texto-titulo3'}).text
        # dbProperty = testcollection(title=title)
        # dbProperty.save()

        # Get auction status
        status = list(bsObj.find('span', {'id': 'status'}).children)[0].get_text()

        # Get current bid
        currentBid = bsObj.find('b', {'id': 'lance_atual'}).text

        # Get starting bid
        startingBid = bsObj.find('span', {'class': 'lance'}).text

        # Get description
        description = list(bsObj.find('span', {'class': 'descricao'}).children)[0].get_text()

        # Get evaluation
        startEvaluation = description.lower().index('avaliação')
        evaluation = description[startEvaluation:]

        
        # # Get the minimum bid value in 'hasta 1'
        # #for i in range(len(list_span)):
        # #    if 'Lance' in str(list_span[i].text):
        # #        print(list_span[i].text)
        # if 'Encerra' not in ending_date:
        #     ending_date = 'Sem data de encerramento'
        sleep(1)

