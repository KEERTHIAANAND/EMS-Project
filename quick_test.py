#!/usr/bin/env python3
"""
Quick test to check specific endpoints
"""
import requests
import json

API_BASE_URL = 'http://localhost:8000/api'

def test_health():
    """Test backend health"""
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        print(f"Health: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health error: {e}")
        return False

def test_events_list():
    """Test events listing"""
    try:
        response = requests.get(f"{API_BASE_URL}/events/", timeout=15)
        print(f"Events list: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Events found: {len(data.get('events', []))}")
            print(f"Storage: {data.get('storage', 'Unknown')}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Events list error: {e}")
        return False

def test_simple_registration():
    """Test simple registration"""
    user_data = {
        "name": "Quick Test User",
        "email": "quicktest@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    
    try:
        print("Attempting registration...")
        response = requests.post(f"{API_BASE_URL}/auth/register/", 
                               json=user_data, 
                               timeout=15)
        print(f"Registration: {response.status_code}")
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"Success! Storage: {data.get('storage', 'Unknown')}")
            return data.get('token')
        elif response.status_code == 400:
            print(f"Registration response: {response.text}")
            # Try login instead
            return test_simple_login()
        else:
            print(f"Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"Registration error: {e}")
        return None

def test_simple_login():
    """Test simple login"""
    login_data = {
        "email": "quicktest@example.com",
        "password": "password123"
    }
    
    try:
        print("Attempting login...")
        response = requests.post(f"{API_BASE_URL}/auth/login/", 
                               json=login_data, 
                               timeout=15)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Storage: {data.get('storage', 'Unknown')}")
            return data.get('token')
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def main():
    print("🧪 Quick MongoDB Atlas Test")
    print("=" * 40)
    
    print("1. Health check...")
    if not test_health():
        print("❌ Backend not healthy")
        return
    
    print("\n2. Events list...")
    test_events_list()
    
    print("\n3. User registration/login...")
    token = test_simple_registration()
    
    if token:
        print(f"✅ Got token: {token[:20]}...")
        
        print("\n4. Testing event creation...")
        event_data = {
            "name": "Quick Test Event",
            "description": "Quick test",
            "date": "2025-06-15",
            "time": "14:00",
            "location": "Test Location"
        }
        
        try:
            response = requests.post(f"{API_BASE_URL}/events/", 
                                   json=event_data,
                                   headers={"Authorization": f"Bearer {token}"},
                                   timeout=15)
            print(f"Event creation: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Event created! Storage: {data.get('storage', 'Unknown')}")
            else:
                print(f"❌ Event creation failed: {response.text}")
        except Exception as e:
            print(f"Event creation error: {e}")
    else:
        print("❌ Could not get authentication token")

if __name__ == "__main__":
    main()
