"""
Fallback event system for when MongoDB is unavailable
"""
import json
import os
from datetime import datetime
from pathlib import Path

# File to store events when MongoDB is unavailable
FALLBACK_EVENTS_FILE = Path(__file__).parent / 'fallback_events.json'

class FallbackEvent:
    """Simple event class for fallback storage"""

    def __init__(self, name, description, date, time, location, created_by_id, created_by_name, image='', event_id=None):
        self.id = event_id or self._generate_id()
        self.name = name
        self.description = description
        self.date = date
        self.time = time
        self.location = location
        self.image = image
        self.created_by_id = created_by_id
        self.created_by_name = created_by_name
        self.rsvps = []
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()

    def _generate_id(self):
        """Generate a simple ID"""
        import uuid
        return str(uuid.uuid4())

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'image': self.image,
            'rsvp_count': len(self.rsvps),
            'rsvps': self.rsvps,
            'created_by': {
                'id': self.created_by_id,
                'name': self.created_by_name,
                'email': ''  # We don't store email in fallback for privacy
            },
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save(self):
        """Save event to fallback storage"""
        events = load_fallback_events()

        # Update existing event or add new one
        event_found = False
        for i, event_data in enumerate(events):
            if event_data.get('id') == self.id:
                events[i] = self.to_dict()
                event_found = True
                break

        if not event_found:
            events.append(self.to_dict())

        save_fallback_events(events)

def load_fallback_events():
    """Load events from fallback storage"""
    if not FALLBACK_EVENTS_FILE.exists():
        return []

    try:
        with open(FALLBACK_EVENTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading fallback events: {e}")
        return []

def save_fallback_events(events):
    """Save events to fallback storage"""
    try:
        # Ensure directory exists
        FALLBACK_EVENTS_FILE.parent.mkdir(exist_ok=True)

        with open(FALLBACK_EVENTS_FILE, 'w') as f:
            json.dump(events, f, indent=2)
    except Exception as e:
        print(f"Error saving fallback events: {e}")

def create_fallback_event(name, description, date, time, location, image='', user=None):
    """Create a new event in fallback storage"""
    try:
        # Create new event
        event = FallbackEvent(
            name=name,
            description=description,
            date=date,
            time=time,
            location=location,
            image=image,
            created_by_id=str(user.id) if hasattr(user, 'id') else str(user.get('id', 'unknown')),
            created_by_name=user.name if hasattr(user, 'name') else user.get('name', 'Unknown User')
        )
        event.save()

        return event
    except Exception as e:
        print(f"Error creating fallback event: {e}")
        raise

def get_all_fallback_events():
    """Get all events from fallback storage"""
    try:
        events_data = load_fallback_events()
        return events_data
    except Exception as e:
        print(f"Error getting fallback events: {e}")
        return []

def is_mongodb_available():
    """Check if MongoDB is available for events"""
    try:
        from events.models import Event
        import mongoengine

        # Test basic connection by trying to count documents
        # This is a lightweight operation that will fail quickly if MongoDB is unavailable
        Event.objects.count()
        return True

    except Exception as e:
        # MongoDB is not available, use fallback storage
        error_msg = str(e)
        if "SSL handshake failed" in error_msg:
            print("MongoDB not available for events (SSL connection issue), using fallback storage")
        elif "ServerSelectionTimeoutError" in error_msg:
            print("MongoDB not available for events (connection timeout), using fallback storage")
        elif "ObjectId" in error_msg:
            print("MongoDB not available for events (ObjectId validation issue), using fallback storage")
        else:
            print(f"MongoDB not available for events, using fallback storage: {error_msg[:100]}...")
        return False

def cleanup_fallback_events():
    """Clean up fallback storage (for testing)"""
    if FALLBACK_EVENTS_FILE.exists():
        FALLBACK_EVENTS_FILE.unlink()
        print("Fallback events storage cleaned up")

def migrate_fallback_to_mongodb():
    """Migrate fallback events to MongoDB when connection is restored"""
    try:
        from events.models import Event
        from authentication.models import User

        fallback_events = load_fallback_events()
        migrated_count = 0

        for event_data in fallback_events:
            try:
                # Find the user who created the event
                user = User.objects(id=event_data['created_by']['id']).first()
                if not user:
                    print(f"User not found for event {event_data['name']}, skipping...")
                    continue

                # Check if event already exists in MongoDB
                existing_event = Event.objects(
                    name=event_data['name'],
                    date=event_data['date'],
                    created_by=user
                ).first()

                if existing_event:
                    print(f"Event {event_data['name']} already exists in MongoDB, skipping...")
                    continue

                # Create event in MongoDB
                mongodb_event = Event(
                    name=event_data['name'],
                    description=event_data['description'],
                    date=event_data['date'],
                    time=event_data['time'],
                    location=event_data['location'],
                    created_by=user
                )
                mongodb_event.save()
                migrated_count += 1
                print(f"Migrated event: {event_data['name']}")

            except Exception as e:
                print(f"Error migrating event {event_data.get('name', 'Unknown')}: {e}")

        if migrated_count > 0:
            print(f"Successfully migrated {migrated_count} events to MongoDB")
            # Optionally clean up fallback storage after successful migration
            # cleanup_fallback_events()

        return migrated_count

    except Exception as e:
        print(f"Error during migration: {e}")
        return 0
