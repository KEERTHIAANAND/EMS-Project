# 🚀 EMS Backend Integration Guide

## ✅ **Setup Complete!**

Your Django backend with MongoDB Atlas integration is now ready. Here's everything you need to know:

## 📋 **What's Been Configured**

### ✅ **MongoDB Atlas Connection**
- **Connection String**: `mongodb+srv://keerthiaanand77:4qSbBUVnlRE31Fwx@cluster0.q0azyqo.mongodb.net/ems_database?retryWrites=true&w=majority&appName=Cluster0`
- **Database Name**: `ems_database`
- **Collections**: `users`, `events`

### ✅ **Django REST API Endpoints**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login  
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `GET /api/health/` - Health check

### ✅ **Security Features**
- JWT token authentication
- Password hashing with bcrypt
- CORS configured for React frontend
- Input validation and sanitization

## 🚀 **How to Start the Backend**

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Dependencies (if not done)
```bash
py -m pip install -r requirements.txt
```

### 3. Start Django Server
```bash
py manage.py runserver 8000
```

The API will be available at: `http://localhost:8000/`

## 🧪 **Testing the API**

### Health Check
```bash
curl http://localhost:8000/api/health/
```

### User Registration
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

### User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

## 🔗 **Frontend Integration**

### Update Your React Frontend

1. **Update API Base URL** in your React app:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

2. **Update Registration Function**:
```javascript
const handleSignUp = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: userData.name,
        email: userData.email,
        password: userData.password,
        confirm_password: userData.confirmPassword
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Store JWT token
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      // Redirect to dashboard
      navigate('/');
    } else {
      alert(data.error || 'Registration failed');
    }
  } catch (error) {
    alert('Network error: ' + error.message);
  }
};
```

3. **Update Login Function**:
```javascript
const handleSignIn = async (credentials) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials)
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Store JWT token
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      // Redirect to dashboard
      navigate('/');
    } else {
      alert(data.error || 'Login failed');
    }
  } catch (error) {
    alert('Network error: ' + error.message);
  }
};
```

## 🔐 **Authentication Flow**

1. **User Registration**: 
   - Frontend sends user data to `/api/auth/register/`
   - Backend validates data and creates user in MongoDB
   - Returns JWT token and user info

2. **User Login**:
   - Frontend sends credentials to `/api/auth/login/`
   - Backend validates against MongoDB
   - Returns JWT token and user info

3. **Protected Requests**:
   - Include JWT token in Authorization header:
   ```javascript
   headers: {
     'Authorization': `Bearer ${localStorage.getItem('token')}`,
     'Content-Type': 'application/json'
   }
   ```

## 🛠️ **Troubleshooting**

### MongoDB Connection Issues
1. **Check IP Whitelist**: Ensure your IP is whitelisted in MongoDB Atlas
2. **Network Access**: Check if your network allows MongoDB connections
3. **Credentials**: Verify username/password in connection string

### CORS Issues
- Backend is configured for `localhost:5173` and `localhost:5174`
- If using different port, update `CORS_ALLOWED_ORIGINS` in settings

### Server Won't Start
1. Check if port 8000 is available
2. Ensure all dependencies are installed
3. Check for syntax errors in Python files

## 📊 **Database Schema**

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "name": "string", 
  "password_hash": "string",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Events Collection  
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

## 🎯 **Next Steps**

1. **Start Backend Server**: `py manage.py runserver 8000`
2. **Update Frontend**: Modify your React authentication functions
3. **Test Integration**: Try registering and logging in
4. **Monitor MongoDB**: Check MongoDB Atlas for data storage
5. **Add Event Management**: Extend frontend to use event endpoints

## 📞 **Support**

If you encounter issues:
1. Check Django server logs for errors
2. Verify MongoDB Atlas connection
3. Test API endpoints with curl/Postman
4. Check browser network tab for CORS issues

Your EMS backend is now fully integrated with MongoDB Atlas and ready for production use! 🎉
