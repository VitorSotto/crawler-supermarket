import sqlite3

conn = sqlite3.connect('crawler.db')

cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE produtos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        fornecedor TEXT,
        mercado TEXT NOT NULL,
        imagem TEXT NOT NULL,
        preco DECIMAL NOT NULL
);
""")

print('Tabela criada com sucesso.')

conn.close()