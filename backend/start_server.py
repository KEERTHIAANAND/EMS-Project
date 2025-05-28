#!/usr/bin/env python
"""
Start Django development server
"""
import os
import sys
import subprocess

def main():
    """Start the Django development server"""
    print("🚀 Starting EMS Backend Server...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found!")
        print("   Please run this script from the backend directory")
        return False
    
    # Check if dependencies are installed
    try:
        import django
        import mongoengine
        import rest_framework
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: py -m pip install -r requirements.txt")
        return False
    
    # Check environment configuration
    if os.path.exists('.env'):
        print("✅ Environment configuration found")
    else:
        print("⚠️  No .env file found, using defaults")
    
    print("\n🌐 Starting Django development server...")
    print("   Server will be available at: http://localhost:8000/")
    print("   API endpoints at: http://localhost:8000/api/")
    print("   Press Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    
    try:
        # Start the Django development server
        os.system('py manage.py runserver 8000')
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
