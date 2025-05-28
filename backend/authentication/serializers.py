"""
Serializers for authentication app
"""
from rest_framework import serializers
from .models import User
import re


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user registration"""

    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    confirm_password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, value):
        """Validate email uniqueness"""
        try:
            if User.objects(email=value).first():
                raise serializers.ValidationError("User with this email already exists")
            return value
        except Exception as e:
            # Handle MongoDB connection issues gracefully
            import pymongo.errors
            if isinstance(e, (pymongo.errors.ServerSelectionTimeoutError,
                            pymongo.errors.NetworkTimeout,
                            pymongo.errors.ConnectionFailure)):
                raise serializers.ValidationError(
                    "Database connection issue. Please try again in a moment."
                )
            # Re-raise other exceptions
            raise serializers.ValidationError(f"Validation error: {str(e)}")

    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long")

        # Check for at least one letter and one number
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one letter and one number")

        return value

    def validate(self, data):
        """Validate password confirmation"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('confirm_password')  # Remove confirm_password

        user = User(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        """Validate user credentials"""
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        except Exception as e:
            # Handle MongoDB connection issues gracefully
            import pymongo.errors
            if isinstance(e, (pymongo.errors.ServerSelectionTimeoutError,
                            pymongo.errors.NetworkTimeout,
                            pymongo.errors.ConnectionFailure)):
                raise serializers.ValidationError(
                    "Database connection issue. Please try again in a moment."
                )
            # Re-raise other exceptions
            raise serializers.ValidationError(f"Login validation error: {str(e)}")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data


class UserSerializer(serializers.Serializer):
    """Serializer for user data"""

    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        """Convert User model to dictionary"""
        if hasattr(instance, 'to_dict'):
            return instance.to_dict()
        return super().to_representation(instance)
