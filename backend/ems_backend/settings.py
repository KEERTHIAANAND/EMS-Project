"""
Django settings for ems_backend project.
"""

from pathlib import Path
try:
    from decouple import config
except ImportError:
    # Fallback if decouple is not installed
    import os
    def config(key, default=None, cast=None):
        value = os.environ.get(key, default)
        if cast and value is not None:
            return cast(value)
        return value

try:
    import mongoengine
except ImportError:
    mongoengine = None
    print("⚠️  mongoengine not installed. MongoDB features will be disabled.")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,testserver').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'mongoengine',
    'authentication',
    'events',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ems_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ems_backend.wsgi.application'

# MongoDB Configuration
MONGODB_URI = config('MONGODB_URI', default='mongodb://localhost:27017/ems_database')
MONGODB_DB_NAME = config('MONGODB_DB_NAME', default='ems_database')

# Connect to MongoDB Atlas with improved settings
if mongoengine:
    try:
        # Disconnect any existing connections first
        mongoengine.disconnect()

        mongoengine.connect(
            db=MONGODB_DB_NAME,
            host=MONGODB_URI,
            alias='default',
            # Connection pool settings
            maxPoolSize=10,
            minPoolSize=1,
            # Increased timeout settings (in milliseconds)
            serverSelectionTimeoutMS=30000,  # 30 seconds
            socketTimeoutMS=30000,  # 30 seconds
            connectTimeoutMS=30000,  # 30 seconds
            # Retry settings
            retryWrites=True,
            retryReads=True,
            # Other settings
            maxIdleTimeMS=60000,  # 60 seconds
            heartbeatFrequencyMS=30000,  # 30 seconds
            # Additional settings for better connectivity
            directConnection=False,
            readPreference='primary',
        )
        print("✓ Successfully connected to MongoDB Atlas")
    except Exception as e:
        print(f"⚠️  MongoDB Atlas connection failed: {e}")
        print("   Please check your MongoDB Atlas configuration and network access")
        print("   Make sure your IP is whitelisted in MongoDB Atlas Network Access")

# Since we're using MongoDB, we'll use a dummy database for Django's requirements
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# JWT Configuration
JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='your-jwt-secret-key')
JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')
JWT_EXPIRATION_HOURS = config('JWT_EXPIRATION_HOURS', default=24, cast=int)

# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173,http://localhost:5174'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
