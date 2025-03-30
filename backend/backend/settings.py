import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'fake-secret-key'

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'django.contrib.auth',           # ✅ adicionar
    'django.contrib.contenttypes',
    'django.contrib.sessions',       # ✅ adicionar
    'django.contrib.staticfiles',
    'api',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'backend.urls'
TEMPLATES = []
WSGI_APPLICATION = 'backend.wsgi.application'

CORS_ALLOW_ALL_ORIGINS = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
