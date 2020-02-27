# Python 3.7.4
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from unicodedata import normalize

source = 'FlexLeilões'

def getCurrentAuctions(Auction):
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

    list_link_properties = ['detalhe-lote/1170/1/'] # TODO remove

    currentAuctions = []
    # Get informations in the property page
    for property_link in list_link_properties:
        # Get property page
        property_page = home_page + property_link
        html = urlopen(property_page)
        bsObj = BeautifulSoup(html.read(), 'html.parser', from_encoding="utf-8") 

        # Get auction title
        title = bsObj.find('h2', {'class': 'texto-titulo3'}).text
        print(f'Scraping {title}')

        # Get auction status
        status = list(bsObj.find('span', {'id': 'status'}).children)[0].get_text()

        # Get current bid
        currentBid = getPrice(bsObj.find('b', {'id': 'lance_atual'}).text)

        # Get starting bid
        startingBid = getPrice(bsObj.find('span', {'class': 'lance'}).text)

        # Get description
        descriptionIter = list(bsObj.find('span', {'class': 'descricao'}).children)
        description = descriptionIter[0].get_text()

        # Get evaluation
        startEvaluation = description.lower().index('avaliação')
        evaluation = getPrice(description[startEvaluation:])
        
        # Get 1st and 2nd auction info
        auction1Opening, auction1Closure, auction1Bid = None, None, None
        auction2Opening, auction2Closure, auction2Bid = None, None, None
        reached2ndAuction = False
        for descriptionPart in descriptionIter:
            descText = descriptionPart.get_text().lower() if descriptionPart else None
            if not descText or ('hasta' not in descText and 'lance' not in descText):
                continue

            if '1ª' in descText:
                if 'abertura' in descText:
                    auction1Opening = getAuctionDate(descText)
                elif 'encerramento' in descText:
                    auction1Closure = getAuctionDate(descText)
            elif '2ª' in descText:
                reached2ndAuction = True
                if 'abertura' in descText:
                    auction2Opening = getAuctionDate(descText)
                elif 'encerramento' in descText:
                    auction2Closure = getAuctionDate(descText)
            elif 'lance mínimo' in descText:
                if reached2ndAuction:
                    auction2Bid = getPrice(descText)
                else:
                    auction1Bid = getPrice(descText)

        currentAuction = Auction(
            status= status.upper().strip(),
            url= property_page.strip(),
            source= source,
            title= title.upper().strip(),
            currentBid= currentBid,
            startingBid= startingBid,
            description= description,
            evaluation= evaluation,
            auction1Opening= auction1Opening,
            auction1Closure= auction1Closure,
            auction1Bid= auction1Bid,
            auction2Opening= auction2Opening,
            auction2Closure= auction2Closure,
            auction2Bid= auction2Bid
        )
        currentAuctions.append(currentAuction)

        # Wait 1s to avoid overloading flex leilões server
        sleep(1)
    
    return currentAuctions


def getPrice(text):
    # TODO % is causing errors, example: https://www.flexleiloes.com.br/detalhe-lote/1170/1/
    # The price should be stored in cents
    # Example: R$7.000,00 should be stored as 700000
    if not text:
        return None

    price = ''
    for letter in text.replace('.', ''):
        if not letter.isnumeric() and letter != ',':
            continue
        if letter == ',':
            # Ignore the cents value of the price
            break
        price += letter
    
    if price != '':
        return int(f'{price}00')
    return None

def getAuctionDate(descText):
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
        if timeStr[:2] == '24':
            timeStr = f'00{timeStr[2:]}'
        return datetime.strptime(f"{dateStr}--{timeStr}", '%d/%m/%Y--%Hh%Mmin')

    return None