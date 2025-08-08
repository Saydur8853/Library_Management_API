# Library Management API

A comprehensive Library Management System API built with Django REST Framework, featuring user authentication, book management, borrowing system, and penalty tracking with complete Swagger documentation.

## Features

- **JWT-based Authentication**: Secure token-based authentication system
- **User Registration & Login**: Complete user management with custom User model
- **Book Management**: Full CRUD operations for books, authors, and categories
- **Borrowing System**: Book borrowing and returning with atomic inventory updates
- **Business Rules**: 3-book borrowing limit, 14-day loan period
- **Penalty System**: Automatic penalty calculation (1 point per day late)
- **Admin Controls**: Admin-only content management and user oversight
- **Advanced Filtering**: Search and filter across all entities
- **API Documentation**: Complete Swagger/OpenAPI 3.0 documentation
- **Transaction Safety**: Atomic database operations for data consistency
- **CORS Support**: Cross-origin resource sharing enabled

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL/MySQL ready
- **Authentication**: JWT tokens via `djangorestframework-simplejwt`
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Filtering**: django-filter with search capabilities
- **CORS**: django-cors-headers
- **Testing**: Django TestCase with comprehensive coverage

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone and navigate to project:**
```bash
git clone <repository-url>
cd library_management_api
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run database migrations:**
```bash
python manage.py migrate
```

5. **Create superuser (optional):**
```bash
python manage.py createsuperuser
```

6. **Load sample data (optional):**
```bash
python manage.py create_sample_data
```

7. **Run the development server:**
```bash
python manage.py runserver
```

### Access URLs
- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Swagger Documentation**: http://localhost:8000/api/docs/
- **ReDoc Documentation**: http://localhost:8000/api/redoc/

## API Endpoints Overview

The API is organized into logical sections with proper Swagger tags for better documentation:

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | Register new user | No |
| POST | `/api/login/` | User login | No |

**Register Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Login Request:**
```json
{
  "username": "john_doe",
  "password": "secure_password123"
}
```

### Authors Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/authors/` | List all authors | No |
| POST | `/api/authors/` | Create author | Admin only |
| GET | `/api/authors/{id}/` | Get author details | No |
| PUT | `/api/authors/{id}/` | Update author | Admin only |
| DELETE | `/api/authors/{id}/` | Delete author | Admin only |

### Categories Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List all categories | No |
| POST | `/api/categories/` | Create category | Admin only |
| GET | `/api/categories/{id}/` | Get category details | No |
| PUT | `/api/categories/{id}/` | Update category | Admin only |
| DELETE | `/api/categories/{id}/` | Delete category | Admin only |

### Books Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/books/` | List books with filtering | No |
| POST | `/api/books/` | Create book | Admin only |
| GET | `/api/books/{id}/` | Get book details | No |
| PUT | `/api/books/{id}/` | Update book | Admin only |
| DELETE | `/api/books/{id}/` | Delete book | Admin only |

**Advanced Filtering & Search:**
```bash
# Search across title, author name, category name
/api/books/?search=django

# Filter by author or category
/api/books/?author=1&category=2

# Ordering options
/api/books/?ordering=title          # A-Z
/api/books/?ordering=-created_at    # Newest first
```

### Borrowing Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/borrow/` | Borrow a book | Yes |
| GET | `/api/my-borrows/` | List active borrows | Yes |
| POST | `/api/return/` | Return a book | Yes |

**Borrow Book Request:**
```json
{
  "book_id": 1
}
```

**Borrowing Validations:**
- ✅ User has less than 3 active borrows
- ✅ Book has available copies (> 0)
- ✅ Atomic inventory update and borrow record creation
- ✅ Automatic due date calculation (14 days)

**Return Book Request:**
```json
{
  "borrow_id": 1
}
```

**Return Process:**
- ✅ Sets return date
- ✅ Restores book inventory atomically
- ✅ Calculates and applies penalties for late returns
- ✅ Returns penalty information in response

### User Management Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/{id}/penalties/` | Get user penalties | Admin or self |

## Database Schema

### User Model (Custom)
```python
class User(AbstractUser):
    penalty_points = models.IntegerField(default=0)
    # Inherits: username, email, first_name, last_name, is_staff, etc.
```

### Core Models
```python
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()  # Auto-calculated: borrow_date + 14 days
    return_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Project Structure

```
library_management_api/
├── authentication/          # User authentication app
│   ├── models.py           # Custom User model with penalty_points
│   ├── serializers.py      # User serializers
│   ├── views.py            # Auth and penalty views
│   └── urls.py             # Auth endpoints
├── books/                   # Books management app
│   ├── models.py           # Author, Category, Book, Borrow models
│   ├── serializers.py      # Book-related serializers
│   ├── views.py            # Book CRUD and borrowing views
│   ├── urls.py             # Book and borrowing endpoints
│   └── management/commands/
│       └── create_sample_data.py  # Sample data generator
├── library_management/      # Main project directory
│   ├── settings.py         # Project settings with drf-spectacular config
│   ├── urls.py             # Main URL configuration
│   └── serializers.py      # Root API serializers
├── requirements.txt         # Project dependencies
├── db.sqlite3              # SQLite database (development)
└── manage.py               # Django management script
```

## Authentication & Security

### JWT Token Authentication
Most endpoints require JWT authentication. Include the token in request headers:

```bash
Authorization: Bearer <your_access_token>
```

### Token Lifecycle
- **Access Token**: 1 hour lifetime
- **Refresh Token**: 7 days lifetime
- **Token Rotation**: Enabled for security
- **Auto-logout**: On token expiry

### Permission Levels
- **Public**: Read access to books, authors, categories
- **Authenticated**: Can borrow/return books, view own data
- **Admin**: Full CRUD access to all resources

## Admin Interface

Access Django admin at `/admin/` for:
- 👥 **User Management**: View users and penalty points
- 📚 **Content Management**: Books, authors, categories
- 📋 **Borrowing History**: Track loans and returns
- ⚠️ **Overdue Monitoring**: Identify late returns

## Business Logic & Rules

### 📚 Borrowing System Rules
- **Maximum Loans**: 3 books per user simultaneously
- **Loan Duration**: 14 days from borrow date
- **Inventory Check**: Only available copies can be borrowed
- **Atomic Operations**: All borrowing/returning uses database transactions

### ⚖️ Penalty System
- **Late Fee**: 1 penalty point per day overdue
- **Automatic Calculation**: Applied during book return process
- **Persistent Tracking**: Penalty points stored in user profile
- **Admin Visibility**: Admins can monitor user penalties

### 🔐 Permission Matrix
| Resource | Public | Authenticated | Admin |
|----------|--------|---------------|-------|
| Books (Read) | ✅ | ✅ | ✅ |
| Books (Write) | ❌ | ❌ | ✅ |
| Borrowing | ❌ | ✅ | ✅ |
| User Penalties | ❌ | Own only | All users |
| Admin Panel | ❌ | ❌ | ✅ |

## API Documentation

### Interactive Documentation
The API includes comprehensive interactive documentation:

- **🔗 Swagger UI**: http://localhost:8000/api/docs/
  - Interactive API testing
  - Request/response schemas
  - Authentication integration
  - Try-it-out functionality

- **📖 ReDoc**: http://localhost:8000/api/redoc/
  - Clean, readable documentation
  - Detailed model schemas
  - Code examples

- **⚙️ OpenAPI Schema**: http://localhost:8000/api/schema/
  - Raw OpenAPI 3.0 specification
  - For integration tools

### Documentation Features
- ✅ **Organized by Tags**: Authentication, Books, Authors, Categories, Borrowing, User Management
- ✅ **Complete Schemas**: All request/response models documented
- ✅ **Permission Info**: Clear auth requirements for each endpoint
- ✅ **Error Responses**: Detailed error code documentation
- ✅ **Interactive Testing**: Built-in API client

## Usage Examples

### 1. User Registration & Authentication
```bash
# Register new user
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login to get tokens
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password123"
  }'
```

### 2. Browse Books with Filtering
```bash
# List all books
curl "http://localhost:8000/api/books/"

# Search books by title/author
curl "http://localhost:8000/api/books/?search=django"

# Filter by category and author
curl "http://localhost:8000/api/books/?category=1&author=2"

# Sort books by title
curl "http://localhost:8000/api/books/?ordering=title"
```

### 3. Borrowing Operations
```bash
# Borrow a book
curl -X POST http://localhost:8000/api/borrow/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1}'

# Check active borrows
curl -X GET http://localhost:8000/api/my-borrows/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Return a book
curl -X POST http://localhost:8000/api/return/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"borrow_id": 1}'
```

### 4. Check User Penalties
```bash
# View own penalties
curl -X GET http://localhost:8000/api/users/1/penalties/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing & Quality Assurance

### Run Test Suite
```bash
# Run all tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML coverage report
```

### Validation & Error Handling
The API includes comprehensive validation:

- ✅ **Input Validation**: All request data validated
- ✅ **Business Rule Enforcement**: Borrowing limits, availability checks
- ✅ **Permission Checks**: Role-based access control
- ✅ **Atomic Operations**: Database transaction safety
- ✅ **Error Messages**: Clear, actionable error responses
- ✅ **Status Codes**: Proper HTTP status code usage

### Sample Data Generation
```bash
# Create sample authors, categories, books for testing
python manage.py create_sample_data
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set secure `SECRET_KEY`
- [ ] Configure static files serving
- [ ] Update `ALLOWED_HOSTS`
- [ ] Configure CORS for production domains
- [ ] Set up HTTPS
- [ ] Configure logging
- [ ] Set up monitoring

### Environment Variables
```bash
# Example production settings
export DEBUG=False
export SECRET_KEY="your-secure-secret-key"
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions/classes
- Update documentation for API changes
- Ensure backward compatibility
- Write comprehensive tests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support & Issues

- 📋 **Issues**: Use GitHub Issues for bug reports
- 📖 **Documentation**: Check `/api/docs/` for API reference
- 💡 **Feature Requests**: Submit via GitHub Issues with enhancement label
- 🔍 **API Testing**: Use Swagger UI for interactive testing
