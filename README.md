# Novafon Case - E-Commerce Application

A comprehensive e-commerce application built with FastAPI (backend) and Astro (frontend), featuring an advanced customer loyalty discount system, real-time shopping cart management, and seamless customer account switching.

## Features

- **Product Catalog Management**: SQLite-based product database with real-time pricing display
- **Advanced Shopping Cart**: Live updates with quantity management and instant discount calculation
- **VIP Customer Loyalty System**: Automatic 10% discount calculation for eligible customers on promotional products
- **Multi-Customer Support**: Dynamic customer ID switching with cart isolation between accounts
- **Real-time Discount Engine**: Backend-calculated pricing with frontend display of original, discounted, and savings amounts
- **Responsive Design**: Modern UI with Tailwind CSS and mobile-first approach
- **Docker Containerization**: Complete deployment-ready setup with multi-stage builds

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11 and automatic API documentation
- **Database**: SQLite3 with JSON data persistence for cart and CRM data
- **API Design**: RESTful API with comprehensive error handling and CORS support
- **Discount Engine**: Real-time VIP customer discount calculation with 10% reduction on promotional products
- **Customer Management**: CRM integration with order history and loyalty status tracking
- **Data Persistence**: File-based storage for shopping cart and customer data with atomic operations

### Frontend (Astro)
- **Framework**: Astro with TypeScript for static site generation and client-side hydration
- **Styling**: Tailwind CSS with custom component styling and responsive design
- **Real-time Updates**: Client-side cart management with live discount calculation display
- **Customer Selection**: Dynamic customer ID switching with automatic cart clearing between sessions
- **Component Architecture**: Modular design with ProductSection and CartDrawer components

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
- **C1001**: VIP customer with loyalty discounts (total orders > €1000)
- **C1002**: Regular customer without discount eligibility
- **Enter**: Defaults to C1001 for demonstration purposes

### Shopping Experience
1. **Browse Products**: View available products with real-time pricing from SQLite database
2. **Add to Cart**: Click the shopping cart icon to add items with automatic quantity calculation
3. **View Cart**: Click the cart button in the top-right corner to open the modal drawer
4. **Manage Quantities**: Use +/- buttons for precise quantity control or remove items entirely
5. **See Discounts**: VIP customers automatically receive 10% discounts on promotional products with stock >= 5

### Cart Features
- **Live Updates**: Cart updates in real-time without page refresh using innerHTML rendering
- **Comprehensive Discount Display**: Shows original price, discounted unit price, line totals, and total savings
- **Advanced Quantity Management**: Increase, decrease, or remove items with backend synchronization
- **Customer-Specific Isolation**: Cart is automatically cleared when switching customers to prevent data mixing
- **Discount Summary**: Aggregated view of total savings and discounted subtotal for eligible items

## API Endpoints

### Products
- `GET /products` - Retrieve all products from SQLite database with ID, name, category, stock, and pricing
- `GET /products/{product_id}` - Get specific product details by ID

### Cart Management
- `GET /cart` - Get current cart contents with product IDs and quantities
- `PUT /cart` - Update entire cart with new items array (used for cart clearing)
- `PUT /cart/items/{product_id}` - Update specific item quantity with automatic discount recalculation
- `GET /cart/annotated?customer_id={id}` - Get cart with comprehensive discount calculations including:
  - Original and discounted unit prices
  - Line totals with and without discounts
  - Individual item savings calculations
  - Aggregated subtotal, discounted subtotal, and total savings

### Customer Management
- `GET /customer/{customer_id}/orders` - Get complete customer order history from CRM database
- `GET /customer/{customer_id}/discount` - Get customer discount eligibility based on total order value
- `GET /orders` - Retrieve all orders from the system

### Discount Engine
The `/cart/annotated` endpoint performs sophisticated discount calculations:
- **VIP Status Check**: Determines customer eligibility based on total order history
- **Product Eligibility**: Only promotional products with stock >= 5 are discountable
- **Discount Calculation**: 10% reduction applied to eligible products for VIP customers
- **Real-time Pricing**: All calculations performed server-side for consistency

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
- **Product Catalog Display**: Renders all products from backend API with SSR data fetching
- **Add-to-Cart Functionality**: Handles product addition with quantity calculation and backend synchronization
- **Discount Price Display**: Shows VIP customer discount prices using `discounted_unit_price` from annotated cart
- **Real-time Updates**: Refreshes discount display after cart modifications

### CartDrawer.astro
- **Modal Shopping Cart Interface**: Slide-out drawer with backdrop and focus management
- **Dynamic Cart Rendering**: Uses innerHTML for real-time item display with comprehensive discount information
- **Advanced Quantity Management**: Increase/decrease/remove buttons with event delegation
- **Discount Summary Display**: Shows aggregated savings and discounted subtotal for eligible items
- **Customer-Specific Data**: All API calls include customer_id parameter for proper isolation

### Customer Management
- **customerId.js**: Handles customer selection via prompt and global storage, automatically clears cart on reload
- **cartDrawer.js**: Basic modal functionality for opening/closing drawer with backdrop click handling

### Cart Logic Implementation
The CartDrawer component implements sophisticated cart management:
- **Real-time Loading**: `loadCart()` function fetches annotated cart data and renders items dynamically
- **Discount Display**: Shows original price, discounted price, and savings per item with conditional rendering
- **Quantity Updates**: `updateProductQuantity()` handles backend synchronization with proper error handling
- **Event Delegation**: Single event listener handles all cart interactions for optimal performance

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

## Technical Implementation Details

### Backend Discount Logic
The FastAPI backend implements a sophisticated discount calculation system in the `cart_annotated` endpoint:

1. **Customer VIP Status Determination**: 
   - Retrieves customer order history from CRM database
   - Calculates total order value across all historical orders
   - Determines VIP status based on configurable threshold (default: €1000+)

2. **Product Eligibility Assessment**:
   - Identifies promotional products from product database
   - Validates stock levels (minimum 5 units required for discount eligibility)
   - Creates discountable product set for efficient lookup

3. **Real-time Price Calculation**:
   - Applies 10% discount to eligible products for VIP customers
   - Calculates line totals with and without discounts
   - Computes individual and aggregate savings amounts
   - Ensures all monetary values are properly rounded to 2 decimal places

### Frontend Cart Management
The Astro frontend implements real-time cart updates using modern web technologies:

1. **Dynamic Content Rendering**:
   - Uses innerHTML for efficient DOM updates without full page reloads
   - Implements event delegation for optimal performance with dynamic content
   - Provides comprehensive error handling for network failures

2. **Customer Session Management**:
   - Global customer ID storage using `window.customerId`
   - Automatic cart clearing on customer switch to prevent data mixing
   - Persistent customer selection across component interactions



## Author

**Max Hersam** -

## Support

