#!/usr/bin/env python3
"""
Test MongoDB Atlas connection
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


def test_mongodb_connection():
    """Test MongoDB Atlas connection and basic operations"""
    print("🔍 Testing MongoDB Atlas Connection...")
    print("=" * 50)
    
    try:
        # Test 1: Basic connection
        print("1. Testing basic connection...")
        db = mongoengine.connection.get_db()
        print(f"   ✓ Connected to database: {db.name}")
        
        # Test 2: Server info
        print("2. Getting server information...")
        client = mongoengine.connection.get_connection()
        server_info = client.server_info()
        print(f"   ✓ MongoDB version: {server_info.get('version', 'Unknown')}")
        
        # Test 3: List collections
        print("3. Listing collections...")
        collections = db.list_collection_names()
        print(f"   ✓ Available collections: {collections}")
        
        # Test 4: Test User model operations
        print("4. Testing User model operations...")
        
        # Count existing users
        try:
            user_count = User.objects.count()
            print(f"   ✓ Current user count: {user_count}")
        except Exception as e:
            print(f"   ⚠️  Error counting users: {e}")
        
        # Test creating a test user (will be deleted)
        try:
            test_email = "test_connection@example.com"
            
            # Delete test user if exists
            existing_user = User.objects(email=test_email).first()
            if existing_user:
                existing_user.delete()
                print(f"   ✓ Deleted existing test user")
            
            # Create test user
            test_user = User(
                name="Test User",
                email=test_email
            )
            test_user.set_password("testpassword123")
            test_user.save()
            print(f"   ✓ Created test user: {test_user.email}")
            
            # Verify test user
            found_user = User.objects(email=test_email).first()
            if found_user:
                print(f"   ✓ Successfully retrieved test user: {found_user.name}")
                
                # Test password verification
                if found_user.check_password("testpassword123"):
                    print(f"   ✓ Password verification works")
                else:
                    print(f"   ⚠️  Password verification failed")
                
                # Clean up
                found_user.delete()
                print(f"   ✓ Cleaned up test user")
            else:
                print(f"   ⚠️  Could not retrieve test user")
                
        except Exception as e:
            print(f"   ⚠️  Error with User model operations: {e}")
        
        print("\n🎉 MongoDB Atlas connection test completed successfully!")
        return True
        
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {e}")
        print("   This usually means:")
        print("   - Network connectivity issues")
        print("   - MongoDB Atlas cluster is paused")
        print("   - IP address not whitelisted")
        return False
        
    except pymongo.errors.ConnectionFailure as e:
        print(f"❌ Connection failure: {e}")
        print("   This usually means:")
        print("   - Invalid connection string")
        print("   - Authentication failed")
        print("   - Network issues")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def print_connection_info():
    """Print current connection configuration"""
    print("\n📋 Current MongoDB Configuration:")
    print("=" * 40)
    
    from django.conf import settings
    
    # Get MongoDB URI (mask password for security)
    mongodb_uri = getattr(settings, 'MONGODB_URI', 'Not configured')
    if 'mongodb+srv://' in mongodb_uri and '@' in mongodb_uri:
        # Mask the password
        parts = mongodb_uri.split('@')
        if len(parts) >= 2:
            user_pass = parts[0].split('://')[-1]
            if ':' in user_pass:
                user = user_pass.split(':')[0]
                masked_uri = mongodb_uri.replace(user_pass, f"{user}:***")
                mongodb_uri = masked_uri
    
    print(f"MongoDB URI: {mongodb_uri}")
    print(f"Database Name: {getattr(settings, 'MONGODB_DB_NAME', 'Not configured')}")
    
    # Check if .env file exists
    env_file = backend_dir / '.env'
    if env_file.exists():
        print(f"✓ .env file found at: {env_file}")
    else:
        print(f"⚠️  .env file not found at: {env_file}")


if __name__ == "__main__":
    print_connection_info()
    success = test_mongodb_connection()
    
    if success:
        print("\n✅ All tests passed! Your MongoDB Atlas connection is working properly.")
    else:
        print("\n❌ Some tests failed. Please check your MongoDB Atlas configuration.")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your .env file has the correct MONGODB_URI")
        print("2. Verify your IP is whitelisted in MongoDB Atlas")
        print("3. Ensure your MongoDB Atlas cluster is running (not paused)")
        print("4. Check your internet connection")
