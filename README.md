# Better Mart - Inventory Management System

A Django REST Framework-based backend for an inventory management system with user authentication and basic e-commerce functionality.

## Features

- Custom User Authentication with email
- Product and Category Management
- Shopping Cart Functionality
- Order Management System
- RESTful API Endpoints

## Tech Stack

- Django
- Django REST Framework
- MySQL 

## Installation & Setup

1. Clone the repository
```bash
git clone <repository-url>
cd backend_better_mart
```

2. Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication Endpoints
```
POST   /api/account/register/      - Register new user
POST   /api/accounnt/login/        - Login user

```

### User Profile
```
GET    /api/account/profile/       - Get information a user

```

### Categories
```
GET    /api/store/categories/      - List all categories
POST   /api/store/categories/      - Create new category (Admin only)
GET    /api/store/categories/{id}/ - Retrieve category details
PUT    /api/store/categories/{id}/ - Update category (Admin only)
DELETE /api/store/categories/{id}/ - Delete category (Admin only)
```

### Products
```
GET    /api/store/products/        - List all products
POST   /api/store/products/        - Create new product (Admin only)
GET    /api/store/products/{id}/   - Retrieve product details
PUT    /api/store/products/{id}/   - Update product (Admin only)
DELETE /api/store/products/{id}/   - Delete product (Admin only)
```

### Shopping Cart
```
GET    /api/store/carts/            - List  cart items of a user
POST   /api/store/carts/            - Add item to cart
GET    /api/store/carts/{id}/       - Retrieve cart item details of a user
PUT    /api/store/carts/{id}/       - Update cart item
DELETE /api/store/carts/{id}/       - Remove item from cart
```

### Orders
```
GET    /api/store/orders/          - List user's orders
POST   /api/store/orders/          - Create new order
GET    /api/store/orders/{id}/     - Retrieve order details
PUT    /api/store/orders/{id}/     - Update order status (Admin only)
DELETE /api/store/orders/{id}/     - Delete order (Admin only)
```



## Authentication

The API uses token-based authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Permissions

- Anonymous users can view products and categories
- Authenticated users can manage their cart and place orders
- Admin users have full access to all endpoints
- Regular users can only view and manage their own data

## Error Handling

The API returns standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
