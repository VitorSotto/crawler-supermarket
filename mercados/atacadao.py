import numpy
from time import sleep
import uuid
from datetime import date

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

from mercados.mercado import Mercado

class CrawlerAtacadao(Mercado):
    
    def cancelButton(self):
      cancelButton = self.browser.find_element(By.CLASS_NAME, 'close')
      cancelButton.click()

    def selectCEP(self):
      sleep(2)
      cpfSelect = self.browser.find_element(By.ID, 'input-cpf-modal')
      ActionChains(self.browser).click(cpfSelect).perform()
      sleep(1)
      inputCEP = self.browser.find_element(By.ID, 'cep')
      inputCEP.send_keys('14801-600')
      sleep(1)
      
      confirmButton = self.browser.find_element(By.ID, 'btn-confirmar')
      confirmButton.click()

    def acceptCookies(self):
       coockieButton = self.browser.find_element(By.ID, 'onetrust-accept-btn-handler')
       coockieButton.click()

    def search(self, searchProduct):
      searchButton = self.browser.find_element(By.CLASS_NAME, 'js-search-query')
      searchButton.send_keys(searchProduct)
      searchButton.submit()

    def filterCategory(self, searchProduct):
      print('filtrando...')
      print()

      filterProducts = []
      inputsProducts = []
      inputsSelected = []

      filterProducts = self.browser.find_element(By.ID, 'js-product-filter')
      inputsProducts = filterProducts.find_elements(By.TAG_NAME, 'input')

      for inputProduct in inputsProducts:
        if (inputProduct.get_attribute('value').lower().find(searchProduct.lower())==0):
          ActionChains(self.browser).scroll_to_element(inputProduct).perform()
          ActionChains(self.browser).click(inputProduct).perform()
      
      inputsSelected = filterProducts.find_elements(By.CSS_SELECTOR, 'input:checked')
      print(f'filtros selecionados: {numpy.size(inputsSelected)}')
      
      for inputSelected in inputsSelected:
        print(inputSelected.get_attribute('value'))
        
      print('filtragem concluido!')
      print()

    def loading(self):
      print('carregando produtos...')
      
      footer = self.browser.find_element(By.TAG_NAME, 'footer')
      navFooter = footer.find_element(By.TAG_NAME, 'nav')
      ActionChains(self.browser).scroll_to_element(navFooter).perform()
      sleep(1)
      
      loadingDiv = self.browser.find_element(By.CLASS_NAME, 'container-catalogo')
      loadingImg = loadingDiv.find_element(By.TAG_NAME, 'img')
      ActionChains(self.browser).scroll_to_element(loadingDiv).perform()
      
      catalogue = self.browser.find_element(By.CLASS_NAME, 'catalogue')
      products = catalogue.find_elements(By.CLASS_NAME, 'product-box')
      # print(f'produtos encontrados: {numpy.size(products)}')
      
      while(loadingImg.is_displayed()):
        ActionChains(self.browser).scroll_to_element(loadingDiv).perform()
        sleep(5)
        products = catalogue.find_elements(By.CLASS_NAME, 'product-box')
        
      print(f'produtos encontrados: {numpy.size(products)}')
      print('carregamento concluido!')
      print()
      
      for product in products:
        ActionChains(self.browser).scroll_to_element(product).perform()

    def getProduct(self, searchProduct):
      
      print("pegando os produtos...")
      print()
      dataProduct = []

      site = BeautifulSoup(self.browser.page_source, 'html.parser')
      products = site.find_all('div', attrs={'class': 'product-box'})

      for product in products:
        product_id = str(uuid.uuid4())
        price_id = str(uuid.uuid4())
        product_name = product.find('h2',attrs={'class':'product-box__name'}).text
        product_category = searchProduct
        product_img = product.find('img')['src']
        product_supplier = product.find('span',attrs={'class':'js-product-box__supplier'}).text
        product_mercado = 'Atacadão'
        product_price = float(product.find('div', attrs={'class':'product-box__price'}).find('span', attrs={'class':'product-box__price--number'}).text.replace(',','.'))
        product_date = date.today()

        dataProduct.append([product_id, price_id, product_name, product_category, product_supplier, product_mercado, product_img, product_price, product_date])
      
      data = []
      data = pd.DataFrame(dataProduct, columns=['Id_Produto', 'Id_Preco', 'Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preco', 'Data']).sort_values('Preco')
      
      print('produtos pegos!')
      print()
      
      return pd.DataFrame(data.iloc[0]).transpose()

    def processa(self):
      print('### INCIANDO ATACADAO ###')
      print()
      
      print('configurando...')

      self.browser.get('https://www.atacadao.com.br/')

      sleep(15)

      # self.cancelButton()
      self.acceptCookies()
      self.selectCEP()
      
      sleep(0.5)

      print('configuração concluida!')
      print()
      
      products = pd.DataFrame(columns=['Id_Produto', 'Nome', 'Fornecedor', 'Mercado', 'Imagem', 'Id_Preco'])
      prices = pd.DataFrame(columns=['Id_Preco', 'Categoria', 'Preco', 'Data', 'Id_Produto'])
      res = []
      
      for searchProduct in self.searchProducts:

        self.browser.get('https://www.atacadao.com.br/')
        
        print(f'Buscando por {searchProduct}...')
        print()

        self.search(searchProduct)

        sleep(5)

        self.filterCategory(searchProduct)

        sleep(10)

        self.loading()

        sleep(5)

        first_line = self.getProduct(searchProduct)
        
        products = pd.concat([products, first_line], join='inner', ignore_index=True)
        prices = pd.concat([prices, first_line], join='inner', ignore_index=True)
        
        print('Busca completa!')
        print()
      
      print('### ATACADAO CONCLUIDO! ###')
      print()
      
      res.append(products)
      res.append(prices)
      
      return res