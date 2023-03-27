import numpy
from time import sleep

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode

from mercados.mercado import Mercado

class CrawlerSuperTonin(Mercado):
        
    def Browsingsite(self):
        print('configurando...')
        
        url = "https://www.supertonin.com.br/"
        self.browser.get(url)
        sleep(5)
        element = self.browser.find_element(By.CSS_SELECTOR,'a.popup-next-tip:nth-child(4)')
        element.click()
        sleep(0.5)
        to_click = self.browser.find_element(By.CSS_SELECTOR,'.header-text > div:nth-child(2)')
        to_click.click()
        sleep(0.5)
        
        # select_city = self.browser.find_element(By.XPATH,'/html/body/header/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div')
        select_city = self.browser.find_element(By.CSS_SELECTOR,'div[tooltip="Araraquara - Vl. Santana - LJ 11 - Superatacado"]')
        select_city.click()
        sleep(0.5)
        
        print('configuração concluida!')
        print()
        
    def Getsearch(self):
        print('fazendo a busca...')
        url = "https://www.supertonin.com.br/busca?order=PD&q=" + self.searchProduct
        self.browser.get(url)
        print('busca feita!')
        print()

    def Getprodutos(self):
        
        print('carregando produtos...')
        
        dataProducts = []

        # elemento ul trazendo a quantidade de li(s) que o elemento possui
        paginations = self.browser.find_elements(By.CSS_SELECTOR, 'ul.pagination > li')
        page = 1
        
        while (page <= numpy.size(paginations)):
            # print(pages.text)
            url_page = "https://www.supertonin.com.br/busca?order=PD&q=" + self.searchProduct + "&pg=" + str(page)
            # print(url_page)
            self.browser.get(url_page)
            sleep(10)
            
            page_content = self.browser.page_source

            site = BeautifulSoup(page_content, 'html.parser')
            # busca de todos os produtos
            product_list = site.findAll('div', attrs={'class': 'produto'})

            for products in product_list:

                product_name = products.select('div.title > a')[0].text
                
                if (product_name.lower().find(unidecode(self.searchProduct.lower())) == 0):

                    product_category = self.searchProduct
                    product_seller = products.find('div', attrs={'class': 'fabricante ng-binding'}).text
                    product_market = 'Tonin'
                    product_image = products.find('img', attrs={'class': 'produto-img lazy'})['src']
                    product_price = products.find('span', attrs={'class': 'ng-binding'}).text
                    product_price = float(product_price.replace('Por: R$', '').replace('De: R$ ', '').replace(',','.'))
                    
                    dataProducts.append([product_name, product_category, product_seller, product_market, product_image, product_price])
            page += 1

        data = pd.DataFrame(dataProducts, columns=['Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preco']).sort_values('Preco')
        # print(data)

        print(f'produtos encontrados: {numpy.size(dataProducts)}')
        print('carregamento concluido!')
        print()
        
        return data

    def processa(self):
        print('### INCIANDO SUPERTONIN ###')
        print()
        
        self.Browsingsite()
        sleep(5)
        self.Getsearch()
        sleep(5)
        data = self.Getprodutos()
        
        print('### SUPERTONIN CONCLUIDO! ###')
        print()
        
        return data.iloc[0]

