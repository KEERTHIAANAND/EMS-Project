# EMS Backend - Django + MongoDB Atlas

A Django REST API backend for the Event Management System using MongoDB Atlas.

## Features

- **User Authentication**: JWT-based authentication with registration, login, logout
- **Event Management**: CRUD operations for events
- **RSVP System**: Allow users to RSVP for events
- **MongoDB Atlas Integration**: Cloud-based MongoDB database
- **RESTful API**: Clean API endpoints for frontend integration
- **CORS Support**: Configured for React frontend

## Tech Stack

- **Django 4.2.7**: Web framework
- **Django REST Framework**: API framework
- **MongoEngine**: MongoDB ODM for Django
- **PyJWT**: JWT token handling
- **MongoDB Atlas**: Cloud database
- **bcrypt**: Password hashing

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Git

### 2. Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. MongoDB Atlas Setup

1. Create a MongoDB Atlas account at https://www.mongodb.com/atlas
2. Create a new cluster
3. Create a database user
4. Get your connection string
5. Whitelist your IP address

### 4. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your MongoDB Atlas credentials
```

Update the `.env` file with your actual values:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ems_database?retryWrites=true&w=majority
MONGODB_DB_NAME=ems_database
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 5. Run the Server

```bash
# Run Django development server
python manage.py runserver 8000
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

### Events
- `GET /api/events/` - List all events
- `POST /api/events/` - Create new event
- `GET /api/events/{id}/` - Get specific event
- `PUT /api/events/{id}/` - Update event
- `DELETE /api/events/{id}/` - Delete event
- `POST /api/events/{id}/rsvp/` - RSVP to event
- `GET /api/events/user/my-events/` - Get user's events

### Health Check
- `GET /api/health/` - Health check endpoint

## API Usage Examples

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

### Login User
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Create Event
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date": "2024-06-15",
    "time": "09:00",
    "location": "Convention Center"
  }'
```

### RSVP to Event
```bash
curl -X POST http://localhost:8000/api/events/EVENT_ID/rsvp/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com"
  }'
```

## Database Schema

### User Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "name": "string",
  "password_hash": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Event Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "description": "string",
  "date": "string (YYYY-MM-DD)",
  "time": "string (HH:MM)",
  "location": "string",
  "created_by": "ObjectId (User reference)",
  "rsvps": [
    {
      "name": "string",
      "email": "string",
      "created_at": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation and sanitization
- Permission-based access control

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
Follow PEP 8 guidelines for Python code style.

## Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Use environment variables for sensitive data
4. Set up proper logging
5. Use a production WSGI server like Gunicorn

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**: Check your connection string and network access
2. **JWT Token Issues**: Verify JWT_SECRET_KEY is set correctly
3. **CORS Errors**: Ensure frontend URL is in CORS_ALLOWED_ORIGINS

### Logs

Check Django logs for detailed error information:
```bash
python manage.py runserver --verbosity=2
```
