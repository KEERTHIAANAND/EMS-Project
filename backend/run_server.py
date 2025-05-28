#!/usr/bin/env python
"""
Simple Django server runner
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_backend.settings')
    
    # Setup Django
    django.setup()
    
    print("🚀 Starting EMS Backend Server...")
    print("✅ MongoDB Atlas configured")
    print("✅ CORS enabled for React frontend")
    print("🌐 Server will be available at: http://localhost:8000/")
    print("📡 API endpoints at: http://localhost:8000/api/")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    execute_from_command_line(['manage.py', 'runserver', '8000'])
