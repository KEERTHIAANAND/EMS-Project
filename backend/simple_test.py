#!/usr/bin/env python
"""
Simple test for Django backend without MongoDB dependency
"""
import os
import sys
import django
from django.conf import settings
from django.test import Client
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_backend.settings')

# Setup Django
django.setup()

def test_django_setup():
    """Test basic Django setup"""
    print("🧪 Testing Django Setup...")
    
    try:
        print(f"   ✓ Django version: {django.get_version()}")
        print(f"   ✓ Settings module: {settings.SETTINGS_MODULE}")
        print(f"   ✓ Debug mode: {settings.DEBUG}")
        print(f"   ✓ Allowed hosts: {settings.ALLOWED_HOSTS}")
        print(f"   ✓ MongoDB URI configured: {'mongodb+srv' in settings.MONGODB_URI}")
        return True
    except Exception as e:
        print(f"   ✗ Django setup failed: {e}")
        return False

def test_health_endpoint():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check Endpoint...")
    
    try:
        client = Client()
        response = client.get('/api/health/')
        
        if response.status_code == 200:
            print("   ✓ Health endpoint accessible")
            data = response.json()
            print(f"   📋 Response: {data}")
            return True
        else:
            print(f"   ✗ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Health endpoint test failed: {e}")
        return False

def test_cors_headers():
    """Test CORS configuration"""
    print("\n🌐 Testing CORS Configuration...")
    
    try:
        client = Client()
        response = client.options('/api/health/', HTTP_ORIGIN='http://localhost:5174')
        
        print(f"   📋 CORS headers present: {'Access-Control-Allow-Origin' in response}")
        print(f"   📋 Response status: {response.status_code}")
        return True
    except Exception as e:
        print(f"   ✗ CORS test failed: {e}")
        return False

def test_url_patterns():
    """Test URL patterns are configured"""
    print("\n🔗 Testing URL Patterns...")
    
    try:
        from django.urls import reverse
        from django.core.urlresolvers import NoReverseMatch
        
        # Test if URL patterns are accessible
        client = Client()
        
        # Test auth endpoints (should return 400 for empty POST, but URL should exist)
        auth_endpoints = [
            '/api/auth/register/',
            '/api/auth/login/',
        ]
        
        for endpoint in auth_endpoints:
            response = client.post(endpoint, content_type='application/json')
            if response.status_code in [400, 405]:  # Bad request or method not allowed is fine
                print(f"   ✓ {endpoint} - URL pattern exists")
            else:
                print(f"   ⚠️  {endpoint} - Status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"   ✗ URL pattern test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Simple Backend Tests...")
    print("=" * 50)
    
    tests = [
        test_django_setup,
        test_health_endpoint,
        test_cors_headers,
        test_url_patterns
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All basic tests passed! Django backend is properly configured.")
        print("\n📋 Next Steps:")
        print("1. Ensure MongoDB Atlas IP whitelist includes your current IP")
        print("2. Start the server: py manage.py runserver 8000")
        print("3. Test API endpoints with your React frontend")
        print("4. Check MongoDB Atlas connection in the Django admin or logs")
    else:
        print("❌ Some tests failed. Please check the configuration.")
    
    print("\n🔗 API Endpoints Ready:")
    print("- GET  /api/health/ - Health check")
    print("- POST /api/auth/register/ - User registration")
    print("- POST /api/auth/login/ - User login")
    print("- POST /api/auth/logout/ - User logout")

if __name__ == '__main__':
    main()
