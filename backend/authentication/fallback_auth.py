"""
Fallback authentication system for when MongoDB is unavailable
This is a temporary solution to allow testing the frontend
"""
import json
import os
import bcrypt
from datetime import datetime
from pathlib import Path

# File to store users when MongoDB is unavailable
FALLBACK_USERS_FILE = Path(__file__).parent / 'fallback_users.json'

class FallbackUser:
    """Simple user class for fallback storage"""
    
    def __init__(self, name, email, password_hash=None, user_id=None):
        self.id = user_id or self._generate_id()
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_active = True
        self.is_admin = False
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
    
    def _generate_id(self):
        """Generate a simple ID"""
        import uuid
        return str(uuid.uuid4())
    
    def set_password(self, password):
        """Hash and set password"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if password is correct"""
        if not self.password_hash:
            return False
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        """Save user to fallback storage"""
        users = load_fallback_users()
        
        # Update existing user or add new one
        user_found = False
        for i, user_data in enumerate(users):
            if user_data.get('email') == self.email:
                users[i] = self.to_dict()
                users[i]['password_hash'] = self.password_hash
                user_found = True
                break
        
        if not user_found:
            user_data = self.to_dict()
            user_data['password_hash'] = self.password_hash
            users.append(user_data)
        
        save_fallback_users(users)

def load_fallback_users():
    """Load users from fallback storage"""
    if not FALLBACK_USERS_FILE.exists():
        return []
    
    try:
        with open(FALLBACK_USERS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading fallback users: {e}")
        return []

def save_fallback_users(users):
    """Save users to fallback storage"""
    try:
        # Ensure directory exists
        FALLBACK_USERS_FILE.parent.mkdir(exist_ok=True)
        
        with open(FALLBACK_USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print(f"Error saving fallback users: {e}")

def find_user_by_email(email):
    """Find user by email in fallback storage"""
    users = load_fallback_users()
    for user_data in users:
        if user_data.get('email') == email:
            user = FallbackUser(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=user_data.get('password_hash'),
                user_id=user_data['id']
            )
            user.is_active = user_data.get('is_active', True)
            user.is_admin = user_data.get('is_admin', False)
            user.created_at = user_data.get('created_at')
            user.updated_at = user_data.get('updated_at')
            return user
    return None

def create_fallback_user(name, email, password):
    """Create a new user in fallback storage"""
    # Check if user already exists
    existing_user = find_user_by_email(email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Create new user
    user = FallbackUser(name=name, email=email)
    user.set_password(password)
    user.save()
    
    return user

def authenticate_fallback_user(email, password):
    """Authenticate user using fallback storage"""
    user = find_user_by_email(email)
    if user and user.check_password(password):
        return user
    return None

def is_mongodb_available():
    """Check if MongoDB is available"""
    try:
        import mongoengine
        from authentication.models import User
        
        # Try a simple query with a very short timeout
        User.objects.count()
        return True
    except Exception:
        return False

def cleanup_fallback_storage():
    """Clean up fallback storage (for testing)"""
    if FALLBACK_USERS_FILE.exists():
        FALLBACK_USERS_FILE.unlink()
        print("Fallback storage cleaned up")
