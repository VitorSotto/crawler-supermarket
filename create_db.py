import sqlite3

conn = sqlite3.connect('crawler.db')

cursor = conn.cursor()

# criando a tabela (schema)

# Cria a tabela "produtos"
conn.execute('''CREATE TABLE produtos (
        id_produto TEXT NOT NULL PRIMARY KEY,
        nome TEXT NOT NULL,
        fornecedor TEXT,
        mercado TEXT NOT NULL,
        imagem TEXT NOT NULL,
        id_preco TEXT NOT NULL UNIQUE,
        FOREIGN KEY (id_preco) REFERENCES precos(id_preco)
)''')

# Cria a tabela "precos"
conn.execute('''CREATE TABLE precos (
        id TEXT NOT NULL PRIMARY KEY,
        categoria TEXT NOT NULL,
        preco DECIMAL NOT NULL,
        data DATE NOT NULL,
        id_produto TEXT NOT NULL,
        FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
)''')

print('Tabela criada com sucesso.')

conn.close()