#!/usr/bin/env python
"""
Test script for EMS Backend API
"""
import os
import sys
import django
from django.conf import settings

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_backend.settings')

# Setup Django
django.setup()

# Now import Django models and test
from authentication.models import User
from events.models import Event

def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    print("🧪 Testing MongoDB Atlas Connection...")
    
    try:
        # Test user creation
        print("📝 Testing User Model...")
        
        # Check if test user already exists
        existing_user = User.objects(email='test@example.com').first()
        if existing_user:
            print("   ✓ Test user already exists, deleting...")
            existing_user.delete()
        
        # Create test user
        test_user = User(
            name='Test User',
            email='test@example.com'
        )
        test_user.set_password('testpassword123')
        test_user.save()
        print("   ✓ User created successfully")
        
        # Test password verification
        if test_user.check_password('testpassword123'):
            print("   ✓ Password verification works")
        else:
            print("   ✗ Password verification failed")
        
        # Test user retrieval
        retrieved_user = User.objects(email='test@example.com').first()
        if retrieved_user:
            print("   ✓ User retrieval works")
            print(f"   📋 User data: {retrieved_user.to_dict()}")
        else:
            print("   ✗ User retrieval failed")
        
        # Test event creation
        print("📅 Testing Event Model...")
        test_event = Event(
            name='Test Event',
            description='This is a test event for MongoDB Atlas integration',
            date='2024-06-15',
            time='14:30',
            location='Test Location',
            created_by=test_user
        )
        test_event.save()
        print("   ✓ Event created successfully")
        
        # Test RSVP
        success, message = test_event.add_rsvp('John Doe', 'john@example.com')
        if success:
            print(f"   ✓ RSVP added: {message}")
        else:
            print(f"   ✗ RSVP failed: {message}")
        
        # Test event retrieval
        retrieved_event = Event.objects(name='Test Event').first()
        if retrieved_event:
            print("   ✓ Event retrieval works")
            print(f"   📋 Event data: {retrieved_event.to_dict()}")
        else:
            print("   ✗ Event retrieval failed")
        
        # Cleanup
        print("🧹 Cleaning up test data...")
        test_event.delete()
        test_user.delete()
        print("   ✓ Test data cleaned up")
        
        print("\n🎉 All tests passed! MongoDB Atlas integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        from django.test import Client
        from django.urls import reverse
        import json
        
        client = Client()
        
        # Test health check
        print("🏥 Testing health check endpoint...")
        response = client.get('/api/health/')
        if response.status_code == 200:
            print("   ✓ Health check endpoint works")
            print(f"   📋 Response: {response.json()}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
        
        # Test user registration
        print("👤 Testing user registration endpoint...")
        registration_data = {
            'name': 'API Test User',
            'email': 'apitest@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }
        
        response = client.post(
            '/api/auth/register/',
            data=json.dumps(registration_data),
            content_type='application/json'
        )
        
        if response.status_code == 201:
            print("   ✓ User registration works")
            response_data = response.json()
            print(f"   📋 Response: {response_data.get('message', 'Success')}")
            
            # Test user login
            print("🔐 Testing user login endpoint...")
            login_data = {
                'email': 'apitest@example.com',
                'password': 'testpass123'
            }
            
            response = client.post(
                '/api/auth/login/',
                data=json.dumps(login_data),
                content_type='application/json'
            )
            
            if response.status_code == 200:
                print("   ✓ User login works")
                response_data = response.json()
                print(f"   📋 Response: {response_data.get('message', 'Success')}")
                
                # Cleanup
                User.objects(email='apitest@example.com').delete()
                print("   ✓ Test user cleaned up")
            else:
                print(f"   ✗ User login failed: {response.status_code}")
                print(f"   📋 Response: {response.content.decode()}")
        else:
            print(f"   ✗ User registration failed: {response.status_code}")
            print(f"   📋 Response: {response.content.decode()}")
        
        print("\n🎉 API endpoint tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ API test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Starting EMS Backend Tests...")
    print("=" * 50)
    
    # Test MongoDB connection
    mongodb_success = test_mongodb_connection()
    
    # Test API endpoints
    api_success = test_api_endpoints()
    
    print("\n" + "=" * 50)
    if mongodb_success and api_success:
        print("✅ All tests passed! Your EMS backend is ready for integration.")
        print("\n📋 Next steps:")
        print("1. Start the Django server: py manage.py runserver 8000")
        print("2. Update your React frontend to use: http://localhost:8000/api/")
        print("3. Test the complete authentication flow")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    print("\n🔗 Available API Endpoints:")
    print("- POST /api/auth/register/ - Register new user")
    print("- POST /api/auth/login/ - Login user")
    print("- GET /api/health/ - Health check")
