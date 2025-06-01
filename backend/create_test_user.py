#!/usr/bin/env python3
"""
Create a test user for testing the admin panel
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_backend.settings')
django.setup()

from authentication.models import User

def create_test_user():
    """Create a test user"""
    try:
        # Check if user already exists
        try:
            existing_user = User.objects.get(email="testadmin@example.com")
            print(f"User already exists: {existing_user.email}")
            existing_user.is_admin = True
            existing_user.save()
            print("Made user an admin")
            return existing_user
        except User.DoesNotExist:
            pass
        
        # Create new user
        user = User(
            name="Test Admin",
            email="testadmin@example.com",
            is_admin=True,
            is_active=True
        )
        user.set_password("testpass123")
        user.save()
        
        print(f"✅ Created test admin user: {user.email}")
        print(f"   Password: testpass123")
        print(f"   Admin: {user.is_admin}")
        
        return user
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None

if __name__ == "__main__":
    print("Creating test user...")
    user = create_test_user()
    
    if user:
        print("\n✅ Test user ready!")
        print("You can now login with:")
        print("Email: testadmin@example.com")
        print("Password: testpass123")
    else:
        print("\n❌ Failed to create test user")
