#!/usr/bin/env python3
"""
Test the authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_registration():
    """Test user registration"""
    print("\n🔍 Testing registration endpoint...")
    
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 201:
            print("   ✅ Registration successful!")
            return True, response.json()
        else:
            print("   ⚠️  Registration failed")
            return False, None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_login():
    """Test user login"""
    print("\n🔍 Testing login endpoint...")
    
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
            return True, response.json()
        else:
            print("   ⚠️  Login failed")
            return False, None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def cleanup_test_user():
    """Clean up test user from database"""
    print("\n🧹 Cleaning up test user...")
    try:
        import os
        import sys
        import django
        from pathlib import Path

        # Setup Django
        backend_dir = Path(__file__).resolve().parent
        sys.path.append(str(backend_dir))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_backend.settings')
        django.setup()

        from authentication.models import User
        
        # Delete test user if exists
        test_user = User.objects(email="test@example.com").first()
        if test_user:
            test_user.delete()
            print("   ✅ Test user deleted")
        else:
            print("   ℹ️  No test user found")
            
    except Exception as e:
        print(f"   ⚠️  Cleanup error: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing EMS Backend Endpoints")
    print("=" * 40)
    
    # Clean up any existing test user first
    cleanup_test_user()
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n❌ Health check failed. Make sure the server is running.")
        return
    
    # Test registration
    reg_success, reg_data = test_registration()
    
    if reg_success:
        # Test login
        login_success, login_data = test_login()
        
        if login_success:
            print("\n🎉 All tests passed! Backend is working correctly.")
        else:
            print("\n⚠️  Registration works but login failed.")
    else:
        print("\n⚠️  Registration failed. Check the error messages above.")
    
    # Clean up
    cleanup_test_user()
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()
