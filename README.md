# Novafon Case - E-Commerce Application

A modern e-commerce application built with FastAPI (backend) and Astro (frontend), featuring customer loyalty discounts, real-time cart updates, and Docker containerization.

## Features

- **Product Catalog**: Display products with real-time pricing
- **Shopping Cart**: Live updates with quantity management
- **Customer Loyalty System**: Automatic discount calculation for VIP customers
- **Multi-Customer Support**: Switch between different customer accounts
- **Responsive Design**: Modern UI with Tailwind CSS
- **Docker Ready**: Complete containerization setup

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11
- **Database**: SQLite3 with JSON data files
- **API Endpoints**: RESTful API for products, cart, and customer management
- **Discount Engine**: Automatic VIP customer discount calculation

### Frontend (Astro)
- **Framework**: Astro with TypeScript
- **Styling**: Tailwind CSS
- **Real-time Updates**: Client-side cart management
- **Customer Selection**: Dynamic customer ID switching

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- Docker (optional)

## Installation

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd novafon-case-neu
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python3 main.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:4321
   - Backend API: http://localhost:8000

### Option 2: Docker

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:4321
   - Backend API: http://localhost:8000

## Usage

### Customer Selection
When you first load the application, you'll be prompted to select a customer:
- **C1001**: VIP customer with loyalty discounts
- **C1002**: Regular customer
- **Enter**: Defaults to C1001

### Shopping Experience
1. **Browse Products**: View available products with pricing
2. **Add to Cart**: Click the shopping cart icon to add items
3. **View Cart**: Click the cart button in the top-right corner
4. **Manage Quantities**: Use +/- buttons or remove items
5. **See Discounts**: VIP customers automatically receive 10% discounts on eligible products

### Cart Features
- **Live Updates**: Cart updates in real-time without page refresh
- **Discount Display**: Shows original price, discounted price, and savings
- **Quantity Management**: Increase, decrease, or remove items
- **Customer-Specific**: Cart is cleared when switching customers

## API Endpoints

### Products
- `GET /products` - Get all products
- `GET /products/{product_id}` - Get specific product

### Cart
- `GET /cart` - Get current cart contents
- `PUT /cart` - Update entire cart
- `PUT /cart/items/{product_id}` - Update specific item quantity
- `GET /cart/annotated` - Get cart with discount calculations

### Customer
- `GET /customer/{customer_id}/orders` - Get customer order history
- `GET /customer/{customer_id}/discount` - Get customer discount eligibility

## Data Structure

### Products
```json
{
  "id": 1,
  "productId": "P100",
  "name": "Massagegerät A",
  "category": "Promo",
  "stock": 12,
  "price": 199.99
}
```

### Cart Items
```json
{
  "productId": "P100",
  "quantity": 2,
  "unit_price": 199.99,
  "line_total": 399.98,
  "discounted_unit_price": 179.99,
  "line_total_discounted": 359.98,
  "savings_total": 40.00
}
```

## Frontend Components

### ProductSection.astro
- Displays product catalog
- Handles add-to-cart functionality
- Shows discount prices for VIP customers

### CartDrawer.astro
- Modal shopping cart interface
- Real-time quantity updates
- Discount summary display

### Customer Management
- `customerId.js`: Handles customer selection and cart clearing
- `cartDrawer.js`: Basic modal functionality

## Docker Configuration

### Dockerfile
- Multi-stage build (Node.js + Python)
- Optimized image size
- Non-root user for security
- Health checks included

### Docker Compose
- Single service configuration
- Volume mounting for data persistence
- Port mapping for development

## Security Features

- Non-root Docker user
- Input validation on API endpoints
- CORS configuration
- SQL injection protection with parameterized queries

## Testing

### Manual Testing
1. Start both backend and frontend
2. Select a customer (C1001 or C1002)
3. Add products to cart
4. Verify discount calculations
5. Test quantity updates
6. Switch customers and verify cart clearing

### API Testing
```bash
# Test products endpoint
curl http://localhost:8000/products

# Test cart endpoint
curl http://localhost:8000/cart

# Test annotated cart with customer
curl "http://localhost:8000/cart/annotated?customer_id=C1001"
```

## Project Structure

```
novafon-case-neu/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── data/               # Database files
├── frontend/
│   ├── src/
│   │   ├── components/     # Astro components
│   │   ├── layouts/        # Page layouts
│   │   ├── pages/          # Route pages
│   │   ├── scripts/        # JavaScript modules
│   │   └── styles/         # CSS files
│   ├── package.json        # Node dependencies
│   └── astro.config.mjs    # Astro configuration
├── data/
│   ├── products.db         # SQLite database
│   ├── crm_data.json       # Customer data
│   └── shopping_cart.json  # Cart storage
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── README.md              # This file
```

## Deployment

### Production Deployment
1. Build the Docker image
2. Configure environment variables
3. Set up reverse proxy (nginx)
4. Configure SSL certificates
5. Set up monitoring and logging

### Environment Variables
- `PYTHONUNBUFFERED=1` - Python output buffering
- `CUSTOMER_ID` - Default customer ID (optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.