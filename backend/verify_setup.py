#!/usr/bin/env python
"""
Verify Django backend setup
"""
import os
import sys

def main():
    print("🔍 Verifying EMS Backend Setup...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found!")
        print("   Please run this script from the backend directory")
        return False
    
    print("✅ Found manage.py")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ Found .env configuration file")
        
        # Check MongoDB URI
        with open('.env', 'r') as f:
            content = f.read()
            if 'mongodb+srv://keerthiaanand77' in content:
                print("✅ MongoDB Atlas connection string configured")
            else:
                print("⚠️  MongoDB Atlas connection string not found in .env")
    else:
        print("⚠️  .env file not found")
    
    # Check if required directories exist
    required_dirs = ['ems_backend', 'authentication', 'events']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Found {dir_name}/ directory")
        else:
            print(f"❌ Missing {dir_name}/ directory")
    
    # Check Python packages
    try:
        import django
        print(f"✅ Django {django.get_version()} installed")
    except ImportError:
        print("❌ Django not installed")
        return False
    
    try:
        import mongoengine
        print("✅ MongoEngine installed")
    except ImportError:
        print("❌ MongoEngine not installed")
        return False
    
    try:
        import rest_framework
        print("✅ Django REST Framework installed")
    except ImportError:
        print("❌ Django REST Framework not installed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Backend setup verification complete!")
    print("\n📋 Next Steps:")
    print("1. Start the Django server:")
    print("   python manage.py runserver 8000")
    print("   OR")
    print("   py manage.py runserver 8000")
    print("\n2. Test the health endpoint:")
    print("   http://localhost:8000/api/health/")
    print("\n3. Test your React frontend registration/login")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
