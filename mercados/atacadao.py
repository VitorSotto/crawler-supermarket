import numpy
from time import sleep

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
      cpfSelect = self.browser.find_element(By.ID, 'input-cpf-modal')
      ActionChains(self.browser).click(cpfSelect).perform()
      
      inputCEP = self.browser.find_element(By.ID, 'cep')
      inputCEP.send_keys('14801-600')
      sleep(1)
      
      confirmButton = self.browser.find_element(By.ID, 'btn-confirmar')
      confirmButton.click()

    def acceptCookies(self):
       coockieButton = self.browser.find_element(By.ID, 'onetrust-accept-btn-handler')
       coockieButton.click()

    def search(self):
      searchButton = self.browser.find_element(By.CLASS_NAME, 'js-search-query')
      searchButton.send_keys(self.searchProduct)
      searchButton.submit()

    def filterCategory(self):
      print('filtrando...')
      filterProducts = self.browser.find_element(By.ID, 'js-product-filter')

      inputsProducts = filterProducts.find_elements(By.TAG_NAME, 'input')

      for inputProduct in inputsProducts:
        if (inputProduct.get_attribute('value').lower().find(self.searchProduct.lower())==0):
          ActionChains(self.browser).scroll_to_element(inputProduct).perform()
          ActionChains(self.browser).click(inputProduct).perform()
      
      inputsSelected = filterProducts.find_elements(By.CSS_SELECTOR, 'input:checked')
      print(f'filtros selecionados: {numpy.size(inputsSelected)}')
      
      for inputSelected in inputsSelected:
        print(inputSelected.get_attribute('value'))
        
      print('filtragem concluido!')
      print()

    def loading(self):
      print('Carregando produtos...')
      
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

    def getProduct(self):
      dataProducts = []

      site = BeautifulSoup(self.browser.page_source, 'html.parser')

      products = site.find_all('div', attrs={'class': 'product-box'})

      for product in products:
          product_name = product.find('h2',attrs={'class':'product-box__name'}).text
          product_category = self.searchProduct
          product_img = product.find('img')['src']
          product_supplier = product.find('span',attrs={'class':'js-product-box__supplier'}).text
          product_mercado = 'Atacadão'
          product_price = float(product.find('div', attrs={'class':'product-box__price'}).find('span', attrs={'class':'product-box__price--number'}).text.replace(',','.'))

          dataProducts.append([product_name, product_category, product_supplier, product_mercado, product_img, product_price])
          
      data = pd.DataFrame(dataProducts, columns=['Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preco']).sort_values('Preco')

      # data.to_csv('atacadao.csv', index=False)
      
      return data

    def processa(self):
      self.browser.get('https://www.atacadao.com.br/')

      sleep(15)

      # self.cancelButton()
      self.acceptCookies()
      self.selectCEP()
      
      sleep(0.5)

      self.search()

      sleep(5)

      self.filterCategory()

      sleep(10)

      self.loading()

      sleep(5)

      data = self.getProduct()
      
      return data.iloc[0]

      # sleep(5)