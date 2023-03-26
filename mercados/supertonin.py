from time import sleep

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

from mercados.mercado import Mercado

class CrawlerSuperTonin(Mercado):
    
    dataProducts = []
        
    def Browsingsite(self):
        url = "https://www.supertonin.com.br/"
        self.browser.get(url)
        sleep(2)
        element = self.browser.find_element(By.CSS_SELECTOR,'a.popup-next-tip:nth-child(4)')
        element.click()
        sleep(0.5)
        to_click = self.browser.find_element(By.CSS_SELECTOR,'.header-text > div:nth-child(2)')
        to_click.click()
        sleep(0.5)
        select_city = self.browser.find_element(By.XPATH,'/html/body/header/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div')
        select_city.click()
        sleep(0.5)
        
    def Getsearch(self):

        url = "https://www.supertonin.com.br/busca?order=PD&q=" + self.searchProduct
        self.browser.get(url)

    def Getprodutos(self):
        page_content = self.browser.page_source

        site = BeautifulSoup(page_content, 'html.parser')
        # busca de todos os produtos
        product_list = site.findAll('div', attrs={'class': 'produto'})
        # elemento ul trazendo a quantidade de li(s) que o elemento possui
        paginations = self.browser.find_element(By.CSS_SELECTOR,'.pagination').text
        
        for pages in paginations:

            for products in product_list:

                product_name = products.find('a', attrs={'class': 'ng-binding'}).text
                
                if (product_name.lower().find(self.searchProduct.lower()) == 0):

                    product_category = self.searchProduct
                    product_seller = products.find('div', attrs={'class': 'fabricante ng-binding'}).text
                    product_market = 'Tonin'
                    product_image = products.find('img', attrs={'class': 'produto-img lazy'})['src']
                    product_price = products.find('span', attrs={'class': 'ng-binding'}).text
                    product_price = product_price.replace('Por: R$', '').replace(',','.')

                    # print("Nome do produto: ", product_name)
                    # print("Categoria: ", product_category)
                    # print("Fabricante: ", product_seller.text)
                    # print("Mercado: ", product_market)
                    # print("Imagem: ", product_image)
                    # print("Preço: ", product_price)

                    # print()
                    # recuperar a li, trazer a quantidade, laço de repetição chamando o get produtos passando a nova url
                    self.dataProducts.append([product_name, product_category, product_seller, product_market, product_image, product_price])

        data = pd.DataFrame(self.dataProducts, columns=['Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preço']).sort_values('Preço')
        print(data)

        url = "https://www.supertonin.com.br/busca?order=PD&q=" + self.searchProduct + "pg=" + pages
        self.browser.get(url)

        return data

    def processa(self):
        self.Browsingsite()
        sleep(10)
        self.Getsearch()
        sleep(10)
        data = self.Getprodutos()
        return data.iloc[0]

