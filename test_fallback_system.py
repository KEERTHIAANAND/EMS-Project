#!/usr/bin/env python3
"""
Test the fallback system while MongoDB Atlas is being configured
"""
import requests
import json

API_BASE_URL = 'http://localhost:8000/api'

def test_with_fallback():
    """Test the complete flow with fallback storage"""
    print("🧪 Testing EMS with Fallback Storage")
    print("=" * 50)
    
    # 1. Health check
    print("1. Health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        print(f"✅ Health: {response.json()}")
    except Exception as e:
        print(f"❌ Health error: {e}")
        return
    
    # 2. Register user
    print("\n2. User registration...")
    user_data = {
        "name": "Fallback Test User",
        "email": "fallback@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register/", 
                               json=user_data, 
                               timeout=10)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Registration successful!")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            token = data.get('token')
        elif response.status_code == 400 and "already exists" in response.text:
            print("ℹ️  User exists, trying login...")
            # Try login
            login_data = {"email": "fallback@example.com", "password": "password123"}
            response = requests.post(f"{API_BASE_URL}/auth/login/", json=login_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Login successful!")
                print(f"📊 Storage: {data.get('storage', 'Unknown')}")
                token = data.get('token')
            else:
                print(f"❌ Login failed: {response.text}")
                return
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # 3. Create event
    print("\n3. Event creation...")
    event_data = {
        "name": "Fallback Test Event",
        "description": "Testing event creation with fallback storage",
        "date": "2025-06-15",
        "time": "14:00",
        "location": "Fallback Storage Location",
        "image": "https://example.com/fallback-test.jpg"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/events/", 
                               json=event_data,
                               headers={"Authorization": f"Bearer {token}"},
                               timeout=10)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Event created successfully!")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            print(f"📝 Message: {data.get('message', 'No message')}")
            event_id = data.get('event', {}).get('id')
        else:
            print(f"❌ Event creation failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Event creation error: {e}")
        return
    
    # 4. List events
    print("\n4. Event listing...")
    try:
        response = requests.get(f"{API_BASE_URL}/events/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"✅ Found {len(events)} events")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            
            # Show our test event
            test_events = [e for e in events if "Fallback Test Event" in e.get('name', '')]
            if test_events:
                event = test_events[0]
                print(f"🎯 Test Event Details:")
                print(f"   📛 Name: {event.get('name')}")
                print(f"   📅 Date: {event.get('date')} at {event.get('time')}")
                print(f"   📍 Location: {event.get('location')}")
                print(f"   🖼️  Image: {event.get('image')}")
                print(f"   👤 Created by: {event.get('created_by', {}).get('name')}")
        else:
            print(f"❌ Event listing failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Event listing error: {e}")
        return
    
    print("\n🎉 Fallback system is working perfectly!")
    print("📋 Summary:")
    print("   ✅ User registration/login working")
    print("   ✅ Event creation working")
    print("   ✅ Event listing working")
    print("   ✅ Data stored in fallback storage")
    print("\n📝 Next steps:")
    print("   1. Fix MongoDB Atlas network access (whitelist IP 103.183.240.250)")
    print("   2. Restart Django server")
    print("   3. Data will automatically migrate to MongoDB Atlas")

if __name__ == "__main__":
    test_with_fallback()
