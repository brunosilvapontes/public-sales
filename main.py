
from crawler import *
from sklearn.feature_extraction.text import TfidfVectorizer


'''
sites_dict = {'capital_leiloes': 'https://www.capitalleiloes.com.br',
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
}
'''

sites_dict = {'luiz_leiloes': 'https://www.luizleiloes.com.br',
              'maria_vitorino_leiloeira': 'https://www.mariavitorinoleiloeira.com.br',
              'moacira': 'https://www.moacira.lel.br',
              'paulo_tolentino': 'https://www.paulotolentino.com.br'}

for homepage_name, homepage_link in sites_dict.items():
    crawler = Crawler(homepage_name, homepage_link)
    crawler.crawl(verbose=1)
    crawler.to_json(homepage_name)
    crawler.to_txt(homepage_name)
    crawler.to_csv(homepage_name)


'''
for page in crawler.pages_list:
    text_list.append(page.text)



vector = TfidfVectorizer(min_df=2, max_df=0.7, ngram_range=(1,2))
features = vector.fit_transform(text_list)
features.todense()

'''