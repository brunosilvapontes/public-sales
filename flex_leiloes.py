from urllib.request import urlopen
from bs4 import BeautifulSoup


# Access homepage
home_page = "https://www.flexleiloes.com.br/"
html = urlopen(home_page)
bsObj = BeautifulSoup(html.read(), 'html.parser')

# Search links with the word 'Imóveis' in the home page
link_list_home = []
for link in bsObj.find_all('a'):
    if 'Imóveis' in link:
        link_list_home.append(link.get('href'))

# Access property page
properties_page = home_page + link_list_home[1]
html = urlopen(properties_page)
bsObj = BeautifulSoup(html.read(), 'html.parser')

# Create a list of property links
list_link_properties = []
for link in bsObj.find_all('a'):
    if 'detalhe' in str(link.get('href')):
        list_link_properties.append(link.get('href'))

list_link_properties = list(set(list_link_properties))
list_link_properties.sort()

# Get informations in the property page
for property_link in list_link_properties:
    # Get property page
    property_page = home_page + property_link
    html = urlopen(property_page)
    bsObj = BeautifulSoup(html.read(), 'html.parser')


    # Get auctions ending date
    ending_date = str(bsObj.find('div', {'class': 'encerra'}).text)
    # Get initial bid
    initial_bid = str(bsObj.find('span', {'class': 'lance'}).text)

    # Get property description
    span_descricao = bsObj.find_all('span', {'class': 'descricao'})
    character_index = 0
    appraised_text = ''
    for span in span_descricao[0]:
        # Get the appraised property value inside description
        if 'AvaliaÃ§Ã£o' in str(span.text):
            appraised_value_start_character = str(span.text).find('AvaliaÃ§Ã£o') + 16
            character_index = appraised_value_start_character
            appraised_text = str(span.text)

        if 'DO BEM' in str(span.text):
            description = str(span.text)
            description = description.replace('DESCRIÃÃO DO BEM:', 'DESCRICAO DO BEM:')
            description = description.replace('imÃ³vel', 'imovel')
            description = description.replace('ImÃ³vel', 'Imovel')
            description = description.replace('imÃ³veis', 'imoveis')
            description = description.replace('ImÃ³veis', 'Imoveis')
            description = description.replace('Ã¡rea', 'area')
            description = description.replace('matrÃ­cula', 'matricula')
            description = description.replace('AvaliaÃ§Ã£o', 'Avaliacao')
            description = description.replace('OfÃ­cio', 'Oficio')
            description = description.replace('Â', '')


    appraised_value = 'Avaliação: R$ '
    while True:
        if appraised_text[character_index] != ' ' and character_index < len(appraised_text) - 1 :
            #print(len(descricao))
            #print(numero_caractere)
            appraised_value = appraised_value + appraised_text[character_index]
            character_index += 1
        else:

            break

    # Get the minimum bid value in 'hasta 1'
    #for i in range(len(list_span)):
    #    if 'Lance' in str(list_span[i].text):
    #        print(list_span[i].text)
    if 'Encerra' not in ending_date:
        ending_date = 'Sem data de encerramento'

    print()
    print('#' * 30)
    print('#' * 30)
    print()
    print(property_page)
    print(ending_date)
    print(appraised_value)
    print(initial_bid)
    print(description)

