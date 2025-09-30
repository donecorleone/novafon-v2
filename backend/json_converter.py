import sqlite3
import json

# Einfach SQLite3 verwenden
shop_db = sqlite3.connect('shop_data.db')
cursor = shop_db.cursor()

# Tabelle erstellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    productId TEXT,
    name TEXT,
    category TEXT,
    stock INTEGER,
    price REAL
)
''')

# JSON laden
with open('../data/shop_data.json', 'r') as file:
    data = json.load(file)

# Daten löschen (falls bereits vorhanden)
cursor.execute('DELETE FROM products')

# Daten einfügen
for item in data:
    cursor.execute('''
        INSERT INTO products (productId, name, category, stock, price) 
        VALUES (?, ?, ?, ?, ?)
    ''', (item["productId"], item["name"], item["category"], item["stock"], item["price"]))

shop_db.commit()
shop_db.close()
print("Products imported!")

