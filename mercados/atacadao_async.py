from caqui import synchronous
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
      # cancelButton = self.browser.find_element(By.CLASS_NAME, 'close')
      cancelButton = synchronous.find_element(*self.browser, By.CLASS_NAME, 'close')
      # cancelButton.click()
      synchronous.click(*self.browser, cancelButton)

    def selectCEP(self):
      sleep(2)
      # cpfSelect = self.browser.find_element(By.ID, 'input-cpf-modal')
      cpfSelect = synchronous.find_element(*self.browser, By.ID, 'input-cpf-modal')
      # ActionChains(self.browser).click(cpfSelect).perform()
      synchronous.actions_click(*self.browser, cpfSelect)
      sleep(1)
      # inputCEP = self.browser.find_element(By.ID, 'cep')
      inputCEP = synchronous.find_element(*self.browser, By.ID, 'cep')
      # inputCEP.send_keys('14801-600')
      synchronous.send_keys(*self.browser, inputCEP, '14801-600')
      sleep(1)
      
      # confirmButton = self.browser.find_element(By.ID, 'btn-confirmar')
      confirmButton = synchronous.find_element(*self.browser, By.ID, 'btn-confirmar')
      # confirmButton.click()
      synchronous.click(*self.browser, confirmButton)

    def acceptCookies(self):
      #  coockieButton = self.browser.find_element(By.ID, 'onetrust-accept-btn-handler')
      coockieButton = synchronous.find_element(*self.browser, By.ID, 'onetrust-accept-btn-handler')
      #  coockieButton.click()
      synchronous.click(*self.browser, coockieButton)

    def search(self):
      # searchButton = self.browser.find_element(By.CLASS_NAME, 'js-search-query')
      searchButton = synchronous.find_element(*self.browser, By.CLASS_NAME, 'js-search-query')
      search = synchronous.find_element(*self.browser, By.XPATH, '//*[@id="formHeader"]/form//button[@type="submit"]')
      # searchButton.send_keys(self.searchProduct)
      synchronous.send_keys(*self.browser, searchButton, self.searchProduct)
      # searchButton.submit()
      synchronous.submit(*self.browser, search)

    def filterCategory(self):
      print('filtrando...')
      print()

      filterProducts = []
      inputsProducts = []
      inputsSelected = []

      # filterProducts = self.browser.find_element(By.ID, 'js-product-filter')
      filterProducts = synchronous.find_element(*self.browser, By.ID, 'js-product-filter')
      # inputsProducts = filterProducts.find_elements(By.TAG_NAME, 'input')
      inputsProducts = synchronous.find_children_elements(*self.browser, filterProducts, By.TAG_NAME, 'input')

      for inputProduct in inputsProducts:
        # value = inputProduct.get_attribute('value')
        value = synchronous.get_attribute(*self.browser, inputProduct, 'value')
        print("produto: ", value)
        if (value.lower().find(self.searchProduct.lower())==0):
          # ActionChains(self.browser).scroll_to_element(inputProduct).perform()
          synchronous.actions_scroll_to_element(*self.browser, inputProduct)
          # ActionChains(self.browser).click(inputProduct).perform()
          synchronous.actions_click(*self.browser, inputProduct)
      
      # inputsSelected = filterProducts.find_elements(By.CSS_SELECTOR, 'input:checked')
      inputsSelected = synchronous.find_children_elements(*self.browser, filterProducts, By.CSS_SELECTOR, 'input:checked')
      print(f'filtros selecionados: {numpy.size(inputsSelected)}')
      
      for inputSelected in inputsSelected:
        # print(inputSelected.get_attribute('value'))
        print(synchronous.get_attribute(*self.browser, inputSelected, 'value'))
        
      print('filtragem concluido!')
      print()

    def loading(self):
      print('carregando produtos...')
      
      # footer = self.browser.find_element(By.TAG_NAME, 'footer')
      footer = synchronous.find_element(*self.browser, By.TAG_NAME, 'footer')
      # navFooter = footer.find_element(By.TAG_NAME, 'nav')
      navFooter = synchronous.find_child_element(*self.browser, footer, By.TAG_NAME, 'nav')
      # ActionChains(self.browser).scroll_to_element(navFooter).perform()
      synchronous.actions_scroll_to_element(*self.browser, navFooter)
      sleep(1)
      
      # loadingDiv = self.browser.find_element(By.CLASS_NAME, 'container-catalogo')
      loadingDiv = synchronous.find_element(*self.browser, By.CLASS_NAME, 'container-catalogo')
      # loadingImg = loadingDiv.find_element(By.TAG_NAME, 'img')
      loadingImg = synchronous.find_child_element(*self.browser, loadingDiv, By.TAG_NAME, 'img')
      # ActionChains(self.browser).scroll_to_element(loadingDiv).perform()
      synchronous.actions_scroll_to_element(*self.browser, loadingDiv)
      
      # catalogue = self.browser.find_element(By.CLASS_NAME, 'catalogue')
      catalogue = synchronous.find_element(*self.browser, By.CLASS_NAME, 'catalogue')
      # products = catalogue.find_elements(By.CLASS_NAME, 'product-box')
      products = synchronous.find_child_element(*self.browser, catalogue, By.CLASS_NAME, 'product-box')
      # print(f'produtos encontrados: {numpy.size(products)}')
      
      # while(loadingImg.is_displayed()):
      product_list_start = synchronous.find_elements(
        *self.browser,
        locator_type="xpath",
        locator_value="//div[contains(@class,'card shadow')]")
      product_list_end = []
      while(len(product_list_start) != len(product_list_end) ):
        product_list_start = synchronous.find_elements(
          *self.browser, locator_type="xpath", locator_value="//div[contains(@class,'card shadow')]")
        # ActionChains(self.browser).scroll_to_element(loadingDiv).perform()
        synchronous.actions_scroll_to_element(*self.browser, loadingDiv)
        sleep(5)
        # products = catalogue.find_elements(By.CLASS_NAME, 'product-box')
        products = synchronous.find_children_elements(*self.browser, catalogue, By.CLASS_NAME, 'product-box')
        product_list_end = synchronous.find_elements(*self.browser, locator_type="xpath", locator_value="//div[contains(@class,'card shadow')]")
        
      print(f'produtos encontrados: {numpy.size(products)}')
      print('carregamento concluido!')
      print()
      
      for product in products:
        # ActionChains(self.browser).scroll_to_element(product).perform()
        synchronous.actions_scroll_to_element(*self.browser, product)

    def getProduct(self):
      
      print("pegando os produtos...")
      print()
      dataProduct = []

      site = BeautifulSoup(
        synchronous.get_page_source(*self.browser, 'html.parser'))
      products = site.find_all('div', attrs={'class': 'product-box'})

      for product in products:
        product_id = str(uuid.uuid4())
        price_id = str(uuid.uuid4())
        product_name = product.find('h2',attrs={'class':'product-box__name'}).text
        product_category = self.searchProduct
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
      return data

    def processa(self):
      print('### INCIANDO ATACADAO ###')
      print()
      
      print('configurando...')

      # self.browser.get('https://www.atacadao.com.br/')
      synchronous.get(*self.browser, 'https://www.atacadao.com.br/')

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

      # self.browser.get('https://www.atacadao.com.br/')
      synchronous.get(*self.browser, 'https://www.atacadao.com.br/')

      self.search()

      sleep(5)

      self.filterCategory()

      sleep(10)

      self.loading()

      sleep(5)

      first_line = self.getProduct()
      
      products = pd.concat([products, first_line], join='inner', ignore_index=True)
      prices = pd.concat([prices, first_line], join='inner', ignore_index=True)
      
      print('Busca completa!')
      print()
      
      print('### ATACADAO CONCLUIDO! ###')
      print()
      
      res.append(products)
      res.append(prices)
      
      return res