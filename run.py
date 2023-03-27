import sys
import os
import sqlite3
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

from mercados.atacadao import CrawlerAtacadao
from mercados.supertonin import CrawlerSuperTonin
from mercados.savegnago import CrawlerSavegnago

homedir = os.path.expanduser("~")
service = Service(f"{homedir}/chromedriver/stable/chromedriver")


options = Options()
options.add_argument('--headless')
options.add_argument('window-size=1920,1080')

argvs = sys.argv
arquivo = argvs[1]

abs_pasta = os.path.abspath('.')

arquivo_abs_caminho = abs_pasta + '/' + arquivo

with open(arquivo_abs_caminho, 'r') as arq:
  searchProducts = arq.read().split(',')

products = []

print('=============================================================')
for searchProduct in searchProducts:
  print(f"Buscando por {searchProduct}...")
  print()
  browser = webdriver.Chrome(service=service,options=options)
  
  # Busca dos produtos no Atacacão
  crawlerAtacadao = CrawlerAtacadao(searchProduct, browser)
  products.append(crawlerAtacadao.processa())
  
  # Busca dos produtos no SuperTonin
  crawlerSuperTonin = CrawlerSuperTonin(searchProduct, browser)
  products.append(crawlerSuperTonin.processa())
  
  # Busca dos produtos no Savegnago
  # crawlerSavegnago = CrawlerSavegnago(searchProduct, browser)
  # products.append(crawlerSavegnago.processa())
  
  browser.close()
  print('Busca concluida!')
  print('=============================================================')
  sleep(1)

data = pd.DataFrame(products, columns=['Nome', 'Categoria', 'Fornecedor', 'Mercado', 'Imagem', 'Preco'])

print(data)

conn = sqlite3.connect('crawler.db')

data.to_sql('produtos', conn, if_exists='replace', index=False)

conn.commit()
print('=============================================================')
print('Adicionados ao Banco de Dados!')
conn.close()
