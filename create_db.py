import sqlite3

conn = sqlite3.connect('crawler.db')

cursor = conn.cursor()

# criando a tabela (schema)

# Cria a tabela "products"
conn.execute('''CREATE TABLE Products (
        id TEXT NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        supplier TEXT,
        market TEXT NOT NULL,
        image TEXT NOT NULL,
        priceId TEXT NOT NULL UNIQUE,
        FOREIGN KEY (priceID) REFERENCES precos(id)
)''')

# Cria a tabela "prices"
conn.execute('''CREATE TABLE Prices (
        id TEXT NOT NULL PRIMARY KEY,
        category TEXT NOT NULL,
        price DECIMAL NOT NULL,
        updatedAt DATE NOT NULL,
        productId TEXT NOT NULL,
        FOREIGN KEY (productID) REFERENCES produtos(id)
)''')

print('Tabela criada com sucesso.')

conn.close()