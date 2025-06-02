#!/usr/bin/env python3
"""
Test script to force MongoDB Atlas connection and verify data storage
"""
import requests
import json
import time

API_BASE_URL = 'http://localhost:8000/api'

def test_mongodb_direct():
    """Test direct MongoDB Atlas storage"""
    print("🗄️  Testing Direct MongoDB Atlas Storage")
    print("=" * 60)
    print("🌐 Your current IP: 106.195.42.148")
    print("📝 Make sure this IP is whitelisted in MongoDB Atlas Network Access")
    print("🔗 MongoDB Atlas: https://cloud.mongodb.com/")
    print("=" * 60)
    
    # 1. Health check
    print("1. 🏥 Health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print("❌ Backend health check failed")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # 2. User registration with MongoDB focus
    print("\n2. 👤 User registration (targeting MongoDB Atlas)...")
    user_data = {
        "name": "MongoDB Direct User",
        "email": "mongodb.direct@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register/", 
                               json=user_data, 
                               timeout=30)  # Longer timeout for MongoDB
        
        if response.status_code == 201:
            data = response.json()
            print("✅ User registration successful!")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            print(f"🗄️  MongoDB Saved: {data.get('mongodb_saved', 'Unknown')}")
            
            if data.get('storage') == 'MongoDB Atlas':
                print("🎉 SUCCESS: Data saved to MongoDB Atlas!")
            else:
                print("⚠️  Data saved to fallback storage - MongoDB Atlas not accessible")
                print("📝 Please whitelist IP 106.195.42.148 in MongoDB Atlas Network Access")
            
            token = data.get('token')
        elif response.status_code == 400 and "already exists" in response.text:
            print("ℹ️  User exists, trying login...")
            # Try login
            login_data = {"email": "mongodb.direct@example.com", "password": "password123"}
            response = requests.post(f"{API_BASE_URL}/auth/login/", json=login_data, timeout=30)
            if response.status_code == 200:
                data = response.json()
                print("✅ Login successful!")
                print(f"📊 Storage: {data.get('storage', 'Unknown')}")
                print(f"🗄️  MongoDB Verified: {data.get('mongodb_verified', 'Unknown')}")
                token = data.get('token')
            else:
                print(f"❌ Login failed: {response.text}")
                return
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration/Login error: {e}")
        return
    
    if not token:
        print("❌ No authentication token received")
        return
    
    # 3. Event creation with MongoDB focus
    print("\n3. 📅 Event creation (targeting MongoDB Atlas)...")
    event_data = {
        "name": "MongoDB Atlas Direct Storage Event",
        "description": "This event should be stored directly in MongoDB Atlas ems_db database, not in fallback storage",
        "date": "2025-07-01",
        "time": "18:00",
        "location": "MongoDB Atlas ems_db.events Collection",
        "image": "https://example.com/mongodb-direct-storage.jpg"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/events/", 
                               json=event_data,
                               headers={"Authorization": f"Bearer {token}"},
                               timeout=30)  # Longer timeout for MongoDB
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Event created successfully!")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            print(f"🗄️  MongoDB Saved: {data.get('mongodb_saved', 'Unknown')}")
            print(f"📝 Message: {data.get('message', 'No message')}")
            
            if data.get('storage') == 'MongoDB Atlas':
                print("🎉 SUCCESS: Event saved to MongoDB Atlas ems_db.events!")
                print("✅ Data is now in your MongoDB Atlas database")
            else:
                print("⚠️  Event saved to fallback storage - MongoDB Atlas not accessible")
                print("📝 Please whitelist IP 106.195.42.148 in MongoDB Atlas Network Access")
            
            if data.get('event'):
                event = data['event']
                print(f"🎯 Event Details:")
                print(f"   🆔 Event ID: {event.get('id')}")
                print(f"   📛 Name: {event.get('name')}")
                print(f"   📅 Date: {event.get('date')} at {event.get('time')}")
                print(f"   📍 Location: {event.get('location')}")
                print(f"   🖼️  Image: {event.get('image')}")
        else:
            print(f"❌ Event creation failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error text: {response.text}")
            return
    except Exception as e:
        print(f"❌ Event creation error: {e}")
        return
    
    # 4. Event listing
    print("\n4. 📋 Event listing...")
    try:
        response = requests.get(f"{API_BASE_URL}/events/", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"✅ Found {len(events)} total events")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            
            if data.get('storage') == 'MongoDB Atlas':
                print("🎉 Events loaded from MongoDB Atlas ems_db.events!")
            else:
                print("⚠️  Events loaded from fallback storage")
            
            # Look for our test event
            test_events = [e for e in events if "MongoDB Atlas Direct Storage Event" in e.get('name', '')]
            if test_events:
                print(f"🎯 Found {len(test_events)} MongoDB direct storage test events")
                for event in test_events:
                    print(f"   ✅ {event.get('name')} (ID: {event.get('id')})")
            else:
                print("⚠️  MongoDB direct storage test event not found")
        else:
            print(f"❌ Event listing failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Event listing error: {e}")
        return
    
    # 5. Instructions
    print("\n" + "="*60)
    print("📋 INSTRUCTIONS TO SAVE DATA IN MONGODB ATLAS")
    print("="*60)
    print("🌐 Your current IP address: 106.195.42.148")
    print("\n📝 Steps to enable MongoDB Atlas storage:")
    print("   1. Go to https://cloud.mongodb.com/")
    print("   2. Navigate to 'Network Access' in left sidebar")
    print("   3. Click 'Add IP Address'")
    print("   4. Add IP: 106.195.42.148")
    print("   5. Save the changes")
    print("   6. Restart Django server: py manage.py runserver 8000")
    print("   7. Test again - data will go to MongoDB Atlas!")
    
    print("\n🗄️  Target Database Structure:")
    print("   📊 Database: ems_db")
    print("   📁 Collection: users (for sign-in/sign-up data)")
    print("   📁 Collection: events (for create event data)")
    
    print("\n⚡ Quick Test After IP Whitelisting:")
    print("   py force_mongodb_test.py")

if __name__ == "__main__":
    test_mongodb_direct()
