#!/usr/bin/env python3
"""
Setup script for EMS Backend
"""

import os
import sys
import subprocess
import secrets
import string

def generate_secret_key(length=50):
    """Generate a random secret key"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        return
    
    if not os.path.exists('.env.example'):
        print("✗ .env.example file not found")
        return
    
    # Read template
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Generate secret keys
    secret_key = generate_secret_key()
    jwt_secret = generate_secret_key()
    
    # Replace placeholders
    content = content.replace('your-secret-key-here', secret_key)
    content = content.replace('your-jwt-secret-key-here', jwt_secret)
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✓ Created .env file with generated secret keys")
    print("⚠️  Please update MongoDB URI in .env file")

def install_dependencies():
    """Install Python dependencies"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False
    return True

def run_migrations():
    """Run Django migrations"""
    try:
        subprocess.check_call([sys.executable, 'manage.py', 'migrate'])
        print("✓ Migrations completed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to run migrations")
        return False
    return True

def collect_static():
    """Collect static files"""
    try:
        subprocess.check_call([sys.executable, 'manage.py', 'collectstatic', '--noinput'])
        print("✓ Static files collected successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to collect static files")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up EMS Backend...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("✗ Please run this script from the backend directory")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("⚠️  Migrations failed, but continuing...")
    
    # Collect static files
    if not collect_static():
        print("⚠️  Static file collection failed, but continuing...")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Update MongoDB URI in .env file")
    print("2. Run: python manage.py runserver")
    print("3. API will be available at http://localhost:8000/")
    print("\nFor more information, see README.md")

if __name__ == '__main__':
    main()
