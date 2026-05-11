import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
<<<<<<< HEAD
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-this')
=======
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-8x@2w!9q#k$m4n%p7r&t*y(u*i*o(p)l+k,j,m/n.b?v8c6x3z')
>>>>>>> 28b90ff430cf4491e0405520df52cbc251e2c053

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

<<<<<<< HEAD
# IMPORTANT: Add your Render.com domain
ALLOWED_HOSTS = [
    'nifty100-analytics.onrender.com',
    'localhost',
    '127.0.0.1',
]
=======
ALLOWED_HOSTS = ['*', '.onrender.com', 'localhost', '127.0.0.1', 'nifty100-analytics.onrender.com']
>>>>>>> 28b90ff430cf4491e0405520df52cbc251e2c053

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'corsheaders',
    
    # Your apps
    'nifty_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
<<<<<<< HEAD
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
=======
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files on Render
>>>>>>> 28b90ff430cf4491e0405520df52cbc251e2c053
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://nifty100-analytics.onrender.com',
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'nifty100_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'nifty100_project.wsgi.application'

<<<<<<< HEAD
# Database
=======
# Database - Using SQLite for simplicity (works on Render free tier)
>>>>>>> 28b90ff430cf4491e0405520df52cbc251e2c053
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

<<<<<<< HEAD
# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
=======
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
>>>>>>> 28b90ff430cf4491e0405520df52cbc251e2c053
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
<<<<<<< HEAD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
=======
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom settings for Nifty 100 API
API_VERSION = '1.0.0'
API_TITLE = 'Nifty 100 Financial Intelligence API'
API_DESCRIPTION = 'REST API for Nifty 100 company financial data, health scores, and analytics'

# CORS settings (for frontend integration)
CORS_ALLOW_ALL_ORIGINS = True

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'nifty_api': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory if not exists
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Create static directory if not exists
STATIC_DIR = os.path.join(BASE_DIR, 'static')
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
>>>>>>> 28b90ff430cf4491e0405520df52cbc251e2c053
