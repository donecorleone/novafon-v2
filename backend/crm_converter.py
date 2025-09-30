import sqlite3
import json

# Einfach SQLite3 verwenden
crm_db = sqlite3.connect('crm_data.db')
cursor = crm_db.cursor()

# Tabellen erstellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    customerId TEXT UNIQUE,
    totalRevenue REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customerId TEXT,
    orderId TEXT UNIQUE,
    date TEXT,
    total REAL,
    FOREIGN KEY (customerId) REFERENCES customers (customerId)
)
''')

# JSON laden
with open('../data/crm_data.json', 'r') as file:
    data = json.load(file)

# Daten löschen (falls bereits vorhanden)
cursor.execute('DELETE FROM orders')
cursor.execute('DELETE FROM customers')

# Daten einfügen
for customer in data:
    # Kunde einfügen
    cursor.execute('''
        INSERT INTO customers (customerId, totalRevenue) 
        VALUES (?, 0)
    ''', (customer["customerId"],))
    
    # Bestellungen einfügen
    for order in customer["orders"]:
        cursor.execute('''
            INSERT INTO orders (customerId, orderId, date, total) 
            VALUES (?, ?, ?, ?)
        ''', (customer["customerId"], order["orderId"], order["date"], order["total"]))

# Gesamtumsatz pro Kunde berechnen und aktualisieren
cursor.execute('''
    UPDATE customers 
    SET totalRevenue = (
        SELECT SUM(total) 
        FROM orders 
        WHERE orders.customerId = customers.customerId
    )
''')

crm_db.commit()
crm_db.close()
print("CRM data imported!")

# Test: Daten anzeigen
conn = sqlite3.connect('crm_data.db')
cursor = conn.cursor()

print("\n=== Kunden ===")
cursor.execute("SELECT * FROM customers")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, CustomerID: {row[1]}, TotalRevenue: {row[2]}€")

print("\n=== Bestellungen ===")
cursor.execute("SELECT * FROM orders")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, CustomerID: {row[1]}, OrderID: {row[2]}, Date: {row[3]}, Total: {row[4]}€")

conn.close()
