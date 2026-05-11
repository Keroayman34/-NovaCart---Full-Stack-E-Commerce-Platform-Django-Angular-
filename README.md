# NovaCart - Full Stack E-Commerce Platform

A modern, scalable e-commerce platform built with Django REST Framework for the backend and Angular for the frontend. NovaCart provides a complete solution for online retail with features including product management, shopping cart, order processing, payments, user reviews, and more.

## ✨ Features

### Core Features

- **User Authentication & Authorization** - Secure user registration, login, and role-based access control
- **Product Management** - Comprehensive product catalog with filtering, search, and categorization
- **Shopping Cart** - Smart cart management with guest cart support and cart merging
- **Checkout Process** - Seamless checkout with order creation and tracking
- **Payment Integration** - Multiple payment method support
- **Order Management** - Complete order lifecycle management with status tracking
- **User Reviews & Ratings** - Product review system with user ratings
- **Wishlist** - Save favorite products for later
- **Notifications** - Real-time user notifications system
- **Admin Dashboard** - Seller/admin panel for managing products and orders

### Technical Features

- RESTful API architecture
- JWT-based authentication
- Comprehensive error handling
- API throttling and rate limiting
- Pagination support
- Advanced filtering and search capabilities
- Test coverage with pytest

## 🛠 Tech Stack

### Backend

- **Framework**: Django 4.x
- **API**: Django REST Framework
- **Database**: PostgreSQL (recommended) / SQLite (default)
- **Authentication**: Django JWT
- **Testing**: pytest, pytest-django
- **API Documentation**: DRF Spectacular

### Frontend

- **Framework**: Angular 15+
- **Language**: TypeScript
- **Styling**: SCSS
- **HTTP Client**: Angular HttpClientModule
- **Routing**: Angular Router
- **State Management**: Services-based architecture

### DevOps & Tools

- **Version Control**: Git
- **Package Management**: pip (Python), npm (Node.js)

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- PostgreSQL 12+ (optional, SQLite for development)

## 🚀 Installation

### Backend Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd E-Commerce/Backend
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
   Create a `.env` file in the `Backend/` directory:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Create a superuser**

```bash
python manage.py createsuperuser
```

7. **Collect static files**

```bash
python manage.py collectstatic --noinput
```

8. **Start the development server**

```bash
python manage.py runserver
```

Backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**

```bash
cd E-Commerce/Frontend
```

2. **Install dependencies**

```bash
npm install
```

3. **Configure environment**
   Update `src/environments/environment.ts` if needed:

```typescript
export const environment = {
  production: false,
  apiUrl: "http://localhost:8000/api",
};
```

4. **Start development server**

```bash
ng serve
```

Frontend will be available at `http://localhost:4200`

## 📁 Project Structure

### Backend Structure

```
Backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
├── apps/                    # Django applications
│   ├── cart/               # Shopping cart functionality
│   ├── notifications/      # Notification system
│   ├── orders/             # Order management
│   ├── payments/           # Payment processing
│   ├── products/           # Product catalog
│   ├── reviews/            # User reviews
│   ├── users/              # User management
│   └── wishlist/           # Wishlist feature
├── config/                 # Django configuration
│   ├── settings.py         # Main settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI config
└── core/                   # Shared utilities
    ├── exceptions.py       # Custom exceptions
    ├── models.py          # Base models
    ├── pagination.py      # API pagination
    ├── permissions.py     # Custom permissions
    └── utils.py           # Utility functions
```

### Frontend Structure

```
Frontend/
├── src/
│   ├── app/
│   │   ├── core/           # Core services and guards
│   │   │   ├── guards/     # Route guards
│   │   │   └── services/   # Core services
│   │   ├── features/       # Feature modules
│   │   │   ├── admin/      # Admin features
│   │   │   ├── auth/       # Authentication
│   │   │   ├── cart/       # Cart features
│   │   │   ├── checkout/   # Checkout process
│   │   │   ├── orders/     # Order management
│   │   │   ├── products/   # Product features
│   │   │   ├── profile/    # User profile
│   │   │   ├── seller/     # Seller features
│   │   │   └── wishlist/   # Wishlist
│   │   └── shared/         # Shared components
│   ├── environments/       # Environment configs
│   └── styles.scss         # Global styles
└── angular.json            # Angular configuration
```

## 🔧 Configuration

### Backend Configuration

Key settings in `Backend/config/settings.py`:

- **INSTALLED_APPS**: Installed Django apps
- **DATABASES**: Database configuration
- **REST_FRAMEWORK**: DRF settings
- **AUTHENTICATION_CLASSES**: Auth configuration
- **CORS_ALLOWED_ORIGINS**: CORS settings

### Frontend Configuration

API endpoint configuration:

- Development: `src/environments/environment.ts`
- Production: `src/environments/environment.prod.ts`

## 🧪 Testing

### Backend Tests

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest Backend/apps/products/tests/test_models.py
```

Run with coverage:

```bash
pytest --cov=apps
```

### Frontend Tests

Run unit tests:

```bash
ng test
```

Run with coverage:

```bash
ng test --code-coverage
```

## 📊 API Endpoints

### Main App Endpoints

- **Products**: `/api/products/`
- **Cart**: `/api/cart/`
- **Orders**: `/api/orders/`
- **Users**: `/api/users/`
- **Reviews**: `/api/reviews/`
- **Wishlist**: `/api/wishlist/`
- **Notifications**: `/api/notifications/`
- **Payments**: `/api/payments/`

See individual app files for detailed endpoint documentation.

## 🔐 Authentication

The platform uses JWT (JSON Web Tokens) for authentication:

1. User logs in with credentials
2. Backend returns JWT access and refresh tokens
3. Frontend stores tokens and includes them in API requests
4. Backend validates tokens for protected endpoints

## 🚢 Deployment

### Backend Deployment

1. Set up production environment variables
2. Configure allowed hosts
3. Set `DEBUG = False`
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Set up a production database
6. Configure static files serving
7. Set up SSL/TLS certificates

### Frontend Deployment

1. Build for production:

```bash
ng build --configuration production
```

2. Serve the built files from a web server (Nginx, Apache)
3. Configure proxy rules for API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 for Python code
- Follow Angular style guide for TypeScript
- Write tests for new features
- Update documentation

## 📝 License

This project is open source and available under the MIT License.

## 📧 Support

For support, email support@novacart.com or open an issue in the repository.

## 🙏 Acknowledgments

- Django REST Framework team
- Angular team
- All contributors and community members

---

**Built with ❤️ by the NovaCart Team**
