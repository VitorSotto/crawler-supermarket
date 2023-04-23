import numpy
from time import sleep
import uuid

from selenium.webdriver.common.by import By
from mercados.mercado import Mercado
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode



class CrawlerSuperTonin(Mercado):
        
    def Browsingsite(self):
        print('configurando...')
        
        url = "https://www.supertonin.com.br/"
        self.browser.get(url)
        sleep(5)
        element = self.browser.find_element(By.CSS_SELECTOR,'a.popup-next-tip:nth-child(4)')
        element.click()
        sleep(2)
        to_click = self.browser.find_element(By.CSS_SELECTOR,'.header-text > div:nth-child(2)')
        to_click.click()
        sleep(0.5)
        
        # select_city = self.browser.find_element(By.XPATH,'/html/body/header/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div')
        select_city = self.browser.find_element(By.CSS_SELECTOR,'div[tooltip="Araraquara - Vl. Santana - LJ 11 - Superatacado"]')
        select_city.click()
        sleep(0.5)
        
        print('configuração concluida!')
        print()

    def Getsearch(self,Product):

        print('fazendo a busca...')
        url = "https://www.supertonin.com.br/busca?order=PD&q=" + str(Product)
        self.browser.get(url)
        print('busca feita!')
        print()

    def Getprodutos(self,Product):
        print('carregando produtos...')

        dataProduct = []

        # elemento ul trazendo a quantidade de li(s) que o elemento possui
        paginations = self.browser.find_elements(By.CSS_SELECTOR, 'ul.pagination > li')
        page = 1
        
        while (page <= numpy.size(paginations)):
            # print(pages.text)
            url_page = "https://www.supertonin.com.br/busca?order=PD&q=" + str(Product) + "&pg=" + str(page)
            # print(url_page)
            self.browser.get(url_page)
            sleep(10)
            
            page_content = self.browser.page_source

            site = BeautifulSoup(page_content, 'html.parser')
            # busca de todos os produtos
            product_list = site.findAll('div', attrs={'class': 'produto'})

            for products in product_list:

                product_name = products.select('div.title > a')[0].text
                
                if (product_name.lower().find(unidecode(str(Product.lower()))) == 0):
                    product_id = str(uuid.uuid4())
                    price_id = str(uuid.uuid4())
                    product_category = Product
                    product_seller = products.find('div', attrs={'class': 'fabricante ng-binding'}).text
                    product_market = 'Tonin'
                    product_image = products.find('img', attrs={'class': 'produto-img lazy'})['src']
                    product_price = products.find('span', attrs={'class': 'ng-binding'}).text
                    product_price = float(product_price.replace('Por: R$', '').replace('De: R$ ', '').replace(',','.'))
                    date_product = date.today()
                    # date = date_product.strftime('%d/%m/%Y')
                    
                    dataProduct.append([product_id, price_id, product_name, product_category, product_seller, product_market, product_image, product_price, date_product])
            page += 1

        data = []
        data = pd.DataFrame(dataProduct, columns=['Id_Produto', 'Id_Preco','Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preco', 'Data']).sort_values('Preco')
        # print(data)
        

        print('carregamento concluido!')
        print()
        
        # array de todos os meus produtos buscados
        return pd.DataFrame(data.iloc[0]).transpose()
    

    def processa(self):
        print('### INCIANDO SUPERTONIN ###')
        print()
        
        self.Browsingsite()
        sleep(5)

        # DataFrame para tabela de produtos
        products = pd.DataFrame(columns=['Id_Produto', 'Nome', 'Fornecedor', 'Mercado', 'Imagem', 'Id_Preco'])
        # DataFrame para tabela de preços
        prices = pd.DataFrame(columns=['Id_Preco', 'Categoria', 'Preco', 'Data', 'Id_Produto'])
        res = []
    
        for Product in self.searchProducts:
            print(Product)
            self.Getsearch(Product)
            sleep(5)

            first_line = (self.Getprodutos(Product))
            products = pd.concat([products, first_line], join='inner', ignore_index=True)
            prices = pd.concat([prices, first_line], join='inner', ignore_index=True)

        print('Busca completa!')
        print()

        print('### SUPERTONIN CONCLUIDO! ###')
        print()

        res.append(products)
        res.append(prices)
        
        return res
