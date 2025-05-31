"""
Authentication views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .authentication import generate_jwt_token
from .models import User
from .fallback_auth import (
    is_mongodb_available,
    create_fallback_user,
    authenticate_fallback_user,
    find_user_by_email
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    try:
        # Get data from request
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Basic validation
        if not all([name, email, password, confirm_password]):
            return Response({
                'error': 'All fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({
                'error': 'Passwords do not match'
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({
                'error': 'Password must be at least 6 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Always try fallback first for reliability, then try MongoDB
        try:
            # Check if user already exists in fallback
            existing_user = find_user_by_email(email)
            if existing_user:
                return Response({
                    'error': 'User with this email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Try to save in MongoDB first
            try:
                if is_mongodb_available():
                    # Check if user exists in MongoDB
                    existing_mongo_user = User.objects(email=email).first()
                    if existing_mongo_user:
                        return Response({
                            'error': 'User with this email already exists'
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Create new user in MongoDB Atlas
                    mongo_user = User(
                        name=name,
                        email=email
                    )
                    mongo_user.set_password(password)
                    mongo_user.save()

                    # Generate JWT token
                    token = generate_jwt_token(mongo_user)

                    print(f"User successfully saved to MongoDB Atlas: {email}")

                    return Response({
                        'message': 'User registered successfully! Stored in MongoDB Atlas',
                        'user': {
                            'id': str(mongo_user.id),
                            'name': mongo_user.name,
                            'email': mongo_user.email,
                            'is_active': mongo_user.is_active,
                            'is_admin': mongo_user.is_admin
                        },
                        'token': token,
                        'storage': 'MongoDB Atlas',
                        'mongodb_saved': True
                    }, status=status.HTTP_201_CREATED)

                else:
                    # MongoDB not available, use fallback storage
                    user = create_fallback_user(name, email, password)
                    token = generate_jwt_token(user)

                    print(f"User saved to fallback storage (MongoDB unavailable): {email}")

                    return Response({
                        'message': 'User registered successfully! Stored in fallback storage',
                        'user': user.to_dict(),
                        'token': token,
                        'storage': 'Fallback Storage (MongoDB unavailable)',
                        'mongodb_saved': False
                    }, status=status.HTTP_201_CREATED)

            except Exception as creation_error:
                print(f"User creation error: {creation_error}")
                return Response({
                    'error': 'Registration failed. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Registration error: {e}")
            return Response({
                'error': 'Registration failed. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print(f"Unexpected registration error: {e}")
        return Response({
            'error': 'Registration failed. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user"""
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        # Basic validation
        if not email or not password:
            return Response({
                'error': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Try MongoDB authentication first, then fallback
        try:
            if is_mongodb_available():
                # Try to authenticate with MongoDB Atlas
                try:
                    mongo_user = User.objects.get(email=email, is_active=True)
                    if mongo_user.check_password(password):
                        # Generate JWT token
                        token = generate_jwt_token(mongo_user)

                        print(f"User successfully authenticated with MongoDB Atlas: {email}")

                        return Response({
                            'message': 'Login successful - Welcome to EMS! Authenticated with MongoDB Atlas',
                            'user': {
                                'id': str(mongo_user.id),
                                'name': mongo_user.name,
                                'email': mongo_user.email,
                                'is_active': mongo_user.is_active,
                                'is_admin': mongo_user.is_admin
                            },
                            'token': token,
                            'authenticated': True,
                            'storage': 'MongoDB Atlas',
                            'mongodb_verified': True
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'error': 'Invalid email or password.'
                        }, status=status.HTTP_400_BAD_REQUEST)

                except User.DoesNotExist:
                    return Response({
                        'error': 'Invalid email or password. Please register first.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            else:
                # MongoDB not available, try fallback authentication
                fallback_user = authenticate_fallback_user(email, password)

                if fallback_user:
                    # Generate JWT token
                    token = generate_jwt_token(fallback_user)

                    print(f"User authenticated with fallback storage (MongoDB unavailable): {email}")

                    return Response({
                        'message': 'Login successful - Welcome to EMS! Authenticated with fallback storage',
                        'user': fallback_user.to_dict(),
                        'token': token,
                        'authenticated': True,
                        'storage': 'Fallback Storage (MongoDB unavailable)',
                        'mongodb_verified': False
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid email or password. Please register first.'
                    }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as auth_error:
            print(f"Authentication error: {auth_error}")
            return Response({
                'error': 'Authentication failed. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print(f"Unexpected login error: {e}")
        return Response({
            'error': 'Login failed. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user (client-side token removal)"""
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get user profile"""
    try:
        user = request.user
        serializer = UserSerializer(user)

        return Response({
            'user': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Failed to get profile: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update user profile"""
    try:
        user = request.user

        # Only allow updating name for now
        name = request.data.get('name')
        if name:
            user.name = name
            user.save()

        serializer = UserSerializer(user)

        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Failed to update profile: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
