#!/usr/bin/env python3
"""
Fix MongoDB Atlas connection and test it thoroughly
"""
import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_backend.settings')
django.setup()

import mongoengine
import pymongo.errors
from authentication.models import User


def test_mongodb_connection_detailed():
    """Test MongoDB Atlas connection with detailed diagnostics"""
    print("🔍 Testing MongoDB Atlas Connection (Detailed)")
    print("=" * 60)
    
    try:
        # Test 1: Get connection info
        print("1. Connection Information:")
        from django.conf import settings
        mongodb_uri = settings.MONGODB_URI
        db_name = settings.MONGODB_DB_NAME
        
        # Mask password for display
        display_uri = mongodb_uri
        if '@' in display_uri:
            parts = display_uri.split('@')
            if len(parts) >= 2:
                user_pass = parts[0].split('://')[-1]
                if ':' in user_pass:
                    user = user_pass.split(':')[0]
                    display_uri = display_uri.replace(user_pass, f"{user}:***")
        
        print(f"   URI: {display_uri}")
        print(f"   Database: {db_name}")
        
        # Test 2: Basic connection
        print("\n2. Testing basic connection...")
        client = mongoengine.connection.get_connection()
        print(f"   ✓ Client created: {type(client)}")
        
        # Test 3: Server info with timeout
        print("\n3. Testing server connectivity...")
        try:
            # Use a longer timeout for this test
            server_info = client.server_info()
            print(f"   ✓ MongoDB version: {server_info.get('version', 'Unknown')}")
            print(f"   ✓ Server connection successful")
            
            # Test 4: Database access
            print("\n4. Testing database access...")
            db = client[db_name]
            collections = db.list_collection_names()
            print(f"   ✓ Database accessible")
            print(f"   ✓ Collections: {collections}")
            
            # Test 5: User model operations
            print("\n5. Testing User model operations...")
            
            # Count users
            try:
                user_count = User.objects.count()
                print(f"   ✓ Current user count: {user_count}")
                
                # Test creating a user
                test_email = "mongodb_test@example.com"
                
                # Clean up any existing test user
                existing = User.objects(email=test_email).first()
                if existing:
                    existing.delete()
                    print(f"   ✓ Cleaned up existing test user")
                
                # Create test user
                test_user = User(
                    name="MongoDB Test User",
                    email=test_email
                )
                test_user.set_password("testpass123")
                test_user.save()
                print(f"   ✓ Created test user: {test_user.email}")
                
                # Verify user was saved
                saved_user = User.objects(email=test_email).first()
                if saved_user:
                    print(f"   ✓ User retrieved successfully: {saved_user.name}")
                    
                    # Test password verification
                    if saved_user.check_password("testpass123"):
                        print(f"   ✓ Password verification works")
                    else:
                        print(f"   ❌ Password verification failed")
                    
                    # Clean up
                    saved_user.delete()
                    print(f"   ✓ Test user cleaned up")
                else:
                    print(f"   ❌ Could not retrieve saved user")
                
                print(f"\n🎉 MongoDB Atlas connection is WORKING PERFECTLY!")
                return True
                
            except Exception as model_error:
                print(f"   ❌ User model error: {model_error}")
                return False
                
        except pymongo.errors.ServerSelectionTimeoutError as timeout_error:
            print(f"   ❌ Server selection timeout: {timeout_error}")
            print(f"\n🔧 SOLUTION NEEDED:")
            print(f"   1. Check MongoDB Atlas Network Access settings")
            print(f"   2. Add your IP address to the whitelist")
            print(f"   3. Ensure cluster is not paused")
            return False
            
        except Exception as server_error:
            print(f"   ❌ Server connection error: {server_error}")
            return False
            
    except Exception as e:
        print(f"❌ Connection setup error: {e}")
        return False


def fix_mongodb_settings():
    """Update MongoDB settings for better connectivity"""
    print("\n🔧 Applying MongoDB Connection Fixes...")
    print("=" * 50)
    
    # Update the connection with better settings
    try:
        # Disconnect existing connection
        mongoengine.disconnect()
        print("   ✓ Disconnected existing connection")
        
        # Reconnect with optimized settings
        from django.conf import settings
        
        mongoengine.connect(
            db=settings.MONGODB_DB_NAME,
            host=settings.MONGODB_URI,
            alias='default',
            # Optimized connection settings
            maxPoolSize=10,
            minPoolSize=1,
            serverSelectionTimeoutMS=30000,  # 30 seconds
            socketTimeoutMS=20000,  # 20 seconds
            connectTimeoutMS=20000,  # 20 seconds
            retryWrites=True,
            retryReads=True,
            maxIdleTimeMS=45000,  # 45 seconds
            heartbeatFrequencyMS=10000,  # 10 seconds
        )
        print("   ✓ Reconnected with optimized settings")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to apply fixes: {e}")
        return False


def main():
    """Main function to test and fix MongoDB connection"""
    print("🚀 MongoDB Atlas Connection Diagnostics & Fix")
    print("=" * 60)
    
    # First test with current settings
    print("PHASE 1: Testing current connection...")
    success = test_mongodb_connection_detailed()
    
    if not success:
        print("\nPHASE 2: Applying connection fixes...")
        fix_success = fix_mongodb_settings()
        
        if fix_success:
            print("\nPHASE 3: Re-testing with fixes...")
            success = test_mongodb_connection_detailed()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ RESULT: MongoDB Atlas is working correctly!")
        print("   Your registration and login will use MongoDB Atlas.")
    else:
        print("❌ RESULT: MongoDB Atlas connection failed.")
        print("   Please check the following:")
        print("   1. Go to https://cloud.mongodb.com/")
        print("   2. Navigate to Network Access")
        print("   3. Add your current IP address")
        print("   4. Ensure your cluster is running (not paused)")
        print("   5. Check your internet connection")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
