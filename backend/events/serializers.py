"""
Serializers for events app
"""
from rest_framework import serializers
from .models import Event, RSVP
from datetime import datetime
import re


class RSVPSerializer(serializers.Serializer):
    """Serializer for RSVP data"""

    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    created_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        """Convert RSVP model to dictionary"""
        if hasattr(instance, 'to_dict'):
            return instance.to_dict()
        return super().to_representation(instance)


class EventSerializer(serializers.Serializer):
    """Serializer for event data"""

    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=True)
    date = serializers.CharField(required=True)
    time = serializers.CharField(required=True)
    location = serializers.CharField(max_length=300, required=True)
    image = serializers.CharField(max_length=500, required=False, allow_blank=True)
    rsvp_count = serializers.IntegerField(read_only=True)
    rsvps = RSVPSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_created_by(self, obj):
        """Get creator information"""
        if hasattr(obj, 'created_by') and obj.created_by:
            return {
                'id': str(obj.created_by.id),
                'name': obj.created_by.name,
                'email': obj.created_by.email
            }
        return None

    def validate_date(self, value):
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError("Date must be in YYYY-MM-DD format")
        return value

    def validate_time(self, value):
        """Validate time format (HH:MM)"""
        if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', value):
            raise serializers.ValidationError("Time must be in HH:MM format")
        return value

    def validate_name(self, value):
        """Validate event name"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Event name must be at least 3 characters long")
        return value.strip()

    def validate_description(self, value):
        """Validate event description"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Event description must be at least 10 characters long")
        return value.strip()

    def validate_location(self, value):
        """Validate event location"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Event location must be at least 3 characters long")
        return value.strip()

    def create(self, validated_data):
        """Create new event"""
        user = self.context['request'].user

        event = Event(
            name=validated_data['name'],
            description=validated_data['description'],
            date=validated_data['date'],
            time=validated_data['time'],
            location=validated_data['location'],
            image=validated_data.get('image', ''),
            created_by=user
        )
        event.save()

        return event

    def update(self, instance, validated_data):
        """Update existing event"""
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.location = validated_data.get('location', instance.location)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance

    def to_representation(self, instance):
        """Convert Event model to dictionary"""
        if hasattr(instance, 'to_dict'):
            return instance.to_dict()
        return super().to_representation(instance)


class EventCreateSerializer(EventSerializer):
    """Serializer for creating events (excludes read-only fields)"""

    class Meta:
        fields = ['name', 'description', 'date', 'time', 'location', 'image']


class RSVPCreateSerializer(serializers.Serializer):
    """Serializer for creating RSVP"""

    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)

    def validate_name(self, value):
        """Validate RSVP name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()

    def validate_email(self, value):
        """Validate RSVP email"""
        return value.lower().strip()
