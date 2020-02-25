# Python 3.7.4
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
from database.models import testcollection
from datetime import datetime
from unicodedata import normalize

source = 'FlexLeilões'

def scrap():
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

    list_link_properties = ['detalhe-lote/1193/1/'] # TODO REMOVE

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
        descriptionIter = list(bsObj.find('span', {'class': 'descricao'}).children)
        description = descriptionIter[0].get_text()

        # Get evaluation
        startEvaluation = description.lower().index('avaliação')
        evaluation = description[startEvaluation:]
        
        # Get 1st and 2nd auction info
        auction1Opening, auction1Closure, auction1Bid = None, None, None
        auction2Opening, auction2Closure, auction2Bid = None, None, None
        for descriptionPart in descriptionIter:
            descText = descriptionPart.get_text().lower() if descriptionPart else None
            if not descText or ('hasta' not in descText and 'lance' not in descText):
                continue

            if '1ª' in descText:
                if 'abertura' in descText:
                    auction1Opening = getDescriptionDate(descText)
                elif 'encerramento' in descText:
                    auction1Closure = getDescriptionDate(descText)
            elif '2ª' in descText:
                if 'abertura' in descText:
                    auction2Opening = getDescriptionDate(descText)
                elif 'encerramento' in descText:
                    auction2Closure = getDescriptionDate(descText)
            elif 'lance' in descText:
                print(f'LANCE : {descText}')
        print(f'1 open {auction1Opening}')
        print(f'1 close {auction1Closure}')
        print(f'2 open {auction2Opening}')
        print(f'2 close {auction2Closure}')
        sleep(1)


def getDescriptionDate(descText):
    hastaParts = descText.split(' ')
    
    dateStr = None
    timeStr = None
    for hastaPart in hastaParts:
        hastaPartNormalized = normalize('NFKD', hastaPart.strip())

        # Get date
        if '/' in hastaPartNormalized:
            # Find where the date begins in the string because .split(' ')
            # doesn't work well in HTML text
            for i, letter in enumerate(hastaPartNormalized):
                if letter.isnumeric() and hastaPartNormalized.strip()[i+2] == '/':
                    dateStr = hastaPartNormalized[i:i+10]
                    break
        # Get time
        elif len(hastaPartNormalized) > 2 and hastaPartNormalized[2] == 'h':
            timeStr = hastaPartNormalized

    if dateStr and timeStr:
        return datetime.strptime(f"{dateStr}--{timeStr}", '%d/%m/%Y--%Hh%Mmin')

    return None