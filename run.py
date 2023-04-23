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

products = pd.DataFrame(columns=['Id_Produto', 'Nome', 'Fornecedor', 'Mercado', 'Imagem', 'Id_Preco'])
prices = pd.DataFrame(columns=['Id_Preco', 'Categoria', 'Preco', 'Data', 'Id_Produto'])

print('=============================================================')
print()

#inciando browser
browser = webdriver.Chrome(service=service,options=options)

# Busca dos produtos no Atacacão
crawlerAtacadao = CrawlerAtacadao(searchProducts, browser)
crawlerAtacadaoRes = crawlerAtacadao.processa()

products = pd.concat([products, crawlerAtacadaoRes[0]], ignore_index=True)
prices = pd.concat([prices, crawlerAtacadaoRes[1]], ignore_index=True)

# Busca dos produtos no SuperTonin
crawlerSuperTonin = CrawlerSuperTonin(searchProducts, browser)
crawlerSuperToninRes = crawlerSuperTonin.processa()

products = pd.concat([products, crawlerSuperToninRes[0]], ignore_index=True)
prices = pd.concat([prices, crawlerSuperToninRes[1]], ignore_index=True)

# Busca dos produtos no Savegnago
crawlerSavegnago = CrawlerSavegnago(searchProducts, browser)
crawlerSavegnagoRes = crawlerSavegnago.processa()

products = pd.concat([products, crawlerSavegnagoRes[0]], ignore_index=True)
prices = pd.concat([prices, crawlerSavegnagoRes[1]], ignore_index=True)

browser.close()
print('Busca concluida!')
print('=============================================================')
sleep(1)

print(products)
print()
print(prices)
print()

conn = sqlite3.connect(f"{homedir}/www/EconomizeJa/backend/prisma/dev.db")
cursor = conn.cursor()

# products.to_sql('products', conn, if_exists='append', index=False)
cursor.executemany('INSERT INTO Products (id, name, supplier, market, image, priceId) VALUES (?, ?, ?, ?, ?, ?)', products.to_numpy())

# prices.to_sql('prices', conn, if_exists='append', index=False)
cursor.executemany('INSERT INTO Prices (id, category, price, updatedAt, productId) VALUES (?, ?, ?, ?, ?)', prices.to_numpy())

conn.commit()
print('=============================================================')
print('Adicionados ao Banco de Dados!')
conn.close()
