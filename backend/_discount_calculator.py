import sqlite3
import json

def get_customer_revenue(customer_id):
    """Holt den Gesamtumsatz 2025 für einen Kunden aus der CRM-Datenbank"""
    conn = sqlite3.connect('crm_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT totalRevenue FROM customers WHERE customerId = ?
    ''', (customer_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]  # totalRevenue
    else:
        return 0

def get_product_info(product_id):
    """Holt Produktinfos aus der Shop-Datenbank"""
    conn = sqlite3.connect('shop_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT productId, name, category, stock, price FROM products WHERE productId = ?
    ''', (product_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'productId': result[0],
            'name': result[1], 
            'category': result[2],
            'stock': result[3],
            'price': result[4]
        }
    else:
        return None

def calculate_discount(customer_id, cart):
    """Berechnet Rabatte für einen Warenkorb"""
    
    # 1. Kundenumsatz prüfen
    total_revenue = get_customer_revenue(customer_id)
    is_eligible = total_revenue >= 1000
    
    print(f"=== Rabattberechnung für Kunde {customer_id} ===")
    print(f"Gesamtumsatz 2025: {total_revenue}€")
    print(f"Rabattberechtigt: {'JA' if is_eligible else 'NEIN'}")
    print()
    
    # 2. Warenkorb verarbeiten
    cart_items = []
    total_original = 0
    total_discount = 0
    
    for item in cart:
        product_id = item['productId']
        quantity = item['quantity']
        
        # Produktinfos holen
        product = get_product_info(product_id)
        
        if not product:
            print(f"⚠️  Produkt {product_id} nicht gefunden!")
            continue
            
        # Preise berechnen
        original_price = product['price'] * quantity
        total_original += original_price
        
        # Rabatt prüfen
        discount_price = original_price
        reason = "Kein Rabatt"
        
        if (is_eligible and 
            product['category'] == 'Promo' and 
            product['stock'] >= 5):
            discount_price = original_price * 0.9  # 10% Rabatt
            reason = "10% Rabatt (Promo + Bestand OK)"
        elif product['category'] == 'Promo' and product['stock'] < 5:
            reason = "Kein Rabatt - Bestand zu niedrig"
        elif not is_eligible:
            reason = "Kein Rabatt - Umsatz zu niedrig"
            
        total_discount += discount_price
        
        # Ausgabe
        print(f"📦 {product['name']} (x{quantity})")
        print(f"   Originalpreis: {original_price:.2f}€")
        print(f"   Rabattpreis: {discount_price:.2f}€")
        print(f"   Grund: {reason}")
        print()
        
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'originalPrice': original_price,
            'discountPrice': discount_price,
            'reason': reason
        })
    
    # 3. Gesamtsumme
    savings = total_original - total_discount
    
    print(f"=== ZUSAMMENFASSUNG ===")
    print(f"Gesamt Originalpreis: {total_original:.2f}€")
    print(f"Gesamt Rabattpreis: {total_discount:.2f}€")
    print(f"Ersparnis: {savings:.2f}€")
    
    return {
        'customerId': customer_id,
        'totalRevenue2025': total_revenue,
        'isEligible': is_eligible,
        'cartItems': cart_items,
        'totalOriginal': total_original,
        'totalDiscount': total_discount,
        'savings': savings
    }

# Test mit dem Beispiel-Warenkorb
if __name__ == "__main__":
    # Beispiel-Warenkorb aus der Aufgabe
    test_cart = [
        {"productId": "P100", "quantity": 1},  # Massagegerät A - Promo, Bestand 12
        {"productId": "P101", "quantity": 1},  # Massagegerät B - Promo, Bestand 3  
        {"productId": "P200", "quantity": 2}   # Zubehör X - Standard, Bestand 50
    ]
    
    print("🛒 TEST: Rabattberechnung")
    print("=" * 50)
    
    # Test Kunde C1001 (Umsatz: 1200.50€ - rabattberechtigt)
    result = calculate_discount("C1001", test_cart)
    
    print("\n" + "=" * 50)
    print("✅ Test abgeschlossen!")
