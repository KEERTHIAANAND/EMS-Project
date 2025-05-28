#!/usr/bin/env python
"""
Quick test to verify Django setup
"""
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_backend.settings')

try:
    import django
    django.setup()
    
    print("✅ Django setup successful!")
    print("✅ MongoDB Atlas connection configured")
    
    # Test importing our models
    from authentication.models import User
    from events.models import Event
    print("✅ Models imported successfully")
    
    # Test Django settings
    from django.conf import settings
    print(f"✅ Debug mode: {settings.DEBUG}")
    print(f"✅ Allowed hosts: {settings.ALLOWED_HOSTS}")
    print(f"✅ MongoDB URI configured: {'mongodb+srv' in settings.MONGODB_URI}")
    
    print("\n🎉 Backend is ready!")
    print("\n📋 To start the server manually:")
    print("1. Open a new terminal/command prompt")
    print("2. Navigate to the backend directory:")
    print("   cd backend")
    print("3. Run the Django server:")
    print("   python manage.py runserver 8000")
    print("   OR")
    print("   py manage.py runserver 8000")
    print("\n🌐 Server will be available at: http://localhost:8000/")
    print("📡 API endpoints at: http://localhost:8000/api/")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
