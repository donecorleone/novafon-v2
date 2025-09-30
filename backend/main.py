"""
Novafon E-commerce Backend API

A FastAPI-based backend service for managing products, orders, and shopping cart
functionality with customer loyalty discount system.

This module provides REST API endpoints for:
- Product catalog management
- Order history retrieval
- Shopping cart operations with real-time discount calculation
- Customer VIP status and loyalty rewards

Author: Novafon Development Team
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from pathlib import Path

# Initialize FastAPI application
app = FastAPI()

# File path configuration
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = (BASE_DIR / ".." / "data").resolve()
CRM_DB = (BASE_DIR / "crm_data.db").resolve()
SHOP_DB = (BASE_DIR / "shop_data.db").resolve()
DEFAULT_CART = (DATA_DIR / "shopping_cart.json").resolve()

# CORS middleware configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://127.0.0.1:4321"],  # Astro dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/orders")
def get_orders() -> list:
    """Retrieve all orders from the CRM database.

    Returns
    -------
    list
        List of all order records from the CRM database. Each record contains
        order details including customer ID, date, total amount, etc.

    Raises
    ------
    HTTPException
        If database connection or query fails (status_code=500)
    """
    try:
        with sqlite3.connect(CRM_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders")
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"DB error (orders): {e}")

@app.get("/products")
def get_products() -> list:
    """Retrieve all products from the shop database.

    Returns
    -------
    list
        List of all product records from the shop database. Each record contains
        product details including ID, name, category, stock, and price.

    Raises
    ------
    HTTPException
        If database connection or query fails (status_code=500)
    """
    try:
        with sqlite3.connect(SHOP_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"DB error (products): {e}")

def get_customer_umsatz() -> dict:
    """Calculate total revenue per customer for year 2025.

    Returns
    -------
    dict
        Dictionary mapping customer IDs to their total revenue in 2025.
        Format: {customer_id: total_revenue}

    Raises
    ------
    HTTPException
        If database connection or query fails (status_code=500)
    """
    try:
        with sqlite3.connect(CRM_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT customerId, SUM(total) AS jahresumsatz
                FROM orders
                WHERE date BETWEEN '2025-01-01' AND '2025-12-31'
                GROUP BY customerId
                """
            )
            results = cursor.fetchall()
            return dict(results)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"DB error (umsatz): {e}")



def get_discount(customer_total: dict) -> dict:
    """Identify VIP customers eligible for discounts.

    VIP customers are those with total revenue >= 1000€ in 2025.

    Parameters
    ----------
    customer_total : dict
        Dictionary mapping customer IDs to their total revenue.
        Format: {customer_id: total_revenue}

    Returns
    -------
    dict
        Dictionary containing only VIP customers (revenue >= 1000€).
        Format: {customer_id: total_revenue}
    """
    rabatt_kunde = {}
    for k, v in customer_total.items():
        if v >= 1000:
            rabatt_kunde[k] = v
    return rabatt_kunde



def save_cart(items: list) -> None:
    """Save shopping cart items to JSON file.

    Saves the cart items list to shopping_cart.json as specified in the case requirements.
    The file contains only the items list, not wrapped in an object.

    Parameters
    ----------
    items : list
        List of cart items in format: [{"productId": "...", "quantity": <int>}, ...]

    Raises
    ------
    HTTPException
        If file write operation fails (status_code=500)
    """
    try:
        with open(DEFAULT_CART, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"IO error (save_cart): {e}")


@app.put("/cart")
def replace_cart(payload: dict = Body(...)):
    """Replace the entire shopping cart with new items.

    Parameters
    ----------
    payload : dict
        Request body containing cart items. Must include 'items' key with list value.

    Returns
    -------
    dict
        Confirmation response with the saved items list.

    Raises
    ------
    HTTPException
        If 'items' is not a list (status_code=400) or save operation fails (status_code=500)
    """
    items = payload.get("items")
    if not isinstance(items, list):
        raise HTTPException(status_code=400, detail="'items' must be a list")

    save_cart(items)  
    return {"items": items}



@app.put("/cart/items/{product_id}")
def set_cart_quantity(
    product_id: str,
    quantity: int = Body(..., embed=True),
    customer_id: str = "C1001",
):
    """
    Sets the quantity of a specific product in the shopping cart.

    - If quantity <= 0, the product will be removed from the cart.
    - If quantity > 0, the product will be added or updated.
    - Returns the annotated cart (e.g. with discount calculations).
    """

    cart = get_cart()
    items = cart.get("items", [])


    product_index = None
    for i, item in enumerate(items):
        if item.get("productId") == product_id:
            product_index = i
            break


    if quantity <= 0:
        if product_index is not None:
            items.pop(product_index)

    else:
        if product_index is not None:
            items[product_index]["quantity"] = quantity
        else:
            new_item = {
                "productId": product_id,
                "quantity": quantity
            }
            items.append(new_item)


    save_cart(items)

    return cart_annotated(customer_id)

   
@app.get("/cart")
def get_cart():
    """Retrieve the current shopping cart contents.

    Returns
    -------
    dict
        Cart data with 'items' key containing list of cart items.
        Format: {"items": [{"productId": "...", "quantity": <int>}, ...]}

    Raises
    ------
    HTTPException
        If cart file read fails or file format is invalid (status_code=500)
    """
    try:
        with open(DEFAULT_CART, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Cart read error: {e}")

    # Handle both dict and list formats for backward compatibility
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data  
    if isinstance(data, list):
        return {"items": data}  

    raise HTTPException(status_code=500, detail="Cart file malformed: expected {'items': [...]} or a list")

        

@app.get("/cart/annotated")
def cart_annotated(customer_id: str = "C1001"):
    """Get shopping cart with detailed product information and discount calculations.

    Returns the cart contents enriched with product details, pricing information,
    and automatic discount calculations based on customer VIP status and product eligibility.

    Parameters
    ----------
    customer_id : str, optional
        Customer ID for VIP status determination and discount calculation (default: "C1001")

    Returns
    -------
    dict
        Annotated cart response containing:
        - items: List of cart items with product details, pricing, and discount info
        - subtotal: Total cart value before discounts
        - subtotal_discounted: Total cart value after discounts
        - total_savings: Total amount saved through discounts

    Raises
    ------
    HTTPException
        If database or cart operations fail (status_code=500)
    """
    cart = get_cart()
    products = get_products()
    customer_total = get_customer_umsatz()
    customer_discount = get_discount(customer_total)
    customer_discount_set = set(customer_discount)

    is_vip = (customer_id in customer_discount_set)

    
    product_by_id = {}
    annotated_items = []
    discountable_ids = set()

    for product in products:
        pid = product[1]       # productId
        category = product[3]  # Kategorie
        stock = product[4]     # Lagerbestand
        product_by_id[pid] = {
            'name': product[2],
            'category': category,
            'stock': stock,
            'price': product[5],
        }
        if category == "Promo" and stock >= 5:
            discountable_ids.add(pid)

    #Set counters
    subtotal = 0.0
    subtotal_discounted = 0.0
    total_savings = 0.0

    for item in cart["items"]:
        pid = item['productId']
        qty = item['quantity']
        if pid in product_by_id:
            info = product_by_id[pid]          
            unit_price = info["price"]
            name = info["name"]
            category = info["category"]

            line_total = round((unit_price * qty), 2)

            if is_vip and (pid in discountable_ids):
                discounted_unit_price = round(unit_price * 0.90, 2)
                line_total_discounted = round(discounted_unit_price * qty, 2)
                savings_total = round(line_total - line_total_discounted, 2)
                rabatt = True
            else:
                discounted_unit_price = unit_price
                line_total_discounted = line_total
                savings_total = 0.00
                rabatt = False
            
            #set up for frontend
            subtotal += line_total
            subtotal_discounted += line_total_discounted
            total_savings += savings_total

            test = {'productId': pid,
                    'name': name,
                    'category': category,
                    'unit_price': unit_price,
                    'quantity': qty,
                    'line_total': line_total,
                    'rabatt': rabatt,
                    'discounted_unit_price': discounted_unit_price,
                    'line_total_discounted': line_total_discounted,
                    'savings_total': savings_total

                    }
            annotated_items.append(test)




    return {
        "items": annotated_items,
        "subtotal": round(subtotal, 2),
        "subtotal_discounted": round(subtotal_discounted, 2),
        "total_savings": round(total_savings, 2),
    }
            
        

if __name__ == "__main__":
    """Run the FastAPI application server.
    
    Starts the development server on localhost:8000 for local development.
    """
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
