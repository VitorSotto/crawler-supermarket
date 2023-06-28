from time import sleep
import numpy as np
import uuid
from datetime import date

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import pandas as pd
import unicodedata

from mercados.mercado import Mercado

class CrawlerSavegnago(Mercado):

  

  def insertCEP(self):
      button_cep = self.browser.find_element(By.CSS_SELECTOR, 'body > div.render-container.render-route-store-home > div > div.vtex-store__template.bg-base > div > div.vtex-sticky-layout-0-x-wrapper.vtex-sticky-layout-0-x-wrapper--top-menu-sticky-desktop > div > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--top-menu-wrapper-desktop > section > div > div:nth-child(2) > div > div > div > div > p > button')
      button_cep.click()
      sleep(1)

      button_cep2 = self.browser.find_element(By.CSS_SELECTOR, 'body > div.render-container.render-route-store-home > div > div.vtex-store__template.bg-base > div > div.vtex-sticky-layout-0-x-wrapper.vtex-sticky-layout-0-x-wrapper--top-menu-sticky-desktop > div > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--top-menu-wrapper-desktop > section > div > div:nth-child(2) > div > div > div.savegnagoio-store-theme-8-x-modalWrapperOpenContainer > div.savegnagoio-store-theme-8-x-containerModalRegionalization > div:nth-child(3) > div > button:nth-child(2)')
      button_cep2.click()
      sleep(1)

      insert_cep = self.browser.find_element(By.CSS_SELECTOR, 'body > div.render-container.render-route-store-home > div > div.vtex-store__template.bg-base > div > div.vtex-sticky-layout-0-x-wrapper.vtex-sticky-layout-0-x-wrapper--top-menu-sticky-desktop > div > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--top-menu-wrapper-desktop > section > div > div:nth-child(2) > div > div > div.savegnagoio-store-theme-8-x-modalWrapperOpenContainer > div.savegnagoio-store-theme-8-x-containerModalRegionalization > div.savegnagoio-store-theme-8-x-containerModalStageThree > form > div > input')
      insert_cep.send_keys("14801-600")
      sleep(2)


      b_insertcep = self.browser.find_element(By.CSS_SELECTOR, 'body > div.render-container.render-route-store-home > div > div.vtex-store__template.bg-base > div > div.vtex-sticky-layout-0-x-wrapper.vtex-sticky-layout-0-x-wrapper--top-menu-sticky-desktop > div > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--top-menu-wrapper-desktop > section > div > div:nth-child(2) > div > div > div.savegnagoio-store-theme-8-x-modalWrapperOpenContainer > div.savegnagoio-store-theme-8-x-containerModalRegionalization > div.savegnagoio-store-theme-8-x-containerModalStageThree > form > button')
      b_insertcep.click()
      sleep(3)

  def Searching(self):
    url_base =  "https://www.savegnago.com.br/" 
    url_svng = (url_base + self.searchProduct)
    self.browser.get(url_svng)

  def FilterProducts(self):
    try:
      input_filter = self.browser.find_element(By.CSS_SELECTOR, f'input[value^="{self.searchProduct}"]')
      ActionChains(self.browser).scroll_to_element(input_filter).perform()
      sleep(0.5)
      ActionChains(self.browser).click(input_filter).perform()

    except NoSuchElementException:
      print('Filtro não encontrado!')

  def OrderByPrice(self):
    # Menor preço
    btn_menPre1 = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div/button')
    btn_menPre1.click()
    sleep(3)

    btn_menPre2 = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div/div/button[6]')
    btn_menPre2.click()
    sleep(2)
  
  def LoadingSite(self):
    print('carregamento produtos...')
   # loading = False
    wait = WebDriverWait(self.browser, 10)
    mostrar_mais = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.render-container.render-route-store-search > div > div.vtex-store__template.bg-base > div > div:nth-child(3) > div > div > section > div.relative.justify-center.flex > div > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--container__search-result-desktop > div > div.pr0.items-stretch.flex-grow-1.flex > div > div:nth-child(5) > div > div > div > div > div > a")))
    
    while mostrar_mais.is_displayed():
      try: 
        ActionChains(self.browser).scroll_to_element(mostrar_mais).perform()
        sleep(5)
        ActionChains(self.browser).click(mostrar_mais).perform()
        #mostrar_mais.click()
        mostrar_mais = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.render-container.render-route-store-search > div > div.vtex-store__template.bg-base > div > div:nth-child(3) > div > div > section > div.relative.justify-center.flex > div > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--container__search-result-desktop > div > div.pr0.items-stretch.flex-grow-1.flex > div > div:nth-child(5) > div > div > div > div > div > a")))

      except StaleElementReferenceException:
        print('carregamento concluido!')
        print()
        break
        
  
  def GetProducts(self):

    print("coletando dados...")

    list_products = []
    sleep(2)
    page_content = self.browser.page_source


    site = BeautifulSoup(page_content, 'html.parser')

    #listagem produtos
    products = site.find_all('div', attrs={'class':'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4'})

    for product in products:
      product_id = str(uuid.uuid4())
      price_id = str(uuid.uuid4())
      
      indisponivel = product.find('p', attrs={'class':'lh-copy vtex-rich-text-0-x-paragraph vtex-rich-text-0-x-paragraph--text-indisponivel'})

      if indisponivel is not None:
        continue
      #bt_comprar = product.find('div', attrs={'class':'vtex-button__label flex items-center justify-center h-100 ph6'})
      
    
      name_prod = product.find('span', attrs={'class':'vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body'}).text
    
      category_prod = self.searchProduct
      supplier_prod = ''
      market_prod = 'Savegnago'   

      #preco_prod = float(unicodedata.normalize('NFKD', product.find('p', attrs={'class':'savegnagoio-store-theme-6-x-priceUnit'}).text).replace('R$ ', '').replace(',', '.'))
      #if bt_comprar != None:
      

      preco_prod = float((product.find('p', attrs={'class':'savegnagoio-store-theme-8-x-priceUnit'}).text.replace('R$','').replace(',', '.')))
      
      img_prod = ''
      img_container = product.find('div', attrs={'class':'vtex-product-summary-2-x-imageContainer'})

      if img_container.find('img') :
        img_prod = img_container.find('img')['src']
      else:
        continue

      product_date = date.today()
    

      list_products.append([product_id, price_id, name_prod, category_prod, supplier_prod, market_prod, img_prod, preco_prod, product_date])
      

    #print(f'produtos encontrados: {np.size(products)}')
    dataproducts = []
    # dataproducts = pd.DataFrame(list_products, columns=['Id_Produto','Id_Preco', 'Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preco', 'Data']).sort_values('Preco')
    
      
    # df = dataproducts.sort_values('Preco')
    print("dados coletados!")
    print()
    # print(dataproducts.iloc[0])

    # return pd.DataFrame(dataproducts.iloc[0]).transpose()
    return dataproducts
      

  def processa(self):
    
      print('### INCIANDO SAVEGNAGO ###')
      print()

      print('configurando...')
      
      self.browser.get("https://www.savegnago.com.br/")
      sleep(5)

      self.insertCEP()
      sleep(5)

      print('configuração concluida!')
      print()
      
      # products = pd.DataFrame(columns=['Id_Produto', 'Nome', 'Fornecedor', 'Mercado', 'Imagem', 'Id_Preco'])
      # prices = pd.DataFrame(columns=['Id_Preco', 'Categoria', 'Preco', 'Data', 'Id_Produto'])
      res = []
      
      self.Searching()
      sleep(10)

      # self.OrderByPrice()
      # sleep(5)

      self.FilterProducts()
      sleep(5)
      
      self.LoadingSite()
      sleep(10)

      first_line = self.GetProducts()
      
      # products = pd.concat([products, first_line], join='inner', ignore_index=True)
      # prices = pd.concat([prices, first_line], join='inner', ignore_index=True)

      sleep(10)
      print("Busca Completa!")
      
      print('### SAVEGNAGO CONCLUIDO! ###')
      print()

      # res.append(products)
      # res.append(prices)
      
      return res
        
     

    