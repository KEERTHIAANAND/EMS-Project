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

        # Try MongoDB first (force MongoDB usage)
        try:
            existing_user = User.objects(email=email).first()
            if existing_user:
                return Response({
                    'error': 'User with this email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create new user in MongoDB
            user = User(
                name=name,
                email=email
            )
            user.set_password(password)
            user.save()

            # Generate JWT token
            token = generate_jwt_token(user)

            return Response({
                'message': 'User registered successfully in MongoDB Atlas',
                'user': user.to_dict(),
                'token': token
            }, status=status.HTTP_201_CREATED)

        except Exception as db_error:
            print(f"MongoDB error during registration: {db_error}")

            # Check if it's a connection issue
            import pymongo.errors
            if isinstance(db_error, (pymongo.errors.ServerSelectionTimeoutError,
                                   pymongo.errors.NetworkTimeout,
                                   pymongo.errors.ConnectionFailure)):
                return Response({
                    'error': 'Cannot connect to database. Please check MongoDB Atlas network settings and try again.'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # For other MongoDB errors, use fallback
            try:
                # Check if user already exists in fallback
                existing_user = find_user_by_email(email)
                if existing_user:
                    return Response({
                        'error': 'User with this email already exists'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Create user in fallback storage
                user = create_fallback_user(name, email, password)

                # Generate JWT token
                token = generate_jwt_token(user)

                return Response({
                    'message': 'User registered successfully (MongoDB unavailable, using temporary storage)',
                    'user': user.to_dict(),
                    'token': token
                }, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"Fallback registration error: {e}")
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

        # Try MongoDB first (force MongoDB usage)
        try:
            user = User.objects.get(email=email, is_active=True)
            if not user.check_password(password):
                return Response({
                    'error': 'Invalid email or password'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT token
            token = generate_jwt_token(user)

            return Response({
                'message': 'Login successful (using MongoDB Atlas)',
                'user': user.to_dict(),
                'token': token
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # User not found in MongoDB, check fallback
            try:
                user = authenticate_fallback_user(email, password)
                if user:
                    token = generate_jwt_token(user)
                    return Response({
                        'message': 'Login successful (using temporary storage)',
                        'user': user.to_dict(),
                        'token': token
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid email or password'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"Fallback authentication error: {e}")
                return Response({
                    'error': 'Invalid email or password'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as db_error:
            print(f"MongoDB error during login: {db_error}")

            # Check if it's a connection issue
            import pymongo.errors
            if isinstance(db_error, (pymongo.errors.ServerSelectionTimeoutError,
                                   pymongo.errors.NetworkTimeout,
                                   pymongo.errors.ConnectionFailure)):
                return Response({
                    'error': 'Cannot connect to database. Please check MongoDB Atlas network settings and try again.'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # For other errors, try fallback
            try:
                user = authenticate_fallback_user(email, password)
                if user:
                    token = generate_jwt_token(user)
                    return Response({
                        'message': 'Login successful (MongoDB unavailable, using temporary storage)',
                        'user': user.to_dict(),
                        'token': token
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid email or password'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"Fallback authentication error: {e}")
                return Response({
                    'error': 'Invalid email or password'
                }, status=status.HTTP_400_BAD_REQUEST)

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
