# Udemy Learning Platform - Backend

A comprehensive Django REST API backend for the Udemy-style learning platform.

## 🚀 Features

### ✅ Authentication & User Management
- JWT-based authentication
- User registration and login
- User profile management
- Avatar upload functionality
- Secure password handling

### ✅ Course Management
- Course CRUD operations
- Category and subcategory management
- Course search and filtering
- Course ratings and reviews
- Course purchase system

### ✅ Video Management
- Video upload and management
- Video progress tracking
- Video completion status
- Preview video functionality

### ✅ Learning Progress
- Course progress tracking
- Video completion tracking
- Learning dashboard
- Progress analytics

### ✅ Advanced Features
- Advanced search and filtering
- Sorting options (price, rating, popularity)
- Purchase status tracking
- Review system
- Admin panel management

## 🛠️ Technology Stack

- **Framework**: Django 5.2.1
- **API**: Django REST Framework 3.16.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **File Storage**: Local media storage
- **CORS**: django-cors-headers
- **Image Processing**: Pillow

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
cd backend/src/udemy
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Create a PostgreSQL database named `udemy1db` with user `udemy` and password `udemy123`, or update the database settings in `udemy/settings.py`.

### 5. Run Setup Script
```bash
python setup_backend.py
```

This script will:
- Run database migrations
- Create a superuser (admin/admin123)
- Create sample data

### 6. Run the Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 📚 API Documentation

Complete API documentation is available in `API_ENDPOINTS.md`

### Key Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/profile/avatar/` - Upload avatar

#### Courses
- `GET /api/courses/` - Get all courses (with filtering)
- `GET /api/courses/{id}/` - Get course details
- `GET /api/courses/{id}/videos/` - Get course videos
- `POST /api/courses/{id}/purchase/` - Purchase course
- `GET /api/courses/{id}/reviews/` - Get course reviews
- `POST /api/courses/{id}/reviews/` - Add course review

#### Learning
- `GET /api/my-courses/` - Get purchased courses
- `GET /api/dashboard/` - Get learning dashboard
- `GET /api/progress/` - Get course progress

#### Videos
- `POST /api/videos/{id}/complete/` - Mark video as completed
- `POST /api/videos/{id}/update_progress/` - Update video progress

## 🗄️ Database Models

### Core Models
- **User**: Extended Django User model with profile
- **UserProfile**: User profile with avatar and additional info
- **MainCategory**: Course main categories
- **SubCategory**: Course subcategories
- **Course**: Course information and metadata
- **Video**: Course video content
- **CoursePurchase**: Course purchase records
- **VideoProgress**: Video watching progress
- **CourseReview**: Course reviews and ratings
- **CourseProgress**: Overall course progress

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login/Register** to get access and refresh tokens
2. **Include token** in Authorization header: `Authorization: Bearer <token>`
3. **Refresh token** when access token expires

## 🎯 Frontend Integration

This backend is designed to work seamlessly with the Next.js frontend:

- **CORS** configured for frontend domain
- **JWT tokens** for secure authentication
- **File uploads** for avatars and course content
- **Real-time progress** tracking
- **Purchase system** integration

## 🛡️ Security Features

- JWT token authentication
- Password validation
- CORS protection
- File upload validation
- SQL injection protection
- XSS protection

## 📊 Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

**Default credentials**: admin/admin123

### Admin Features
- User management
- Course management
- Video management
- Purchase tracking
- Progress monitoring
- Review management

## 🧪 Testing

Run tests to ensure everything works correctly:

```bash
python manage.py test
```

## 📝 Environment Variables

Create a `.env` file in the project root for environment-specific settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Configure media file storage
5. Set up proper CORS origins
6. Use environment variables for sensitive data

### Docker Deployment
```bash
docker build -t udemy-backend .
docker run -p 8000:8000 udemy-backend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation
- Review the Django logs
- Check the admin panel for data issues
- Ensure all dependencies are installed

## 🔄 Updates

To update the backend:

1. Pull latest changes
2. Install new dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Restart the server

---

**Happy Learning! 🎓** 