"""
Event models using MongoEngine
"""
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, EmbeddedDocument, EmbeddedDocumentField
from datetime import datetime
from authentication.models import User


class RSVP(EmbeddedDocument):
    """RSVP embedded document"""
    
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=255)
    created_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        """Convert RSVP to dictionary"""
        return {
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Event(Document):
    """Event model for MongoDB"""
    
    name = StringField(required=True, max_length=200)
    description = StringField(required=True)
    date = StringField(required=True)  # Store as string in YYYY-MM-DD format
    time = StringField(required=True)  # Store as string in HH:MM format
    location = StringField(required=True, max_length=300)
    created_by = ReferenceField(User, required=True)
    rsvps = ListField(EmbeddedDocumentField(RSVP), default=list)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'events',
        'indexes': ['created_by', 'date', 'created_at']
    }
    
    def save(self, *args, **kwargs):
        """Override save to update timestamp"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def add_rsvp(self, name, email):
        """Add RSVP to event"""
        # Check if email already exists in RSVPs
        for rsvp in self.rsvps:
            if rsvp.email == email:
                return False, "Email already registered for this event"
        
        new_rsvp = RSVP(name=name, email=email)
        self.rsvps.append(new_rsvp)
        self.save()
        return True, "RSVP added successfully"
    
    def get_rsvp_count(self):
        """Get total number of RSVPs"""
        return len(self.rsvps)
    
    def to_dict(self, include_creator=True):
        """Convert event to dictionary"""
        event_dict = {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'rsvp_count': self.get_rsvp_count(),
            'rsvps': [rsvp.to_dict() for rsvp in self.rsvps],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_creator and self.created_by:
            event_dict['created_by'] = {
                'id': str(self.created_by.id),
                'name': self.created_by.name,
                'email': self.created_by.email
            }
        
        return event_dict
    
    def __str__(self):
        return f"Event: {self.name} on {self.date}"
