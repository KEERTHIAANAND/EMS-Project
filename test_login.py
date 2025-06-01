#!/usr/bin/env python3
"""
Test login endpoint directly
"""
import requests
import json

def test_login():
    url = "http://localhost:8000/api/auth/login/"
    
    # Test with the credentials from the screenshot
    credentials = {
        "email": "abc@gmail.com",
        "password": "password123"  # Common password, might need to try others
    }
    
    try:
        print(f"Testing login with: {credentials['email']}")
        response = requests.post(url, json=credentials, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token: {data.get('token', 'No token')[:50]}...")
            return True
        else:
            print("❌ Login failed")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Backend server not reachable")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout Error - Backend server not responding")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    try:
        response = requests.get("http://localhost:8000/api/health/", timeout=5)
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Backend Connectivity...")
    print("=" * 50)
    
    if test_health():
        print("✅ Backend is reachable")
        test_login()
    else:
        print("❌ Backend is not reachable")
