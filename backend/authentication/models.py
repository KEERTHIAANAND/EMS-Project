"""
User models using MongoEngine
"""
from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField
from datetime import datetime
import bcrypt


class User(Document):
    """User model for MongoDB"""
    
    email = EmailField(required=True, unique=True)
    name = StringField(required=True, max_length=100)
    password_hash = StringField(required=True)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': ['email', 'created_at']
    }
    
    def set_password(self, password):
        """Hash and set password"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def save(self, *args, **kwargs):
        """Override save to update timestamp"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def to_dict(self):
        """Convert user to dictionary (excluding password)"""
        return {
            'id': str(self.id),
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        return f"User: {self.email}"
