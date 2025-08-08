# Library Management API

A comprehensive Library Management System API built with Django REST Framework, featuring user authentication, book management, borrowing system, and penalty tracking.

## Features

- **JWT-based Authentication**: Secure token-based authentication system
- **User Registration & Login**: Complete user management with custom User model
- **Book Management**: Full CRUD operations for books, authors, and categories
- **Borrowing System**: Book borrowing and returning with atomic inventory updates
- **Business Rules**: 3-book borrowing limit, 14-day loan period
- **Penalty System**: Automatic penalty calculation (1 point per day late)
- **Admin Controls**: Admin-only content management and user oversight
- **Advanced Filtering**: Search and filter across all entities
- **Transaction Safety**: Atomic database operations for data consistency
- **CORS Support**: Cross-origin resource sharing enabled

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: SQLite (development)
- **Authentication**: JWT tokens via `djangorestframework-simplejwt`
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
git clone https://github.com/Saydur8853/Library_Management_API.git
cd Library_Management_API
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

## API Endpoints Overview

The API is organized into logical sections:

### Authentication Endpoints

| Method | Endpoint           | Description       | Auth Required |
| ------ | ------------------ | ----------------- | ------------- |
| POST   | `/api/register/` | Register new user | No            |
| POST   | `/api/login/`    | User login        | No            |

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

| Method | Endpoint               | Description        | Auth Required |
| ------ | ---------------------- | ------------------ | ------------- |
| GET    | `/api/authors/`      | List all authors   | No            |
| POST   | `/api/authors/`      | Create author      | Admin only    |
| GET    | `/api/authors/{id}/` | Get author details | No            |
| PUT    | `/api/authors/{id}/` | Update author      | Admin only    |
| DELETE | `/api/authors/{id}/` | Delete author      | Admin only    |

### Categories Endpoints

| Method | Endpoint                  | Description          | Auth Required |
| ------ | ------------------------- | -------------------- | ------------- |
| GET    | `/api/categories/`      | List all categories  | No            |
| POST   | `/api/categories/`      | Create category      | Admin only    |
| GET    | `/api/categories/{id}/` | Get category details | No            |
| PUT    | `/api/categories/{id}/` | Update category      | Admin only    |
| DELETE | `/api/categories/{id}/` | Delete category      | Admin only    |

### Books Endpoints

| Method | Endpoint             | Description               | Auth Required |
| ------ | -------------------- | ------------------------- | ------------- |
| GET    | `/api/books/`      | List books with filtering | No            |
| POST   | `/api/books/`      | Create book               | Admin only    |
| GET    | `/api/books/{id}/` | Get book details          | No            |
| PUT    | `/api/books/{id}/` | Update book               | Admin only    |
| DELETE | `/api/books/{id}/` | Delete book               | Admin only    |

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

| Method | Endpoint             | Description         | Auth Required |
| ------ | -------------------- | ------------------- | ------------- |
| POST   | `/api/borrow/`     | Borrow a book       | Yes           |
| GET    | `/api/my-borrows/` | List active borrows | Yes           |
| POST   | `/api/return/`     | Return a book       | Yes           |

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

| Method | Endpoint                       | Description        | Auth Required |
| ------ | ------------------------------ | ------------------ | ------------- |
| GET    | `/api/users/{id}/penalties/` | Get user penalties | Admin or self |

## Database Schema & ER Diagram

### Entity-Relationship Diagram

```
┌─────────────────────────┐
│         User            │
├─────────────────────────┤
│ id (PK)                 │
│ username (UNIQUE)       │
│ password                │
│ email                   │
│ first_name              │
│ last_name               │
│ is_staff                │
│ is_active               │
│ is_superuser            │
│ last_login              │
│ date_joined             │
│ penalty_points          │
└─────────────────────────┘
              │
              │ 1:N
              │
              ▼
┌─────────────────────────┐
│        Borrow           │
├─────────────────────────┤
│ id (PK)                 │
│ user_id (FK)            │
│ book_id (FK)            │
│ borrow_date             │
│ due_date                │
│ return_date             │
│ created_at              │
└─────────────────────────┘
              │
              │ N:1
              │
              ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│         Book            │         │        Author           │
├─────────────────────────┤         ├─────────────────────────┤
│ id (PK)                 │         │ id (PK)                 │
│ title                   │  N:1    │ name                    │
│ description             │ ◄─────── │ bio                     │
│ author_id (FK)          │         │ created_at              │
│ category_id (FK)        │         └─────────────────────────┘
│ total_copies            │
│ available_copies        │
│ created_at              │         ┌─────────────────────────┐
│ updated_at              │         │       Category          │
└─────────────────────────┘         ├─────────────────────────┤
              │                     │ id (PK)                 │
              │ N:1                 │ name                    │
              └───────────────────► │ created_at              │
                                    └─────────────────────────┘
```

### Relationships

- **Author → Book** (One-to-Many): Each author can write multiple books
- **Category → Book** (One-to-Many): Each category can contain multiple books  
- **User → Borrow** (One-to-Many): Each user can borrow multiple books
- **Book → Borrow** (One-to-Many): Each book can have multiple borrow records

### User Model (Custom)

```python
class User(AbstractUser):
    penalty_points = models.IntegerField(default=0)
    # Inherits: username, email, first_name, last_name, is_staff, etc.
```

### Core Models

```python
class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()  # Auto-calculated: borrow_date + 14 days
    return_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
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

### 📚 Borrowing/Return Logic

#### How Borrowing Works:

1. **Pre-Borrowing Validations**:
   - User must be authenticated
   - User must have fewer than 3 active (unreturned) borrows
   - Book must have available copies (`available_copies > 0`)
   - Book must exist in the system

2. **Atomic Borrowing Process**:
   ```python
   # Database transaction ensures data consistency
   with transaction.atomic():
       # Decrease available copies
       book.available_copies -= 1
       book.save()
       
       # Create borrow record
       borrow = Borrow.objects.create(
           user=user,
           book=book,
           due_date=timezone.now() + timedelta(days=14)
       )
   ```

3. **Automatic Due Date Calculation**:
   - Due date is automatically set to **14 days** from borrow date
   - No manual due date input required
   - Due date is calculated using Django's timezone-aware datetime

#### How Returning Works:

1. **Return Validations**:
   - User must own the borrow record
   - Book must not already be returned (`return_date` must be null)
   - Borrow record must exist

2. **Atomic Return Process**:
   ```python
   with transaction.atomic():
       # Set return date
       borrow.return_date = timezone.now()
       
       # Calculate penalties if late
       penalty_points = borrow.calculate_penalty_on_return()
       if penalty_points > 0:
           user.penalty_points += penalty_points
           user.save()
       
       # Restore book inventory
       book.available_copies += 1
       book.save()
       
       borrow.save()
   ```

3. **Return Response**:
   ```json
   {
     "message": "Book returned successfully",
     "penalty_applied": 3,
     "total_penalty_points": 8,
     "was_overdue": true,
     "days_late": 3
   }
   ```

### ⚖️ Penalty Point System

#### How Penalties Are Calculated:

1. **Penalty Formula**:
   ```python
   def calculate_penalty_on_return(self):
       if not self.return_date:
           return 0
       
       if self.return_date > self.due_date:
           days_late = (self.return_date - self.due_date).days
           return days_late  # 1 point per day late
       return 0
   ```

2. **When Penalties Apply**:
   - Only applied when a book is **actually returned**
   - Based on the difference between `return_date` and `due_date`
   - **1 penalty point = 1 day late**
   - Partial days count as full days (e.g., 1.5 days late = 2 penalty points)

3. **Penalty Examples**:
   - Due: Jan 15, Returned: Jan 15 → **0 points** (on time)
   - Due: Jan 15, Returned: Jan 18 → **3 points** (3 days late)
   - Due: Jan 15, Returned: Jan 25 → **10 points** (10 days late)

4. **Real-time Overdue Detection**:
   ```python
   @property
   def is_overdue(self):
       if self.return_date:  # Already returned
           return False
       return timezone.now() > self.due_date
   
   @property
   def days_overdue(self):
       if not self.is_overdue:
           return 0
       return (timezone.now() - self.due_date).days
   ```

#### Penalty Point Management:

- **Accumulation**: Penalty points accumulate in the user's profile
- **Persistence**: Points remain even after book return
- **Admin Visibility**: Admins can view all user penalty points
- **No Automatic Reset**: Points persist unless manually adjusted by admin
- **Future Enhancement**: Could implement point expiration or redemption system

### ⚠️ Assumptions & Limitations

1. **Borrowing Assumptions**:
   - Users are trusted to return books (no reservation system)
   - No renewals system implemented (must return and re-borrow)
   - No waiting list or book reservation functionality
   - Book inventory is manually managed by administrators

2. **Penalty Limitations**:
   - No automatic blocking based on penalty points
   - No automatic notification system for overdue books
   - Penalties are only calculated upon return, not in real-time
   - No fine payment or point reduction system

3. **Technical Limitations**:
   - Uses SQLite for development (consider PostgreSQL for production)
   - No background tasks for sending reminders
   - No caching implemented for high-traffic scenarios
   - Book metadata is minimal (no ISBN, publisher info, etc.)

4. **Future Enhancements**:
   - Book reservation system
   - Automated email reminders for due dates
   - Barcode/QR code scanning for physical libraries
   - Integration with payment systems for penalty clearing
   - User-facing dashboard with borrowing history and recommendations

### 🔐 Permission Matrix

| Resource       | Public | Authenticated | Admin     |
| -------------- | ------ | ------------- | --------- |
| Books (Read)   | ✅     | ✅            | ✅        |
| Books (Write)  | ❌     | ❌            | ✅        |
| Borrowing      | ❌     | ✅            | ✅        |
| User Penalties | ❌     | Own only      | All users |
| Admin Panel    | ❌     | ❌            | ✅        |


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

## Support

- 📖 **Admin Panel**: Use `/admin/` for database management
- 🔍 **API Testing**: Use curl or Postman for API testing
