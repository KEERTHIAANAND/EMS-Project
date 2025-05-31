"""
JWT Authentication for Django REST Framework
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class JWTAuthentication(BaseAuthentication):
    """Custom JWT Authentication class"""

    def authenticate(self, request):
        """Authenticate user using JWT token"""
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')

            # Try to find user in MongoDB first
            try:
                user = User.objects.get(id=user_id, is_active=True)
                return (user, token)
            except User.DoesNotExist:
                pass
            except Exception as mongo_error:
                print(f"MongoDB user lookup failed: {mongo_error}")

            # If not found in MongoDB, try fallback storage
            try:
                from .fallback_auth import find_user_by_id
                fallback_user = find_user_by_id(user_id)
                if fallback_user and fallback_user.is_active:
                    return (fallback_user, token)
                else:
                    raise AuthenticationFailed('User not found in fallback storage')
            except Exception as fallback_error:
                print(f"Fallback user lookup failed: {fallback_error}")
                raise AuthenticationFailed('User not found')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')


def generate_jwt_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token
