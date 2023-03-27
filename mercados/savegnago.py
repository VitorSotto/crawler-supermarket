from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd

from mercados.mercado import Mercado

class CrawlerSavegnago(Mercado):

  list_products = []

  def insertCEP(self):
      button_cep = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/section/div/div[2]/div/div/div[1]/div')
      button_cep.click()
      sleep(1)

      button_cep2 = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/section/div/div[2]/div/div/div[2]/div/div[2]/button[1]')
      button_cep2.click()
      sleep(1)

      insert_cep = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/section/div/div[2]/div/div/div[2]/div/form/input')
      insert_cep.send_keys("14801-600")
      sleep(2)


      b_insertcep = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/section/div/div[2]/div/div/div[2]/div/form/button')
      b_insertcep.click()
      sleep(3)

  def Searching(self):
    url_base =  "https://www.savegnago.com.br/" 
    url_svng = (url_base + self.searchProduct)
    self.browser.get(url_svng)

  def FilterProducts(self):
    pass

  def OrderByPrice(self):
    # Menor preço
    btn_menPre1 = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div/button')
    btn_menPre1.click()
    sleep(3)

    btn_menPre2 = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div/div/button[6]')
    btn_menPre2.click()
    sleep(2)

  def LoadingSite(self):
    pass

  def GetProducts(self):
    sleep(2)
    page_content = self.browser.page_source


    site = BeautifulSoup(page_content, 'html.parser')

    #listagem produtos
    products = site.find_all('div', attrs={'class':'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4'})

    for product in products:

      #nome
      name_prod = product.find('span', attrs={'class':'vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body'})
      # print('Nome:',name_prod.text)

      #categoria
      category_prod = self.searchProduct

      #fornecedor
      supplier_prod = ''
      
      #mercado
      market_prod = 'Savegnago'

      #preco
      preco_prod = product.find('p', attrs={'class':'savegnagoio-store-theme-6-x-priceUnit'})
      #  print('Preço:', preco_prod.text)

      #preco
      img_prod = product.find('img', attrs={'class':'vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image'})
      # print('Imagem:', img_prod['src'])


      self.list_products.append([name_prod.text, category_prod, supplier_prod, market_prod, img_prod['src']], float(preco_prod.text.replace('R$ ', '').replace(',','.')))

    dataproducts = pd.DataFrame(self.dataProducts, columns=['Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preco']).sort_values('Preco')

    # print(dataproducts)

    return dataproducts      

  def processa(self):
      print('### INCIANDO SAVEGNAGO ###')
      print()
    
      self.Searching()
      sleep(5)
      self.insertCEP()
      sleep(5)
      self.FilterProducts()
      sleep(5)
      self.OrderByPrice()
      sleep(5)
      self.LoadingSite()
      sleep(5)
      data = self.GetProducts()
      
      print('### SAVEGNAGO CONCLUIDO! ###')
      print()
      
      return data.iloc[0]

    