# Novafon E-commerce Case Study

A full-stack e-commerce application built with FastAPI (backend) and Astro (frontend) for managing product catalogs, shopping carts, and customer loyalty discounts.

## Architecture Overview

This project consists of two main components:

- **Backend**: FastAPI-based REST API with SQLite databases
- **Frontend**: Astro-based static site with modern UI components

## Project Structure

```
novafon-case/
├── backend/                 # FastAPI backend application
│   ├── main.py             # Main API server with all endpoints
│   ├── crm_data.db         # Customer relationship management database
│   ├── shop_data.db        # Product catalog database
│   ├── requirements.txt    # Python dependencies
│   └── _discount_calculator.py  # Discount calculation utilities
├── frontend/               # Astro frontend application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   │   ├── CartDrawer.astro    # Shopping cart sidebar
│   │   │   └── ProductSection.astro # Product catalog display
│   │   ├── layouts/        # Page layouts
│   │   ├── pages/          # Application pages
│   │   ├── scripts/        # Client-side JavaScript
│   │   │   └── cartDrawer.js       # Cart drawer interactions
│   │   └── styles/         # Global CSS styles
│   ├── public/             # Static assets
│   │   └── assets/         # Product images and icons
│   ├── package.json        # Node.js dependencies
│   └── astro.config.mjs    # Astro configuration
├── data/                   # JSON data files
│   ├── crm_data.json       # Customer and order data
│   ├── shop_data.json      # Product catalog data
│   └── shopping_cart.json  # Current shopping cart state
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:4321`

## API Endpoints

### Products & Orders

- **GET `/products`** - Retrieve all products from catalog
- **GET `/orders`** - Retrieve all customer orders

### Shopping Cart

- **GET `/cart`** - Get current cart contents
- **PUT `/cart`** - Replace entire cart with new items
- **PUT `/cart/items/{product_id}`** - Update quantity for specific product
- **GET `/cart/annotated`** - Get cart with product details and discount calculations

### Example API Usage

```bash
# Get all products
curl http://localhost:8000/products

# Add item to cart
curl -X PUT http://localhost:8000/cart/items/P101 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 2}'

# Get cart with discounts
curl http://localhost:8000/cart/annotated?customer_id=C1001
```

## Discount System

The application features an automatic customer loyalty discount system:

### VIP Customer Criteria
- Customers with **≥ €1000** total revenue in 2025 are eligible for VIP status
- VIP customers receive **10% discount** on eligible products

### Discount Eligibility
- Only products in **"Promo"** category with **≥ 5 units** in stock are discountable
- Discounts are calculated automatically in real-time

### Example Discount Calculation
```
Customer C1001: €1200.50 revenue in 2025 → VIP Status ✅
Product P101: Massagegerät B (Promo, 10 units) → Discountable ✅
Original Price: €249.99
Discounted Price: €224.99 (10% off)
Savings: €25.00
```

## Frontend Features

### Product Catalog (`ProductSection.astro`)
- **Dynamic Product Loading**: Fetches products from backend API
- **Real-time Pricing**: Shows original and discounted prices
- **Add to Cart**: One-click product addition with automatic cart opening
- **Responsive Design**: Mobile-friendly product cards

### Shopping Cart (`CartDrawer.astro`)
- **Slide-out Panel**: Modern drawer interface
- **Live Updates**: Real-time quantity and price updates without page reload
- **Discount Display**: Shows savings per item and total savings
- **Quantity Controls**: Increase/decrease buttons with live calculation
- **Item Removal**: Remove items with instant UI updates

### Interactive Features (`cartDrawer.js`)
- **Drawer Management**: Open/close with backdrop click support
- **Event Handling**: Clean separation of UI logic from API calls
- **Responsive Behavior**: Works seamlessly across devices

## Database Schema

### Products Table (`shop_data.db`)
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    productId TEXT UNIQUE,
    name TEXT,
    category TEXT,
    stock INTEGER,
    price REAL
);
```

### Orders Table (`crm_data.db`)
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customerId TEXT,
    date TEXT,
    total REAL
);
```

## Data Flow

1. **Product Loading**: Frontend fetches products from `/products` endpoint
2. **Cart Operations**: User interactions trigger API calls to update cart
3. **Discount Calculation**: Backend automatically calculates discounts based on:
   - Customer VIP status (revenue ≥ €1000)
   - Product eligibility (Promo category, stock ≥ 5)
4. **Real-time Updates**: Frontend updates UI without page reload
5. **Persistence**: Cart state saved to `shopping_cart.json`

## Key Features

### Backend
- ✅ **RESTful API** with FastAPI
- ✅ **SQLite Integration** for data persistence
- ✅ **Automatic Discount Calculation** based on customer loyalty
- ✅ **CORS Support** for frontend integration
- ✅ **Error Handling** with proper HTTP status codes
- ✅ **Type Hints** and comprehensive documentation

### Frontend
- ✅ **Modern UI** with Astro and Tailwind CSS
- ✅ **Real-time Updates** without page reloads
- ✅ **Responsive Design** for all screen sizes
- ✅ **Interactive Cart** with quantity controls
- ✅ **Discount Visualization** with color-coded savings
- ✅ **Clean Architecture** with separated concerns

## Testing the Application

### Manual Testing Steps

1. **Start both servers** (backend on :8000, frontend on :4321)
2. **Browse products** - verify product information displays correctly
3. **Add items to cart** - test buy buttons and cart opening
4. **Modify quantities** - use +/- buttons to change quantities
5. **Remove items** - test remove functionality
6. **Check discounts** - verify VIP customer discounts display
7. **Test responsiveness** - check mobile/tablet layouts

### API Testing with curl

```bash
# Test product endpoint
curl http://localhost:8000/products

# Test cart operations
curl -X PUT http://localhost:8000/cart/items/P101 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 3}'

# Test annotated cart with discounts
curl "http://localhost:8000/cart/annotated?customer_id=C1001"
```

## Development Notes

### Code Organization
- **Backend**: Single-file architecture with clear function separation
- **Frontend**: Component-based structure with Astro
- **Styling**: Tailwind CSS for utility-first styling
- **JavaScript**: Vanilla JS for simplicity and performance

### Performance Considerations
- **Live Updates**: DOM manipulation instead of full page reloads
- **Efficient API Calls**: Minimal requests with comprehensive responses
- **Static Assets**: Optimized images and icons
- **Database Queries**: Simple SQLite queries for fast response times

### Error Handling
- **Backend**: Comprehensive error handling with HTTP status codes
- **Frontend**: Graceful degradation with user-friendly error messages
- **Validation**: Input validation on both client and server side

## Case Study Requirements

This implementation fulfills all case study requirements:

- ✅ **Product Catalog**: Dynamic loading from database
- ✅ **Shopping Cart**: Full CRUD operations with persistence
- ✅ **Customer Loyalty**: Automatic VIP discount calculation
- ✅ **Real-time Updates**: Live cart updates without reload
- ✅ **Modern UI**: Responsive design with smooth interactions
- ✅ **API Integration**: RESTful backend with frontend consumption
- ✅ **Data Persistence**: SQLite databases and JSON cart storage


## FAST API CHECK

- **API Documentation**: Available at `http://localhost:8000/docs` when server is running

---

**Built with ❤️ for the Novafon E-commerce Case Study**