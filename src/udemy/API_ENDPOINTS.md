# Udemy Learning Platform API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication Endpoints

### User Registration
```
POST /api/auth/register/
```
**Request Body:**
```json
{
    "username": "user@example.com",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "password123",
    "password_confirm": "password123"
}
```

### User Login
```
POST /api/auth/login/
```
**Request Body:**
```json
{
    "username": "user@example.com",
    "password": "password123"
}
```

### User Logout
```
POST /api/auth/logout/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
    "refresh_token": "your_refresh_token"
}
```

### Get User Profile
```
GET /api/auth/profile/
```
**Headers:** `Authorization: Bearer <token>`

### Update User Profile
```
PUT /api/auth/profile/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
    "bio": "Updated bio",
    "phone": "+1234567890"
}
```

### Upload Avatar
```
POST /api/auth/profile/avatar/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:** `multipart/form-data` with `avatar` file

## Course Endpoints

### Get All Courses
```
GET /api/courses/
```

**Query Parameters:**
- `search`: Search in title, description, or instructor
- `main_category`: Filter by main category ID
- `created_by`: Filter by instructor name
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `min_rating`: Minimum rating filter
- `sort_by`: Sort options (newest, price-low, price-high, rating)
- `limit`: Limit number of results

### Get Course Details
```
GET /api/courses/{course_id}/
```

### Get Course Videos (Authenticated)
```
GET /api/courses/{course_id}/videos/
```
**Headers:** `Authorization: Bearer <token>`

### Purchase Course (Authenticated)
```
POST /api/courses/{course_id}/purchase/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
    "payment_method": "online",
    "transaction_id": "txn_123456"
}
```

### Get Course Reviews
```
GET /api/courses/{course_id}/reviews/
```

### Add Course Review (Authenticated)
```
POST /api/courses/{course_id}/reviews/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
    "rating": 5,
    "comment": "Great course!"
}
```

## Video Endpoints

### Mark Video as Completed (Authenticated)
```
POST /api/videos/{video_id}/complete/
```
**Headers:** `Authorization: Bearer <token>`

### Update Video Progress (Authenticated)
```
POST /api/videos/{video_id}/update_progress/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
    "current_time": 120
}
```

## User Learning Endpoints

### Get My Purchased Courses (Authenticated)
```
GET /api/my-courses/
```
**Headers:** `Authorization: Bearer <token>`

### Get Learning Dashboard (Authenticated)
```
GET /api/dashboard/
```
**Headers:** `Authorization: Bearer <token>`

### Get My Course Progress (Authenticated)
```
GET /api/progress/
```
**Headers:** `Authorization: Bearer <token>`

## Category Endpoints

### Get All Main Categories
```
GET /api/main-categories/
```

### Get Main Category with Subcategories
```
GET /api/main-categories/{category_id}/
```

### Get All Subcategories
```
GET /api/subcategories/
```

## Response Formats

### Success Response
```json
{
    "status": "success",
    "message": "Operation completed successfully",
    "data": {
        // Response data
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description",
    "errors": {
        // Validation errors
    }
}
```

### Course Object
```json
{
    "id": 1,
    "title": "Course Title",
    "description": "Course description",
    "price": "999.00",
    "image": "/media/courses/course_image.jpg",
    "rating_point": "4.5",
    "reviews": "150",
    "created_by": "Instructor Name",
    "premium": false,
    "best_seller": true,
    "main_category": "Development",
    "purchased": true,
    "progress": 75.5,
    "videos": [...],
    "reviews": [...]
}
```

### Video Object
```json
{
    "id": 1,
    "title": "Video Title",
    "description": "Video description",
    "video_file": "/media/course_videos/video.mp4",
    "duration": "00:15:30",
    "order": 1,
    "is_preview": false,
    "is_completed": true,
    "watched_duration": 930.0
}
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## File Uploads

For file uploads (avatars, course images, videos), use `multipart/form-data` content type.

## Error Codes

- `400`: Bad Request - Invalid data
- `401`: Unauthorized - Missing or invalid token
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Server error 