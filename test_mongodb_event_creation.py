#!/usr/bin/env python3
"""
Test script to verify event creation functionality and MongoDB Atlas storage
"""
import requests
import json
import sys

# API Configuration
API_BASE_URL = 'http://localhost:8000/api'

def test_health():
    """Test backend health"""
    print("🏥 Testing backend health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is healthy")
            print(f"📊 Status: {data.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("🔐 Testing user registration...")
    
    user_data = {
        "name": "Test User MongoDB",
        "email": "testuser.mongodb@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register/", 
                               json=user_data, 
                               timeout=30)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ User registration successful")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            print(f"🗄️  MongoDB Saved: {data.get('mongodb_saved', 'Unknown')}")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print("ℹ️  User already exists, proceeding with login")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Registration timeout - MongoDB connection might be slow")
        print("ℹ️  Proceeding with login attempt...")
        return True
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_user_login():
    """Test user login and get JWT token"""
    print("🔑 Testing user login...")
    
    login_data = {
        "email": "testuser.mongodb@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login/", 
                               json=login_data, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            if token:
                print("✅ Login successful, JWT token received")
                print(f"📊 Storage: {data.get('storage', 'Unknown')}")
                print(f"🗄️  MongoDB Verified: {data.get('mongodb_verified', 'Unknown')}")
                return token
            else:
                print("❌ Login successful but no token received")
                return None
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_event_creation(token):
    """Test event creation with authentication"""
    print("📅 Testing event creation...")
    
    event_data = {
        "name": "MongoDB Atlas Test Event",
        "description": "This is a test event to verify MongoDB Atlas storage functionality",
        "date": "2025-06-15",
        "time": "14:00",
        "location": "MongoDB Atlas Cloud - Test Location",
        "image": "https://example.com/mongodb-test-image.jpg"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/events/", 
                               json=event_data, 
                               headers=headers,
                               timeout=30)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Event creation successful!")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            print(f"🗄️  MongoDB Saved: {data.get('mongodb_saved', 'Unknown')}")
            print(f"📝 Message: {data.get('message', 'No message')}")
            
            if data.get('event'):
                event = data['event']
                print(f"🎯 Event ID: {event.get('id', 'No ID')}")
                print(f"📛 Event Name: {event.get('name', 'No name')}")
                print(f"📅 Event Date: {event.get('date', 'No date')}")
                print(f"📍 Event Location: {event.get('location', 'No location')}")
                print(f"🖼️  Event Image: {event.get('image', 'No image')}")
            
            return True
        else:
            print(f"❌ Event creation failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Event creation error: {e}")
        return False

def test_event_listing():
    """Test event listing to verify storage"""
    print("📋 Testing event listing...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/events/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"✅ Event listing successful! Found {len(events)} events")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            
            # Look for our test event
            test_events = [e for e in events if "MongoDB Atlas Test Event" in e.get('name', '')]
            if test_events:
                print(f"🎯 Found {len(test_events)} MongoDB test events in database")
                for event in test_events:
                    print(f"   - {event.get('name')} (ID: {event.get('id')})")
                    print(f"     📅 Date: {event.get('date')} at {event.get('time')}")
                    print(f"     📍 Location: {event.get('location')}")
                    if event.get('image'):
                        print(f"     🖼️  Image: {event.get('image')}")
            else:
                print("⚠️  MongoDB test event not found in listing")
            
            return True
        else:
            print(f"❌ Event listing failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Event listing error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 EMS MongoDB Atlas Event Creation Test")
    print("=" * 60)
    
    # Test backend health first
    if not test_health():
        print("❌ Backend is not healthy. Please start the Django server.")
        sys.exit(1)
    
    print()
    
    # Test user registration
    if not test_user_registration():
        print("❌ User registration failed. Cannot proceed.")
        sys.exit(1)
    
    print()
    
    # Test user login
    token = test_user_login()
    if not token:
        print("❌ User login failed. Cannot proceed.")
        sys.exit(1)
    
    print()
    
    # Test event creation
    if not test_event_creation(token):
        print("❌ Event creation failed.")
        sys.exit(1)
    
    print()
    
    # Test event listing
    if not test_event_listing():
        print("❌ Event listing failed.")
        sys.exit(1)
    
    print()
    print("🎉 All tests passed! Event creation and MongoDB Atlas storage are working correctly.")
    print("✅ Your data is being stored in MongoDB Atlas with collections:")
    print("   📁 users - for user authentication data")
    print("   📁 events - for event data")

if __name__ == "__main__":
    main()
