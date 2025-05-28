# 🚀 EMS Backend Startup Guide

## ✅ **Integration Complete!**

Your React frontend has been updated to connect to the Django backend. The 404 error you're seeing is because the Django server isn't running yet.

## 📋 **Step-by-Step Instructions to Start Backend**

### **Step 1: Open a New Terminal/Command Prompt**
1. Open a new terminal window (separate from your React frontend)
2. Navigate to your project directory:
   ```bash
   cd "D:\Python Project 2025\EMS-Project\ems"
   ```

### **Step 2: Navigate to Backend Directory**
```bash
cd backend
```

### **Step 3: Start Django Server**
Try one of these commands (use the one that works on your system):

**Option A:**
```bash
python manage.py runserver 8000
```

**Option B:**
```bash
py manage.py runserver 8000
```

**Option C:**
```bash
python3 manage.py runserver 8000
```

### **Step 4: Verify Server is Running**
You should see output like:
```
✓ Successfully connected to MongoDB Atlas
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 28, 2025 - 18:30:00
Django version 4.2.7, using settings 'ems_backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## 🌐 **Test the Backend**

### **1. Health Check**
Open your browser and go to:
```
http://localhost:8000/api/health/
```

You should see:
```json
{
  "status": "healthy",
  "message": "EMS Backend is running"
}
```

### **2. Test with Your React Frontend**
1. Make sure your React frontend is running (`npm run dev`)
2. Go to the sign-up page
3. Try registering a new user
4. The data should be stored in MongoDB Atlas

## 🔧 **API Endpoints Available**

- `GET /api/health/` - Health check
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

## 🎯 **What's Been Updated in Your Frontend**

### **SignUpPage.jsx**
- ✅ Now sends registration data to Django backend
- ✅ Stores JWT token from server response
- ✅ Shows proper error messages

### **SignInPage.jsx**
- ✅ Now validates credentials against MongoDB Atlas
- ✅ Stores JWT token for authenticated sessions
- ✅ Shows proper error messages

### **Navbar.jsx**
- ✅ Logout now calls Django backend
- ✅ Properly clears authentication tokens

## 🔍 **Troubleshooting**

### **If Django Server Won't Start:**

1. **Check if you're in the right directory:**
   ```bash
   pwd  # Should show: .../ems/backend
   ls   # Should show: manage.py, ems_backend/, etc.
   ```

2. **Check Python installation:**
   ```bash
   python --version
   # OR
   py --version
   ```

3. **Install dependencies if needed:**
   ```bash
   pip install -r requirements.txt
   # OR
   py -m pip install -r requirements.txt
   ```

### **If You Get MongoDB Connection Errors:**
- Check if your IP is whitelisted in MongoDB Atlas
- Verify the connection string in `.env` file
- Check your internet connection

### **If You Get CORS Errors:**
- Make sure Django server is running on port 8000
- Check that React frontend is running on port 5173 or 5174

## 📊 **Database Verification**

After registering users, you can check MongoDB Atlas:
1. Go to https://cloud.mongodb.com/
2. Navigate to your cluster
3. Click "Browse Collections"
4. Look for `ems_database` → `users` collection
5. You should see your registered users there

## 🎉 **Success Indicators**

You'll know everything is working when:
1. ✅ Django server starts without errors
2. ✅ Health check endpoint returns JSON response
3. ✅ User registration works from React frontend
4. ✅ User login works from React frontend
5. ✅ Data appears in MongoDB Atlas

## 📞 **Need Help?**

If you encounter issues:
1. Check the Django server console for error messages
2. Check the browser console for network errors
3. Verify both servers are running (React on 5173/5174, Django on 8000)
4. Check MongoDB Atlas connection and IP whitelist

Your EMS system is now fully integrated with MongoDB Atlas! 🎉
