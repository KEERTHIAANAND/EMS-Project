#!/usr/bin/env python3
"""
Test user registration and login
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_registration():
    """Test user registration"""
    url = f"{BASE_URL}/auth/register/"
    
    user_data = {
        "name": "Test Admin",
        "email": "testadmin@example.com",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    
    try:
        print(f"Registering user: {user_data['email']}")
        response = requests.post(url, json=user_data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            return data.get('token'), user_data['email'], user_data['password']
        else:
            print("❌ Registration failed")
            return None, None, None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None, None, None

def test_login(email, password):
    """Test user login"""
    url = f"{BASE_URL}/auth/login/"
    
    credentials = {
        "email": email,
        "password": password
    }
    
    try:
        print(f"Testing login with: {email}")
        response = requests.post(url, json=credentials, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            return data.get('token')
        else:
            print("❌ Login failed")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_admin_endpoint(token):
    """Test admin endpoint with token"""
    url = f"{BASE_URL}/events/admin/stats/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing admin endpoint...")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Admin endpoint accessible!")
            return True
        else:
            print("❌ Admin endpoint failed")
            return False
            
    except Exception as e:
        print(f"❌ Admin endpoint error: {e}")
        return False

if __name__ == "__main__":
    print("Testing EMS Registration and Login...")
    print("=" * 50)
    
    # Test registration
    token, email, password = test_registration()
    
    if token:
        print(f"\n✅ Got token from registration: {token[:50]}...")
        
        # Test admin endpoint
        test_admin_endpoint(token)
    else:
        # Try with existing user
        print("\nTrying with existing user...")
        token = test_login("abc@gmail.com", "password123")
        
        if token:
            test_admin_endpoint(token)
    
    print("\n" + "=" * 50)
    print("Test completed!")
