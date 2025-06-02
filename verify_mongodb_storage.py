#!/usr/bin/env python3
"""
Verification script to confirm data is being saved to MongoDB Atlas
Run this AFTER whitelisting your IP address in MongoDB Atlas
"""
import requests
import json
import time

API_BASE_URL = 'http://localhost:8000/api'

def verify_mongodb_atlas_storage():
    """Verify that data is being saved to MongoDB Atlas, not fallback storage"""
    print("🔍 VERIFYING MONGODB ATLAS STORAGE")
    print("=" * 60)
    print("📝 Run this AFTER whitelisting IP 106.195.42.148 in MongoDB Atlas")
    print("🔗 MongoDB Atlas: https://cloud.mongodb.com/ > Network Access")
    print("=" * 60)
    
    # 1. Health check
    print("1. 🏥 Health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print("❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # 2. Test user registration
    print("\n2. 👤 Testing user registration...")
    user_data = {
        "name": "MongoDB Verification User",
        "email": "verify.mongodb@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register/", 
                               json=user_data, 
                               timeout=15)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ User registration successful!")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            print(f"🗄️  MongoDB Saved: {data.get('mongodb_saved', 'Unknown')}")
            
            if data.get('storage') == 'MongoDB Atlas' and data.get('mongodb_saved') == True:
                print("🎉 SUCCESS: User data saved to MongoDB Atlas ems_db.users!")
                mongodb_working = True
            else:
                print("❌ FAILED: User data saved to fallback storage")
                print("📝 Please check MongoDB Atlas Network Access settings")
                mongodb_working = False
            
            token = data.get('token')
        elif response.status_code == 400 and "already exists" in response.text:
            print("ℹ️  User exists, trying login...")
            # Try login
            login_data = {"email": "verify.mongodb@example.com", "password": "password123"}
            response = requests.post(f"{API_BASE_URL}/auth/login/", json=login_data, timeout=15)
            if response.status_code == 200:
                data = response.json()
                print("✅ Login successful!")
                print(f"📊 Storage: {data.get('storage', 'Unknown')}")
                print(f"🗄️  MongoDB Verified: {data.get('mongodb_verified', 'Unknown')}")
                
                if data.get('storage') == 'MongoDB Atlas':
                    print("🎉 SUCCESS: User authenticated from MongoDB Atlas!")
                    mongodb_working = True
                else:
                    print("❌ FAILED: User authenticated from fallback storage")
                    mongodb_working = False
                
                token = data.get('token')
            else:
                print(f"❌ Login failed: {response.text}")
                return False
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration/Login error: {e}")
        return False
    
    if not token:
        print("❌ No authentication token received")
        return False
    
    # 3. Test event creation
    print("\n3. 📅 Testing event creation...")
    event_data = {
        "name": "MongoDB Atlas Verification Event",
        "description": "This event verifies that data is being saved directly to MongoDB Atlas ems_db.events collection, not fallback storage",
        "date": "2025-07-15",
        "time": "19:30",
        "location": "MongoDB Atlas ems_db Database",
        "image": "https://example.com/mongodb-verification.jpg"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/events/", 
                               json=event_data,
                               headers={"Authorization": f"Bearer {token}"},
                               timeout=15)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Event created successfully!")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            print(f"🗄️  MongoDB Saved: {data.get('mongodb_saved', 'Unknown')}")
            print(f"📝 Message: {data.get('message', 'No message')}")
            
            if data.get('storage') == 'MongoDB Atlas' and data.get('mongodb_saved') == True:
                print("🎉 SUCCESS: Event saved to MongoDB Atlas ems_db.events!")
                event_mongodb_working = True
            else:
                print("❌ FAILED: Event saved to fallback storage")
                print("📝 Please check MongoDB Atlas Network Access settings")
                event_mongodb_working = False
            
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
            return False
    except Exception as e:
        print(f"❌ Event creation error: {e}")
        return False
    
    # 4. Test event listing
    print("\n4. 📋 Testing event listing...")
    try:
        response = requests.get(f"{API_BASE_URL}/events/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"✅ Found {len(events)} total events")
            print(f"📊 Storage: {data.get('storage', 'Unknown')}")
            
            if data.get('storage') == 'MongoDB Atlas':
                print("🎉 SUCCESS: Events loaded from MongoDB Atlas ems_db.events!")
                listing_mongodb_working = True
            else:
                print("❌ FAILED: Events loaded from fallback storage")
                listing_mongodb_working = False
            
            # Look for our verification event
            test_events = [e for e in events if "MongoDB Atlas Verification Event" in e.get('name', '')]
            if test_events:
                print(f"🎯 Found {len(test_events)} verification events in database")
                for event in test_events:
                    print(f"   ✅ {event.get('name')} (ID: {event.get('id')})")
            else:
                print("⚠️  Verification event not found in listing")
        else:
            print(f"❌ Event listing failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Event listing error: {e}")
        return False
    
    # 5. Final verification results
    print("\n" + "="*60)
    if mongodb_working and event_mongodb_working and listing_mongodb_working:
        print("🎉 VERIFICATION SUCCESSFUL!")
        print("✅ ALL DATA IS BEING SAVED TO MONGODB ATLAS!")
        print("="*60)
        print("✅ Users saved to: ems_db.users collection")
        print("✅ Events saved to: ems_db.events collection")
        print("✅ No more fallback storage usage")
        print("✅ Your EMS system is using MongoDB Atlas directly!")
        
        print("\n🗄️  MongoDB Atlas Database Structure:")
        print("   📊 Database: ems_db")
        print("   📁 Collection: users")
        print("      └── User authentication data (name, email, password)")
        print("   📁 Collection: events")
        print("      └── Event data (name, description, date, time, location, image)")
        
        print("\n🚀 Your EMS system is now production-ready with MongoDB Atlas!")
        return True
    else:
        print("❌ VERIFICATION FAILED!")
        print("⚠️  DATA IS STILL GOING TO FALLBACK STORAGE")
        print("="*60)
        print("📝 Please check the following:")
        print("   1. IP 106.195.42.148 is whitelisted in MongoDB Atlas Network Access")
        print("   2. MongoDB Atlas cluster is running (not paused)")
        print("   3. Network connection is stable")
        print("   4. Restart Django server after whitelisting IP")
        
        print("\n🔗 MongoDB Atlas Network Access:")
        print("   https://cloud.mongodb.com/ > Network Access > Add IP Address")
        return False

if __name__ == "__main__":
    success = verify_mongodb_atlas_storage()
    if success:
        print("\n🎯 RESULT: MongoDB Atlas storage is working correctly!")
    else:
        print("\n🎯 RESULT: Please whitelist your IP and try again.")
